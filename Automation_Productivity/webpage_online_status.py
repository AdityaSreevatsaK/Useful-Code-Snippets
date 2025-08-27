import requests


def is_website_online(url):
    """
        Description:
            Check if a website is online by sending a GET request.

        Args:
            url (str): The URL of the website to check.

        Returns:
            bool: True if the website is online (status code 200), False otherwise.
    """
    try:
        response = requests.get(url, timeout=5)
        status_code = response.status_code == 200
    except requests.exceptions.RequestException:
        status_code = False

    if status_code:
        print(f"{url} is online.")
    else:
        print(f"{url} is offline.")


# Example usage
is_website_online("https://www.google.com")
