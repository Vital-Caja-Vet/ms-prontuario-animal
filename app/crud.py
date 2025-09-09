from sqlalchemy.orm import Session
from . import models, schemas

def create_tutor(db: Session, tutor: schemas.TutorCreate):
    db_tutor = models.Tutor(**tutor.dict())
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

def create_animal(db: Session, animal: schemas.AnimalCreate):
    db_animal = models.Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def inativar_animal(db: Session, animal_id: int):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if animal and animal.historico:
        animal.status = models.StatusAnimal.inativo
        db.commit()
    return animal

def create_prontuario(db: Session, prontuario: schemas.ProntuarioCreate):
    db_prontuario = models.Prontuario(**prontuario.dict())
    db.add(db_prontuario)
    db.commit()
    db.refresh(db_prontuario)
    return db_prontuario
