import tkinter as tk
from tools.system_control import SystemControl
from tools.file_manager import FileManager
from tools.browser_control import BrowserControl
from llm.client import interpret_command
from memory.database import (
    initialize_database,
    save_command,
    get_recent_commands,
    add_favorite_app,
    get_favorite_apps,
    add_todo,
    complete_todo,
    uncomplete_todo,
    get_todos,
    add_habit,
    log_habit,
    get_habits,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def execute_action(action_data, system_control, file_manager, browser_control):
    action = action_data.get("action", "unknown")
    target = action_data.get("target", "")

    if action == "open_app":
        success = system_control.open_app(target)
        return f"Opened {target}." if success else f"Sorry, I don't know how to open '{target}' yet."

    elif action == "close_app":
        success = system_control.close_app(target)
        return f"Closed {target}." if success else f"Sorry, I couldn't close '{target}'."

    elif action == "restart_app":
        success = system_control.restart_app(target)
        return f"Restarted {target}." if success else f"Sorry, I couldn't restart '{target}'."

    elif action == "open_folder":
        success = system_control.open_folder(target)
        return f"Opened the {target} folder." if success else f"Sorry, I don't know how to open the '{target}' folder yet."

    elif action == "search_apps":
        results = system_control.search_installed_apps(target)
        return "Found: " + ", ".join(results) if results else f"No installed apps found matching '{target}'."

    elif action == "create_folder":
        success = file_manager.create_folder(target)
        return f"Created folder at '{target}'." if success else f"Sorry, I couldn't create the folder at '{target}'."

    elif action == "delete_file":
        success = file_manager.delete_file(target)
        return f"Deleted '{target}'." if success else f"Sorry, I couldn't delete '{target}'."

    elif action == "search_google":
        browser_control.search_google(target)
        return f"Searching Google for '{target}'."

    elif action == "open_website":
        success = browser_control.open_website(target)
        return f"Opened {target}." if success else f"Sorry, I couldn't open '{target}'."

    elif action == "add_favorite":
        added = add_favorite_app(target)
        return f"Added '{target}' to your favorites." if added else f"'{target}' is already in your favorites."

    elif action == "show_favorites":
        favorites = get_favorite_apps()
        return "Favorites: " + ", ".join(favorites) if favorites else "You don't have any favorite apps saved yet."

    elif action == "show_history":
        history = get_recent_commands()
        if not history:
            return "No command history yet."
        return "Recent commands:\n" + "\n".join(f"  [{ts}] {cmd}" for cmd, ts in history)

    elif action == "add_todo":
        add_todo(target)
        return f"Added '{target}' to your to-do list."

    elif action == "complete_todo":
        completed = complete_todo(target)
        return f"Nice work! Marked '{completed}' as done. 🎉" if completed else f"Couldn't find an open to-do matching '{target}'."

    elif action == "uncomplete_todo":
        reopened = uncomplete_todo(target)
        return f"Okay, marked '{reopened}' as not done yet." if reopened else f"Couldn't find a completed to-do matching '{target}'."

    elif action == "show_todos":
        todos = get_todos()
        if not todos:
            return "Your to-do list is empty."
        lines = []
        for _, task, completed in todos:
            mark = "[x]" if completed else "[ ]"
            lines.append(f"{mark} {task}")
        return "Your to-do list:\n" + "\n".join(lines)

    elif action == "add_habit":
        added = add_habit(target)
        return f"Now tracking '{target}' as a habit." if added else f"'{target}' is already being tracked."

    elif action == "log_habit":
        logged = log_habit(target)
        return f"Logged '{target}' for today. Keep it up! 💪" if logged else f"'{target}' is either already logged today or not a tracked habit yet."

    elif action == "show_habits":
        habits = get_habits()
        if not habits:
            return "You're not tracking any habits yet."
        lines = [f"{name}: {count} times logged" for name, count in habits]
        return "Your habits:\n" + "\n".join(lines)

    else:
        return "Sorry, I don't understand that command yet."


class AssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ram - Assistant")

        window_width = 380
        window_height = 520
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - window_width - 20
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        self.chat_display = tk.Text(
            root, wrap="word", state="disabled",
            bg="#1e1e2f", fg="#f5f5f5", font=("Segoe UI", 10), padx=10, pady=10
        )
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=(5, 0))

        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=5, pady=5)

        self.input_box = tk.Entry(input_frame, font=("Segoe UI", 11))
        self.input_box.pack(side="left", fill="x", expand=True, ipady=6)
        self.input_box.bind("<Return>", self.handle_send)

        send_button = tk.Button(input_frame, text="Send", command=self.handle_send)
        send_button.pack(side="right", padx=(5, 0))

        initialize_database()
        self.system_control = SystemControl()
        self.file_manager = FileManager()
        self.browser_control = BrowserControl()

        self.append_message("Ram", "Hey! How are you doing? What do you want to do today?")

    def append_message(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: {message}\n\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def handle_send(self, event=None):
        user_input = self.input_box.get().strip()
        if not user_input:
            return

        self.input_box.delete(0, "end")
        self.append_message("You", user_input)

        save_command(user_input)
        actions = interpret_command(user_input)

        for action_data in actions:
            reply = execute_action(action_data, self.system_control, self.file_manager, self.browser_control)
            self.append_message("Ram", reply)


if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantApp(root)
    root.mainloop()