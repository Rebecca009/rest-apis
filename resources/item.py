
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from schemas import PlainItemschema,Itemschema, Itemupdateschema
from flask_jwt_extended import jwt_required

from db import db
from models import itemmodel
blp= Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class item(MethodView):
    @jwt_required(fresh= True)
    @blp.response(200,Itemschema)
    def get(self,item_id):
        item= itemmodel.query.get_or_404(item_id)
        return item
    @jwt_required(fresh= True)
    def delete(self,item_id):
        item= itemmodel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message" : "item deleted"}

    @jwt_required(fresh= True)
    @blp.arguments(Itemupdateschema)
    @blp.response(200,Itemschema)
    def put(self,item_data,item_id):
        item= itemmodel.query.get(item_id)
        if item:
            item.price= item_data["price"]
            item.name= item_data["name"]
        else:
            item= itemmodel(id= item_id,**item_data)

        db.session.add(item)
        db.session.commit()

@blp.route("/item")
class itemsList(MethodView):
     @jwt_required(fresh= True)
     @blp.arguments(Itemschema)
     @blp.response(201,Itemschema)
     def post(self,item_data):
         item= itemmodel(**item_data)
         try:
             db.session.add(item)
             db.session.commit()
         except SQLAlchemyError:
             abort(500, message= "an error")

         return item
     @jwt_required(fresh= True)
     @blp.response(200,Itemschema(many=True))
     def get(self):
          return itemmodel.query.all()
