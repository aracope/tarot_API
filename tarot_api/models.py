from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

@dataclass
class Card(db.Model):
    __tablename__ = "cards"

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(120), nullable=False, index=True)
    # “Major Arcana” / “Minor Arcana”
    arcana: str = db.Column(db.String(50), nullable=False, index=True)   
    # Cups, Swords, Wands, Pentacles, or NULL for majors
    suit: str = db.Column(db.String(30), nullable=True, index=True)      
    upright_meaning: str = db.Column(db.Text, nullable=True)
    reversed_meaning: str = db.Column(db.Text, nullable=True)
    # Yes/No/Maybe
    yes_no: str = db.Column(db.String(10), nullable=True)                
    image_url: str = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "arcana": self.arcana,
            "suit": self.suit,
            "upright_meaning": self.upright_meaning,
            "reversed_meaning": self.reversed_meaning,
            "yes_no": self.yes_no,
            "image_url": self.image_url,
        }
