from flask import jsonify, Request, Response

from db import db
from util.reflection import populate_object
from models.categories import Categories, categories_schema, category_schema


def category_add(req: Request) -> Response:
    post_data = req.form if req.form else req.json
    category_name = post_data.get("category_name")
    
    new_record = Categories.get_new_category()

    populate_object(new_record, post_data)

    try:

        db.session.add(new_record)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("ERROR: Unable to add record."), 400

    query = db.session.query(Categories).filter(Categories.category_name == new_record.category_name).first()

    return jsonify(category_schema.dump(query)), 201


def categories_get_all(req: Request) -> Response:
    query = db.session.query(Categories).all()

    # record_list = []

    # for record in query:
    #     category_record = {
    #         "category_id": record.category_id,
    #         "category_name": record.category_name
    #     }

    #     record_list.append(category_record)

    return jsonify(categories_schema.dump(query)), 200


def category_update_by_id(req: Request, category_id) -> Response:
    post_data = req.form if req.form else req.json
    category_name = post_data.get("category_name")

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if category_query:

        # if category_name:
        #     category_query.category_name = category_name

        populate_object(category_query, post_data)

        # category_record = {
        #     "category_id": category_query.category_id,
        #     "category_name": category_query.category_name
        # }

        try:

            db.session.commit()

        except:
        
            db.session.rollback()

            return jsonify("ERROR: Unable to update record"), 400
    
        return jsonify(category_schema.dump(category_query)), 200
    
    else:
        return jsonify(f"Category with category_id {category_id} not found"), 404
    

def category_delete_by_id(req: Request, category_id) -> Response:
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    try:
        db.session.delete(category_query)
        db.session.commit()

    except:
        db.session.rollback()

        return jsonify("ERROR: Unable to delete record."), 400
    
    return jsonify("Record successfully deleted."), 200