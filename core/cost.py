from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from schemas import *
from typing import List


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


@app.get('/costs/', response_model=List[CostResponseSchema])
def list_costs(cost_id: int | None = Query(None, ge=1, description='cost id must be greater than 1')):
    if cost_id:
        return [cost for cost in costs if cost['id'] == cost_id]
    return costs
