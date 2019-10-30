import CssSelectors as cs
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class SeleniumManager:
    def __init__(self, username, password, headless=True):
        self.driver = self.init_chrome_webdrive(headless)
        self.login(username, password)

    @staticmethod
    def init_chrome_webdrive(headless=True):
        """
        Initializing chrome webdriver.
        :param headless: if set to true, the chrome tab will not open up.
        :return driver:
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        return webdriver.Chrome(chrome_options=options)

    def login(self, username, password):
        """
        Log into the Deshe page, using basic-auth.
        :param username:
        :param password:
        :return:
        """
        try:
            self.driver.set_page_load_timeout(10)
            self.driver.get(f'https://{username}:{password}@deshe.matrix.co.il/')
        except TimeoutException:
            self.driver.close()
            raise TimeoutException("Timeout. Check your credentials or your internet connection")

    def report_shift(self, start_date: datetime, end_date: datetime, elaboration_text=None):
        """
        Report a shift into a logged in Deshe session.
        :param start_date: Datetime object
        :param end_date: Datetime object
        :param elaboration_text: string, elaboration text to be added.
        :return:
        """
        # Due to the Deshe system, cannot report shifts on a couple of days.
        if start_date.month != end_date.month or start_date.day != end_date.day:
            raise ValueError("Cannot report shifts on multiple days")

        # start_date and end_date should be in the same date.
        self.navigate_to_month(start_date.month, start_date.year)
        # from now on we are working inside the report frame.
        self.enter_add_report_frames()

        # check that month is not locked (we may report in that month)
        if not self.can_report_in_current_month():
            raise ValueError(f'Cannot report hours in this month {start_date.month}')

        self.choose_customer()

        # report elaboration_text
        if elaboration_text:
            self.enter_elaboration_text(elaboration_text)

        self.navigate_to_day(start_date.day)
        self.enter_start_hours(start_date)
        self.enter_end_hours(end_date)

        # self.save_hour_report()
        self.exit_add_report_frames()

    def enter_special_occasion(self, special_occasion: str, date: datetime, hours: int, minutes: int,
                               elaboration_text=None):
        """
        Report a special occasion, such as a holiday or disease.
        :param special_occasion: 'holiday' or 'disease'
        :param date: datetime obejct, representing the date the occasion happened at.
        :param hours: number representing the number of hours to report
        :param minutes: number representing the numer of minutes to report.
        :param elaboration_text: text which will be added in the פירוט section of the deshe hours report.
        :return:
        """
        self.navigate_to_month(date.month, date.year)
        # from now on we are working inside the report frame.
        self.enter_add_report_frames()

        # check that month is not locked (we may report in that month)
        if not self.can_report_in_current_month():
            raise ValueError(f'Cannot report hours in this month {date.month}')

        self.choose_customer(special_occasion=True)
        special_occasions = {
            'holiday': self.report_holiday,
            'disease': self.report_disease,
        }
        # run the relevant function
        special_occasions[special_occasion]()

        # report elaboration_text
        if elaboration_text:
            self.enter_elaboration_text(elaboration_text)

        self.navigate_to_day(date.day)
        self.enter_hours(hours, minutes)
        self.save_hour_report()
        self.exit_add_report_frames()

    def navigate_to_month(self, month, year):
        """
        Navigating the Deshe page to the requested month.
        :param month: the desired month, as a number.
        :param year: number representing the last 2 digits of the dedired year (2019 will be represented as 19)
        :return:
        """
        cur_year = self.get_current_year()
        current_date = datetime(cur_year, self.get_current_month(), 1)
        dest_date = datetime(year, month, 1)
        while current_date != dest_date:
            # find button to click on: (prev or next year)
            if current_date < dest_date:
                # month is ahead, click on month forward.
                button_selector = cs.NEXT_MONTH
            else:
                # month is before, go back in month timeline.
                button_selector = cs.PREVIOUS_MONTH

            # click on the selected button. if possible.
            button_to_click = self.driver.find_element_by_css_selector(button_selector)
            if button_to_click.is_enabled():
                button_to_click.click()
            else:
                raise ValueError(
                    f'Cannot go to {month}/{year} (mm/yy) as it seems to be blocked. please check your are not trying to access months in the future.')

            current_date = datetime(self.get_current_year(), self.get_current_month(), 1)
        print(len(self.driver.find_elements_by_css_selector(cs.SELECTED_DAY)))

    def get_current_month(self):
        """
        Get the current displayed month, in numbers.
        :return: number representing the current month
        """
        current_month = self.driver.find_element_by_css_selector(cs.CURRENT_MONTH).text
        months_to_numbers = {
            'ינואר': 1,
            'פבואר': 2,
            'מרץ': 3,
            'אפריל': 4,
            'מאי': 5,
            'יוני': 6,
            'יולי': 7,
            'אוגוסט': 8,
            'ספטמבר': 9,
            'אוקטובר': 10,
            'נובמבר': 11,
            'דצמבר': 12,
        }
        return months_to_numbers[current_month]

    def get_current_year(self):
        """
        Return the current year in the Deshe system.
        :return: number representing the current year.
        """
        return 2000 + int(self.driver.find_element_by_css_selector(cs.CURRENT_YEAR).text)

    def navigate_to_day(self, day):
        """
        Once the page is navigated to the currect month, use this function to choose the current day in the month.
        :param day: number representing the day num in the month
        :return:
        """
        # check requested day is NOT the selected day
        selected_day = self.driver.find_element_by_css_selector(cs.SELECTED_DAY).text
        if selected_day != str(day):
            # change to requested day
            # using an ugly xpath selector here since matching by text is not available at css selector level.
            xpath_day_selector = f'//td[@class="calDay"][text()={day}]'
            self.driver.find_element_by_xpath(xpath_day_selector).click()

    def enter_add_report_frames(self):
        """
        Since the Deshe site is built like so:
        ...
        <iframe>
            ...
            <frameset>
                <frame id="frmHoursReportsDataEntry"> </frame>
                ...
            </frameset>
        </iframe>
        we will need to access those frames in order to get to their content.
        :return:
        """
        # because we are working inside two frames, first we will need to change the frame context to inside those frames.
        frame = self.driver.find_element_by_css_selector('#frmMainHoursReportsManagement')
        self.driver.switch_to.frame(frame)
        sec_frame = self.driver.find_element_by_css_selector('#frmHoursReportsDataEntry')
        self.driver.switch_to.frame(sec_frame)

    def exit_add_report_frames(self):
        # this is done twice since we are exiting 2 frames.
        self.driver.switch_to.default_content()
        self.driver.switch_to.default_content()

    def enter_start_hours(self, start_date: datetime):
        """
        Will enter the start hour into the relevant fields.
        :param start_date:
        :return:
        """
        self.fill_hours_field(cs.START_MINUTES_INPUT, cs.START_HOURS_INPUT, start_date)

    def enter_end_hours(self, end_date: datetime):
        """
        Will enter the start hour into the relevant fields.
        :param start_date:
        :return:
        """
        self.fill_hours_field(cs.END_MINUTES_INPUT, cs.END_HOURS_INPUT, end_date)

    def enter_hours(self, hours: int, minutes: int):
        """
        When in special occasion you have only the hours field.
        Reporting into that field.
        :param hours:
        :param minutes:
        :return:
        """
        date = datetime(1990, 1, 1, hours, minutes)
        self.fill_hours_field(cs.MINUTES_INPUT, cs.HOURS_INPUT, date)

    def fill_hours_field(self, minutes_css: str, hours_css: str, date: datetime):
        """
        Filling an hour field.
        :param minutes_css: minutes element cs selector.
        :param hours_css: hours element cs selector.
        :param date: date with the hour to report.
        :return:
        """
        hour = date.strftime('%H')
        minutes = date.strftime('%M')
        hours_input_element = self.driver.find_element_by_css_selector(hours_css)
        minutes_input_element = self.driver.find_element_by_css_selector(minutes_css)
        self.enter_text_into_input_field(hours_input_element, hour)
        self.enter_text_into_input_field(minutes_input_element, minutes)

    def enter_text_into_input_field(self, element, text):
        """
        First clearing the element text, then entering it.
        :param element: WebDriver element
        :param text: string
        :return:
        """
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)

    def save_hour_report(self):
        self.driver.find_element_by_css_selector(cs.SAVE_HOURS_REPORT).click()

    def can_report_in_current_month(self):
        """
        Once a month is over, you may no longer report for it.
        Checks if we can report for the current month, returns boolean to check if possible or not
        :return:
        """
        # if selectedDay is available then oyu may report, else the report table does exists but is invisible.
        return len(self.driver.find_elements_by_css_selector(cs.SELECTED_DAY)) >= 1

    def enter_elaboration_text(self, elaboration_text: str):
        """
        Adding elaboration (פירוט) text field.
        :param elaboration_text: string
        :return:
        """
        elaboration_text_field = self.driver.find_element_by_css_selector(cs.TEXT_ELABORATION)
        elaboration_text_field.send_keys(elaboration_text)

    def choose_customer(self, special_occasion=False):
        """
        Choosing a customer. In case of special report (holiday, deceases, ... ) choose העדרויות שונות
        else choosing אינפיניטי לבס  ארץ אנד די בע"מ
        :return:
        """
        if special_occasion:
            self.choose_select_element(cs.DROPDOWN_CUSTOMER, 'העדרויות שונות')
        else:
            self.choose_select_element(cs.DROPDOWN_CUSTOMER, 'אינפיניטי לאבס אר. אנד. די בע"מ')

    def choose_select_element(self, css_selector, visible_text):
        """
        Choosing a select element in the site.
        :param css_selector: the element css selector
        :param visible_text: the text represnting the select we want to choose
        :return: Null or error in case task is not avilable
        """
        select = Select(self.driver.find_element_by_css_selector(css_selector))
        select.select_by_visible_text(visible_text)

    def report_holiday(self):
        """
        Choosing a holiday for the report
        :return:
        """
        self.choose_select_element(cs.DROPDOWN_PROJECT, 'חופשה')

    def report_disease(self):
        self.choose_select_element(cs.DROPDOWN_PROJECT, 'מחלה')
        self.choose_select_element(cs.DROPDOWN_TASK, 'מחלת עובד')


if __name__ == '__main__':
    pass