from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from dotenv import load_dotenv
import os, yaml

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost/ms_prontuario_animal')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar banco de dados
db = SQLAlchemy(app)

# Configurar Swagger para documentação da API, carregando do swagger.yml
swagger_path = os.path.join(os.path.dirname(__file__), 'swagger.yml')
with open(swagger_path, 'r', encoding='utf-8') as f:
    swagger_template = yaml.safe_load(f)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # inclui todas as rotas
            "model_filter": lambda tag: True,  # inclui todos os modelos
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Importar modelos e rotas
from models.animal import Animal
from models.consulta import Consulta
from routes.animal_routes import animal_bp
from routes.consulta_routes import consulta_bp

# Registrar blueprints
app.register_blueprint(animal_bp, url_prefix='/api/v1/animais')
app.register_blueprint(consulta_bp, url_prefix='/api/v1/consultas')

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return {"status": "OK", "service": "ms_prontuario_animal"}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 8001))
    app.run(host='0.0.0.0', port=port, debug=True)
