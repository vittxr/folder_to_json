import os
import json
from typing import Any, Literal


def create_folder_structure_json(path: str, ignore: list[str] = []) -> dict[str, Any]:
    """
    Recursively creates a dict representation of the folder structure starting from the given path.

    Args:
        path (str): The path of the folder to create the JSON structure from.
        ignore (list[str], optional): A list of file or folder names to ignore during the creation of the JSON structure. Defaults to [].

    Returns:
        dict[str, Any]: A dictionary representing the folder structure in JSON format.
    """
    result = {"name": os.path.basename(path), "type": "folder", "children": []}

    if not os.path.isdir(path):
        return result

    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)

        should_be_ignored = any(ignored_entry in entry_path for ignored_entry in ignore)
        if should_be_ignored:
            continue

        if os.path.isdir(entry_path):
            result["children"].append(
                create_folder_structure_json(entry_path, ignore=ignore)
            )
        else:
            result["children"].append({"name": entry, "type": "file"})

    return result


def output(data: dict[str, Any], type: Literal["file", "stdout"]) -> None:
    """
    Writes the given data to a file or prints it to stdout.

    Args:
        data (dict[str, Any]): The data to be written or printed.
        type (Literal["file", "stdout"]): The type of output.
            - "file": Writes the data to a file named "output.json".
            - "stdout": Prints the data to the standard output.

    Returns:
        None
    """
    if type == "file":
        with open("output.json", "w") as f:
            json.dump(data, f)
        return

    if type == "stdout":
        return print(json.dumps(data, indent=4))


folder_path = "path/to/folder"
folder_json = create_folder_structure_json(
    path=folder_path,
    ignore=[
        "__pycache__",
        "venv",
        ".git",
        "node_modules",
        ".vscode",
        ".VSCodeCounter",
        ".pytest_cache",
    ],
)
output(data=folder_json, type="file")
