from datetime import timedelta, datetime
from tkinter.messagebox import showinfo

from SeleniumRequestManager import SeleniumManager
from selenium.common.exceptions import TimeoutException


class NetworkManager:
    def __init__(self, state_changer):
        self.selenium_manager = None
        self.is_logged_in = False
        self.state_changer = state_changer

    def login(self, entries):
        try:
            if not self.is_logged_in:
                self.selenium_manager = SeleniumManager(username=entries['username'].get(),
                                                        password=entries['password'].get())
                self.is_logged_in = True
            else:
                self.selenium_manager = None
                self.is_logged_in = False
            self.state_changer(self.is_logged_in)
        except TimeoutException as ex:
            self.order_failed('Timeout', 'Error ' + str(ex))

    def report_shift(self, start_date, end_date, elaboration_text, override_data=False):
        try:
            # if not self.selenium_manager.get_shift().time or override_data:
            self.selenium_manager.report_shift(start_date=start_date, end_date=end_date,
                                               elaboration_text=elaboration_text)
        except TimeoutException as ex:
            self.order_failed('Timeout', 'Error ' + str(ex))

    def enter_special_occasion(self, reason, start_date, hours, minutes, elaboration_text, override_data=False):
        try:
            # if not self.selenium_manager.get_shift().time or override_data:
            self.selenium_manager.enter_special_occasion(special_occasion=reason, date=start_date, hours=hours,
                                                         minutes=minutes, elaboration_text=elaboration_text)
        except TimeoutException as ex:
            self.order_failed('Timeout', 'Error ' + str(ex))

    def get_last_salary(self):
        last_salary = 0
        PER_HOUR = 40
        try:
            start_date = datetime.today().date()
            if start_date.day < 21:
                start_date = start_date.replace(month=start_date.month - 1)
            start_date = start_date.replace(day=21)
            end_date = start_date.replace(month=start_date.month + 1)
            for day in range(int((end_date - start_date).days)):  # Won't include last day so it would be 20->21
                day = start_date + timedelta(day)
                hours, minutes = self.selenium_manager.get_shift()
                if hours >= 8:
                    time = (((hours - 8) + (minutes / 60)) * 1.25) + 8
                else:
                    time = hours + (minutes / 60)
                last_salary = last_salary + (time * PER_HOUR)
            end_date = end_date.replace(day=end_date.day - 1)
            salary_message = 'Your salary from ', start_date, " until ", end_date, " was: ", last_salary
            showinfo("Last Salary", salary_message)
        except TimeoutException as ex:
            self.order_failed('Timeout', 'Error ' + str(ex))

    def order_failed(self, title, exception_string):
        self.is_logged_in = False
        self.state_changer(self.is_logged_in)
        showinfo(title, exception_string)


if __name__ == '__main__':
    pass
