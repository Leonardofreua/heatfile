from pathlib import Path
from unittest.mock import Mock

from click import ClickException
from click.testing import CliRunner

from heatfile.console import application

FILE = Path("tree.py")
SEARCH_STRING = "string_reference"


def test_invokes_build_tree_method(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """It invokes Tree.build_tree."""
    runner.invoke(application.tree)
    assert mock_tree_build_tree.called


def test_without_options(
    runner: CliRunner, mock_tree_build_tree: Mock, mock_current_directory_path: Path
) -> None:
    """It uses only the tree command without options."""
    runner.invoke(application.tree)
    args, _ = mock_tree_build_tree.call_args

    mock_tree_build_tree.assert_called_once()
    assert mock_current_directory_path == args[0]


def test_with_only_path_option(
    runner: CliRunner, mock_tree_build_tree: Mock, mock_current_directory_path: Path
) -> None:
    """It uses only path option"""
    runner.invoke(application.tree, [f"--path={mock_current_directory_path}"])
    mock_tree_build_tree.assert_called_with(mock_current_directory_path, None)


def test_search_string_references(
    runner: CliRunner, mock_tree_build_tree: Mock, mock_current_directory_path: Path
) -> None:
    """It uses only search option"""
    runner.invoke(application.tree, [f"--search={SEARCH_STRING}"])
    args, _ = mock_tree_build_tree.call_args

    mock_tree_build_tree.assert_called_with(mock_current_directory_path, SEARCH_STRING)
    assert mock_current_directory_path == args[0]


def test_search_string_references_for_a_specific_path(
    runner: CliRunner, mock_tree_build_tree: Mock, mock_current_directory_path: Path
) -> None:
    """It uses a specific path and searches for a string reference to the path."""
    runner.invoke(
        application.tree,
        [f"--path={mock_current_directory_path}", f"--search={SEARCH_STRING}"],
    )
    mock_tree_build_tree.assert_called_with(mock_current_directory_path, SEARCH_STRING)


def test_fails_path_option_with_nonexistent_directory_or_file(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """
    It should fail by passing a DIRECTORY or FILE that doesn't exist in the path option.
    """
    mock_tree_build_tree.side_effect = ClickException("Directory/File not found.")
    dir_result = runner.invoke(application.tree, ["--path=directory_non_existent/"])
    file_result = runner.invoke(application.tree, ["--path=file_non_existent.py"])

    assert dir_result.exit_code == 1
    assert file_result.exit_code == 1


def test_fails_search_string_references_for_a_nonexistent_path(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """
    It should fail by passing a non-existent path and searches for a string reference to
    it.
    """
    mock_tree_build_tree.side_effect = ClickException("Directory/File not found.")
    dir_result = runner.invoke(
        application.tree,
        ["--path=directory_non_existent/", f"--search={SEARCH_STRING}"],
    )
    file_result = runner.invoke(
        application.tree, ["--path=file_non_existent.py", f"--search={SEARCH_STRING}"]
    )

    assert dir_result.exit_code == 1
    assert file_result.exit_code == 1


def test_fails_with_file_in_the_path_option_without_search_option(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """It should fail by passing a file in the path option without a search string."""
    mock_tree_build_tree.side_effect = ClickException(
        "Provide a string to find references in the given file."
    )
    result = runner.invoke(application.tree, [f"--path={FILE}"])

    assert result.exit_code == 1
