import pytest
from mock import patch, Mock

from scripts.c2r_script import OutputCollector, main


@patch("scripts.c2r_script.archive_analysis_report", side_effect=Mock())
@patch("scripts.c2r_script.cleanup")
@patch("scripts.c2r_script.OutputCollector")
@patch("scripts.c2r_script.setup_sos_report", side_effect=Mock())
@patch("scripts.c2r_script.archive_old_logger_files", side_effect=Mock())
@patch("scripts.c2r_script.setup_logger_handler", side_effect=Mock())
# pylint: disable=too-many-arguments
def test_main_invalid_script_value(
    mock_setup_logger_handler,
    mock_setup_sos_report,
    mock_archive_old_logger_files,
    mock_output_collector,
    mock_cleanup,
    mock_archive,
    capsys,
    caplog,
):
    mock_output_collector.return_value = OutputCollector(entries=["non-empty"])

    main()

    output = capsys.readouterr().out
    assert "Exiting because RHC_WORKER_SCRIPT_MODE" in caplog.text
    assert '"alert": false' in output

    mock_output_collector.assert_called()
    mock_cleanup.assert_not_called()
    mock_archive.assert_not_called()
    assert mock_setup_logger_handler.call_count == 1
    assert mock_setup_sos_report.call_count == 1
    assert mock_archive_old_logger_files.call_count == 1


@pytest.mark.parametrize(("script_type"), [("ANALYSIS"), ("CONVERSION")])
@patch("scripts.c2r_script.archive_analysis_report", side_effect=Mock())
@patch(
    "scripts.c2r_script.get_system_distro_version",
    return_value=("centos", "7"),
)
@patch("scripts.c2r_script.cleanup")
@patch("scripts.c2r_script.OutputCollector")
@patch("scripts.c2r_script.setup_sos_report", side_effect=Mock())
@patch("scripts.c2r_script.archive_old_logger_files", side_effect=Mock())
@patch("scripts.c2r_script.setup_logger_handler", side_effect=Mock())
# pylint: disable=too-many-arguments
def test_main_non_eligible_release(
    mock_setup_logger_handler,
    mock_setup_sos_report,
    mock_archive_old_logger_files,
    mock_output_collector,
    mock_cleanup,
    mock_get_system_distro_version,
    mock_archive,
    script_type,
):
    mock_output_collector.return_value = OutputCollector(entries=["non-empty"])

    with patch("scripts.c2r_script.SCRIPT_TYPE", script_type):
        main()

    mock_get_system_distro_version.assert_called_once()
    mock_output_collector.assert_called()
    mock_cleanup.assert_not_called()
    mock_archive.assert_not_called()
    assert mock_setup_logger_handler.call_count == 1
    assert mock_setup_sos_report.call_count == 1
    assert mock_archive_old_logger_files.call_count == 1
