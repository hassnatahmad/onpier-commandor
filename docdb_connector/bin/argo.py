import httpx


def get_token(username, password):
    response = httpx.post("https://argo.prod.huk.onpier.de/api/v1/session", json={"username": username, "password": password})
    if response.status_code != 200:
        raise Exception("Could not validate credentials")
    return response.json()["token"]


token = get_token('argo-apps-manager', 'QVZPjfhdRpZAxsHplyoFy0m9sRtTj50Z8Ut4MXvDJQi38lT0lvWsrVakpREjeVVk')
print(token)
