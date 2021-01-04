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