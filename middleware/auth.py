import os
import re
from functools import wraps

import requests
from flask import request, jsonify


def validar_token_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '').strip()

        match = re.match(r'^\s*(?:Bearer|Token)\s+(.+)$', auth_header, flags=re.IGNORECASE)
        token = match.group(1).strip() if match else auth_header

        if not token:
            return jsonify({"error": "Token de autorização requerido"}), 401

        try:
            auth_url = (os.getenv('AUTH_SERVICE_URL') or '').rstrip('/')
            response = requests.get(
                f"{auth_url}/profile/me/",
                headers={"Authorization": token},
                timeout=10,
            )

            if response.status_code != 200:
                return jsonify({"error": "Token inválido"}), 401

            request.user_data = response.json()

        except requests.RequestException as e:
            return jsonify({"error": "Erro ao validar token", "details": str(e)}), 500

        return f(*args, **kwargs)

    return decorated_function

