from pathlib import Path
from unittest.mock import patch

import pytest

from oslash import IO, Return, read_file


def test_read_file_map_reads_file_not_stdin(tmp_path: Path) -> None:
    filename = tmp_path / "message.txt"
    filename.write_text("hello\n", encoding="utf-8")
    with patch("builtins.input", side_effect=AssertionError("unexpected stdin read")):
        action = read_file(str(filename)).map(str.upper)
        assert action.run(0) == "HELLO\n"


def test_read_file_map_is_lazy_and_can_change_type(tmp_path: Path) -> None:
    filename = tmp_path / "message.txt"
    action: IO[int] = read_file(str(filename)).map(len)
    filename.write_text("hello", encoding="utf-8")
    with patch("builtins.input", side_effect=AssertionError("unexpected stdin read")):
        assert action() == 5


def test_read_file_map_after_bind_and_composition(tmp_path: Path) -> None:
    filename = tmp_path / "message.txt"
    filename.write_text("hello", encoding="utf-8")
    with patch("builtins.input", side_effect=AssertionError("unexpected stdin read")):
        action = read_file(str(filename)).bind(lambda text: Return(text + "!"))
        assert action.map(str.upper).map(len)() == 6
        assert action.map(lambda text: len(text.upper()))() == 6
        assert action.map(lambda text: text)() == action()
        assert action.map(len).bind(lambda size: Return(size + 1))() == 7


def test_read_file_map_preserves_file_errors(tmp_path: Path) -> None:
    action = read_file(str(tmp_path / "missing.txt")).map(str.upper)
    with (
        patch("builtins.input", side_effect=AssertionError("unexpected stdin read")),
        pytest.raises(FileNotFoundError),
    ):
        action()
