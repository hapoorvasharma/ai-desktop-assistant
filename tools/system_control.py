import subprocess
from utils.logger import get_logger

logger = get_logger(__name__)


class SystemControl:
    """
    Handles operating-system level actions: opening, closing,
    and restarting applications.
    """

    KNOWN_APPS = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
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