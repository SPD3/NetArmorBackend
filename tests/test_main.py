from src.main import basic_endpoint

def test_basic():
    assert 1 == 1

def test_basic_endpoint():
    assert basic_endpoint() == "Hello World"