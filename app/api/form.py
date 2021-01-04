from bson.objectid import ObjectId
from flask import abort

from app import mongo
from app.api import bp


@bp.route('/v1.0/prefectures', methods=['GET'])
def get_prefectures():
    documents = mongo.db.models.find({'active': True})

    prefectures = []

    for document in documents:
        prefecture = {
            'id': str(document['_id']),
            'name': document['prefecture']
        }
        prefectures.append(prefecture)

    if not prefectures:
        abort(404)

    return {'prefectures': prefectures}


@bp.route('/v1.0/form/<string:model_id>', methods=['GET'])
def get_form_elements(model_id):
    document = mongo.db.models.find_one({
        '_id': ObjectId(model_id),
        'active': True
    })

    if not document:
        abort(404)

    return {'form': document['form_elements']}