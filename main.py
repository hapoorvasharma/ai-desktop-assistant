import time
from tools.system_control import SystemControl
from tools.file_manager import FileManager
from tools.browser_control import BrowserControl
from tools.voice import Voice
from llm.client import interpret_command
from memory.database import (
    initialize_database,
    save_command,
    get_recent_commands,
    add_favorite_app,
    get_favorite_apps,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def execute_action(action_data, system_control, file_manager, browser_control):
    """
    Takes a single structured action dictionary and executes
    the matching function.
    """
    action = action_data.get("action", "unknown")
    target = action_data.get("target", "")

    if action == "open_app":
        success = system_control.open_app(target)
        if not success:
            print(f"Sorry, I don't know how to open '{target}' yet.")

    elif action == "close_app":
        success = system_control.close_app(target)
        if not success:
            print(f"Sorry, I couldn't close '{target}'.")

    elif action == "restart_app":
        success = system_control.restart_app(target)
        if not success:
            print(f"Sorry, I couldn't restart '{target}'.")

    elif action == "open_folder":
        success = system_control.open_folder(target)
        if not success:
            print(f"Sorry, I don't know how to open the '{target}' folder yet.")

    elif action == "search_apps":
        results = system_control.search_installed_apps(target)
        if results:
            print("Found these apps:")
            for app in results:
                print(f"  - {app}")
        else:
            print(f"No installed apps found matching '{target}'.")

    elif action == "create_folder":
        success = file_manager.create_folder(target)
        if not success:
            print(f"Sorry, I couldn't create the folder at '{target}'.")

    elif action == "delete_file":
        success = file_manager.delete_file(target)
        if not success:
            print(f"Sorry, I couldn't delete '{target}'.")

    elif action == "search_google":
        browser_control.search_google(target)

    elif action == "open_website":
        success = browser_control.open_website(target)
        if not success:
            print(f"Sorry, I couldn't open '{target}'.")

    elif action == "add_favorite":
        added = add_favorite_app(target)
        if added:
            print(f"Added '{target}' to your favorites.")
        else:
            print(f"'{target}' is already in your favorites.")

    elif action == "show_favorites":
        favorites = get_favorite_apps()
        if favorites:
            print("Your favorite apps:")
            for app in favorites:
                print(f"  - {app}")
        else:
            print("You don't have any favorite apps saved yet.")

    elif action == "show_history":
        history = get_recent_commands()
        if history:
            print("Your recent commands:")
            for command, timestamp in history:
                print(f"  [{timestamp}] {command}")
        else:
            print("No command history yet.")

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
    initialize_database()

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

        save_command(user_input)

        actions = interpret_command(user_input)
        for action_data in actions:
            execute_action(action_data, system_control, file_manager, browser_control)

        if mode == "voice":
            print("(pausing for 2 seconds before listening again...)")
            time.sleep(2)


if __name__ == "__main__":
    main()