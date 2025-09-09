from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime

class StatusAnimal(str, enum.Enum):
    ativo = "ativo"
    inativo = "inativo"

class Tutor(Base):
    __tablename__ = "tutores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    contato = Column(String, nullable=False)

    animais = relationship("Animal", back_populates="tutor")

class Animal(Base):
    __tablename__ = "animais"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    raca = Column(String)
    idade = Column(Integer)
    status = Column(Enum(StatusAnimal), default=StatusAnimal.ativo)

    tutor_id = Column(Integer, ForeignKey("tutores.id"))
    tutor = relationship("Tutor", back_populates="animais")
    historico = relationship("Prontuario", back_populates="animal")

class Prontuario(Base):
    __tablename__ = "prontuarios"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, default=datetime.utcnow)
    diagnostico = Column(Text)
    tratamento = Column(Text)
    cirurgia = Column(Text)
    peso = Column(Float)
    imagem = Column(String)  # URL ou caminho de arquivo

    animal_id = Column(Integer, ForeignKey("animais.id"))
    animal = relationship("Animal", back_populates="historico")
