import os
import uuid
from datetime import datetime
from typing import Optional

from fastapi import UploadFile, HTTPException
from passlib.context import CryptContext

# ---- Configurações ----
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB por arquivo
DEFAULT_UPLOAD_DIR = "uploads"

# ---- Passlib (opcional, caso você tenha usuários/senhas) ----
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash de senha com bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica senha plain vs hash."""
    return pwd_context.verify(plain_password, hashed_password)

# ---- Helpers de arquivos ----
def ensure_upload_dir(path: str = DEFAULT_UPLOAD_DIR) -> str:
    """Garante que o diretório de upload exista e retorna o caminho."""
    os.makedirs(path, exist_ok=True)
    return path

def _ext_from_content_type(content_type: str) -> str:
    mapping = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
    }
    return mapping.get(content_type, "")

async def save_upload_file(upload_file: UploadFile, upload_dir: str = DEFAULT_UPLOAD_DIR) -> str:
    """
    Salva um UploadFile no disco (async).
    Retorna o caminho relativo do arquivo salvo.
    - Valida tipo e tamanho.
    """
    # valida tipo
    if upload_file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido. Use jpg/png/gif.")

    # lê conteúdo (async)
    contents = await upload_file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo muito grande (máx 5MB).")

    # cria pasta
    ensure_upload_dir(upload_dir)

    # ext e nome único
    ext = os.path.splitext(upload_file.filename)[1] or _ext_from_content_type(upload_file.content_type)
    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, filename)

    # grava no disco
    with open(file_path, "wb") as f:
        f.write(contents)

    return file_path  # pode salvar esse path no campo `imagem` do prontuário

def remove_file(path: str) -> None:
    """Remove arquivo se existir (ignora erros)."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass
