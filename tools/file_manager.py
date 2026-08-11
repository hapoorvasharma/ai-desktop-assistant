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

    def rename_file(self, old_path: str, new_path: str) -> bool:
        """
        Renames (or moves) a file from old_path to new_path.
        Returns True if successful, False otherwise.
        """
        try:
            if not os.path.exists(old_path):
                logger.warning(f"File not found: {old_path}")
                return False

            os.rename(old_path, new_path)
            logger.info(f"Renamed '{old_path}' to '{new_path}'")
            return True
        except Exception as e:
            logger.error(f"Failed to rename '{old_path}': {e}")
            return False

    def delete_file(self, path: str) -> bool:
        """
        Permanently deletes a file at the given path.
        Returns True if deleted successfully, False otherwise.
        """
        try:
            if not os.path.exists(path):
                logger.warning(f"File not found: {path}")
                return False

            if os.path.isdir(path):
                logger.warning(f"Refusing to delete '{path}': it is a folder, not a file")
                return False

            os.remove(path)
            logger.info(f"Deleted file: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete '{path}': {e}")
            return False