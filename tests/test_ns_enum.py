from __future__ import annotations

import pytest

from natsort import ns


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        ("FLOAT", 0x0001),
        ("SIGNED", 0x0002),
        ("NOEXP", 0x0004),
        ("PATH", 0x0008),
        ("LOCALEALPHA", 0x0010),
        ("LOCALENUM", 0x0020),
        ("IGNORECASE", 0x0040),
        ("LOWERCASEFIRST", 0x0080),
        ("GROUPLETTERS", 0x0100),
        ("UNGROUPLETTERS", 0x0200),
        ("NANLAST", 0x0400),
        ("COMPATIBILITYNORMALIZE", 0x0800),
        ("NUMAFTER", 0x1000),
        ("PRESORT", 0x2000),
        ("DEFAULT", 0x0000),
        ("INT", 0x0000),
        ("UNSIGNED", 0x0000),
        ("REAL", 0x0003),
        ("LOCALE", 0x0030),
        ("I", 0x0000),
        ("U", 0x0000),
        ("F", 0x0001),
        ("S", 0x0002),
        ("R", 0x0003),
        ("N", 0x0004),
        ("P", 0x0008),
        ("LA", 0x0010),
        ("LN", 0x0020),
        ("L", 0x0030),
        ("IC", 0x0040),
        ("LF", 0x0080),
        ("G", 0x0100),
        ("UG", 0x0200),
        ("C", 0x0200),
        ("CAPITALFIRST", 0x0200),
        ("NL", 0x0400),
        ("CN", 0x0800),
        ("NA", 0x1000),
        ("PS", 0x2000),
    ],
)
def test_ns_enum(given: str, expected: int) -> None:
    assert ns[given] == expected
