import json

import requests
import SessionService

API_URL = "http://127.0.0.1:8080"


def register(email, username, password) -> (bool, str):
    response = requests.post(f"{API_URL}/auth/register",
                             json={"email": email, "username": username, "password": password})

    if response.status_code == 200:
        return response.json()['success'], response.json()['error']

    return None


def login(username, password):
    response = requests.post(f"{API_URL}/auth/token", data={"username": username, "password": password})
    if response.status_code == 200:
        SessionService.set_access_token(response.json()['access_token'])
        SessionService.set_refresh_token(response.json()["refresh_token"])

        return True, ""

    return False, response.json()["detail"]


def get_user_info():
    response = requests.get(f"{API_URL}/user/get_info",
                            headers={"Authorization": f"Bearer {SessionService.get_access_token()}"})
    if response.status_code == 200:
        return response.json()["success"], response.json()["user"]

    return False, response.json()["detail"]


def create_thread(link: str, title: str, platform: str, comment: str):
    payload = json.dumps({
        "link": link,
        "title": title,
        "platform": platform,
        "comment": comment
    })

    response = requests.post(f"{API_URL}/thread/create",
                             headers={"Authorization": f"Bearer {SessionService.get_access_token()}"},
                             data=payload)
    try:
        if response.json()["detail"]:
            return False, "You are not logged in :("
    except:
        pass

    return response.json()["success"], response.json()["error"]


def search(url: bool, query: str):
    if query:
        response = requests.get(f"{API_URL}/thread/search?url={url}&query={query}&limit=100")
    else:
        response = requests.get(f"{API_URL}/thread/search?limit=100")

    return response.json()['threads']


def get_thread_details(link_id):
    response = requests.get(f"{API_URL}/thread/get/{link_id}")

    return response.json()["feedback"]


def add_feedback(link_id, comment):
    payload = json.dumps({
        "link_id": link_id,
        "comment": comment
    })

    response = requests.post(f"{API_URL}/thread/feedback/add",
                             data=payload,
                             headers={"Authorization": f"Bearer {SessionService.get_access_token()}"})

    try:
        if response.json()["detail"]:
            return False, "You are not logged in :("
    except:
        pass

    return response.json()["success"], response.json()["error"]
