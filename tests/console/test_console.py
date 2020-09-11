from unittest.mock import Mock

from click.testing import CliRunner
import pytest

from heatfile.console import application


def test_cli_succeeds(runner: CliRunner, mock_tree_build_tree: Mock) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(application.cli)
    assert result.exit_code == 0


@pytest.mark.e2e
def test_cli_succeeds_in_production_env(runner: CliRunner) -> None:
    """It exits with a status code of zero (end-to-end)."""
    result = runner.invoke(application.cli)
    assert result.exit_code == 0
