from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type =float,
        required=True,
        help='This field cannot be left blank')

    parser.add_argument('store_id',
        type =int,
        required=True,
        help='Every item needs a store_id')

    @jwt_required()
    def get(self, name):
        row = ItemModel.find_by_name(name)

        if row:
          return row.json(), 200

        return {'message': 'Item not found'},404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message':'Item exists'},400

        data = Item.parser.parse_args()
        item1 = ItemModel(name, data['price'], data['store_id'])
        item1.save_to_db()

        return item1.json(),201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.save_to_db()
            return item.json(), 200
        else:
            item = ItemModel(name, data['price'], data['store_id'])
            item.save_to_db()
            return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item is None:
            return {'message':'Item does not exist'},400
        else:
            item.delete_from_db()
            return {'message': 'Item deleted sucessfully'},200

class ItemList(Resource):
    def get(self):

        return {'items':[item.json() for item in ItemModel.query.all()]},200
