from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o banco sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./tarefas.db"

# Conexão ao banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria a sessão (comunicação com o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos (tabelas)
Base = declarative_base()
