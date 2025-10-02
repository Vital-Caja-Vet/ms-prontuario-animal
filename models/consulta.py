from app import db
from datetime import datetime
import json


class Consulta(db.Model):
    __tablename__ = 'consultas'

    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animais.id'), nullable=False)

    data_consulta = db.Column(db.DateTime, default=datetime.utcnow)

    peso_consulta = db.Column(db.Float)
    cirurgias = db.Column(db.Text)
    diagnostico = db.Column(db.Text)
    tratamento = db.Column(db.Text)

    imagens_exames = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'data_consulta': self.data_consulta.isoformat() if self.data_consulta else None,
            'peso_consulta': self.peso_consulta,
            'cirurgias': self.cirurgias,
            'diagnostico': self.diagnostico,
            'tratamento': self.tratamento,
            'imagens_exames': json.loads(self.imagens_exames) if self.imagens_exames else []
        }

