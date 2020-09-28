import re

from heatfile.console.commands import Tree


filename_prefix_middle = "├──"
filename_prefix_last = "└──"
parent_prefix_middle = "    "
parent_prefix_last = "│   "


def tree_line(line: Tree, string_references: int = 0) -> str:
    if line.parent_path is None:
        return line.display_name

    tree = ""
    filename_prefix = filename_prefix_last if line.is_last else filename_prefix_middle

    references = (
        f"({string_references})"
        if line.path.is_file() and string_references != 0
        else ""
    )
    parts = [f"{filename_prefix} {line.display_name} {references}"]

    previous_parent = line.parent_path
    while previous_parent and previous_parent.parent_path is not None:
        parts.append(
            parent_prefix_middle if previous_parent.is_last else parent_prefix_last
        )
        previous_parent = previous_parent.parent_path

    tree = "".join(reversed(parts))

    return tree


def get_tree_line(line_tree: str) -> str:
    line_list = re.split("├──|└──|    |│   ", line_tree)

    while "" in line_list:
        line_list.remove("")

    return line_list[0].lstrip().rstrip()
