from db import db



class itemmodel(db.Model):
    __tablename__= "items"

    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(80), unique= True, nullable=False)
    price=db.Column(db.Float(precision=2),unique=False, nullable=False)
    description= db.Column(db.String)
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False, nullable= False)
    store= db.relationship("storemodel",back_populates="items")
    tags= db.relationship("tagsmodel",back_populates="items",secondary="item_tags")
