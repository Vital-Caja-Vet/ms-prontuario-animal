from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, auth
from app.utils.jwt_handler import create_access_token, verify_token

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="MS Prontuário Animal", description="API de prontuário veterinário", version="1.0")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

fake_user_db = {
    "admin": {
        "username": "admin",
        "password": "senha123"  # ⚠️ em produção use hash (bcrypt)
    }
}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_user_db.get(form_data.username)
    if not user_dict or form_data.password != user_dict["password"]:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")

    token = create_access_token(data={"sub": user_dict["username"]})
    return {"access_token": token, "token_type": "bearer"}


# Rotas protegidas com JWT
@app.post("/tutores/", response_model=schemas.TutorOut, dependencies=[Depends(auth.verify_token)])
def create_tutor(tutor: schemas.TutorCreate, db: Session = Depends(get_db)):
    return crud.create_tutor(db, tutor)

@app.post("/animais/", response_model=schemas.AnimalOut, dependencies=[Depends(auth.verify_token)])
def create_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    return crud.create_animal(db, animal)

@app.put("/animais/{animal_id}/inativar", response_model=schemas.AnimalOut, dependencies=[Depends(auth.verify_token)])
def inativar_animal(animal_id: int, db: Session = Depends(get_db)):
    return crud.inativar_animal(db, animal_id)

@app.post("/prontuarios/", response_model=schemas.ProntuarioOut, dependencies=[Depends(auth.verify_token)])
def create_prontuario(prontuario: schemas.ProntuarioCreate, db: Session = Depends(get_db)):
    return crud.create_prontuario(db, prontuario)
