from xlrd import open_workbook


class ExcelAnalyzer:
    def __init__(self, path):
        self.sheet = open_workbook(path).sheet_by_index(0)
        self.column = 1

    def same_date_next_line(self):
        row = 11
        if self.next_day_exists():
            return self.sheet.cell_value(self.column, row) == self.sheet.cell_value(self.column + 1, row)

    def get_date(self):
        row = 1
        return self.sheet.cell_value(self.column, row)

    def get_start_time(self):
        row = 9
        return self.sheet.cell_value(self.column, row)

    def get_end_time(self):
        row = 8
        return self.sheet.cell_value(self.column, row)

    def get_comments(self):
        row = 3
        return self.sheet.cell_value(self.column, row)

    def next_day_exists(self):
        row = 14
        if self.column != self.sheet.ncols:
            return self.sheet.cell_value(self.column + 1, row)
        else:
            return False

    def go_next_line(self):
        self.column += 1

    def what_day(self):
        # row = 16
        raise ValueError("Unimplemented")
        if self.sheet.nrows != 16:
            return 'work'
        else:
            return self.sheet.cell_value(self.column, row)


if __name__ == '__main__':
    pass
