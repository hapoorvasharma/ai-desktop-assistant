import time
from tools.system_control import SystemControl
from tools.file_manager import FileManager
from tools.browser_control import BrowserControl
from tools.voice import Voice
from utils.logger import get_logger

logger = get_logger(__name__)


def process_command(user_input, system_control, file_manager, browser_control):
    """
    Takes a command (from typing or voice) and executes the matching action.
    """
    lower_input = user_input.lower()

    if lower_input.startswith("open folder "):
        folder_name = user_input[len("open folder "):]
        success = system_control.open_folder(folder_name)
        if not success:
            print(f"Sorry, I don't know how to open the '{folder_name}' folder yet.")

    elif lower_input.startswith("search apps "):
        keyword = user_input[len("search apps "):]
        results = system_control.search_installed_apps(keyword)
        if results:
            print("Found these apps:")
            for app in results:
                print(f"  - {app}")
        else:
            print(f"No installed apps found matching '{keyword}'.")

    elif lower_input.startswith("open "):
        app_name = user_input[len("open "):]
        success = system_control.open_app(app_name)
        if not success:
            print(f"Sorry, I don't know how to open '{app_name}' yet.")

    elif lower_input.startswith("close "):
        app_name = user_input[len("close "):]
        success = system_control.close_app(app_name)
        if not success:
            print(f"Sorry, I couldn't close '{app_name}'.")

    elif lower_input.startswith("restart "):
        app_name = user_input[len("restart "):]
        success = system_control.restart_app(app_name)
        if not success:
            print(f"Sorry, I couldn't restart '{app_name}'.")

    elif lower_input.startswith("create folder "):
        path = user_input[len("create folder "):]
        success = file_manager.create_folder(path)
        if not success:
            print(f"Sorry, I couldn't create the folder at '{path}'.")

    elif lower_input.startswith("delete file "):
        path = user_input[len("delete file "):]
        success = file_manager.delete_file(path)
        if not success:
            print(f"Sorry, I couldn't delete '{path}'.")

    elif lower_input.startswith("rename file "):
        rest = user_input[len("rename file "):]
        if " to " not in rest:
            print("Please use the format: rename file <old_path> to <new_path>")
        else:
            old_path, new_path = rest.split(" to ", 1)
            success = file_manager.rename_file(old_path.strip(), new_path.strip())
            if not success:
                print(f"Sorry, I couldn't rename '{old_path.strip()}'.")

    elif lower_input.startswith("move file "):
        rest = user_input[len("move file "):]
        if " to " not in rest:
            print("Please use the format: move file <path> to <destination folder>")
        else:
            source_path, destination_folder = rest.split(" to ", 1)
            success = file_manager.move_file(source_path.strip(), destination_folder.strip())
            if not success:
                print(f"Sorry, I couldn't move '{source_path.strip()}'.")

    elif lower_input.startswith("search files "):
        rest = user_input[len("search files "):]
        if " in " not in rest:
            print("Please use the format: search files <keyword> in <folder>")
        else:
            keyword, folder = rest.split(" in ", 1)
            results = file_manager.search_files(keyword.strip(), folder.strip())
            if results:
                print("Found these files:")
                for f in results:
                    print(f"  - {f}")
            else:
                print(f"No files found matching '{keyword.strip()}' in '{folder.strip()}'.")

    elif lower_input.startswith("search google "):
        query = user_input[len("search google "):]
        browser_control.search_google(query)

    elif lower_input.startswith("go to "):
        url = user_input[len("go to "):]
        success = browser_control.open_website(url)
        if not success:
            print(f"Sorry, I couldn't open '{url}'.")

    elif lower_input in browser_control.KNOWN_SITES:
        browser_control.open_known_site(lower_input)

    else:
        print("Sorry, I don't understand that command yet.")


def choose_mode(voice):
    """
    Asks the user whether they want to interact by text or voice.
    Returns "text" or "voice".
    """
    print("Would you like to text or voice command me?")

    for attempt in range(3):
        spoken = voice.listen()
        if spoken:
            print(f"You said: {spoken}")
            if "text" in spoken.lower():
                return "text"
            if "voice" in spoken.lower():
                return "voice"

        print("Please say 'I'll text you' or 'I'll voice command you'.")

    print("Couldn't understand a choice — defaulting to text mode.")
    return "text"


def listen_with_retries(voice, max_attempts=3):
    """
    Tries listening multiple times before giving up.
    Returns the recognized text, or an empty string if all attempts fail.
    """
    for attempt in range(max_attempts):
        print("\nListening...")
        spoken_text = voice.listen()

        if spoken_text:
            return spoken_text

        remaining = max_attempts - attempt - 1
        if remaining > 0:
            print(f"Couldn't catch that — let's try again ({remaining} attempt(s) left)...")

    return ""


def main():
    system_control = SystemControl()
    file_manager = FileManager()
    browser_control = BrowserControl()
    voice = Voice()

    mode = choose_mode(voice)
    print(f"\nMode selected: {mode}")
    print("Say or type 'exit' to quit, or 'thank you' to pause voice listening.")

    while True:
        if mode == "voice":
            spoken_text = listen_with_retries(voice)

            if spoken_text:
                user_input = spoken_text
                print(f"You said: {user_input}")
            else:
                print("Still couldn't catch that. You can type instead:")
                user_input = input("You: ").strip()
        else:
            user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        if mode == "voice" and user_input.lower() == "thank you":
            print("Paused. Press Enter when you're ready to continue listening...")
            input()
            continue

        process_command(user_input, system_control, file_manager, browser_control)

        if mode == "voice":
            print("(pausing for 2 seconds before listening again...)")
            time.sleep(2)


if __name__ == "__main__":
    main()