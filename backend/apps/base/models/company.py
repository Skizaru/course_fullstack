# -*- encoding: utf-8 -*-
from apps import db
from sqlalchemy.sql import func


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text())

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('companies', lazy=True, cascade='all, delete'))


    def __repr__(self):
        return f"{self.user} - {self.name}"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime('%d %b %Y - %H:%M:%S') if self.created_at else self.created_at,
            'updated_at': self.updated_at.strftime('%d %b %Y - %H:%M:%S') if self.updated_at else self.updated_at,
            'user_id': self.user_id,
            'user': self.user.serialize
        }

