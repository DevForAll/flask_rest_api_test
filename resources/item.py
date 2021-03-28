from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#	CLASE ESTUDIANTE ESTA HEREDANDO LA CLASE "RESOURCE"
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank!'	
    )

    parser.add_argument('store_id',
        type = int,
        required = True,
        help = 'Every item needs a store id'	
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        
        return {'message':'Item not found'},404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        
        data = Item.parser.parse_args()

        item =  ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {'message': "An error ocurred inserting the item."}, 500

        return item.json(),201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item =  ItemModel(name, **data)
            except:
                return {'message': "An error ocurred inserting the item."}, 500
        else:
            try:
                item.price = data['price']
            except:
                    return {'message': "An error ocurred inserting the item."}, 500
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        items_list = []
        items = ItemModel.query.all()

        for item in items:
            items_list.append(item.json())
        
        return {'items': items_list}