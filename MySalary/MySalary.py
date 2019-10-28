from tkinter import Tk, Button, Menu, Entry, Label, Checkbutton, Toplevel, BooleanVar
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

from DateManager import DateManager
from NetworkManager import NetworkManager
from selenium.common.exceptions import TimeoutException


class ViewManager:
    def __init__(self):
        self.network_manager = NetworkManager(self.state_changer)
        self.running = True
        self.labels, self.entries, self.buttons = dict(), dict(), dict()
        self.root = Tk()
        self.override_data = BooleanVar()
        self.override_data.set(True)
        self.tk_root_setup()

    def tk_root_setup(self):
        self.root.title("Deshe AutoReporter")
        self.labels.update({'username': Label(master=self.root, text="Username: ")})
        self.labels.update({'password': Label(master=self.root, text="Password: ")})
        self.entries.update({'username': Entry(master=self.root, text="Username", command=None)})
        self.entries.update({'password': Entry(master=self.root, text="Password", show="*", command=None)})
        self.buttons.update({'authentication': Button(master=self.root, text="Login",
                                                      command=lambda: self.network_manager.login(
                                                          entries=self.entries))})
        self.buttons.update(
            {'override_data': Checkbutton(master=self.root, text="Override existing data", variable=self.override_data,
                                          onvalue=True, offvalue=False)})
        self.buttons.update(
            {'submit_excel_hours': Button(master=self.root, text="Submit Hours from Excel",
                                          command=lambda: self.set_hours_from_excel(self.override_data.get()),
                                          state='disabled')})
        self.buttons.update({'get_salary': Button(master=self.root, text="Last Salary",
                                                  command=self.network_manager.get_last_salary, state='disabled')})
        row = 0
        for key in self.labels:
            self.labels[key].grid(row=row, column=0)
            row += 1
        row = 0
        for key in self.entries:
            self.entries[key].bind('<Return>',
                                   lambda event: self.network_manager.login(entries=self.entries))
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
        self.root.after(200, lambda: self.geometry_setter(self.root))
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
        self.geometry_setter(top, minimum_x=500, minimum_y=160)

    def close_app(self):
        self.running = False
        self.root.quit()

    def state_changer(self, is_logged_in):
        if is_logged_in:
            self.update_when_need(self.buttons['submit_excel_hours'], 'state', 'normal')
            self.update_when_need(self.buttons['get_salary'], 'state', 'normal')
            self.update_when_need(self.buttons['authentication'], 'text', 'Logout')
            for key in self.entries:
                self.update_when_need(self.entries[key], 'state', 'disabled')
        else:
            self.update_when_need(self.buttons['submit_excel_hours'], 'state', 'normal')
            self.update_when_need(self.buttons['get_salary'], 'state', 'disabled')
            self.update_when_need(self.buttons['authentication'], 'text', 'Login')
            for key in self.entries:
                self.update_when_need(self.entries[key], 'state', 'normal')

    @staticmethod
    def update_when_need(element, field_to_change, variable):
        if element[field_to_change] != variable:
            element[field_to_change] = variable

    @staticmethod
    def set_hours_from_excel(override_data):
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
                    # self.network_manager.report_shift(date['start_date'], date['end_date'], date['comments'], override_data=override_data)
                showinfo('Submitted', 'Hours succesfully passed!')
            except TimeoutException as ex:
                showinfo('Timeout', 'Error ' + str(ex))
        else:
            showinfo('Cancelled', 'Process cancelled.')

    @staticmethod
    def geometry_setter(root, minimum_x=0, minimum_y=0):
        root.minsize(width=root.winfo_width() + minimum_x, height=root.winfo_height() + minimum_y)
        x_width_pos = int((root.winfo_screenwidth() - (root.winfo_width() + minimum_x)) / 2)
        y_height_pos = int(
            (root.winfo_screenheight() - (root.winfo_height() + minimum_y)) / 2)
        geometry_text = str(root.winfo_width() + minimum_x) + "x" + str(root.winfo_height() + minimum_y) + "+" + str(
            x_width_pos - 75) + "+" + str(y_height_pos) + ""
        root.geometry(geometry_text)
        root.update()


if __name__ == '__main__':
    ViewManager()
