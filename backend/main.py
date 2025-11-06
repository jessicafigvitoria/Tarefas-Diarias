from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from fastapi.middleware.cors import CORSMiddleware

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Permitir o acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para abrir uma sessão no banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas básicas
@app.get("/")
def root():
    return {"mensagem": "API de Tarefas funcionando 🚀"}

@app.post("/tarefas/", response_model=schemas.TarefaResponse)
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db)):
    nova_tarefa = models.Tarefa(**tarefa.dict())
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa

@app.get("/tarefas/", response_model=list[schemas.TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.Tarefa).all()

# Marcar ou desmarcar como concluída
@app.patch("/tarefas/{tarefa_id}", response_model=schemas.TarefaResponse)
def atualizar_tarefa(tarefa_id: int, dados: dict, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    if "concluida" in dados:
        tarefa.concluida = dados["concluida"]

    db.commit()
    db.refresh(tarefa)
    return tarefa

# Deletar tarefa
@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.Tarefa).filter(models.Tarefa.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(tarefa)
    db.commit()
    return {"mensagem": "Tarefa deletada com sucesso"}
