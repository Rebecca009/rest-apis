from db import db

class storemodel(db.Model):
    __tablename__= "stores"

    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(80), unique= True, nullable=False)
    items= db.relationship("itemmodel",back_populates="store",lazy="dynamic")
    tags= db.relationship("tagsmodel",back_populates="store", lazy="dynamic")
