from huggingface_hub import HfApi, login
from huggingface_hub.utils import HfHubHTTPError


def delete_folder_on_hub(repo_id: str, path_in_repo: str, repo_type: str = "dataset", hf_token: str = None):
    """
    Deletes a folder from a specified Hugging Face Hub repository.

    Args:
        repo_id (str): The ID of the repository on the Hub.
        path_in_repo (str): The folder path to delete within the repository.
        repo_type (str, optional): The type of repository. Defaults to "dataset".
        hf_token (str, optional): The huggingface token to sign in and delete required folder.
    """
    print(f"Attempting to delete folder '{path_in_repo}' in repo '{repo_id}'...")

    try:
        login(token=hf_token)
        api = HfApi()

        # Execute the delete operation
        api.delete_folder(
            repo_id=repo_id,
            path_in_repo=path_in_repo,
            repo_type=repo_type,
            commit_message=f"feat: delete content in {path_in_repo}"
        )
        print(f"Successfully deleted folder '{path_in_repo}'.")
        return True, f"Successfully deleted folder '{path_in_repo}'."

    except HfHubHTTPError as e:
        failed_message = ""
        # Specifically handle cases where the folder or repo is not found
        if e.response.status_code == 404:
            print(f"Could not delete. Folder '{path_in_repo}' or repo '{repo_id}' not found.")
            failed_message = f"Could not delete. Folder '{path_in_repo}' or repo '{repo_id}' not found."
        else:
            print(f"An HTTP error occurred while deleting folder: {e}")
            failed_message = f"An HTTP error occurred while deleting folder: {e}"
        return False, failed_message
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False, f"An unexpected error occurred: {e}"
