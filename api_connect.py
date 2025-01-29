import base64
from base64 import b64encode
import requests


def conexao(data):
    client_id = 'uHpXjsZAi49A'
    client_secret = '2tZrvxqLYZ1N'

    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("ascii")
    auth = base64.b64encode(auth_bytes).decode("ascii")

    auth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth}'
    }

    # Corpo da requisição de autenticação
    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_url = 'https://api.anbima.com.br/oauth/access-token'

    auth_response = requests.post(
        auth_url, headers=auth_headers, data=auth_data)

    access_token = auth_response.json().get('access_token')

    headers = {
        'access_token': access_token,
        'client_id': client_id
    }

    parameters = {
        'data': f'{data}'
    }

    data_url = 'https://api.anbima.com.br/feed/precos-indices/v1/debentures/mercado-secundario'

    try:
        data_response = requests.get(
            data_url, headers=headers, params=parameters)
    except:
        print("Acesso negado à API")

    if data_response.status_code == 200:
        data = data_response.json()
    else:
        print(f"Erro ao obter os dados: {
            data_response.status_code} - {data_response.text}")

    return data
