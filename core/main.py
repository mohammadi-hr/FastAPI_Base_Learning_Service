from schemas import PersonCreateSchema, PersonResposeSchema, PersonUpdateSchema
from fastapi import FastAPI, status, Body, Query, HTTPException, Path, Form
from contextlib import asynccontextmanager
import random
import string
from typing import Annotated, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app startup process ...")
    yield
    print("app shutdown process ...")


app = FastAPI(lifespan=lifespan)
persons_list = [{"id": 1, "firstname": "name1", "lastname": "lname1", "national_code": "0534989036"},
                {"id": 2, "firstname": "name2",
                 "lastname": "lname2", "national_code": "0123456789"},
                {"id": 3, "firstname": "name3",
                 "lastname": "lname3", "national_code": "0123456789"},
                {"id": 4, "firstname": "name4",
                 "lastname": "lname4", "national_code": "0123456789"},
                {"id": 5, "firstname": "name5", "lastname": "lname5", "national_code": "0123456789"}]

# -------------- get methods ------------


@app.get("/users", response_model=List[PersonResposeSchema])
def read_root(q: str | None = Query(default=None, max_length=20, alias='query')):
    if q:
        return [person for person in persons_list if person['national_code'] == q]
    return persons_list


@app.get("/users/{person_id}", status_code=status.HTTP_200_OK, response_model=PersonResposeSchema)
def retrive_person(person_id: int = Path(description='search in persons list by id')):
    for person in persons_list:
        if person['id'] == person_id:
            return JSONResponse(content=jsonable_encoder(person))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"object with {person_id} id not found!")

# -------------- post methods ------------


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=Annotated[PersonResposeSchema, Body(embed=True)])
def create_person(person: PersonCreateSchema):

    # # return {"massge": "Hello world ^|^"}
    random_id = random.randint(1, 100)
    # randon_firstname = ''.join(random.choices(
    #     string.ascii_letters + string.digits, k=10))
    # randon_lastname = ''.join(random.choices(
    #     string.ascii_letters + string.digits, k=10))
    # randon_national_code = ''.join(random.choices(string.digits, k=9))

    person_abj = {"id": random_id, "firstname": person.firstname,
                  "lastname": person.lastname, "national_code": person.national_code}
    print(person_abj)
    persons_list.append(person_abj)
    return person_abj

# -------------- put methods ------------


@app.put("/users/{person_id}", response_model=PersonResposeSchema, status_code=status.HTTP_200_OK)
def update_person(person_schema: PersonUpdateSchema, person_id: int = Path()):
    for person in persons_list:
        if person['id'] == person_id:
            person['firstname'] = person_schema.firstname
            person['lastname'] = person_schema.lastname
            person['national_code'] = person_schema.national_code
            print(person)
            return person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'{person_id} not found in the persons list!')


@app.delete("/users/{id}")
def person_delete(id: int):
    for person in persons_list:
        if person['id'] == id:
            persons_list.remove(person)
            return JSONResponse(content=jsonable_encoder(person))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="delete failed! object not found...")
