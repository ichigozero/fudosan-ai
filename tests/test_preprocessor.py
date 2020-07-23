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
