from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.cats.models import Cat
from src.database import get_db
from src.missions.models import Mission, Target
from src.missions.schemas import MissionOut, MissionCreate, AssignCatRequest, TargetUpdate

router = APIRouter(
    prefix="/missions",
    tags=["Missions & Targets"],
)

@router.post("/", response_model=MissionOut)
def create_mission(data: MissionCreate, db: Session = Depends(get_db)):
    if not (1 <= len(data.targets) <= 3):
        raise HTTPException(status_code=400, detail="Must have 1–3 targets")

    mission = Mission()
    db.add(mission)
    db.flush()

    for target_data in data.targets:
        target = Target(mission_id=mission.id, **target_data.dict())
        db.add(target)

    db.commit()
    db.refresh(mission)
    return mission


@router.get("/", response_model=list[MissionOut])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


@router.get("/{mission_id}", response_model=MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already assigned")
    db.delete(mission)
    db.commit()
    return {"message": "Mission deleted"}


@router.patch("/{mission_id}/assign")
def assign_cat(mission_id: int, req: AssignCatRequest, db: Session = Depends(get_db)):
    mission = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if db.query(Cat).get(req.cat_id) is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    mission.cat_id = req.cat_id
    db.commit()
    return {"message": "Cat assigned"}


@router.patch("/targets/{target_id}")
def update_target(target_id: int, update: TargetUpdate, db: Session = Depends(get_db)):
    target = db.query(Target).get(target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    if target.completed or target.mission.completed:
        raise HTTPException(status_code=400, detail="Target or mission completed")

    if update.notes is not None:
        target.notes = update.notes
    if update.completed is True:
        target.completed = True

    db.commit()
    return {"message": "Target updated"}
