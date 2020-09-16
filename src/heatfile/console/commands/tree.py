from collections import OrderedDict
from pathlib import Path
from re import compile, findall, IGNORECASE, search
from typing import Dict, Iterator, List, Optional, Union

from heatfile.alerts import Alert


class Tree:
    _filename_prefix_middle = "├──"
    _filename_prefix_last = "└──"
    _parent_prefix_middle = "    "
    _parent_prefix_last = "│   "
    _directories_count = 0
    _files_count = 0
    _string_references = 0
    _found_directories = {}  # type: Dict[object, bool]

    __slots__ = ["path", "parent_path", "is_last", "search_string"]

    def __init__(
        self, path, search_string=None, parent_path=None, is_last=False
    ):  # type: (Path, str, "Tree", bool) -> None
        self.path = Path(str(path))
        self.parent_path = parent_path
        self.is_last = is_last
        self.search_string = search_string

    @classmethod
    def _make_tree_with_references(
        cls, path, search_string, parent_path=None, is_last=False
    ):  # type: (Path, str, "Tree", bool) -> Iterator["Tree"]
        root = Path(str(path)).resolve()
        displayable_root = cls(root, search_string, parent_path, is_last)
        children = []

        if root.is_dir():
            children = cls._get_directory_children(root)
        else:
            children.append(Path(str(displayable_root.path)))

        if not cls._found_directories or displayable_root not in cls._found_directories:
            cls._found_directories[displayable_root] = False

        directory_index = 1
        for path in children:
            is_last = directory_index == len(children)
            if path.is_dir():
                yield from cls._make_tree_with_references(
                    path, search_string, parent_path=displayable_root, is_last=is_last,
                )
            else:
                cls._string_references = cls._find_string_references(
                    path, search_string
                )
                if cls._string_references != 0:
                    previous_parents = cls._get_previous_parents(displayable_root)

                    if previous_parents is not None:
                        for parent, is_displayed in previous_parents.items():
                            if (
                                cls._found_directories.get(displayable_root.parent_path)
                                == is_displayed
                            ):
                                cls._directories_count += 1
                                cls._found_directories[parent] = True
                                yield parent
                        del previous_parents

                    if displayable_root.path.is_dir() and not cls._found_directories.get(
                        displayable_root
                    ):
                        cls._directories_count += 1
                        cls._found_directories[displayable_root] = True
                        yield displayable_root
                    cls._files_count += 1
                    yield cls(path, search_string, displayable_root, is_last)
            directory_index += 1

    @classmethod
    def _make_only_tree(
        cls, path, parent_path=None, is_last=False
    ):  # type: (Path, "Tree", bool) -> Iterator["Tree"]
        root = Path(str(path)).resolve()
        displayable_root = cls(path=root, parent_path=parent_path, is_last=is_last)

        yield displayable_root

        children = cls._get_directory_children(root)

        directory_index = 1
        for path in children:
            is_last = directory_index == len(children)
            if path.is_dir():
                cls._directories_count += 1
                yield from cls._make_only_tree(
                    path, parent_path=displayable_root, is_last=is_last
                )
            else:
                cls._files_count += 1
                yield cls(path=path, parent_path=displayable_root, is_last=is_last)
            directory_index += 1

    @classmethod
    def _get_previous_parents(
        cls, root
    ):  # type: ("Tree") -> Union[OrderedDict["Tree", Optional[bool]], None]
        if not cls._found_directories.get(root.parent_path):
            previous_parents = OrderedDict()
            previous = root.parent_path

            while previous is not None:
                value = cls._found_directories.get(previous)
                previous_parents.update({previous: value})
                previous_parents.move_to_end(previous, last=False)
                previous = previous.parent_path
                return previous_parents
        return None

    @staticmethod
    def _find_string_references(file_path: Path, search_string: str) -> int:
        pattern = compile(search_string, flags=IGNORECASE)
        length = 0
        with open(file_path, "r", encoding="latin-1") as file:
            content = file.read()
            if search(pattern, content) is not None:
                return len(findall(pattern, content))
        return length

    @staticmethod
    def _get_directory_children(root: Path) -> List[Path]:
        return sorted(list(path for path in root.iterdir()))

    @staticmethod
    def _validate_inputs(path, search_string) -> None:
        if path.is_file() and search_string is None:
            Alert.raise_error_message(
                "Provide a string to find references in the given file."
            )
        elif not path.exists():
            Alert.raise_error_message("Directory/File not found.")

    @property
    def display_name(self) -> str:
        return f"{self.path.name}/" if self.path.is_dir() else self.path.name

    def _displayable(self) -> str:
        if self.parent_path is None:
            return self.display_name

        tree = ""
        filename_prefix = (
            self._filename_prefix_last if self.is_last else self._filename_prefix_middle
        )

        references = (
            f"({self._string_references})"
            if self.path.is_file() and self._string_references != 0
            else ""
        )
        parts = [f"{filename_prefix} {self.display_name} {references}"]

        previous_parent = self.parent_path
        while previous_parent and previous_parent.parent_path is not None:
            parts.append(
                self._parent_prefix_middle
                if previous_parent.is_last
                else self._parent_prefix_last
            )
            previous_parent = previous_parent.parent_path

        tree = "".join(reversed(parts))

        return tree

    @classmethod
    def build_tree(
        cls, path, search_string
    ):  # type: (Path, Union[Optional[str], None]) -> None
        cls._validate_inputs(path, search_string)

        iterable_paths: Iterator[Tree] = iter(())

        if search_string is not None:
            iterable_paths = cls._make_tree_with_references(path, search_string)
        elif path.is_dir():
            iterable_paths = cls._make_only_tree(path=path)

        for line in iterable_paths:
            print(line._displayable())

        print(
            f"\n{cls._directories_count} directories" + (f", {cls._files_count} files")
        )
