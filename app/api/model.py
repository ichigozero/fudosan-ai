import pickle

from bson.objectid import ObjectId
from flask import abort
from flask import request

from app import mongo
from app.api import bp

@bp.route(
    '/v1.0/model/<string:model_id>/rent-price',
    methods=['GET']
)
def predict_rent_price(model_id):
    document = mongo.db.models.find_one({
        '_id': ObjectId(model_id),
        'active': True
    })

    try:
        mean_error = document['model']['mean_abs_error']['test']

        with open(document['model']['pickle_path'], 'rb') as f:
            model = pickle.load(f)
    except (KeyError, IOError, TypeError):
        abort(404)

    rent_data = request.args.getlist('val')

    for index, element in enumerate(rent_data):
        try:
            rent_data[index] = float(element)
        except ValueError:
            pass

    rent_prices = model.predict([rent_data])

    return {
        'result': {
            'price': round(rent_prices[0], 4),
            'mean_error': mean_error
        }
    }
