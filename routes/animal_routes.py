from flask import Blueprint, request, jsonify
from app import db
from models.animal import Animal
from middleware.auth import validar_token_jwt
import re

animal_bp = Blueprint('animal', __name__)

def validar_cpf(cpf):
    # Remove pontos e hífens
    cpf = re.sub(r'[^0-9]', '', cpf)
    return len(cpf) == 11 and cpf.isdigit()

@animal_bp.route('/', methods=['GET'])
def listar_animais():
    """
    Listar todos os animais ativos
    ---
    tags:
      - Animais
    responses:
      200:
        description: Lista de animais
        schema:
          type: array
          items:
            $ref: '#/definitions/Animal'
      500:
        description: Erro interno
    """
    try:
        animais = Animal.query.filter_by(ativo=True).all()
        return jsonify([animal.to_dict() for animal in animais]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@animal_bp.route('/<int:animal_id>', methods=['GET'])
@validar_token_jwt
def buscar_animal(animal_id):
    """Buscar animal por ID (protegido)"""
    try:
        animal = Animal.query.get(animal_id)
        if not animal or not animal.ativo:
            return jsonify({"error": "Animal não encontrado"}), 404
        
        return jsonify(animal.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@animal_bp.route('/', methods=['POST'])
@validar_token_jwt
def cadastrar_animal():
    """Cadastrar novo animal (protegido)"""
    try:
        data = request.get_json()
        
        # Validações obrigatórias
        required_fields = ['nome', 'especie', 'nome_tutor', 'cpf_tutor']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Campo '{field}' é obrigatório"}), 400
        
        # Validar CPF
        if not validar_cpf(data['cpf_tutor']):
            return jsonify({"error": "CPF inválido"}), 400
        
        # Verificar se CPF já existe
        #cpf_existente = Animal.query.filter_by(cpf_tutor=data['cpf_tutor']).first()
        #if cpf_existente:
            #return jsonify({"error": "CPF já cadastrado no sistema"}), 400

        # Verificar se já existe animal com mesmo nome para o mesmo tutor
        animal_existente = Animal.query.filter_by(
            nome=data['nome'],
            cpf_tutor=data['cpf_tutor']
        ).first()

        if animal_existente:
            return jsonify({
                "error": f"Já existe um animal chamado '{data['nome']}' para este tutor (CPF {data['cpf_tutor']})"
            }), 400

        # Criar novo animal
        novo_animal = Animal(
            nome=data['nome'],
            especie=data['especie'],
            raca=data.get('raca'),
            idade=data.get('idade'),
            peso_atual=data.get('peso_atual'),
            sexo=data.get('sexo'),
            cor=data.get('cor'),
            nome_tutor=data['nome_tutor'],
            cpf_tutor=data['cpf_tutor'],
            telefone_tutor=data.get('telefone_tutor'),
            email_tutor=data.get('email_tutor'),
            endereco_tutor=data.get('endereco_tutor'),
            observacoes=data.get('observacoes')
        )
        
        db.session.add(novo_animal)
        db.session.commit()
        
        return jsonify(novo_animal.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@animal_bp.route('/<int:animal_id>', methods=['PUT'])
@validar_token_jwt
def atualizar_animal(animal_id):
    """Atualizar dados do animal (protegido)"""
    try:
        animal = Animal.query.get(animal_id)
        if not animal or not animal.ativo:
            return jsonify({"error": "Animal não encontrado"}), 404
        
        data = request.get_json()
        
        # Atualizar campos permitidos
        campos_permitidos = [
            'nome', 'raca', 'idade', 'peso_atual', 'sexo', 'cor',
            'telefone_tutor', 'email_tutor', 'endereco_tutor', 'observacoes'
        ]
        
        for campo in campos_permitidos:
            if campo in data:
                setattr(animal, campo, data[campo])
        
        db.session.commit()
        return jsonify(animal.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@animal_bp.route('/<int:animal_id>', methods=['DELETE'])
@validar_token_jwt
def inativar_animal(animal_id):
    """Inativar animal (soft delete) - (protegido)"""
    try:
        animal = Animal.query.get(animal_id)
        if not animal:
            return jsonify({"error": "Animal não encontrado"}), 404
        
        # Verificar se tem consultas (histórico médico)
        if len(animal.consultas) > 0:
            # Soft delete - apenas inativar
            animal.ativo = False
            db.session.commit()
            return jsonify({"message": "Animal inativado (possui histórico médico)"}), 200
        else:
            # Delete físico se não tem histórico
            db.session.delete(animal)
            db.session.commit()
            return jsonify({"message": "Animal removido do sistema"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@animal_bp.route('/<int:animal_id>/historico', methods=['GET'])
@validar_token_jwt
def historico_animal(animal_id):
    """Buscar histórico médico completo do animal (protegido)"""
    try:
        animal = Animal.query.get(animal_id)
        if not animal or not animal.ativo:
            return jsonify({"error": "Animal não encontrado"}), 404
        
        consultas = [consulta.to_dict() for consulta in animal.consultas]
        consultas.sort(key=lambda x: x['data_consulta'], reverse=True)
        
        historico = {
            "animal": animal.to_dict(),
            "consultas": consultas,
            "total_consultas": len(consultas)
        }
        
        return jsonify(historico), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500