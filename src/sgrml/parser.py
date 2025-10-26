# Standard https://ecma-international.org/wp-content/uploads/ECMA-48_5th_edition_june_1991.pdf
from __future__ import annotations

import inspect
from collections import deque
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any

# ESC - Escape
# Belongs to the CO set of control functions.
# It's bit combination in this set is 01/11, meaning it's has has hex value of 0x1B.
# This is described in 5.2 section of ECMA-48 standard.
#
# Possible values for ESC is:
# ^[    Caret notation
# 0x1B  C0 set code
# \x1B  C escape sequence
# \033  C escape sequence
# \e
ESC = "\x1b"

# CSI - CONTROL SEQUENCE INTRODUCER
# Belongs to the C1 set.
# CSI is represented by bit combinations 01/11 (representing ESC) and 05/11 in a 7-bit code or by bit
# combination 09/11 in an 8-bit code.
# This is described in 5.4 section of ECMA-48 standard.
#
# Possible values for CSI is:
# [     ASCII
# 0x5B  C1 7bit code
# 0x9B  C1 8bit code
CSI = f"{ESC}\x5b"

# Final Byte of CSI
# Terminates the control sequence. Identifies the control function.
# SELECT GRAPHIC RENDITION (SGR) is a control function of CSI.
# SGR is used to establish one or more graphic rendition aspects for subsequent text.
# This is described in 5.4 section of ECMA-48 standard.
#
# Possible values for SGR Final Byte is:
# m     ASCII
# 0x6D  hex
SGR_FINAL_BYTE = "\x6d"


def wrap_sgr(code: str | int) -> str:
    return f"{CSI}{code}{SGR_FINAL_BYTE}"


@dataclass(frozen=True)
class SGRTag:
    html_tag: str
    sgr_sequence: str

    def __str__(self) -> str:
        return self.sgr_sequence

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self.html_tag == value
        if isinstance(value, SGRTag):
            return self.html_tag == value.html_tag
        raise ValueError(f"Can't compare to type {type(value)}")


class SGRSequences:
    @classmethod
    def reset(cls) -> str:
        """Reset."""
        return wrap_sgr(0)

    @classmethod
    def b(cls) -> SGRTag:
        """Bold."""
        return SGRTag("b", wrap_sgr(1))

    @classmethod
    def dim(cls) -> SGRTag:
        """Dim."""
        return SGRTag("dim", wrap_sgr(2))

    @classmethod
    def i(cls) -> SGRTag:
        """Italic."""
        return SGRTag("i", wrap_sgr(3))

    @classmethod
    def u(cls, type: str = "solid") -> SGRTag:  # noqa: A002
        """Underline.

        Args:
            type (str): Type of underline. Must be one of this:
                - solid (Default)
                - double
                - wavy
                - dotted
                - dashed
        """
        underline_types = {"solid": 1, "double": 2, "wavy": 3, "dotted": 4, "dashed": 5}
        if type not in underline_types:
            raise ValueError(f"Unknown underline type '{type}'")
        return SGRTag("u", wrap_sgr(f"4:{underline_types[type]}"))

    @classmethod
    def blink(cls, type: str = "slow") -> SGRTag:  # noqa: A002
        """Blink."""
        blink_types = {"slow": 5, "rapid": 6, "fast": 6}
        if type not in blink_types:
            raise ValueError(f"Unknown blink type '{type}'")
        return SGRTag("blink", wrap_sgr(blink_types[type]))


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags_stack: deque[SGRTag] = deque()
        self.result: list[str] = []

    def validate_tag(self, tag: str) -> None:
        if not hasattr(SGRSequences, tag):
            raise ValueError(f"Unknown tag '{tag}'")

    def sgr_reset(self) -> None:
        """Clears all SGR sequences."""
        self.result.append(SGRSequences.reset())
        self.tags_stack.clear()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Handle void tag 'reset'
        if tag == "reset":
            self.sgr_reset()
            return
        self.validate_tag(tag)

        sgr_func = getattr(SGRSequences, tag)
        sgr_func_kwargs: dict[str, Any] = {}
        # Match tag attrs with function arguments and fill func_kwargs
        if attrs:
            sgr_func_parameters = inspect.signature(sgr_func).parameters
            for attr, value in attrs:
                if attr not in sgr_func_parameters:
                    raise ValueError(f"Tag '{tag}' don't have attribute '{attr}'")
                sgr_func_kwargs[attr] = value

        sgr_tag: SGRTag = sgr_func(**sgr_func_kwargs)
        self.tags_stack.appendleft(sgr_tag)
        # Add SGR sequence to result
        self.result.append(str(sgr_tag))

    def handle_endtag(self, tag: str) -> None:
        # Handle void tag 'reset'
        if tag == "reset":
            self.sgr_reset()
            return
        self.validate_tag(tag)
        self.tags_stack.remove(tag)  # type: ignore # SGRTag can do compassing to str
        # Reset all SGR sequences
        self.result.append(SGRSequences.reset())
        # Reapply all SGR sequences that left in the stack
        for stack_tag in self.tags_stack:
            self.result.append(str(stack_tag))

    def handle_data(self, data: str) -> None:
        self.result.append(data)

    def get_result(self) -> str:
        self.sgr_reset()
        return "".join(self.result)


class SGR:
    """Stores and parses a piece of marked-up text.

    Attributes:
        sgrml (str): Text with markup.
    """

    def __init__(self, sgrml: str) -> None:
        self.sgrml = sgrml
        self._parsed: str | None = None
        self._parser = Parser()

    def parse(self) -> str:
        """Parses raw markup and returns formatted string with SGR sequences."""
        if self._parsed is not None:
            return self._parsed
        self._parser.feed(self.sgrml)
        self._parsed = self._parser.get_result()
        return self._parsed

    def __str__(self) -> str:
        return self.parse()

    def __repr__(self) -> str:
        return repr(self.parse())

    def __eq__(self, value: object) -> None:
        if isinstance(value, str):
            return str(self) == value
        if isinstance(value, SGR):
            return str(self) == str(value)
        raise ValueError(f"Can't compare to type {type(value)}")
