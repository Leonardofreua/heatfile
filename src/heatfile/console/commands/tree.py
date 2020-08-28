from collections import OrderedDict
from pathlib import Path
from re import compile, findall, IGNORECASE, search
from typing import Dict, Iterator


class Tree:
    __filename_prefix_middle = "├──"
    __filename_prefix_last = "└──"
    __parent_prefix_middle = "    "
    __parent_prefix_last = "│   "
    __directories_count = 0
    __files_count = 0
    __strings_incidences = 0
    __found_directories = {}  # type: Dict[object, bool]

    def __init__(
        self,
        path: Path,
        parent_path: "Tree" = None,
        is_last: bool = False,
        search_string: str = None,
    ) -> None:
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        self.search_string = search_string

    @classmethod
    def __make_tree(
        cls,
        root: Path,
        parent: "Tree" = None,
        is_last: bool = False,
        search_string: str = None,
    ) -> Iterator["Tree"]:
        root = Path(str(root))

        displayable_root = cls(root, parent, is_last, search_string)

        childrens = sorted(list(path for path in root.iterdir()))

        if (
            not cls.__found_directories
            or displayable_root not in cls.__found_directories
        ):
            cls.__found_directories[displayable_root] = False

        directory_index = 1
        for path in childrens:
            is_last = directory_index == len(childrens)
            if path.is_dir():
                yield from cls.__make_tree(
                    path,
                    parent=displayable_root,
                    is_last=is_last,
                    search_string=search_string,
                )
            else:
                cls.__strings_incidences = cls.__find_string_incidences(
                    path, search_string
                )
                if cls.__strings_incidences != 0:
                    if not cls.__found_directories.get(displayable_root.parent):
                        previous_parents = OrderedDict()
                        previous = displayable_root.parent

                        while previous is not None:
                            value = cls.__found_directories.get(previous)
                            previous_parents.update({previous: value})
                            previous_parents.move_to_end(previous, last=False)
                            previous = previous.parent

                        for key, value in previous_parents.items():
                            if (
                                cls.__found_directories.get(displayable_root.parent)
                                == value
                            ):
                                cls.__directories_count += 1
                                cls.__found_directories[key] = True
                                yield key

                        del previous_parents

                    if not cls.__found_directories.get(displayable_root):
                        cls.__directories_count += 1
                        cls.__found_directories[displayable_root] = True
                        yield displayable_root
                    cls.__files_count += 1
                    yield cls(path, displayable_root, is_last, search_string)
            directory_index += 1

    @staticmethod
    def __find_string_incidences(file_path: Path, search_string: str) -> int:
        pattern = compile(search_string, flags=IGNORECASE)
        length = 0
        with open(file_path, "r", encoding="latin-1") as file:
            content = file.read()
            if search(pattern, content) is not None:
                return len(findall(pattern, content))
        return length

    @property
    def display_name(self) -> str:
        return f"{self.path.name}/" if self.path.is_dir() else self.path.name

    def displayable(self) -> str:
        if self.parent is None:
            return self.display_name

        tree = ""
        _filename_prefix = (
            self.__filename_prefix_last
            if self.is_last
            else self.__filename_prefix_middle
        )

        incidences = (
            f"({self.__strings_incidences})"
            if self.path.is_file() and self.__strings_incidences != 0
            else ""
        )
        parts = [f"{_filename_prefix} {self.display_name} {incidences}"]

        previous_parent = self.parent
        while previous_parent and previous_parent.parent is not None:
            parts.append(
                self.__parent_prefix_middle
                if previous_parent.is_last
                else self.__parent_prefix_last
            )
            previous_parent = previous_parent.parent

        tree = "".join(reversed(parts))

        return tree

    @classmethod
    def build_tree(cls, path: Path, search_string: str = None) -> None:
        interable_paths = cls.__make_tree(root=path, search_string=search_string)

        for line in interable_paths:
            print(line.displayable())

        print(
            f"\n{cls.__directories_count} directories"
            + (f", {cls.__files_count} files")
        )
