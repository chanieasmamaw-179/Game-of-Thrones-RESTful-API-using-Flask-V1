from sqlalchemy import Column, Integer, String
from config.database import db



class Character(db.Model):
    __tablename__ = 'characters'  # Explicitly defining table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    house = db.Column(db.String(150), nullable=False)
    animal = db.Column(db.String(150), nullable=False)
    symbol = db.Column(db.String(150), nullable=False)
    nickname = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    death = db.Column(db.Integer, nullable=True)
    strength = db.Column(db.String, nullable=True)

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
