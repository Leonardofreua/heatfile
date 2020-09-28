import logging

import pytest

from heatfile.console.logging.alert import Alert

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_alert_class() -> Alert:
    alert = Alert()
    return alert


def test_error_logging(mock_alert_class: Alert, caplog) -> None:
    error_message = "test error message"
    mock_alert_class.error(error_message)
    args, message = caplog.records[0], caplog.messages[0]
    assert args.levelname == "ERROR"
    assert message == error_message


def test_info_logging(mock_alert_class: Alert, caplog) -> None:
    info_message = "test info message"
    mock_alert_class.info(info_message)
    args, message = caplog.records[0], caplog.messages[0]
    assert args.levelname == "INFO"
    assert message == info_message


def test_warning_logging(mock_alert_class: Alert, caplog) -> None:
    warning_message = "test warning message"
    mock_alert_class.warning(warning_message)
    args, message = caplog.records[0], caplog.messages[0]
    assert args.levelname == "WARNING"
    assert message == warning_message


def test_help_logging(mock_alert_class: Alert, caplog) -> None:
    mock_alert_class.help()
    args, message = caplog.records[0], caplog.messages[0]
    assert args.levelname == "INFO"
    assert message == "Type [COMMAND] -H for help.\n"
