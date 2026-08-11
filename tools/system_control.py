import subprocess
import time
import os
from utils.logger import get_logger

logger = get_logger(__name__)


class SystemControl:
    """
    Handles operating-system level actions: opening, closing,
    and restarting applications, and opening folders.
    """

    KNOWN_APPS = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
    }

    KNOWN_FOLDERS = {
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    }

    def open_app(self, app_name: str) -> bool:
        """
        Opens an application by its friendly name.
        Returns True if it launched successfully, False otherwise.
        """
        app_name = app_name.lower().strip()

        if app_name not in self.KNOWN_APPS:
            logger.warning(f"Tried to open unknown app: '{app_name}'")
            return False

        command = self.KNOWN_APPS[app_name]

        try:
            subprocess.Popen(command)
            logger.info(f"Opened application: {app_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to open '{app_name}': {e}")
            return False

    def close_app(self, app_name: str) -> bool:
        """
        Closes a running application by its friendly name.
        Returns True if it closed successfully, False otherwise.
        """
        app_name = app_name.lower().strip()

        if app_name not in self.KNOWN_APPS:
            logger.warning(f"Tried to close unknown app: '{app_name}'")
            return False

        process_name = self.KNOWN_APPS[app_name]

        try:
            subprocess.run(
                ["taskkill", "/IM", process_name, "/F"],
                check=True,
                capture_output=True,
            )
            logger.info(f"Closed application: {app_name}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to close '{app_name}': {e}")
            return False

    def restart_app(self, app_name: str) -> bool:
        """
        Restarts an application by closing it and opening it again.
        Returns True if both steps succeeded, False otherwise.
        """
        app_name = app_name.lower().strip()

        closed = self.close_app(app_name)
        time.sleep(1)
        opened = self.open_app(app_name)

        if closed and opened:
            logger.info(f"Restarted application: {app_name}")
            return True
        else:
            logger.warning(f"Restart may have partially failed for: {app_name}")
            return False

    def open_folder(self, folder_name: str) -> bool:
        """
        Opens a known folder by its friendly name.
        Returns True if it opened successfully, False otherwise.
        """
        folder_name = folder_name.lower().strip()

        if folder_name not in self.KNOWN_FOLDERS:
            logger.warning(f"Tried to open unknown folder: '{folder_name}'")
            return False

        path = self.KNOWN_FOLDERS[folder_name]

        try:
            os.startfile(path)
            logger.info(f"Opened folder: {folder_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to open folder '{folder_name}': {e}")
            return False