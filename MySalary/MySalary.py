from tkinter import Tk, Button, Menu
from json import loads, dumps
from threading import Thread
from requests import post, get


class ExcelAnalyzer:
    def __init__(self, path):
        self.path = path

    def same_date_next_line(self):
        if self.next_day_exists():
            pass

    def get_date(self):
        pass

    def get_start_time(self):
        pass

    def get_end_time(self):
        pass

    def get_comments(self):
        pass

    def next_day_exists(self):
        pass

    def go_next_line(self):
        pass


class RequestManager:
    def __init__(self, url, credentials):
        self.url = url
        self.credentials = credentials

    def login(self):
        pass

    def pass_hours_for_date(self, data):
        pass


class DateManager:
    def __init__(self, path_to_excel):
        self.excel_analyzer = ExcelAnalyzer(path_to_excel)

    def get_day(self):
        date = self.excel_analyzer.get_date()
        comments = self.excel_analyzer.get_comments()
        start_end_times = list()
        start_time = self.excel_analyzer.get_start_time()
        end_time = self.excel_analyzer.get_end_time()
        start_end_times.append((start_time, end_time))
        while self.excel_analyzer.same_date_next_line():
            self.excel_analyzer.go_next_line()
            start_time = self.excel_analyzer.get_start_time()
            end_time = self.excel_analyzer.get_end_time()
            start_end_times.append((start_time, end_time))
        return {'date': date, 'comments': comments, 'start_end_times': start_end_times}

    def get_all_days(self):
        days = list()
        days.append(self.get_day())
        while self.excel_analyzer.next_day_exists():
            self.excel_analyzer.go_next_line()
            days.append(self.get_day())
        return days


class ViewManager:
    def __init__(self):
        self.tk_root_setup()

    def tk_root_setup(self):
        root = Tk()
        root.title("WarZone Master Trader")
        buttons = list()
        buttons.append(Button(master=root, text="Attempt Login", command=None))
        buttons.append(
            Button(master=root, text="Submit Hours from Excel", command=None))
        elements = buttons
        for element in elements:
            element.pack()
        menubar = Menu(master=root)
        root.config(menu=menubar)
        menubar.add_command(label="Close Window", command=root.quit)
        root.after(200, lambda: self.geometry_setter(root))
        root.mainloop()

    @staticmethod
    def geometry_setter(root):
        root.minsize(width=root.winfo_width() + 150,
                     height=root.winfo_height())
        x_width_pos = int((root.winfo_screenwidth() - root.winfo_width()) / 2)
        y_height_pos = int(
            (root.winfo_screenheight() - root.winfo_height()) / 2)
        geometry_text = "" + str(root.winfo_width() + 150) + "x" + str(root.winfo_height()) + "+" + str(
            x_width_pos - 75) + "+" + str(y_height_pos) + ""
        root.geometry(geometry_text)
        root.update()


if __name__ == '__main__':
    ViewManager()
