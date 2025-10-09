from schemas import PersonBaseSchema, PersonCreateSchema, PersonResposeSchema, PersonUpdateSchema
from fastapi import FastAPI, status, Body, Query, HTTPException, Path, Form, Depends
from contextlib import asynccontextmanager
import random
from typing import Annotated, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import SessionLocal, engine, Base, get_db
from models.ticket import Ticket
from models.person import Person
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield
    session.close()


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
def read_root(q: str | None = Query(default=None, max_length=20, alias='query'), db: Session = Depends(get_db)):
    query = db.query(Person)
    if q:
        person = db.query(Person).filter_by(firstname=q).all()
        return person
    return query.all()

    #     return [person for person in persons_list if person['national_code'] == q]
    # return persons_list


@app.get("/users/{person_id}", status_code=status.HTTP_200_OK, response_model=PersonResposeSchema)
def retrive_person(person_id: int = Path(description='search in persons list by id'), db: Session = Depends(get_db)):
    fetch_person = db.query(Person).filter_by(id=person_id).one_or_none()
    if fetch_person:
        return fetch_person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"object with {person_id} id not found!")

    # for person in persons_list:
    #     if person['id'] == person_id:
    #         return JSONResponse(content=jsonable_encoder(person))
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f"object with {person_id} id not found!")

# -------------- post methods ------------


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=Annotated[PersonResposeSchema, Body(embed=True)])
def create_person(person: PersonCreateSchema, db: Session = Depends(get_db)):
    new_person = Person(
        firstname=person.firstname, lastname=person.lastname, national_code=person.national_code, is_active=person.is_active)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person

    # return {"massge": "Hello world ^|^"}
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
    # return person_abj

# -------------- put methods ------------


@app.put("/users/{person_id}", response_model=PersonResposeSchema, status_code=status.HTTP_200_OK)
def update_person(person: PersonUpdateSchema, person_id: int = Path(), db: Session = Depends(get_db)):
    # for person in persons_list:
    #     if person['id'] == person_id:
    #         person['firstname'] = person.firstname
    #         person['lastname'] = person.lastname
    #         person['national_code'] = person.national_code
    #         print(person)
    #         return person

    fetch_person_to_update = db.query(
        Person).filter_by(id=person_id).one_or_none()
    if fetch_person_to_update:
        fetch_person_to_update.firstname = person.firstname
        fetch_person_to_update.lastname = person.lastname
        fetch_person_to_update.national_code = person.national_code
        fetch_person_to_update.is_active = person.is_active

        db.commit()
        db.refresh(fetch_person_to_update)
        return fetch_person_to_update
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{person_id} not found in the persons list!')

# --------- delete mothod ----------------


@app.delete("/users/{id}")
def person_delete(person_id: int, db: Session = Depends(get_db)):
    # for person in persons_list:
    #     if person['id'] == id:
    #         persons_list.remove(person)
    fetch_person_to_delete = db.query(
        Person).filter_by(id=person_id).one_or_none()
    if fetch_person_to_delete:
        db.delete(fetch_person_to_delete)
        db.commit()
        return JSONResponse(content={"detail": "person has been deleted successfully"}, status_code=status.HTTP_200_OK)
        # return JSONResponse(content=jsonable_encoder(person))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="delete failed! object not found...")
