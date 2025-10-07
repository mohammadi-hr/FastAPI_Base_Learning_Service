from fastapi import FastAPI, Query, status, Request, Body, Path, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from schemas import *
from typing import List, Annotated
from pydantic import ValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app startup process ...")
    yield
    print("app shutdown process ...")


app = FastAPI(lifespan=lifespan)

costs = [{"id": 1, "description": "Buy a bookshelf", "amount": 450.211},
         {"id": 2, "description": "buying a white desk", "amount": 785.358},
         {"id": 3, "description": "Painting the walls of the house", "amount": 6985.124},
         {"id": 4, "description": "Elevator repairs and maintenance", "amount": 54.25},
         {"id": 5, "description": "Cleaning the building", "amount": 68.124}]


@app.get('/costs/', response_model=List[CostResponseSchema], status_code=status.HTTP_200_OK)
def list_costs(cost_id: int | None = Query(None, ge=1, description='cost id must be equal or greater than 1')):
    if cost_id:
        return [cost for cost in costs if cost['id'] == cost_id]
    return costs


@app.post("/costs/", status_code=status.HTTP_201_CREATED, response_model=Annotated[CostResponseSchema, Body(embed=True)])
def create_cost(cost: CostCreateSchema):
    cost_id = max(c["id"] for c in costs) + 1 if cost else 1
    new_cost = {
        "id": cost_id,
        "description": cost.description,
        "amount": cost.amount
    }

    new_cost_obj = CostResponseSchema(
        id=cost_id, description=cost.description, amount=cost.amount)

    if isinstance(new_cost_obj, CostResponseSchema):
        print(f"object created successfully : {new_cost_obj}")
        costs.append(new_cost)

    return new_cost_obj


@app.put("/post/{cost_id}", status_code=status.HTTP_202_ACCEPTED)
def update_cost(cost_obj: CostUpdateSchema, cost_id: int = Path()):
    for cost in costs:
        if cost['id'] == cost_id:
            cost['description'] = cost_obj.description
            cost['amount'] = cost_obj.amount
            return cost
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'{cost_id} not found in costs list')


@app.delete("/cost/{cost_id}")
def delete_cost(cost_id: int):
    for cost in costs:
        if cost['id'] == cost_id:
            costs.remove(cost)
            return {"message": "cost delete successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="delete failed! object not found...")
