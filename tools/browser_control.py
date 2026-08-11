import webbrowser
import os
from urllib.parse import quote_plus
from utils.logger import get_logger

logger = get_logger(__name__)

# Common locations Chrome might be installed at, on different PCs.
POSSIBLE_CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]

chrome_available = False

for path in POSSIBLE_CHROME_PATHS:
    if os.path.exists(path):
        try:
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(path))
            chrome_available = True
            logger.info(f"Chrome found and registered at: {path}")
            break
        except Exception as e:
            logger.error(f"Failed to register Chrome at '{path}': {e}")

if not chrome_available:
    logger.warning("Chrome not found on this system. Falling back to default browser.")


class BrowserControl:
    """
    Handles browser-based actions: opening websites, searching Google,
    and opening common sites like YouTube and GitHub.
    """

    KNOWN_SITES = {
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com",
        "google": "https://www.google.com",
    }

    def open_website(self, url: str) -> bool:
        """
        Opens a given website — in Chrome if available on this system,
        otherwise in whatever the system's default browser is.
        Returns True if successful, False otherwise.
        """
        try:
            if not url.startswith("http"):
                url = "https://" + url

            if chrome_available:
                webbrowser.get("chrome").open(url)
            else:
                webbrowser.open(url)

            logger.info(f"Opened website: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to open website '{url}': {e}")
            return False

    def open_known_site(self, site_name: str) -> bool:
        """
        Opens a known site (like YouTube, GitHub) by friendly name.
        Returns True if successful, False otherwise.
        """
        site_name = site_name.lower().strip()

        if site_name not in self.KNOWN_SITES:
            logger.warning(f"Unknown site: '{site_name}'")
            return False

        return self.open_website(self.KNOWN_SITES[site_name])

    def search_google(self, query: str) -> bool:
        """
        Searches Google for the given query.
        Returns True if successful, False otherwise.
        """
        safe_query = quote_plus(query.strip())
        search_url = f"https://www.google.com/search?q={safe_query}"

        return self.open_website(search_url)