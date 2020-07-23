import pandas as pd
from pandas._testing import assert_series_equal


def test_price_str_to_float(preprocessor):
    input_series = pd.Series([
        '0.72万円',
        '1.2万円※',
        '1.5〜1.7万円',
        '3,000円',
        'なし',
        'なし※'
    ])
    expected = pd.Series([
        7200.0,
        12000.0,
        16000.0,
        3000.0,
        0.0,
        0.0
    ])
    output = input_series.apply(preprocessor._convert_price_str_to_float)

    assert_series_equal(output, expected)


def test_extract_city_of_tokyo_address(preprocessor):
    input_series = pd.Series([
        '東京都文京区本郷4[地図を確認]',
        '東京都港区高輪1',
    ])
    expected = pd.Series([
        '文京区',
        '港区',
    ])
    output = input_series.apply(
        preprocessor._extract_city_of_address,
        args=('東京都', '区',)
    )

    assert_series_equal(output, expected)


def test_extract_city_of_chiba_address(preprocessor):
    input_series = pd.Series([
        '千葉県我孫子市天王台1[地図を確認]',
        '千葉県船橋市東船橋001',
        '千葉県市川市下新宿',
        '木更津市岩根3丁目',
        '千葉県印旛郡栄町安食2',
    ])
    expected = pd.Series([
        '我孫子市',
        '船橋市',
        '市川市',
        '木更津市',
        '印旛郡',
    ])
    output = input_series.apply(
        preprocessor._extract_city_of_address,
        args=('千葉県', '市|郡',)
    )

    assert_series_equal(output, expected)
