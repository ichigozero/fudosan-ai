import pytest
from bson.objectid import ObjectId

from app import create_app
from app import mongo


class TestConfig():
    TESTING=True
    MONGO_URI = 'mongodb://localhost:27017/fudosan-ai-test'


@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)

    with app.app_context():
        app.test_request_context().push()
        yield app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def app_mongodb(app):
    models = [
        {
            '_id': ObjectId('5ff25ce597d6747527584bea'),
            'csv_checksum' : 'd013d2241bb249bb044ac227ed948d02',
            'prefecture' : '東京部',
            'form_elements' : {
                'checkbox' : {
                    'features' : ['24時間セキュリティー', 'カード決済可能'],
                    'popular_items' : ['エアコン', 'オートロック']
                },
                'dropdown_range' : {
                    'access' : [1, 14],
                    'build_date' : [1970, 2020],
                    'room_size' : [20.0, 100.0],
                    'floor_number' : [-2, 35],
                    'number_of_floors' : [2, 62]
                },
                'dropdown_choice' : {
                    'location' : ['新宿区'],
                    'room_layout' : ['2LDK', 'ワンルーム'],
                    'category' : ['アパート', 'マンション'],
                    'azimuth' : ['北', '南'],
                    'building_structure' : ['木造', '鉄骨']
                },
                'radiobutton' : {'has_parking' : [0, 1]}
            },
            'model' : {
                'pickle_path' : '/static/東京部/東京部_20210104_090939.pkl',
                'checksum' : 'e7708d20df5a1fcdc243466b6b2213b1',
                'mean_abs_error' : {
                    'training' : '755.0167',
                    'test' : '5583.1486'
                }
            },
            'active' : True
        },
    ]

    mongo.db.models.insert_many(models)

    yield mongo

    mongo.db.command('dropDatabase')