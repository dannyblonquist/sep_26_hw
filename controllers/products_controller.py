from flask import jsonify, Request, Response

from db import db
from models.products import Products, products_schema, product_schema
from models.categories import Categories
from util.reflection import populate_object


def product_add(req: Request) -> Response:
    post_data = req.form if req.form else req.json
    # product_name = post_data.get("product_name")
    # description = post_data.get("description")
    # price = post_data.get("price")
    # category_id = post_data.get("category_id")
    # active = True

    new_record = Products.get_new_product()

    populate_object(new_record, post_data)

    db.session.add(new_record)
    db.session.commit()

    product_query = db.session.query(Products).filter(Products.product_name == new_record.product_name).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == new_record.category_id).first()

    product_query.categories.append(category_query)
    db.session.commit()

    # product_record = {
    #     "product_id": query.product_id,
    #     "product_name": query.product_name,
    #     "description": query.description,
    #     "price": query.price,
    #     "active": query.active,
    # }

    return jsonify(product_schema.dump(product_query)), 201


def products_get_all(req: Request) -> Response:
    query = db.session.query(Products).all()

    # records_list = []

    # for record in query:
    #     product_record = {
    #     "product_id": record.product_id,
    #     "product_name": record.product_name,
    #     "description": record.description,
    #     "price": record.price,
    #     "active": record.active,
    # }
        
    #     records_list.append(product_record)

    return jsonify(products_schema.dump(query)), 200


def product_get_by_id(req: Request, product_id) -> Response:
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if query:

        # product_record = {
        #     "product_id": query.product_id,
        #     "product_name": query.product_name,
        #     "description": query.description,
        #     "price": query.price,
        #     "active": query.active,
        # }

        return jsonify(product_schema.dump(query)), 200
    
    else:

        return jsonify("Product with product_id {product_id} not found"), 404
    

def product_update_by_id(req: Request, product_id) -> Response:
    post_data = req.form if req.form else req.json
    # product_name = post_data.get("product_name")
    # description = post_data.get("description")
    # price = post_data.get("price")

    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if query:

        populate_object(query, post_data)

        # if product_name:
        #     query.product_name = product_name
        # if description:
        #     query.description = description
        # if price:
        #     query.price = price

    try:

        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("ERROR: Unable to update record"), 400
    
    return jsonify({"message": "Record updated successfully.", "product": product_schema.dump(query)}), 200


def product_activity(req: Request, product_id) -> Response:
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if query:

        query.active = not query.active

        try:

            db.session.commit()

            if query.active:

                return jsonify("Record activated successfully."), 200
        
            else:

                return jsonify("Record deactivated successfully."), 200

        except:
            
            db.session.rollback()

            if query.active:

                return jsonify("ERROR: Unable to activate product."), 400
            
            else:

                return jsonify("ERROR: Unable to deactivate product."), 400
            
    else:

        return jsonify(f"Product with product_id {product_id} not found."), 404
        

def product_delete_by_id(req: Request, product_id) -> Response:
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if query:

        try:

            db.session.delete(query)
            db.session.commit()

            return jsonify("Product deleted successfully"), 200
        
        except:

            db.session.rollback()

            return jsonify("ERROR: Product could not be deleted."), 400
        
    else:

        return jsonify(f"Product with product_id {product_id} not found."), 404
    

def product_add_category(req: Request) -> Response:
    post_data = req.form if req.form else req.json
    product_id = post_data.get("product_id")
    category_id = post_data.get("category_id")

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    product_query.categories.append(category_query)
    db.session.commit()

    return jsonify({"message": "Category added.", "product": product_schema.dump(product_query)}), 200