from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.src.database.databaseConfig import databaseConfig

class FormacaoAcademica(databaseConfig.base):
    __tablename__ = "formacao_academica"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, nullable=False)
    instituicao = Column(String, nullable=False)
    curso = Column(String, nullable=False)
    ano_inicio = Column(Integer)
    ano_fim = Column(Integer)
    titulo_trabalho = Column(String)
    id_pesquisador = Column(Integer, ForeignKey("pesquisador.id", ondelete="CASCADE"), nullable=False)

    pesquisador = relationship("Pesquisador", back_populates="formacoes")
