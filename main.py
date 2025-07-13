# main.py

import ast
import os
import importlib
import inspect
import pickle
import signal
import sys

from functools import wraps

from src.address_book.core.address_book import AddressBook

# gracefully handle the exit signal
def handle_exit_signal(signum, frame):
    save_book_state(book)
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit_signal)


SAVE_FILE = "addressbook.pkl"


def save_book_state(book):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(book, f)


def load_book_state():
    try:
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


book = load_book_state()


def aliases(*names):
    def wrapper(func):
        func._aliases = names
        return func
    return wrapper


def input_error(func):
    @wraps(func)

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as e:
            return f"Error: {str(e)}"

    return wrapper


# parsing user input
@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return convert_command_to_function(cmd), *args

@input_error
def get_functions_from_file(filepath: str) -> dict[str, dict[str, dict[str, str]]]:
    with open(filepath, "r", encoding="utf-8") as file:
        node = ast.parse(file.read(), filename=filepath)

    functions = {}
    # Get module name from file name (without .py)
    module_name = os.path.splitext(os.path.basename(filepath))[0]

    for n in node.body:
        if isinstance(n, ast.FunctionDef):
            function_name = n.name
            aliases = [function_name]

            # Look for @aliases(...) decorator
            for decorator in n.decorator_list:
                if (
                        isinstance(decorator, ast.Call)
                        and getattr(decorator.func, "id", "") == "aliases"
                ):
                    for arg in decorator.args:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                            aliases.append(arg.value)

            # registering all functions names (main + aliases)
            for alias in aliases:
                functions[alias] = {
                    "module_name": module_name,
                    "function_name": function_name
                }

    return functions


@input_error
def convert_command_to_function(cmd: str) -> str:
    return cmd.replace("-", "_")


@input_error
def run_command(supported_commands, command_to_execute: str, *args):
    if command_to_execute in supported_commands:
        command_to_execute = supported_commands[command_to_execute]
        module_name = command_to_execute["module_name"]
        func_name = command_to_execute["function_name"]
        module = importlib.import_module(f"src.bot_helper.{module_name}")
        func = getattr(module, func_name)

        named_params = {}
        if "book" in inspect.signature(func).parameters:
            named_params["book"] = book

        # dynamically adding decorator to the function we need to make a call
        decorated_func = input_error(func)

        return decorated_func(*args, **named_params)
    else:
        raise IndexError(f"Invalid command. Please use one of the supported commands: ", ", ".join(cmd.replace("_", "-") for cmd in supported_commands.keys()))


def main():
    print("Welcome to the assistant bot!")

    supported_commands = {}

    # getting list of commands for user based on modules for out bot_helper
    for f in os.listdir("src/bot_helper"):
        if f.endswith(".py"):
            filepath = os.path.join("src/bot_helper", f)
            supported_commands.update(get_functions_from_file(filepath))

    print(f"List of supported commands: ", ", ".join(cmd.replace("_", "-") for cmd in supported_commands.keys()))

    try:
        while True:
            user_input = input("Enter a command: ").strip().lower()

            command_to_execute, *args = parse_input(user_input)

            command_result = run_command(supported_commands, command_to_execute, *args)
            if command_result is False:
                break
            else:
                print(command_result)
    finally:
        save_book_state(book)
        print("\nAddress book saved.")

if __name__ == "__main__":
    main()
