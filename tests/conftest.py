import os

import pytest

from fudosan_ai import Preprocessor


def test_file_folder(filename):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
        filename
    )


@pytest.fixture(scope='module')
def raw_rent_data():
    return os.path.join(test_file_folder('raw_rent_data.csv'))


@pytest.fixture(scope='module')
def cleaned_rent_data():
    return os.path.join(test_file_folder('cleaned_rent_data.csv'))


@pytest.fixture(scope='module')
def one_hot_encoded_rent_data():
    return os.path.join(test_file_folder('one_hot_encoded_rent_data.csv'))


@pytest.fixture(scope='module')
def form_elements():
    return os.path.join(test_file_folder('form_elements.json'))


@pytest.fixture
def preprocessor():
    return Preprocessor()
