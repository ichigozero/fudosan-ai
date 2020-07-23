import pytest

from fudosan_ai import Preprocessor


@pytest.fixture
def preprocessor():
    return Preprocessor()
