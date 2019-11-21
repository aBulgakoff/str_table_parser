from typing import cast, Iterable, List, Dict, Tuple, Optional


class Table(object):

    def __init__(self):
        self._fields = None
        self._rows = []
        self._columns = {}

    def __str__(self) -> str:
        return str(self.rows)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def fields(self) -> List['str']:
        return list(self._fields.keys())

    @fields.setter
    def fields(self, fields: Iterable[str]):
        composed_fields = {}
        for key in fields:
            composed_fields[key] = ''  # prepare rows structure
            self._columns[key] = []  # prepare columns structure
        self._fields = composed_fields

    def get_row(self, index: int) -> Dict[str, str]:
        try:
            return self._rows[index].copy()
        except IndexError as e:
            raise IndexError(f'Row with index {index} does not exist. Amount of rows is {len(self._rows)}.') from e

    def add_row(self, row: Iterable[str]) -> None:
        row = cast(List[str], row)  # cast on Type hint level
        # if table does not have a header make it using indexes of elements in row 0
        if not self._fields:
            self.fields = [str(value) for value in range(len(row))]

        field_values_row = self._fields.copy()
        index = 0
        for field in field_values_row.keys():
            try:
                row_value = row[index]
            except IndexError as e:
                raise IndexError(f'Element with index {index} does not exist in the row. '
                                 f'Amount of fields is {len(field_values_row.keys())} '
                                 f'when amount of elements in the row is {len(row)}.') from e
            field_values_row[field] = row_value  # compose rows
            self._columns[field].append(row_value)  # compose columns
            index += 1
        self._rows.append(field_values_row)

    def get_column(self, index: int) -> List[str]:
        try:
            key_by_index = self.fields[index]
        except IndexError as e:
            raise IndexError(
                f'Column with index {index} does not exist. Amount of columns is {len(self.fields)}.') from e
        return self._columns[key_by_index][:]

    @property
    def columns(self) -> Dict[str, List[str]]:
        return self._columns.copy()

    @property
    def rows(self) -> List[Dict[str, str]]:
        return self._rows[:]


def parse_str_table(data: str, table_with_header: bool = True) -> Table:
    """
    Parser of string representation tables

    :param data: string representation table
    with header in a first line, columns divided by "|" and rows divided by EOL "\n"
    :param table_with_header: parameter which marks header/no header table
    :return Table object

    Example of data variable:
    | header_1st_col   | header_2nd_col   | header_3rd_col   |\n
    | row_1_of_1st_col | row_1_of_2nd_col | row_1_of_3rd_col |\n
    | row_2_of_1st_col | row_2_of_2nd_col | row_2_of_3rd_col |

    Example of basic usage:
    >>> parse_str_table(f'| head |\\n| body_1 |\\n| body_2 |')
    [{'head': 'body_1'}, {'head': 'body_2'}]

    """
    table = Table()
    if table_with_header:
        unformatted_header, unformatted_body = split_str_table(data)
        table.fields = extract_values_from_row(unformatted_header)
    else:
        unformatted_body = split_str_table(data, header=False)[1]
    for line in unformatted_body:
        table.add_row(extract_values_from_row(line))
    return table


def split_str_table(data: str, header: bool = True) -> Tuple[Optional[str], List[str]]:
    """
    :param data: string representation table with rows divided by EOL "\n"
    :param header: parameter which marks header/no header table
    :return: tuple where 1st element is an optional Table Header's line and 2nd is an array with Table Body lines

    Example:
    >>> split_str_table(f'| head |\\n| body_1 |\\n| body_2 |')
    ('| head |', ['| body_1 |', '| body_2 |'])
    >>> split_str_table(f'| body_1 |\\n| body_2 |', header=False)
    (None, ['| body_1 |', '| body_2 |'])
    """
    splitted_data = data.splitlines()
    return (splitted_data[0], splitted_data[1:]) if header else (None, splitted_data)


def extract_values_from_row(line: str) -> List[str]:
    """
    Example:
    >>> extract_values_from_row('| head1 | head2 |')
    ['head1', 'head2']
    """
    return [value.strip() for value in line.split('|') if value]
