def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_wrong_url(client):
    response = client.get("/wrong_url")
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Url not found'


def test_url_shortener(client):
    url = 'https://github.com/georgegozal/url_shortener_api'
    response = client.post('/', json={'url': url})
    assert response.status_code == 201
    assert response.json['status'] == 'success'
    shortened_url = response.json['result']

    # Try to redirect to the original url
    response = client.get(shortened_url)
    assert response.status_code == 302

    # Try to create the same shortened url again
    response = client.post('/', json={'url': url})
    assert response.status_code == 409
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'Url already exists'
