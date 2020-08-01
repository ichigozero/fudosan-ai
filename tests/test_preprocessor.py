import pandas as pd
from pandas._testing import assert_frame_equal
from pandas._testing import assert_index_equal
from pandas._testing import assert_series_equal


def test_get_index_of_rows_with_no_access_to_public_transports(preprocessor):
    input_df = pd.DataFrame({
        'access': [
            '成田線椎柴駅 車で6',
            '四街道駅 徒歩22分',
            'つくばエクスプレス 車1分|花野井神社 停歩6分以内',
            'JR内房線五井駅より',
            None,
        ]
    })
    expected = pd.Int64Index([0, 3, 4])
    output = (
        preprocessor
        ._get_index_of_rows_with_no_access_to_public_transports(
            input_df,
            'access'
        )
    )

    assert_index_equal(output, expected)


def test_get_index_of_rows_with_no_floor_numbers(preprocessor):
    input_df = pd.DataFrame({
        'floor_number': [
            '1階部分',
            '-',
            '',
            '地下1階部分',
            None,
        ]
    })
    expected = pd.Int64Index([1, 2, 4])
    output = preprocessor._get_index_of_rows_with_no_floor_numbers(
        input_df,
        'floor_number'
    )

    assert_index_equal(output, expected)


def test_price_str_to_float(preprocessor):
    input_series = pd.Series([
        '0.72万円',
        '1.2万円※',
        '1.5～1.7万円',
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


def test_extract_minimum_access_time_to_public_transport(preprocessor):
    input_series = pd.Series([
        '四街道駅 徒歩22分',
        '川間駅 徒歩9分|柏駅 徒歩268分',
        '総武本線 徒歩67分|物井駅 徒歩51分|都賀駅 徒歩23分',
        'つくばエクスプレス 車1分|花野井神社 停歩6分以内|総武本線 徒歩19分',
    ])
    expected = pd.Series([22, 9, 23, 6, ])
    output = input_series.apply(
        preprocessor._extract_minimum_access_time_to_public_transport
    )

    assert_series_equal(output, expected)


def test_extract_room_layout(preprocessor):
    input_series = pd.Series([
        '2LDK (洋6 洋4.5 LDK16.5)',
        'ワンルーム (洋8.5)',
        'ワンルーム',
    ])
    expected = pd.Series(['2LDK', 'ワンルーム', 'ワンルーム'])
    output = input_series.apply(preprocessor._extract_room_layout)

    assert_series_equal(output, expected)


def test_extract_build_year(preprocessor):
    input_series = pd.Series([
        '築41年(1980年)',
        '築27年(1994年04月)',
    ])
    expected = pd.Series([1980, 1994, ])
    output = input_series.apply(preprocessor._extract_build_year)

    assert_series_equal(output, expected)


def test_extract_floor_number(preprocessor):
    input_series = pd.Series([
        '1階部分',
        '10階部分',
        '地下1階部分',
        '地下4階部分',
    ])
    expected = pd.Series([1, 10, -1, -4, ])
    output = input_series.apply(preprocessor._extract_floor_number)

    assert_series_equal(output, expected)


def test_convert_multi_categorical_variables_to_binaries(preprocessor):
    input_series = pd.Series([
        'a|b|c|c',
        'c|d|',
        'd',
        None,
    ])
    expected = pd.DataFrame({
        'col_a': [1, 0, 0, 0, ],
        'col_b': [1, 0, 0, 0, ],
        'col_c': [1, 1, 0, 0, ],
        'col_d': [0, 1, 1, 0, ],
    })
    output = preprocessor._convert_multi_categorical_variables_to_binaries(
        series=input_series,
        prefix='col'
    )

    assert_frame_equal(output, expected)


def test_convert_to_binary(preprocessor):
    input_series = pd.Series([
        'あり',
        'あり 無料',
        'なし',
        '空きなし',
    ])
    expected = pd.Series([1, 1, 0, 0, ])
    output = input_series.apply(preprocessor._convert_to_binary)

    assert_series_equal(output, expected)
