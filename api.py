# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from nqueen import NQueen
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class NQueenRequest(BaseModel):
    number: int

@app.post("/solve")
def solve_nqueen(req: NQueenRequest):
    nqueen = NQueen(req.number)
    nqueen.master_list.clear()
    nqueen.create_master_and_queen(number=req.number, master_list=nqueen.master_list)
    nqueen.create_homes(number=req.number, master_list=nqueen.master_list)
    nqueen.solve_nqueens(master_list=nqueen.master_list, row=0)
    print("       Found     ")
    nqueen.beautiful_print(master_list=nqueen.master_list)
    return {"solution": nqueen.master_list}
1