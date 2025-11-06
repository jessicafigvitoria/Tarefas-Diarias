from pydantic import BaseModel

class TarefaBase(BaseModel):
    titulo: str
    descricao: str

class TarefaCreate(TarefaBase):
    pass

class TarefaResponse(TarefaBase):
    id: int
    concluida: bool

    class Config:
        orm_mode = True
