import os

from dotenv import load_dotenv
from huggingface_hub import HfApi, login
from huggingface_hub.utils import HfHubHTTPError


def delete_folder_on_hub(repo_id: str, path_in_repo: str, repo_type: str = "dataset"):
    """
    Deletes a folder from a specified Hugging Face Hub repository.

    Args:
        repo_id (str): The ID of the repository on the Hub.
        path_in_repo (str): The folder path to delete within the repository.
        repo_type (str, optional): The type of repository. Defaults to "dataset".
    """
    print(f"Attempting to delete folder '{path_in_repo}' in repo '{repo_id}'...")

    # Load environment variables and authenticate
    load_dotenv()
    hf_token = os.getenv("HUGGINGFACE_REPO_KEY")
    if not hf_token:
        print("Hugging Face token 'HUGGINGFACE_REPO_KEY' not found in .env file.")
        return

    try:
        login(token=hf_token)
        api = HfApi()

        # Execute the delete operation
        api.delete_folder(
            repo_id=repo_id,
            path_in_repo=path_in_repo,
            repo_type=repo_type,
            # Use a descriptive commit message for the deletion
            commit_message=f"feat: delete content in {path_in_repo}"
        )
        print(f"Successfully deleted folder '{path_in_repo}'.")

    except HfHubHTTPError as e:
        # Specifically handle cases where the folder or repo is not found
        if e.response.status_code == 404:
            print(f"Could not delete. Folder '{path_in_repo}' or repo '{repo_id}' not found.")
        else:
            print(f"An HTTP error occurred while deleting folder: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
