from tkinter import Tk, Button, Menu, Entry, Label, Checkbutton


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
        self.tk_root_setup()

    def tk_root_setup(self):
        root = Tk()
        root.title("Deshe AutoReporter")
        self.labels.append(Label(master=root, text="Username: "))
        self.labels.append(Label(master=root, text="Password: "))
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i, column=0)
        self.entries.append(Entry(master=root, text="Username", command=None))
        self.entries.append(Entry(master=root, text="Password", show="*", command=None))
        for i in range(len(self.entries)):
            self.entries[i].grid(row=i, column=1)
        self.buttons.append(Button(master=root, text="Login", command=self.login))
        self.buttons.append(Checkbutton(master=root, text="Override existing data"))
        self.buttons.append(
            Button(master=root, text="Submit Hours from Excel", command=None, state='disabled'))
        for entry in self.entries:
            entry.bind('<Return>', self.login)
        for i in range(len(self.buttons)):
            self.buttons[i].grid(row=2, column=i)
        menubar = Menu(master=root)
        root.config(menu=menubar)
        menubar.add_command(label="Close Window", command=root.quit)
        root.after(200, lambda: self.geometry_setter(root))
        root.mainloop()

    def state_setter(self):
        if self.network_manager.is_logged_in:
            self.buttons['submitexcelhours']['state'] = 'normal'
            self.buttons['authentication']['text'] = 'logout'
            for entry in self.entries:
                entry['state']['state'] = 'disabled'
        else:
            self.buttons['submitexcelhours']['state'] = 'disabled'
            self.buttons['authentication']['text'] = 'login'
            for entry in self.entries:
                entry['state']['state'] = 'normal'

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
