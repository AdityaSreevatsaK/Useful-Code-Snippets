import requests

token = 'your-personal-access-token'
headers = {'Authorization': f'token {token}'}

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

for name in repos:
    print(name)
