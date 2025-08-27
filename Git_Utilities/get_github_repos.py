import requests


def get_all_repos(github_token):
    """
    Retrieves all GitHub repository names for the authenticated user.

    Returns:
        list: A list of repository names (str).

    Uses pagination to fetch up to 100 repositories per page until all are retrieved.
    Prints an error message and stops if the API request fails.
    """
    headers = {'Authorization': f'token {github_token}'}
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
