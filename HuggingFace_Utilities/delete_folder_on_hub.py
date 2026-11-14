"""Delete a single folder with request-scoped Hugging Face authentication."""

from pathlib import PurePosixPath

from huggingface_hub import HfApi
from huggingface_hub.utils import HfHubHTTPError


def delete_folder_on_hub(repo_id: str, path_in_repo: str,
                         repo_type: str = "dataset", hf_token: str | None = None):
    try:
        path = path_in_repo.strip().strip("/")
        parts = PurePosixPath(path).parts
        if (not path or path in (".", "..") or not parts
                or any(part in ("", ".", "..") for part in parts)
                or "\\" in path):
            return False, "A valid, non-root folder path is required"
        if repo_type not in ("dataset", "model", "space"):
            return False, "Invalid repository type"
        if not repo_id.strip() or not hf_token:
            return False, "Repository ID and token are required"
        # Never call login(): it persists credentials in a shared process.
        HfApi(token=hf_token).delete_folder(
            repo_id=repo_id, path_in_repo=path,
            repo_type=repo_type, commit_message=f"Delete folder {path}",
        )
        return True, f"Deleted folder '{path}' from '{repo_id}'"
    except HfHubHTTPError as exc:
        return False, f"Hugging Face request failed (HTTP {exc.response.status_code})"
    except Exception as exc:
        return False, f"Deletion failed ({type(exc).__name__})"
