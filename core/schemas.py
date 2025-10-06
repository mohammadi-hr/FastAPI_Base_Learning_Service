from pydantic import BaseModel, field_validator, Field, field_serializer
import re

#  ------------- Perosn Schemas ----------------


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

#  ----------- Cost Schemas ---------------


class CostBasicSchema(BaseModel):
    description: str = Field(min_length=10, max_length=256, pattern="^[A-Za-z0-9.,!?'-_ ]+$",
                             description="description text between 10 to 256 characters, number and punctuatinn only")
    amount: float

    @field_serializer('description', mode='plain')
    def serialize(self, v: str) -> str:
        return v.capitalize()

    @field_validator('description')
    def validate_text(cls, v: str) -> str:
        value = v.strip()
        if len(value) < 10:
            raise ValueError("description must be at least 10 characters long")
        if len(value) > 256:
            raise ValueError(
                "description should not be more than 256 characters long")

        banned_words = ["someword1", "someword2"]
        if any(bad_word in value.lower() for bad_word in banned_words):
            raise ValueError("description has forbbiden words")

        return value


class CostCreateSchema(CostBasicSchema):
    pass


class CostUpdateSchema(CostBasicSchema):
    pass


class CostResponseSchema(CostBasicSchema):
    id: int
