from collections import OrderedDict
from pathlib import Path
from re import compile, findall, IGNORECASE, search
from typing import Dict, Iterator, List, Optional, Union


class Tree:
    __filename_prefix_middle = "├──"
    __filename_prefix_last = "└──"
    __parent_prefix_middle = "    "
    __parent_prefix_last = "│   "
    __directories_count = 0
    __files_count = 0
    __string_references = 0
    __found_directories = {}  # type: Dict[object, bool]

    def __init__(
        self, path, parent_path=None, is_last=False, search_string=None,
    ):  # type: (Path, "Tree", bool, str) -> None
        self.path = Path(str(path))
        self.parent_path = parent_path
        self.is_last = is_last
        self.search_string = search_string

    @classmethod
    def __make_tree_with_references(
        cls, path=None, parent_path=None, is_last=False, search_string=None,
    ):  # type: (Path, "Tree", bool, str) -> Iterator["Tree"]
        root = Path(str(path)).resolve()
        displayable_root = cls(root, parent_path, is_last, search_string)
        children = []

        if root.is_dir():
            children = cls.__get_directory_children(root)
        else:
            children.append(Path(str(displayable_root.path)))

        if (
            not cls.__found_directories
            or displayable_root not in cls.__found_directories
        ):
            cls.__found_directories[displayable_root] = False

        directory_index = 1
        for path in children:
            is_last = directory_index == len(children)
            if path.is_dir():
                yield from cls.__make_tree_with_references(
                    path,
                    parent_path=displayable_root,
                    is_last=is_last,
                    search_string=search_string,
                )
            elif search_string is not None:
                cls.__string_references = cls.__find_string_references(
                    path, search_string
                )
                if cls.__string_references != 0:
                    previous_parents = cls.__get_previous_parents(displayable_root)

                    if previous_parents is not None:
                        for parent, is_displayed in previous_parents.items():
                            if (
                                cls.__found_directories.get(
                                    displayable_root.parent_path
                                )
                                == is_displayed
                            ):
                                cls.__directories_count += 1
                                cls.__found_directories[parent] = True
                                yield parent
                        del previous_parents

                    if displayable_root.path.is_dir() and not cls.__found_directories.get(
                        displayable_root
                    ):
                        cls.__directories_count += 1
                        cls.__found_directories[displayable_root] = True
                        yield displayable_root
                    cls.__files_count += 1
                    yield cls(path, displayable_root, is_last, search_string)
            directory_index += 1

    @classmethod
    def __make_only_tree(
        cls, path, parent_path=None, is_last=False
    ):  # type: (Path, "Tree", bool) -> Iterator["Tree"]
        root = Path(str(path)).resolve()
        displayable_root = cls(root, parent_path, is_last)

        yield displayable_root

        children = cls.__get_directory_children(root)

        directory_index = 1
        for path in children:
            is_last = directory_index == len(children)
            if path.is_dir():
                cls.__directories_count += 1
                yield from cls.__make_only_tree(
                    path, parent_path=displayable_root, is_last=is_last
                )
            else:
                cls.__files_count += 1
                yield cls(path, displayable_root, is_last)
            directory_index += 1

    @classmethod
    def __get_previous_parents(
        cls, root
    ):  # type: ("Tree") -> Union[OrderedDict["Tree", Optional[bool]], None]
        if not cls.__found_directories.get(root.parent_path):
            previous_parents = OrderedDict()
            previous = root.parent_path

            while previous is not None:
                value = cls.__found_directories.get(previous)
                previous_parents.update({previous: value})
                previous_parents.move_to_end(previous, last=False)
                previous = previous.parent_path
                return previous_parents
        return None

    @staticmethod
    def __find_string_references(file_path: Path, search_string: str) -> int:
        pattern = compile(search_string, flags=IGNORECASE)
        length = 0
        with open(file_path, "r", encoding="latin-1") as file:
            content = file.read()
            if search(pattern, content) is not None:
                return len(findall(pattern, content))
        return length

    @staticmethod
    def __get_directory_children(root: Path) -> List[Path]:
        return sorted(list(path for path in root.iterdir()))

    @property
    def __display_name(self) -> str:
        return f"{self.path.name}/" if self.path.is_dir() else self.path.name

    def __displayable(self) -> str:
        if self.parent_path is None:
            return self.__display_name

        tree = ""
        _filename_prefix = (
            self.__filename_prefix_last
            if self.is_last
            else self.__filename_prefix_middle
        )

        references = (
            f"({self.__string_references})"
            if self.path.is_file() and self.__string_references != 0
            else ""
        )
        parts = [f"{_filename_prefix} {self.__display_name} {references}"]

        previous_parent = self.parent_path
        while previous_parent and previous_parent.parent_path is not None:
            parts.append(
                self.__parent_prefix_middle
                if previous_parent.is_last
                else self.__parent_prefix_last
            )
            previous_parent = previous_parent.parent_path

        tree = "".join(reversed(parts))

        return tree

    @classmethod
    def build_tree(
        cls, path, search_string
    ):  # type: (Path, Union[Optional[str], None]) -> None
        if search_string is not None:
            iterable_paths = cls.__make_tree_with_references(
                path=path, search_string=search_string
            )
        elif path.is_dir():
            iterable_paths = cls.__make_only_tree(path=path)

        for line in iterable_paths:
            print(line.__displayable())

        print(
            f"\n{cls.__directories_count} directories"
            + (f", {cls.__files_count} files")
        )
