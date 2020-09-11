import os
from pathlib import Path
from unittest.mock import Mock

from click import ClickException
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture

from heatfile.console import application


PATH = Path("/home")
FILE = Path("tree.py")
SEARCH_STRING = "string_reference"


@pytest.fixture
def mock_tree_build_tree(mocker: MockFixture) -> Mock:
    """Fixture for mocking Tree.build_tree."""
    return mocker.patch("heatfile.console.commands.tree.Tree.build_tree", autospec=True)


def test_main_succeeds(runner: CliRunner, mock_tree_build_tree: Mock) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(application.cli)
    assert result.exit_code == 0


@pytest.mark.e2e
def test_cli_succeeds_in_production_env(runner: CliRunner) -> None:
    """It exits with a status code of zero (end-to-end)."""
    result = runner.invoke(application.cli)
    assert result.exit_code == 0


def test_invokes_build_tree_method(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """It invokes Tree.build_tree."""
    runner.invoke(application.tree)
    assert mock_tree_build_tree.called


def test_without_options(runner: CliRunner, mock_tree_build_tree: Mock) -> None:
    """It uses only the tree command without options."""
    runner.invoke(application.tree)
    args, _ = mock_tree_build_tree.call_args

    mock_tree_build_tree.assert_called_once()
    assert Path(os.getcwd()) == args[0]


def test_with_only_path_option(runner: CliRunner, mock_tree_build_tree: Mock) -> None:
    """It uses only path option"""
    runner.invoke(application.tree, [f"--path={PATH}"])
    mock_tree_build_tree.assert_called_with(PATH, None)


def test_search_string_references(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """It uses only search option"""
    runner.invoke(application.tree, [f"--search={SEARCH_STRING}"])
    args, _ = mock_tree_build_tree.call_args

    mock_tree_build_tree.assert_called_with(Path(os.getcwd()), SEARCH_STRING)
    assert Path(os.getcwd()) == args[0]


def test_search_string_references_for_a_specific_path(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """It uses a specific path and searches for a string reference to the path."""
    runner.invoke(application.tree, [f"--path={PATH}", f"--search={SEARCH_STRING}"])
    mock_tree_build_tree.assert_called_with(PATH, SEARCH_STRING)


def test_fails_with_file_in_the_path_option_without_search_option(
    runner: CliRunner, mock_tree_build_tree: Mock
) -> None:
    """It should fail by passing a file in the path option without a search string."""
    mock_tree_build_tree.side_effect = ClickException("Boom")
    result = runner.invoke(application.tree, [f"--path={FILE}"])

    assert result.exit_code == 1
