import os
from pathlib import Path
from unittest.mock import Mock

from _pytest.config import Config
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture
def mock_tree_build_tree(mocker: MockFixture) -> Mock:
    """Fixture for mocking Tree.build_tree."""
    return mocker.patch("heatfile.console.commands.tree.Tree.build_tree", autospec=True)


@pytest.fixture
def mock_current_directory_path() -> Path:
    """Fixture for mocking current path"""
    return Path(os.getcwd())


@pytest.fixture
def mock_path_with_file() -> Path:
    """Fixture for mocking a patch with file"""
    return Path(f"{os.getcwd()}/src/heatfile/console/commands/tree.py")


@pytest.fixture
def mock_non_existent_path() -> Path:
    """Fixture for mocking a non-existent patch"""
    return Path("non_existent_path/")


@pytest.fixture
def mock_search_string() -> str:
    """Fixture for mocking search string"""
    return "test"
