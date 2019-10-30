from xlrd import open_workbook


class ExcelAnalyzer:
    def __init__(self, path):
        self.sheet = open_workbook(path).sheet_by_index(0)
        self.row = 1

    def same_date_next_line(self):
        return self.current_date() == self.next_date()

    def current_date(self):
        column = 11
        return self.sheet.cell_value(self.row, column)

    def next_date(self):
        column = 11
        if self.next_day_exists():
            return self.sheet.cell_value(self.row + 1, column)
        return False

    def get_date(self):
        column = 1
        return self.sheet.cell_value(self.row, column)

    def get_start_time(self):
        column = 9
        return self.sheet.cell_value(self.row, column)

    def get_end_time(self):
        column = 8
        return self.sheet.cell_value(self.row, column)

    def get_comments(self):
        column = 3
        return self.sheet.cell_value(self.row, column)

    def next_day_exists(self):
        column = 14
        if self.row + 1 < self.sheet.nrows:
            return self.sheet.cell_value(self.row + 1, column)
        else:
            return False

    def go_next_line(self):
        self.row += 1

    def what_day(self):
        column = 15
        if self.sheet.ncols - 1 > 14:
            reason = self.sheet.cell_value(self.row, column)
            if reason.strip():
                if reason == 'מחלה':
                    return 'disease'
                elif reason == 'חופשה':
                    return 'holiday'
            else:
                return 'work'
        else:
            return 'work'


if __name__ == '__main__':
    pass
