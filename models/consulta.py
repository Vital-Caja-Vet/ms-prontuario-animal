from app import db
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'), nullable=False)
    
    data_consulta = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_consulta = db.Column(db.String(50))  # rotina, emergência, cirurgia
    veterinario = db.Column(db.String(100), nullable=False)
    
    # Dados da consulta
    peso_consulta = db.Column(db.Float)
    temperatura = db.Column(db.Float)
    diagnostico = db.Column(db.Text)
    tratamento = db.Column(db.Text)
    medicamentos = db.Column(db.Text)
    observacoes = db.Column(db.Text)
    
    # Anexos (URLs de imagens)
    imagens_exames = db.Column(db.Text)  # JSON string com URLs
    
    # Próxima consulta
    retorno_em = db.Column(db.Date)
    
    def to_dict(self):
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'data_consulta': self.data_consulta.isoformat() if self.data_consulta else None,
            'tipo_consulta': self.tipo_consulta,
            'veterinario': self.veterinario,
            'peso_consulta': self.peso_consulta,
            'temperatura': self.temperatura,
            'diagnostico': self.diagnostico,
            'tratamento': self.tratamento,
            'medicamentos': self.medicamentos,
            'observacoes': self.observacoes,
            'imagens_exames': self.imagens_exames,
            'retorno_em': self.retorno_em.isoformat() if self.retorno_em else None
        }