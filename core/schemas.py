from pydantic import BaseModel, field_validator, Field
import re


class PersonBaseSchema(BaseModel):
    firstname: str
    lastname: str
    national_code: str

    @field_validator('national_code')
    def validate_national_code(cls, v):
        pattern = '^[0-9]{10}'

        if not re.match(pattern, v):
            raise ValueError('Invalid Nationl Code')
        return v


class PersonCreateSchema(PersonBaseSchema):
    pass


class PersonResposeSchema(PersonBaseSchema):
    id: int


class PersonUpdateSchema(PersonBaseSchema):
    pass
