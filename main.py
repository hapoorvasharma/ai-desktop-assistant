from tools.system_control import SystemControl
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    system_control = SystemControl()

    print("Assistant is running. Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip().lower()

        if user_input == "exit":
            print("Goodbye!")
            break

        if user_input.startswith("open "):
            app_name = user_input.replace("open ", "", 1)
            success = system_control.open_app(app_name)
            if not success:
                print(f"Sorry, I don't know how to open '{app_name}' yet.")
        else:
            print("Sorry, I don't understand that command yet.")


if __name__ == "__main__":
    main()