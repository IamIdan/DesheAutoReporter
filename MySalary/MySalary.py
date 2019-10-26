from datetime import datetime
from tkinter import Tk, Button, Menu, Entry, Label, Checkbutton, Toplevel
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

from SeleniumRequestManger import SeleniumManager
from selenium.common.exceptions import TimeoutException
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


class DateManager:
    def __init__(self, path_to_excel):
        self.excel_analyzer = ExcelAnalyzer(path_to_excel)

    @staticmethod
    def convert_hours_and_minutes_to_int(time):
        time = time.split(':')
        hours = time[0]
        minutes = time[1]
        return hours * 60 + minutes

    def get_day(self):
        date = self.excel_analyzer.get_date()
        comments = self.excel_analyzer.get_comments()
        start_time = self.excel_analyzer.get_start_time()
        end_time = self.excel_analyzer.get_end_time()
        while self.excel_analyzer.same_date_next_line():
            self.excel_analyzer.go_next_line()
            new_start_time = self.excel_analyzer.get_start_time()
            if self.convert_hours_and_minutes_to_int(new_start_time) < self.convert_hours_and_minutes_to_int(
                    start_time):
                start_time = new_start_time
            new_end_time = self.excel_analyzer.get_end_time()
            if self.convert_hours_and_minutes_to_int(new_end_time) > self.convert_hours_and_minutes_to_int(end_time):
                end_time = new_end_time
        year, month, day = date.split(' ')[0].split('/')
        hour, minute = start_time.split(':')
        start_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
        hour, minute = end_time.split(':')
        end_time = datetime(int(year), int(month), int(day), int(hour), int(minute))
        return {'start_time': start_time, 'end_time': end_time, 'comments': comments}

    def get_all_days(self):
        days = list()
        days.append(self.get_day())
        while self.excel_analyzer.next_day_exists():
            self.excel_analyzer.go_next_line()
            days.append(self.get_day())
        return days


class ViewManager:
    def __init__(self):
        self.network_manager = None
        self.running = True
        self.is_logged_in = False
        self.labels, self.entries, self.buttons = dict(), dict(), dict()
        self.root = Tk()
        self.tk_root_setup()

    def tk_root_setup(self):
        self.root.title("Deshe AutoReporter")
        self.labels.update({'username': Label(master=self.root, text="Username: ")})
        self.labels.update({'password': Label(master=self.root, text="Password: ")})
        self.entries.update({'username': Entry(master=self.root, text="Username", command=None)})
        self.entries.update({'password': Entry(master=self.root, text="Password", show="*", command=None)})
        self.buttons.update({'authentication': Button(master=self.root, text="Login", command=self.login)})
        self.buttons.update({'override_data': Checkbutton(master=self.root, text="Override existing data")})
        self.buttons.update(
            {'submit_excel_hours': Button(master=self.root, text="Submit Hours from Excel",
                                          command=self.set_hours_from_excel, state='disabled')})
        row = 0
        for key in self.labels:
            self.labels[key].grid(row=row, column=0)
            row += 1
        row = 0
        for key in self.entries:
            self.entries[key].bind('<Return>', self.login)
            self.entries[key].grid(row=row, column=1)
            row += 1
        column = 0
        for key in self.buttons:
            self.buttons[key].grid(row=2, column=column)
            column += 1
        menu_bar = Menu(master=self.root)
        self.root.config(menu=menu_bar)
        menu_bar.add_command(label="Close Window", command=self.close_app)
        menu_bar.add_command(label="Help!", command=self.help_user)
        self.root.after(200, self.geometry_setter)
        self.root.mainloop()

    def help_user(self):
        """
        Input: Clicked by user!
        Output: Explains about the program.
        Meaning: Contains information about the program.
        """
        top = Toplevel(master=self.root)
        top.title("Instructions")
        top.resizable(width=False, height=False)
        menu_bar = Menu(master=top)
        menu_bar.add_command(label="Quit", command=top.destroy)
        top.config(menu=menu_bar)
        labels = list()
        labels.append(Label(master=top, text="1) Insert your username and password in the given fields."))
        labels.append(Label(master=top, text="2) Click login."))
        labels.append(Label(master=top,
                            text="3) Once you get the message you're authenticated you're good to go, else, retry."))
        labels.append(Label(master=top,
                            text="4) If you want to run on existing dates tick v on override existing data."))
        labels.append(Label(master=top, text="5) Click Submit Hours from Excel, choose your excel hours file."))
        labels.append(Label(master=top, text="6)You're free to go, your hours have been submitted."))
        labels.append(Label(master=top,
                            text="\nNote) It doesn't take breaks in count, only the earliest hour and the latest one."))
        for label in labels:
            label.pack()

    def close_app(self):
        self.running = False
        self.root.quit()
        showinfo('Quitting', 'Goodbye!')

    def state_changer(self):
        if self.is_logged_in:
            self.update_when_need(self.buttons['submit_excel_hours'], 'state', 'normal')
            self.update_when_need(self.buttons['authentication'], 'text', 'logout')
            for key in self.entries:
                self.update_when_need(self.entries[key], 'state', 'disabled')
        else:
            self.update_when_need(self.buttons['submit_excel_hours'], 'state', 'disabled')
            self.update_when_need(self.buttons['authentication'], 'text', 'login')
            for key in self.entries:
                self.update_when_need(self.entries[key], 'state', 'normal')

    @staticmethod
    def update_when_need(element, field_to_change, variable):
        if element[field_to_change] != variable:
            element[field_to_change] = variable

    def login(self, event=None):
        try:
            if not self.is_logged_in:
                self.network_manager = SeleniumManager(username=self.entries['username'],
                                                       password=self.entries['password'])
                self.is_logged_in = True
            else:
                self.network_manager = None
                self.is_logged_in = False
            self.state_changer()
        except TimeoutException as ex:
            showinfo('Timeout', 'Error ' + str(ex))

    @staticmethod
    def set_hours_from_excel():
        path_to_excel = askopenfilename(title="Select your Excel file for import",
                                        filetypes=(("Excel Files", ".xlsx"),))
        if path_to_excel:
            try:
                # Example of date formats:
                # start_date = datetime(2019, 9, 29, 8)
                # end_date = datetime(2019, 9, 29, 12)
                dates = DateManager(path_to_excel).get_all_days()
                for date in dates:
                    pass
                    # self.network_manager.report_shift(date['start_date'], date['end_date'], date['comments'])
                showinfo('Submitted', 'Hours succesfully passed!')
            except TimeoutException as ex:
                showinfo('Timeout', 'Error ' + str(ex))
        else:
            showinfo('Cancelled', 'Process cancelled.')

    def geometry_setter(self):
        self.root.minsize(width=self.root.winfo_width(), height=self.root.winfo_height())
        x_width_pos = int((self.root.winfo_screenwidth() - self.root.winfo_width()) / 2)
        y_height_pos = int(
            (self.root.winfo_screenheight() - self.root.winfo_height()) / 2)
        geometry_text = str(self.root.winfo_width()) + "x" + str(self.root.winfo_height()) + "+" + str(
            x_width_pos - 75) + "+" + str(y_height_pos) + ""
        self.root.geometry(geometry_text)
        self.root.update()


if __name__ == '__main__':
    ViewManager()
