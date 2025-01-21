# -*- encoding: utf-8 -*-
from apps import db
from sqlalchemy.sql import func


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text())
    comment = db.Column(db.Text())
    quantity = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    # Relationships
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('products', lazy=True, cascade='all, delete'))


    def __repr__(self):
        return f"{self.customer} - {self.circuit} - {self.period}"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'comment': self.comment,
            'quantity': self.quantity,
            'created_at': self.created_at.strftime('%d %b %Y - %H:%M:%S') if self.created_at else self.created_at,
            'updated_at': self.updated_at.strftime('%d %b %Y - %H:%M:%S') if self.updated_at else self.updated_at,
            'company_id': self.company_id,
            'company': self.company.serialize
        }

