import requests
from flask import request, jsonify
from functools import wraps
import os

def validar_token_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Pegar token do header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({"error": "Token de autorização requerido"}), 401
        
        try:
            # Validar token com o serviço de autenticação
            auth_url = os.getenv('AUTH_SERVICE_URL', 'https://02321cb3f955.ngrok-free.app/api/v1')
            response = requests.get(
                f"{auth_url}/profile/me/",
                headers={"Authorization": auth_header},
                timeout=10
            )
            
            if response.status_code != 200:
                return jsonify({"error": "Token inválido"}), 401
                
            # Anexar dados do usuário à request
            request.user_data = response.json()
            
        except requests.RequestException as e:
            return jsonify({"error": "Erro ao validar token", "details": str(e)}), 500
        
        return f(*args, **kwargs)
    
    return decorated_function