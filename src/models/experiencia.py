from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class ExperienciaProfissional(Base):
    __tablename__ = "experiencia_profissional"

    id = Column(Integer, primary_key=True, autoincrement=True)
    instituicao = Column(String, nullable=False)
    tipo_vinculo = Column(String)
    cargo = Column(String, nullable=False)
    ano_inicio = Column(Integer)
    ano_fim = Column(Integer)
    atualizacao = Column(DateTime, default=datetime.utcnow)
    id_pesquisador = Column(Integer, ForeignKey("pesquisador.id", ondelete="CASCADE"), nullable=False)

    pesquisador = relationship("Pesquisador", back_populates="experiencias")
