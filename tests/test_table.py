# encoding: utf-8

"""
Test suite for the docx.table module
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.table import (
    _Cell, _Column, _ColumnCollection, _Row, _RowCellCollection,
    _RowCollection, Table
)

from .oxml.unitdata.table import a_gridCol, a_tbl, a_tblGrid, a_tc, a_tr
from .oxml.unitdata.text import a_p


class DescribeTable(object):

    def it_provides_access_to_the_table_rows(self, table):
        rows = table.rows
        assert isinstance(rows, _RowCollection)

    def it_provides_access_to_the_table_columns(self, table):
        columns = table.columns
        assert isinstance(columns, _ColumnCollection)

    def it_provides_access_to_a_cell_by_row_and_col_indices(self, table):
        for row_idx in range(2):
            for col_idx in range(2):
                cell = table.cell(row_idx, col_idx)
                assert isinstance(cell, _Cell)
                tr = table._tbl.tr_lst[row_idx]
                tc = tr.tc_lst[col_idx]
                assert tc is cell._tc

    def it_can_add_a_column(self, add_column_fixture):
        table, expected_xml = add_column_fixture
        col = table.add_column()
        assert table._tbl.xml == expected_xml
        assert isinstance(col, _Column)

    def it_can_add_a_row(self, add_row_fixture):
        table, expected_xml = add_row_fixture
        row = table.add_row()
        assert table._tbl.xml == expected_xml
        assert isinstance(row, _Row)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_column_fixture(self):
        tbl = _tbl_bldr(2, 1).element
        table = Table(tbl)
        expected_xml = _tbl_bldr(2, 2).xml()
        return table, expected_xml

    @pytest.fixture
    def add_row_fixture(self):
        tbl = _tbl_bldr(rows=1, cols=2).element
        table = Table(tbl)
        expected_xml = _tbl_bldr(rows=2, cols=2).xml()
        return table, expected_xml

    @pytest.fixture
    def table(self):
        tbl = _tbl_bldr(rows=2, cols=2).element
        table = Table(tbl)
        return table


class Describe_ColumnCollection(object):

    def it_knows_how_many_columns_it_contains(self, columns_fixture):
        columns, column_count = columns_fixture
        assert len(columns) == column_count

    def it_can_interate_over_its__Column_instances(self, columns_fixture):
        columns, column_count = columns_fixture
        actual_count = 0
        for column in columns:
            assert isinstance(column, _Column)
            actual_count += 1
        assert actual_count == column_count

    def it_provides_indexed_access_to_columns(self, columns_fixture):
        columns, column_count = columns_fixture
        for idx in range(-column_count, column_count):
            column = columns[idx]
            assert isinstance(column, _Column)

    def it_raises_on_indexed_access_out_of_range(self, columns_fixture):
        columns, column_count = columns_fixture
        too_low = -1 - column_count
        too_high = column_count
        with pytest.raises(IndexError):
            columns[too_low]
        with pytest.raises(IndexError):
            columns[too_high]

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def columns_fixture(self):
        column_count = 2
        tbl = _tbl_bldr(rows=2, cols=column_count).element
        columns = _ColumnCollection(tbl)
        return columns, column_count


class Describe_Row(object):

    def it_provides_access_to_the_row_cells(self, cells_access_fixture):
        row = cells_access_fixture
        cells = row.cells
        assert isinstance(cells, _RowCellCollection)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cells_access_fixture(self):
        tr = a_tr().with_nsdecls().element
        row = _Row(tr)
        return row


class Describe_RowCellCollection(object):

    def it_can_iterate_over_its__Cell_instances(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        actual_count = 0
        for cell in cells:
            assert isinstance(cell, _Cell)
            actual_count += 1
        assert actual_count == cell_count

    def it_knows_how_many_cells_it_contains(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        assert len(cells) == cell_count

    def it_provides_indexed_access_to_cells(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        for idx in range(-cell_count, cell_count):
            cell = cells[idx]
            assert isinstance(cell, _Cell)

    def it_raises_on_indexed_access_out_of_range(self, cell_count_fixture):
        cells, cell_count = cell_count_fixture
        too_low = -1 - cell_count
        too_high = cell_count
        with pytest.raises(IndexError):
            cells[too_low]
        with pytest.raises(IndexError):
            cells[too_high]

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def cell_count_fixture(self):
        cell_count = 2
        tr_bldr = a_tr().with_nsdecls()
        for idx in range(cell_count):
            tr_bldr.with_child(a_tc())
        tr = tr_bldr.element
        cells = _RowCellCollection(tr)
        return cells, cell_count


class Describe_RowCollection(object):

    def it_knows_how_many_rows_it_contains(self, rows_fixture):
        rows, row_count = rows_fixture
        assert len(rows) == row_count

    def it_can_iterate_over_its__Row_instances(self, rows_fixture):
        rows, row_count = rows_fixture
        actual_count = 0
        for row in rows:
            assert isinstance(row, _Row)
            actual_count += 1
        assert actual_count == row_count

    def it_provides_indexed_access_to_rows(self, rows_fixture):
        rows, row_count = rows_fixture
        for idx in range(-row_count, row_count):
            row = rows[idx]
            assert isinstance(row, _Row)

    def it_raises_on_indexed_access_out_of_range(self, rows_fixture):
        rows, row_count = rows_fixture
        with pytest.raises(IndexError):
            too_low = -1 - row_count
            rows[too_low]
        with pytest.raises(IndexError):
            too_high = row_count
            rows[too_high]

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def rows_fixture(self):
        row_count = 2
        tbl = _tbl_bldr(rows=row_count, cols=2).element
        rows = _RowCollection(tbl)
        return rows, row_count


# fixtures -----------------------------------------------------------

def _tbl_bldr(rows, cols):
    tblGrid_bldr = a_tblGrid()
    for i in range(cols):
        tblGrid_bldr.with_child(a_gridCol())
    tbl_bldr = a_tbl().with_nsdecls().with_child(tblGrid_bldr)
    for i in range(rows):
        tr_bldr = _tr_bldr(cols)
        tbl_bldr.with_child(tr_bldr)
    return tbl_bldr


def _tc_bldr():
    return a_tc().with_child(a_p())


def _tr_bldr(cols):
    tr_bldr = a_tr()
    for i in range(cols):
        tc_bldr = _tc_bldr()
        tr_bldr.with_child(tc_bldr)
    return tr_bldr
