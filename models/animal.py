from app import db
from datetime import datetime

class Animal(db.Model):
    __tablename__ = 'animais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    peso_atual = db.Column(db.Float)
    sexo = db.Column(db.String(10))
    cor = db.Column(db.String(50))
    
    nome_tutor = db.Column(db.String(100), nullable=False)
    cpf_tutor = db.Column(db.String(14), nullable=False)
    telefone_tutor = db.Column(db.String(15))
    email_tutor = db.Column(db.String(100))
    endereco_tutor = db.Column(db.Text)
    
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    observacoes = db.Column(db.Text)
    
    consultas = db.relationship('Consulta', backref='animal', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'especie': self.especie,
            'raca': self.raca,
            'idade': self.idade,
            'peso_atual': self.peso_atual,
            'sexo': self.sexo,
            'cor': self.cor,
            'nome_tutor': self.nome_tutor,
            'cpf_tutor': self.cpf_tutor,
            'telefone_tutor': self.telefone_tutor,
            'email_tutor': self.email_tutor,
            'endereco_tutor': self.endereco_tutor,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'observacoes': self.observacoes,
            'total_consultas': len(self.consultas)
        }