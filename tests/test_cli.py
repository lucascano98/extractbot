from typer.testing import CliRunner
from extractbot.cli import app
import json
runner = CliRunner()

def test_parse():
    result = runner.invoke(app, ["parse", "examples/test_notes.txt"])
    print(result.output)
    assert result.exit_code == 0
    assert "Text" in result.output
    assert "This is just a test." in result.output

def test_version():
    result = runner.invoke(app, "--version")
    assert "Extractbot Version: 0.1.0" in result.output

def test_error_file_not_found():
    result = runner.invoke(app, ["parse", "imaginary_text.txt"])
    assert result.exit_code == 1
    assert "Error: [Errno 2] No such file or directory: 'imaginary_text.txt'" in result.output

def test_error_empty_file():
    result = runner.invoke(app, ["parse", "examples/sample_meeting.txt"])
    assert result.exit_code == 1
    assert "Input is empty" in result.output

def test_json_format():
    result = runner.invoke(app, ["parse", "examples/test_notes.txt", "--format", "json"])
    data = json.loads(result.output)
    assert result.exit_code == 0
    assert data["text"] == "This is just a test.\n"


def test_markdown_format():
    result = runner.invoke(app, ["parse", "examples/test_notes.txt", "--format", "markdown"])
    assert result.exit_code == 0
    assert "This is just a test." in result.output
