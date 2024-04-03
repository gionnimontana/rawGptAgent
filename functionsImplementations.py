import requests

def get_all_teams():
    url = f"http://45.32.153.85:8084/api/collections/teams/records?filter=(league=%27ernyanuus7tdszx%27)"
    token = "Bearer tokenValue"
    headers = {
        "Authorization": token
    }
    print('@DEVLOG@ --> calling: get_all_teams')
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Errore durante la chiamata all'API:", response.status_code)
        exit()