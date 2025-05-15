from pydantic import BaseModel, constr, Field, field_validator, ConfigDict


class CatBase(BaseModel):
    name: str
    experience: int
    breed: str
    salary: float

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) > 255:
            raise ValueError('Field "name" must be at most 255 characters.')
        return v

    @field_validator('experience')
    def validate_experience(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Field "experience" must be between 0 and 100.')
        return v

    @field_validator('salary')
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError('Field "salary" must be greater than 0.')
        return v

    model_config = ConfigDict(from_attributes=True)


class CatCreate(CatBase):
    pass


class CatUpdate(BaseModel):
    salary: float

    @field_validator('salary')
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError('Field "salary" must be greater than 0.')
        return v


class CatOut(CatBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
