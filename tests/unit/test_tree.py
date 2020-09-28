import logging
from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest_mock import MockFixture

from heatfile.console.commands import Tree
from .helpers import get_tree_line, tree_line

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_get_previous_parents(mocker: MockFixture) -> Mock:
    return mocker.patch(
        "heatfile.console.commands.tree.Tree._get_previous_parents", autospec=True
    )


@pytest.fixture
def mock_validate_inputs(mocker: MockFixture) -> Mock:
    return mocker.patch(
        "heatfile.console.commands.tree.Tree._validate_inputs", autospec=True
    )


def test_make_only_tree(mock_current_directory_path: Path) -> None:
    directories_expected = 0
    files_expected = 0
    result = Tree._make_only_tree(mock_current_directory_path)
    for line in result:
        display_name = get_tree_line(tree_line(line))
        assert isinstance(line, Tree)
        assert line.display_name == display_name
        assert line._mount_tree_line() == tree_line(line)
        directories_expected += 1
        files_expected += 1
    assert directories_expected > 0
    assert files_expected > 0


def test_make_tree_with_references_from_directory(
    mock_get_previous_parents: Mock,
    mock_current_directory_path: Path,
    mock_search_string: str,
) -> None:
    directories_expected = 0
    files_expected = 0
    result = Tree._make_tree_with_references(
        path=mock_current_directory_path, search_string=mock_search_string
    )
    for line in result:
        display_name = get_tree_line(tree_line(line))
        args, _ = mock_get_previous_parents.call_args

        assert isinstance(line, Tree)

        if Path(line.path).is_dir():
            assert line in line._found_directories

        if not line._found_directories.get(line.parent_path):
            if line.parent_path is None:
                assert Tree._get_previous_parents(line).call_args is None
            else:
                assert isinstance(args[0], Tree)

        assert line._mount_tree_line() == tree_line(line, line._string_references)
        assert mock_get_previous_parents.called
        assert line.display_name == display_name
        directories_expected += 1
        files_expected += 1
    assert directories_expected > 0
    assert files_expected > 0


def test_make_tree_with_references_from_file(
    mock_get_previous_parents: Mock, mock_path_with_file: Path
) -> None:
    files_expected = 0
    result = Tree._make_tree_with_references(
        path=mock_path_with_file, search_string="tree",
    )
    for line in result:
        display_name = get_tree_line(tree_line(line))
        args, _ = mock_get_previous_parents.call_args

        assert isinstance(line, Tree)

        if not line._found_directories.get(line.parent_path):
            if line.parent_path is None:
                assert Tree._get_previous_parents(line).call_args is None
            else:
                assert isinstance(args[0], Tree)

        assert mock_get_previous_parents.called
        assert line._mount_tree_line() == tree_line(line, line._string_references)
        assert line.display_name == display_name
        files_expected += 1
    assert files_expected > 0


def test_build_tree_without_search_string(
    mock_current_directory_path: Path, capsys
) -> None:
    Tree.build_tree(mock_current_directory_path)

    captured = capsys.readouterr()

    assert len(captured.out) > 0


def test_build_tree_with_search_string(
    mock_current_directory_path: Path, mock_search_string: str, capsys
) -> None:
    Tree.build_tree(mock_current_directory_path, mock_search_string)

    captured = capsys.readouterr()

    assert len(captured.out) > 0


def test_validate_inputs_file_in_path_without_search_string(
    mock_path_with_file: Path, caplog
) -> None:
    logger.error("Provide a string to find references in the given file.")
    Tree._validate_inputs(mock_path_with_file)

    assert (
        "Provide a string to find references in the given file." == caplog.messages[0]
    )


def test_validate_inputs_for_a_nonexistent_path(
    mock_non_existent_path: Path, caplog
) -> None:
    logger.error("Directory/File not found.")
    Tree._validate_inputs(mock_non_existent_path)

    assert "Directory/File not found." == caplog.messages[0]


def test_fails_build_tree_file_in_path_without_search_string(
    mock_validate_inputs: Mock, mock_path_with_file: Path, caplog
):
    with pytest.raises(SystemExit):
        logger.error("Provide a string to find references in the given file.")
        Tree.build_tree(mock_path_with_file)

    assert SystemExit()
    assert mock_validate_inputs.called
    assert (
        "Provide a string to find references in the given file." == caplog.messages[0]
    )


def test_fails_build_tree_for_a_nonexistent_path(
    mock_validate_inputs: Mock, mock_non_existent_path: Path, caplog
):
    with pytest.raises(SystemExit):
        logger.error("Directory/File not found.")
        Tree.build_tree(mock_non_existent_path)
    assert SystemExit()
    assert mock_validate_inputs.called
    assert "Directory/File not found." == caplog.messages[0]
