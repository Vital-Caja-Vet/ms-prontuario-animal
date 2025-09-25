from flask import Blueprint, request, jsonify
from app import db
from models.animal import Animal
from models.consulta import Consulta
from middleware.auth import validar_token_jwt
import json

consulta_bp = Blueprint('consulta', __name__)

@consulta_bp.route('/', methods=['POST'])
@validar_token_jwt
def registrar_consulta():
    """Registrar nova consulta (protegido)"""
    try:
        data = request.get_json()
        
        # Validações obrigatórias
        required_fields = ['animal_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo '{field}' é obrigatório"}), 400
        
        # Verificar se animal existe e está ativo
        animal = Animal.query.get(data['animal_id'])
        if not animal or not animal.ativo:
            return jsonify({"error": "Animal não encontrado ou inativo"}), 404
        
        # Criar nova consulta
        nova_consulta = Consulta(
            animal_id=data['animal_id'],
            peso_consulta=data.get('peso_consulta'),
            cirurgias=data.get('cirurgias'),
            diagnostico=data.get('diagnostico'),
            tratamento=data.get('tratamento'),
            imagens_exames=json.dumps(data.get('imagens_exames', [])) if data.get('imagens_exames') else None,
        )
        
        # Atualizar peso atual do animal se informado
        if data.get('peso_consulta'):
            animal.peso_atual = data['peso_consulta']
        
        db.session.add(nova_consulta)
        db.session.commit()
        
        return jsonify(nova_consulta.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@consulta_bp.route('/<int:consulta_id>', methods=['GET'])
@validar_token_jwt
def buscar_consulta(consulta_id):
    """Buscar consulta por ID (protegido)"""
    try:
        consulta = Consulta.query.get(consulta_id)
        if not consulta:
            return jsonify({"error": "Consulta não encontrada"}), 404
        
        return jsonify(consulta.to_dict()), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@consulta_bp.route('/recentes', methods=['GET'])
@validar_token_jwt
def consultas_recentes():
    """Listar consultas mais recentes (protegido)"""
    try:
        consultas = Consulta.query.order_by(Consulta.data_consulta.desc()).limit(20).all()
        return jsonify([consulta.to_dict() for consulta in consultas]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
