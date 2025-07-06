from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta
import enum
import uuid

# Configuração do banco de dados
DATABASE_URL = "postgresql://user:password@localhost:5432/saas_nfe_validator"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Enums
class TipoUsuarioEnum(str, enum.Enum):
    admin = "admin"
    gerente = "gerente"
    analista = "analista"
    auditor = "auditor"

class StatusValidacaoEnum(str, enum.Enum):
    sucesso = "sucesso"
    erro = "erro"
    pendente = "pendente"
    processando = "processando"

class PlanoEnum(str, enum.Enum):
    free = "free"
    basic = "basic"
    professional = "professional"
    enterprise = "enterprise"
    teste = "teste"