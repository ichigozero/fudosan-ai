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