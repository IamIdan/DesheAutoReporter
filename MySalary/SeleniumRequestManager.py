from datetime import datetime
import CssSelectors as cs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


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
            raise TimeoutException("Timeout. Check your credentials or your internet connection.")

    def report_shift(self, start_date: datetime, end_date: datetime):
        """
        Report a shift into a logged in Deshe session.
        :param start_date: Datetime object
        :param end_date: Datetime object
        :return:
        """
        # Due to the Deshe system, cannot report shifts on a couple of days.
        if start_date.month != end_date.month or start_date.day != end_date.day:
            raise ValueError("Cannot report shifts on multiple days")

        # start_date and end_date should be in the same date.
        self.navigate_to_month(start_date.month, start_date.year)
        # from now on we are working inside the report frame.
        self.enter_add_report_frames()
        self.navigate_to_day(start_date.day)
        self.enter_start_hours(start_date)
        self.enter_end_hours(end_date)
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
        cur_month = self.get_current_month()
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
                raise ValueError(f'Cannot go to {month}/{year} (mm/yy) as it seems to be blocked. please check your are not trying to access months in the future.')

            current_date = datetime(self.get_current_year(), self.get_current_month(), 1)

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
        hour = start_date.strftime('%H')
        minutes = start_date.strftime('%M')
        hours_input_element = self.driver.find_element_by_css_selector(cs.START_HOURS_INPUT)
        minutes_input_element = self.driver.find_element_by_css_selector(cs.START_MINUTES_INPUT)
        self.enter_text_into_input_field(hours_input_element, hour)
        self.enter_text_into_input_field(minutes_input_element, minutes)

    def enter_end_hours(self, end_date: datetime):
        """
        Will enter the start hour into the relevant fields.
        :param start_date:
        :return:
        """
        hour = end_date.strftime('%H')
        minutes = end_date.strftime('%M')
        hours_input_element = self.driver.find_element_by_css_selector(cs.END_HOURS_INPUT)
        minutes_input_element = self.driver.find_element_by_css_selector(cs.END_MINUTES_INPUT)
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


if __name__ == '__main__':
    pass
