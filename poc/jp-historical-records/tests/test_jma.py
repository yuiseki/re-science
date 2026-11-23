import pytest

import jma


def _row(year, temp, cls="data_0_0", n=27):
    cells = ['<td class="data_0_0"> </td>'] * n
    cells[jma.MEAN_TEMP_CELL] = f'<td class="{cls}">{temp}</td>'
    return (
        '<tr class="mtx2" style="text-align:right;"><td style="white-space:nowrap">'
        f'<div class="a_print"><a href="monthly_s1.php?prec_no=1&block_no=2&year={year}&month=&day=&view=p1">{year}</a></div></td>'
        + "".join(cells)
        + "</tr>"
    )


def test_parse_value_variants():
    assert jma.parse_value("16.3") == 16.3
    assert jma.parse_value("-1.2 )") == -1.2
    assert jma.parse_value("16.3 ]") is None
    for missing in ("", " ", "--", "///", "×", "#"):
        assert jma.parse_value(missing) is None


def test_parse_annual_reads_year_value_and_marks():
    html = _row(1999, "17.0") + _row(2000, "17.4", "data_1t_0") + _row(2001, "17.2 ]", "data_2t_0")
    assert jma.parse_annual(html) == [
        {"year": 1999, "temp": 17.0, "mark": "none"},
        {"year": 2000, "temp": 17.4, "mark": "dotted"},
        {"year": 2001, "temp": None, "mark": "solid"},
    ]


def test_line_under_a_row_belongs_to_the_next_year():
    html = _row(1999, "17.0", "data_0_2b") + _row(2000, "17.4", "data_1t_0") + _row(2001, "17.2", "data_3t_0")
    assert [r["mark"] for r in jma.parse_annual(html)] == ["none", "solid", "solid"]


def test_line_under_a_row_is_dropped_when_the_next_year_is_absent():
    html = _row(1999, "17.0", "data_0_1b") + _row(2005, "17.4")
    assert [r["mark"] for r in jma.parse_annual(html)] == ["none", "none"]


def test_parse_annual_fails_on_changed_layout():
    with pytest.raises(ValueError):
        jma.parse_annual(_row(2000, "17.4", n=26))
    with pytest.raises(ValueError):
        jma.parse_annual(_row(2000, "17.4", "data_9t_0"))
    with pytest.raises(ValueError):
        jma.parse_annual("<html></html>")


def test_parse_stations_keeps_only_staffed_type():
    html = (
        "onmouseover=\"javascript:viewPoint('s','47830','宮崎','ミヤザキ','31','56.3');\" "
        "onmouseover=\"javascript:viewPoint('a','1234','えびの','エビノ');\" "
        "onmouseover=\"javascript:viewPoint('s','47830','宮崎','ミヤザキ','31','56.3');\""
    )
    assert jma.parse_stations(html) == [("47830", "宮崎")]
