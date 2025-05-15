from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.cats import utils
from src.cats.models import Cat
from src.cats.schemas import CatOut, CatCreate, CatUpdate
from src.database import get_db

router = APIRouter(
    prefix="/cats",
    tags=["Spy cats"],
)

@router.post("/", response_model=CatOut)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    breed_valid = utils.validate_cat_breed(cat.breed)
    if not breed_valid:
        raise HTTPException(status_code=400, detail="Invalid breed")

    new_cat = Cat(**cat.model_dump())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


@router.get("/", response_model=list[CatOut])
def list_cats(db: Session = Depends(get_db)):
    return db.query(Cat).all()


@router.get("/{cat_id}", response_model=CatOut)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


@router.patch("/{cat_id}", response_model=CatOut)
def update_cat(cat_id: int, update: CatUpdate, db: Session = Depends(get_db)):
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = update.salary
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat)
    db.commit()
    return {"message": "Cat deleted"}
