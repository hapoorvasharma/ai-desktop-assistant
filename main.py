from tools.system_control import SystemControl
from tools.file_manager import FileManager
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    system_control = SystemControl()
    file_manager = FileManager()

    print("Assistant is running. Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()
        lower_input = user_input.lower()

        if lower_input == "exit":
            print("Goodbye!")
            break

        # --- System control commands ---
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

        # --- File manager commands ---
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

        else:
            print("Sorry, I don't understand that command yet.")


if __name__ == "__main__":
    main()