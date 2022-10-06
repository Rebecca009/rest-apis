from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import tagsmodel,storemodel,itemmodel
from schemas import tagschema, TagandItemschema

blp = Blueprint("Tags","tags",description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class Tagsinstore(MethodView):
    @blp.response(200,tagschema(many=True))
    def get(self, store_id):
        store= storemodel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(tagschema)
    @blp.response(201,tagschema)
    def post(self,tag_data,store_id):
        if TagModel.query.filter(TagModel.store_id == store_id).first():
            abort(400, message="A tag with that name already exists in that store.")
        tag= tagsmodel(**tag_data, store_id= store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
            500,
            message=str(e)
            )
        return tag

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200,tagschema)
    def get(self,tag_id):
        tag= tagsmodel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self,tag_id):
        tag= tagsmodel.query.get_or_404(tag_id)
        if not tag.items:
             db.session.delete(tag)
             db.session.commit()
             return {"message": "tag deleted"}
             
        abort(400, message= "cannot delete tag")

@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class Linktagstoitem(MethodView):
    @blp.response(201,tagschema)
    def post(self, item_id,tag_id):
        item= itemmodel.query.get_or_404(item_id)
        tag= tagsmodel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            abort(500, message="an error")

        return tag

    @blp.response(200,TagandItemschema)
    def delete(self, item_id, tag_id):
        item= itemmodel.query.get_or_404(item_id)
        tag= tagsmodel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError :
            abort(500, message="an error")

        return {"message": "item deleted"}
