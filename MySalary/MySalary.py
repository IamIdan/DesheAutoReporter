from threading import Thread
from time import sleep
from tkFileDialog import askopenfilename
from tkMessageBox import showinfo

from tkinter import Tk, Button, Menu, Entry, Label, Checkbutton, Toplevel


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
        self.running = True
        self.labels, self.entries, self.buttons, self.threads = dict(), dict(), dict(), dict()
        self.path_to_excel = ''
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
        self.threads.update({'updater': Thread(target=self.updater)})
        self.threads['updater'].start()
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

    def updater(self):
        while self.running:
            try:
                sleep(1)
                if False:
                    # if self.network_manager.is_logged_in:
                    self.update_when_need(self.buttons['submit_excel_hours'], 'state', 'normal')
                    self.update_when_need(self.buttons['authentication'], 'text', 'logout')
                    for key in self.entries:
                        self.update_when_need(self.entries[key], 'state', 'disabled')
                else:
                    self.update_when_need(self.buttons['submit_excel_hours'], 'state', 'normal')
                    self.update_when_need(self.buttons['authentication'], 'text', 'login')
                    for key in self.entries:
                        self.update_when_need(self.entries[key], 'state', 'normal')
            except Exception:
                pass

    @staticmethod
    def update_when_need(element, field_to_change, variable):
        if element[field_to_change] != variable:
            element[field_to_change] = variable

    def login(self, event=None):
        # if self.network_manager.is_logged_in:
        #     self.network_manager.login(credentials (username with password credentials))
        # else:
        #     self.network_manager.logout()
        pass

    def set_hours_from_excel(self):
        self.path_to_excel = askopenfilename(title="Select your Excel file for import",
                                             filetypes=(("CSV Files", "*.csv"),))
        if self.path_to_excel:
            pass
            # Example of date formats:
            # start_date = datetime(2019, 9, 29, 8)
            # end_date = datetime(2019, 9, 29, 12)
            # dates = self.dater.get_all_days
            # for date in dates:
            #     self.network_manager.report_shift(date['start_date'], date['end_date'])
            showinfo('Submitted', 'Hours succesfully passed!')
        else:
            showinfo('Cancelled', 'Process cancelled.')
        pass

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
