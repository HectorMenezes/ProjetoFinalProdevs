def test_get_produtos(web_client):
    result = web_client.get(f'/produtos')
    print(result)
    response = result.json()
    assert result.status_code == 200
    assert response['status'] == 'SUCESSO'

