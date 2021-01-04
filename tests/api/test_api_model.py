import json
import pickle

from flask import url_for


def test_get_rent_price(mocker, client, app_mongodb):
    mocked_model = mocker.MagicMock()
    mocked_model.predict.return_value = [999.99]

    mocked_open = mocker.patch('builtins.open', mocker.MagicMock())
    mocker.patch(
        'pickle.load',
        mocker.MagicMock(side_effect=[mocked_model])
    )

    url = '/api/v1.0/model/{id}/rent-price?{args}'

    response = client.get(
        url.format(
            id='5ff25ce597d6747527584bea',
            args='val=foo&val=1'
        )
    )

    expected = {
        'price': 999.99,
        'mean_error': 5583.1486
    }

    mocked_open.assert_called_once_with('東京部_20210104_090939.pkl', 'rb')
    mocked_model.predict.assert_called_once_with([['foo', 1]])
    assert response.status_code == 200
    assert response.json['result'] == expected
