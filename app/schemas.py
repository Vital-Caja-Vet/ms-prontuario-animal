from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StatusAnimal(str, Enum):
    ativo = "ativo"
    inativo = "inativo"

class TutorBase(BaseModel):
    nome: str
    contato: str

class TutorCreate(TutorBase):
    pass

class TutorOut(TutorBase):
    id: int
    class Config:
        orm_mode = True

class AnimalBase(BaseModel):
    nome: str
    especie: str
    raca: Optional[str]
    idade: Optional[int]

class AnimalCreate(AnimalBase):
    tutor_id: int

class AnimalOut(AnimalBase):
    id: int
    status: StatusAnimal
    tutor: TutorOut
    class Config:
        orm_mode = True

class ProntuarioBase(BaseModel):
    diagnostico: Optional[str]
    tratamento: Optional[str]
    cirurgia: Optional[str]
    peso: Optional[float]
    imagem: Optional[str]

class ProntuarioCreate(ProntuarioBase):
    animal_id: int

class ProntuarioOut(ProntuarioBase):
    id: int
    data: datetime
    class Config:
        orm_mode = True
