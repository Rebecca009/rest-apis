import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import Plainstoreschema, storeschema

from db import db
from models import storemodel


blp= Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,storeschema)
    def get(self, store_id):
            store= storemodel.query.get_or_404(store_id)
            return store

    def delete(self,store_id):
            store= storemodel.query.get_or_404(store_id)
            db.session.delete(store)
            db.session.commit()
            return {"message": "store deleted"}

@blp.route("/store")
class storeList(MethodView):
    @blp.response(200,storeschema(many=True))
    def get(self):
         return storemodel.query.all()
    @blp.arguments(storeschema)
    @blp.response(200,storeschema)
    def post(self,store_data):
        store= storemodel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="store already found")
        except SQLAlchemyError:
            abort(500, message= "an error")
        return store, 201
