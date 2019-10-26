from tkinter import Tk, Button, Menu, Entry, Label, Checkbutton
from threading import Thread
from time import sleep

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
        # self.network_manager = SeleniumManager()
        # self.dater = DateManager()
        self.labels, self.entries, self.buttons = list(), list(), list()
        self.root = Tk()
        self.tk_root_setup()

    def tk_root_setup(self):
        self.root.title("Deshe AutoReporter")
        self.labels.append(Label(master=self.root, text="Username: "))
        self.labels.append(Label(master=self.root, text="Password: "))
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i, column=0)
        self.entries.append(Entry(master=self.root, text="Username", command=None))
        self.entries.append(Entry(master=self.root, text="Password", show="*", command=None))
        for i in range(len(self.entries)):
            self.entries[i].grid(row=i, column=1)
        self.buttons.append(Button(master=self.root, text="Login", command=self.login))
        self.buttons.append(Checkbutton(master=self.root, text="Override existing data"))
        self.buttons.append(
            Button(master=self.root, text="Submit Hours from Excel", command=None, state='disabled'))
        for entry in self.entries:
            entry.bind('<Return>', self.login)
        for i in range(len(self.buttons)):
            self.buttons[i].grid(row=2, column=i)
        menubar = Menu(master=self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Close Window", command=self.root.quit)
        self.root.after(200, self.geometry_setter)
        Thread(target=self.updater).start()
        self.root.mainloop()

    def updater(self):
        while True:
            sleep(1)
            # if self.network_manager.is_logged_in:
            #     self.update_when_need(self.buttons['submitexcelhours'], 'state', 'normal')
            #     self.update_when_need(self.buttons['authentication'], 'text', 'logout')
            #     for entry in self.entries:
            #         self.update_when_need(entry, 'state', 'disabled')
            # else:
            #     self.update_when_need(self.buttons['submitexcelhours'], 'state', 'disabled')
            #     self.update_when_need(self.buttons['authentication'], 'text', 'login')
            #     for entry in self.entries:
            #         self.update_when_need(entry, 'state', 'normal')

    @staticmethod
    def update_when_need(element, field_to_change, variable):
        if element[field_to_change] != variable:
            element[field_to_change] = variable

    def login(self, event=None):
        # self.network_manager.login(url (const), credentials (username with password credentials))
        # if self.network_manager.is_logged_in:
        #     button[1]['state'] = 'normal'
        # else:
        #     button[1]['state'] = 'disabled'
        pass

    def set_hours(self):
        # Example of date formats:
        # start_date = datetime(2019, 9, 29, 8)
        # end_date = datetime(2019, 9, 29, 12)
        # dates = self.dater.get_all_days
        # for date in dates:
        #     self.network_manager.report_shift(date['start_date'], date['end_date'])
        pass

    def geometry_setter(self):
        self.root.minsize(width=self.root.winfo_width() + 150, height=self.root.winfo_height())
        x_width_pos = int((self.root.winfo_screenwidth() - self.root.winfo_width()) / 2)
        y_height_pos = int(
            (self.root.winfo_screenheight() - self.root.winfo_height()) / 2)
        geometry_text = "" + str(self.root.winfo_width() + 150) + "x" + str(self.root.winfo_height()) + "+" + str(
            x_width_pos - 75) + "+" + str(y_height_pos) + ""
        self.root.geometry(geometry_text)
        self.root.update()


if __name__ == '__main__':
    ViewManager()

