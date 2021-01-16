from flask import url_for


def test_get_prefectures(client, app_mongodb):
    response = client.get(url_for('api.get_prefectures'))
    expected = [
        {
            'id': '5ff25ce597d6747527584bea',
            'name': '東京部'
        },
    ]

    assert response.status_code == 200
    assert response.json['prefectures'] == expected


def test_get_form_elements(client, app_mongodb):
    response = client.get(url_for(
        'api.get_form_elements',
        model_id='5ff25ce597d6747527584bea'
    ))
    expected = {
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
    }

    assert response.status_code == 200
    assert response.json['form'] == expected
