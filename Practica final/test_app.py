import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello(client):
    """Prueba que la ruta raiz devuelva el saludo correcto"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hola Mundo desde DevOps Final!" in response.data