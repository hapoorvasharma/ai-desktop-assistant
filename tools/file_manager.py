import os
from utils.logger import get_logger

logger = get_logger(__name__)


class FileManager:
    """
    Handles file and folder operations: creating, renaming,
    deleting, moving, and searching files.
    """

    def create_folder(self, path: str) -> bool:
        """
        Creates a new folder at the given path.
        Returns True if created successfully, False otherwise.
        """
        try:
            os.makedirs(path, exist_ok=False)
            logger.info(f"Created folder: {path}")
            return True
        except FileExistsError:
            logger.warning(f"Folder already exists: {path}")
            return False
        except Exception as e:
            logger.error(f"Failed to create folder '{path}': {e}")
            return False