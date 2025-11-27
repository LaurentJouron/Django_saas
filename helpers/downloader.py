import requests
from pathlib import Path


def download_to_local(
    url: str,
    out_path: Path,
    parent_mkdir: bool = True,
    timeout: int = 30,
    chunk_size: int = 8192,
) -> bool:
    """Download a file from a URL to a local path.

    Args:
        url: Source URL to download from
        out_path: Destination path for the downloaded file
        parent_mkdir: Create parent directories if they don't exist
        timeout: Request timeout in seconds
        chunk_size: Size of chunks for large file downloads

    Returns:
        True if download succeeded, False otherwise

    Raises:
        ValueError: If out_path is not a valid pathlib.Path object

    Example:
        >>> from pathlib import Path
        >>> url = "https://example.com/file.css"
        >>> download_to_local(url, Path("static/vendors/file.css"))
        True
    """
    if not isinstance(out_path, Path):
        raise ValueError(f"{out_path} must be a valid pathlib.Path object")

    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()

        # Write file in chunks to handle large files efficiently
        with out_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)

        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return False
