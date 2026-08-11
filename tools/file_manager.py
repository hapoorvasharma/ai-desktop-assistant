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

    def move_file(self, source_path: str, destination_folder: str) -> bool:
        """
        Moves a file into a destination folder, keeping its original filename.
        Returns True if successful, False otherwise.
        """
        if not os.path.exists(source_path):
            logger.warning(f"File not found: {source_path}")
            return False

        if not os.path.isdir(destination_folder):
            logger.warning(f"Destination is not a valid folder: {destination_folder}")
            return False

        filename = os.path.basename(source_path)
        destination_path = os.path.join(destination_folder, filename)

        return self.rename_file(source_path, destination_path)

    def search_files(self, keyword: str, search_folder: str) -> list:
        """
        Searches for files whose name contains the given keyword,
        looking inside search_folder and all its sub-folders.
        Returns a list of full file paths that match.
        """
        keyword = keyword.lower().strip()
        found_files = []

        if not os.path.isdir(search_folder):
            logger.warning(f"Search folder does not exist: {search_folder}")
            return found_files

        for root, dirs, files in os.walk(search_folder):
            for file in files:
                if keyword in file.lower():
                    full_path = os.path.join(root, file)
                    found_files.append(full_path)

        logger.info(f"Search for '{keyword}' in '{search_folder}' found {len(found_files)} result(s)")
        return found_files