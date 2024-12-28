from sqlalchemy import Column, Integer, String
from config.database import db



class Character(db.Model):
    __tablename__ = 'characters'  # Explicitly defining table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    house = db.Column(db.String(150), nullable=True)
    animal = db.Column(db.String(100), nullable=True)
    symbol = db.Column(db.String(100), nullable=True)
    nickname = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    death = db.Column(db.Integer, nullable=True)
    strength = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Character {self.name} (House: {self.house})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "house": self.house,
            "animal": self.animal,
            "symbol": self.symbol,
            "nickname": self.nickname,
            "role": self.role,
            "age": self.age,
            "death": self.death,
            "strength": self.strength
        }
