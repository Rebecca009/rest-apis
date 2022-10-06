from db import db



class tagsmodel(db.Model):
    __tablename__= "tags"

    id= db.Column(db.Integer,primary_key=True)
    name= db.Column(db.String(80), unique= True, nullable=False)

    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"),unique=False, nullable= False)
    store= db.relationship("storemodel",back_populates="tags")
    items= db.relationship("itemmodel",back_populates="tags", secondary="item_tags")
