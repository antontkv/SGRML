import pytest

from sgrml import SGR
from sgrml import wrap_sgr as w


def dr() -> str:
    """Double Reset."""
    return f"{w(0)}{w(0)}"


def test_bold() -> None:
    assert SGR("<b>bold</b>") == f"{w(1)}bold{dr()}"


def test_italic() -> None:
    assert SGR("<i>italic</i>") == f"{w(3)}italic{dr()}"


def test_multiple() -> None:
    assert SGR("<b>bold</b><i>italic</i>") == f"{w(1)}bold{w(0)}{w(3)}italic{dr()}"


def test_mix() -> None:
    assert (
        SGR("<b>bold <i>italic and bold</b> italic</i> normal")
        == f"{w(1)}bold {w(3)}italic and bold{w(0)}{w(3)} italic{w(0)} normal{w(0)}"
    )


def test_underline() -> None:
    assert SGR("<u>underline</u>") == f"{w('4:1')}underline{dr()}"


@pytest.mark.parametrize(
    "underline_type,sgr_sequence",
    [
        pytest.param("solid", "4:1", id="solid"),
        pytest.param("double", "4:2", id="double"),
        pytest.param("wavy", "4:3", id="wavy"),
        pytest.param("dotted", "4:4", id="dotted"),
        pytest.param("dashed", "4:5", id="dashed"),
    ],
)
def test_underline_types(underline_type: str, sgr_sequence: str) -> None:
    assert SGR(f"<u type={underline_type}>underline</u>") == f"{w(sgr_sequence)}underline{dr()}"


def test_error_on_wrong_tag() -> None:
    with pytest.raises(ValueError):
        str(SGR("<unsupported>text</unsupported>"))


def test_error_on_wrong_attr() -> None:
    with pytest.raises(ValueError):
        str(SGR("<u unsupported=none>underline</u>"))
