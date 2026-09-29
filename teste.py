import requests 

headers ={
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzkwOTY4MDY5fQ.j00mZuDul1pUAiSgVI6-XcsdM3X11NzWkUr69Q286G0"
}

requisicao = requests.get("http://127.0.0.1:8000/auth#/refresh", headers = headers)
print(requisicao)
print(requisicao.json())