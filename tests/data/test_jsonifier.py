import json

import pandas as pd

from app.data.jsonifier import Jsonifier

def test_to_json(cleaned_rent_data, form_elements):
    cleaned_df = pd.read_csv(cleaned_rent_data)
    cleaned_df.fillna('', inplace=True)

    output = Jsonifier.to_json(cleaned_df)

    with open(form_elements) as f:
        expected = json.load(f)

    assert output == expected