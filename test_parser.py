import pytest

"""
Input:
| header_1st_col   | header_2nd_col   | header_3rd_col   |
| row_1_of_1st_col | row_1_of_2nd_col | row_1_of_3rd_col |
| row_2_of_1st_col | row_2_of_2nd_col | row_2_of_3rd_col |
"""

header = '| header_1st_col | header_2nd_col | header_3rd_col |'
body_row1 = '| row_1_of_1st_col | row_1_of_2nd_col | row_1_of_3rd_col |'
body_row2 = '| row_2_of_1st_col | row_2_of_2nd_col | row_2_of_3rd_col |'

source_table = f'{header}\n{body_row1}\n{body_row2}'

exp_fields = ['header_1st_col', 'header_2nd_col', 'header_3rd_col']
exp_body = [body_row1, body_row2]

exp_col_0 = ['row_1_of_1st_col', 'row_2_of_1st_col']
exp_col_1 = ['row_1_of_2nd_col', 'row_2_of_2nd_col']
exp_col_2 = ['row_1_of_3rd_col', 'row_2_of_3rd_col']
exp_cols = {exp_fields[0]: exp_col_0, exp_fields[1]: exp_col_1, exp_fields[2]: exp_col_2}
exp_get_col = [(0, exp_col_0), (1, exp_col_1), (2, exp_col_2)]
exp_col_negative_index = (-4, 3, 4)

exp_row_0 = {'header_1st_col': 'row_1_of_1st_col',
             'header_2nd_col': 'row_1_of_2nd_col',
             'header_3rd_col': 'row_1_of_3rd_col'}
exp_row_1 = {'header_1st_col': 'row_2_of_1st_col',
             'header_2nd_col': 'row_2_of_2nd_col',
             'header_3rd_col': 'row_2_of_3rd_col'}
exp_rows = [exp_row_0, exp_row_1]
exp_get_row = [(0, exp_row_0), (1, exp_row_1), (-1, exp_row_1), (-2, exp_row_0)]
exp_row_negative_index = (2, 3, -3)


def test_fields_extracted(tf):
    header_fields = tf(source_table).fields
    assert header_fields == exp_fields, \
        F'Not all fields match. Found {len(header_fields)} field(s) when expected {len(exp_fields)}'


@pytest.mark.parametrize('index, expected_column', exp_get_col)
def test_get_column(tf, index, expected_column):
    assert tf(source_table).get_column(index) == expected_column


@pytest.mark.parametrize('index', exp_col_negative_index)
def test_try_get_nonexistent_column(tf, index):
    with pytest.raises(IndexError):
        tf(source_table).get_column(index)


def test_get_all_columns(tf):
    assert tf(source_table).columns == exp_cols, 'Columns do not match.'


@pytest.mark.parametrize('index, expected_row', exp_get_row)
def test_get_row(tf, index, expected_row):
    assert tf(source_table).get_row(index) == expected_row


@pytest.mark.parametrize('index', exp_row_negative_index)
def test_get_nonexistent_row(tf, index):
    with pytest.raises(IndexError):
        tf(source_table).get_row(index)


def test_get_all_rows(tf):
    assert tf(source_table).rows == exp_rows, 'Rows do not match.'
