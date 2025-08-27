import os

import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}


def get_all_repos():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Error:", response.json())
            break

        data = response.json()
        if not data:
            break

        repos.extend([repo['name'] for repo in data])
        page += 1

    return repos
