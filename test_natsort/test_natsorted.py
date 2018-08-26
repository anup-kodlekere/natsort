# -*- coding: utf-8 -*-
"""\
Here are a collection of examples of how this module can be used.
See the README or the natsort homepage for more details.
"""
from __future__ import print_function, unicode_literals

from operator import itemgetter

import pytest
from natsort import natsorted, ns, as_utf8
from natsort.compat.py23 import PY_VERSION
from pytest import raises

DEFAULT = 0


@pytest.fixture
def float_list():
    return ["a50", "a51.", "a50.31", "a-50", "a50.4", "a5.034e1", "a50.300"]


@pytest.fixture
def fruit_list():
    return ["Apple", "corn", "Corn", "Banana", "apple", "banana"]


@pytest.fixture
def mixed_list():
    return ["Á", "0", "ä", 3, "b", 1.5, "2", "Z"]


def test_natsorted_numbers_in_ascending_order():
    given = ["a2", "a5", "a9", "a1", "a4", "a10", "a6"]
    expected = ["a1", "a2", "a4", "a5", "a6", "a9", "a10"]
    assert natsorted(given) == expected


def test_natsorted_can_sort_as_signed_floats_with_exponents(float_list):
    expected = ["a-50", "a50", "a50.300", "a50.31", "a5.034e1", "a50.4", "a51."]
    assert natsorted(float_list, alg=ns.REAL) == expected


@pytest.mark.parametrize(
    # UNSIGNED is default
    "alg",
    [ns.NOEXP | ns.FLOAT | ns.UNSIGNED, ns.NOEXP | ns.FLOAT],
)
def test_natsorted_can_sort_as_unsigned_and_ignore_exponents(float_list, alg):
    expected = ["a5.034e1", "a50", "a50.300", "a50.31", "a50.4", "a51.", "a-50"]
    assert natsorted(float_list, alg=alg) == expected


# INT, DIGIT, and VERSION are all equivalent.
@pytest.mark.parametrize("alg", [DEFAULT, ns.INT, ns.DIGIT, ns.VERSION])
def test_natsorted_can_sort_as_unsigned_ints_which_is_default(float_list, alg):
    expected = ["a5.034e1", "a50", "a50.4", "a50.31", "a50.300", "a51.", "a-50"]
    assert natsorted(float_list, alg=alg) == expected


def test_natsorted_can_sort_as_signed_ints(float_list):
    expected = ["a-50", "a5.034e1", "a50", "a50.4", "a50.31", "a50.300", "a51."]
    assert natsorted(float_list, alg=ns.SIGNED) == expected


@pytest.mark.parametrize(
    "alg, expected",
    [(ns.UNSIGNED, ["a7", "a+2", "a-5"]), (ns.SIGNED, ["a-5", "a+2", "a7"])],
)
def test_natsorted_can_sort_with_or_without_accounting_for_sign(alg, expected):
    given = ["a-5", "a7", "a+2"]
    assert natsorted(given, alg=alg) == expected


@pytest.mark.parametrize("alg", [DEFAULT, ns.VERSION])
def test_natsorted_can_sort_as_version_numbers(alg):
    given = ["1.9.9a", "1.11", "1.9.9b", "1.11.4", "1.10.1"]
    expected = ["1.9.9a", "1.9.9b", "1.10.1", "1.11", "1.11.4"]
    assert natsorted(given, alg=alg) == expected


@pytest.mark.parametrize(
    "alg, expected",
    [
        (DEFAULT, ["0", 1.5, "2", 3, "Á", "Z", "ä", "b"]),
        (ns.NUMAFTER, ["Á", "Z", "ä", "b", "0", 1.5, "2", 3]),
    ],
)
def test_natsorted_handles_mixed_types(mixed_list, alg, expected):
    assert natsorted(mixed_list, alg=alg) == expected


@pytest.mark.parametrize(
    "alg, expected, slc",
    [
        (DEFAULT, [float("nan"), 5, "25", 1E40], slice(1, None)),
        (ns.NANLAST, [5, "25", 1E40, float("nan")], slice(None, 3)),
    ],
)
def test_natsorted_handles_nan(alg, expected, slc):
    given = ["25", 5, float("nan"), 1E40]
    # The slice is because NaN != NaN
    # noinspection PyUnresolvedReferences
    assert natsorted(given, alg=alg)[slc] == expected[slc]


@pytest.mark.skipif(PY_VERSION < 3.0, reason="error is only raised on Python 3")
def test_natsorted_with_mixed_bytes_and_str_input_raises_type_error():
    with raises(TypeError, match="bytes"):
        natsorted(["ä", b"b"])

    # ...unless you use as_utf (or some other decoder).
    assert natsorted(["ä", b"b"], key=as_utf8) == ["ä", b"b"]


def test_natsorted_raises_type_error_for_non_iterable_input():
    with raises(TypeError, match="'int' object is not iterable"):
        natsorted(100)


def test_natsorted_recurses_into_nested_lists():
    given = [["a1", "a5"], ["a1", "a40"], ["a10", "a1"], ["a2", "a5"]]
    expected = [["a1", "a5"], ["a1", "a40"], ["a2", "a5"], ["a10", "a1"]]
    assert natsorted(given) == expected


def test_natsorted_applies_key_to_each_list_element_before_sorting_list():
    given = [("a", "num3"), ("b", "num5"), ("c", "num2")]
    expected = [("c", "num2"), ("a", "num3"), ("b", "num5")]
    assert natsorted(given, key=itemgetter(1)) == expected


def test_natsorted_returns_list_in_reversed_order_with_reverse_option(float_list):
    expected = natsorted(float_list)[::-1]
    assert natsorted(float_list, reverse=True) == expected


def test_natsorted_handles_filesystem_paths():
    given = [
        "/p/Folder (10)/file.tar.gz",
        "/p/Folder/file.tar.gz",
        "/p/Folder (1)/file (1).tar.gz",
        "/p/Folder (1)/file.tar.gz",
    ]
    expected_correct = [
        "/p/Folder/file.tar.gz",
        "/p/Folder (1)/file.tar.gz",
        "/p/Folder (1)/file (1).tar.gz",
        "/p/Folder (10)/file.tar.gz",
    ]
    expected_incorrect = [
        "/p/Folder (1)/file (1).tar.gz",
        "/p/Folder (1)/file.tar.gz",
        "/p/Folder (10)/file.tar.gz",
        "/p/Folder/file.tar.gz",
    ]
    # Is incorrect by default.
    assert natsorted(given) == expected_incorrect
    # Need ns.PATH to make it correct.
    assert natsorted(given, alg=ns.PATH) == expected_correct


def test_natsorted_handles_numbers_and_filesystem_paths_simultaneously():
    # You can sort paths and numbers, not that you'd want to
    given = ["/Folder (9)/file.exe", 43]
    expected = [43, "/Folder (9)/file.exe"]
    assert natsorted(given, alg=ns.PATH) == expected


@pytest.mark.parametrize(
    "alg, expected",
    [
        (DEFAULT, ["Apple", "Banana", "Corn", "apple", "banana", "corn"]),
        (ns.IGNORECASE, ["Apple", "apple", "Banana", "banana", "corn", "Corn"]),
        (ns.LOWERCASEFIRST, ["apple", "banana", "corn", "Apple", "Banana", "Corn"]),
        (ns.GROUPLETTERS, ["Apple", "apple", "Banana", "banana", "Corn", "corn"]),
        (ns.G | ns.LF, ["apple", "Apple", "banana", "Banana", "corn", "Corn"]),
    ],
)
def test_natsorted_supports_case_handling(alg, expected, fruit_list):
    assert natsorted(fruit_list, alg=alg) == expected


@pytest.mark.parametrize(
    "alg, expected",
    [
        (DEFAULT, [("A5", "a6"), ("a3", "a1")]),
        (ns.LOWERCASEFIRST, [("a3", "a1"), ("A5", "a6")]),
        (ns.IGNORECASE, [("a3", "a1"), ("A5", "a6")]),
    ],
)
def test_natsorted_supports_nested_case_handling(alg, expected):
    given = [("A5", "a6"), ("a3", "a1")]
    assert natsorted(given, alg=alg) == expected


@pytest.mark.parametrize(
    "alg, expected",
    [
        (DEFAULT, ["apple", "Apple", "banana", "Banana", "corn", "Corn"]),
        (ns.CAPITALFIRST, ["Apple", "Banana", "Corn", "apple", "banana", "corn"]),
        (ns.LOWERCASEFIRST, ["Apple", "apple", "Banana", "banana", "Corn", "corn"]),
        (ns.C | ns.LF, ["apple", "banana", "corn", "Apple", "Banana", "Corn"]),
    ],
)
@pytest.mark.usefixtures("with_locale_en_us")
def test_natsorted_can_sort_using_locale(fruit_list, alg, expected):
    assert natsorted(fruit_list, alg=ns.LOCALE | alg) == expected


@pytest.mark.usefixtures("with_locale_en_us")
def test_natsorted_can_sort_locale_specific_numbers_en():
    given = ["c", "a5,467.86", "ä", "b", "a5367.86", "a5,6", "a5,50"]
    expected = ["a5,6", "a5,50", "a5367.86", "a5,467.86", "ä", "b", "c"]
    assert natsorted(given, alg=ns.LOCALE | ns.F) == expected


@pytest.mark.usefixtures("with_locale_de_de")
def test_natsorted_can_sort_locale_specific_numbers_de():
    given = ["c", "a5.467,86", "ä", "b", "a5367.86", "a5,6", "a5,50"]
    expected = ["a5,50", "a5,6", "a5367.86", "a5.467,86", "ä", "b", "c"]
    assert natsorted(given, alg=ns.LOCALE | ns.F) == expected


@pytest.mark.parametrize(
    "alg, expected",
    [
        (DEFAULT, ["0", 1.5, "2", 3, "ä", "Á", "b", "Z"]),
        (ns.NUMAFTER, ["ä", "Á", "b", "Z", "0", 1.5, "2", 3]),
        (ns.UNGROUPLETTERS, ["0", 1.5, "2", 3, "Á", "Z", "ä", "b"]),
        (ns.UG | ns.NA, ["Á", "Z", "ä", "b", "0", 1.5, "2", 3]),
        # Adding PATH changes nothing.
        (ns.PATH, ["0", 1.5, "2", 3, "ä", "Á", "b", "Z"]),
        (ns.PATH | ns.NUMAFTER, ["ä", "Á", "b", "Z", "0", 1.5, "2", 3]),
        (ns.PATH | ns.UNGROUPLETTERS, ["0", 1.5, "2", 3, "Á", "Z", "ä", "b"]),
        (ns.PATH | ns.UG | ns.NA, ["Á", "Z", "ä", "b", "0", 1.5, "2", 3]),
    ],
)
@pytest.mark.usefixtures("with_locale_en_us")
def test_natsorted_handles_mixed_types_with_locale(mixed_list, alg, expected):
    assert natsorted(mixed_list, alg=ns.LOCALE | alg) == expected


@pytest.mark.parametrize(
    "alg, expected",
    [
        (DEFAULT, ["73", "5039", "Banana", "apple", "corn", "~~~~~~"]),
        (ns.NUMAFTER, ["Banana", "apple", "corn", "~~~~~~", "73", "5039"]),
    ],
)
def test_natsorted_sorts_an_odd_collection_of_strings(alg, expected):
    given = ["apple", "Banana", "73", "5039", "corn", "~~~~~~"]
    assert natsorted(given, alg=alg) == expected


def test_natsorted_sorts_mixed_ascii_and_non_ascii_numbers():
    given = [
        "1st street",
        "10th street",
        "2nd street",
        "2 street",
        "1 street",
        "1street",
        "11 street",
        "street 2",
        "street 1",
        "Street 11",
        "۲ street",
        "۱ street",
        "۱street",
        "۱۲street",
        "۱۱ street",
        "street ۲",
        "street ۱",
        "street ۱",
        "street ۱۲",
        "street ۱۱",
    ]
    expected = [
        "1 street",
        "۱ street",
        "1st street",
        "1street",
        "۱street",
        "2 street",
        "۲ street",
        "2nd street",
        "10th street",
        "11 street",
        "۱۱ street",
        "۱۲street",
        "street 1",
        "street ۱",
        "street ۱",
        "street 2",
        "street ۲",
        "Street 11",
        "street ۱۱",
        "street ۱۲",
    ]
    assert natsorted(given, alg=ns.IGNORECASE) == expected
