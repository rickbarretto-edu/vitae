from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class Pesquisador(Base):
    __tablename__ = "pesquisador"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    nome = Column(String, nullable=False)
    cidade = Column(String)
    estado = Column(String)
    pais = Column(String)
    nomes_citacoes = Column(String)
    orcid = Column(String)
    resumo = Column(String)
    instituicao_profissional = Column(String)
    atualizacao = Column(DateTime, default=datetime.utcnow)

    formacoes = relationship("FormacaoAcademica", back_populates="pesquisador", cascade="all, delete-orphan")
    experiencias = relationship("ExperienciaProfissional", back_populates="pesquisador", cascade="all, delete-orphan")