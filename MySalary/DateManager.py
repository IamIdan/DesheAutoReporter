from datetime import datetime

from ExcelAnalyzer import ExcelAnalyzer


class DateManager:
    def __init__(self, path_to_excel):
        self.excel_analyzer = ExcelAnalyzer(path_to_excel)

    @staticmethod
    def convert_hours_and_minutes_to_int(time):
        time = time.split(':')
        hours = int(time[0])
        minutes = int(time[1])
        return hours * 60 + minutes

    def get_day(self):
        date = self.excel_analyzer.get_date()
        elaboration_text = self.excel_analyzer.get_comments()
        if not elaboration_text.strip():
            elaboration_text = None
        start_time = self.excel_analyzer.get_start_time()
        if not start_time.strip():
            start_time = None
        end_time = self.excel_analyzer.get_end_time()
        if not end_time.strip():
            end_time = None
        while self.excel_analyzer.same_date_next_line():
            self.excel_analyzer.go_next_line()
            new_start_time = self.excel_analyzer.get_start_time()
            if new_start_time.strip() and start_time:
                if self.convert_hours_and_minutes_to_int(new_start_time) < self.convert_hours_and_minutes_to_int(
                        start_time):
                    start_time = new_start_time
            elif not start_time:
                start_time = new_start_time

            new_end_time = self.excel_analyzer.get_end_time()
            if new_end_time.strip() and end_time:
                if self.convert_hours_and_minutes_to_int(new_end_time) > self.convert_hours_and_minutes_to_int(
                        end_time):
                    end_time = new_end_time
            elif not start_time:
                end_time = new_start_time
        year, month, day = date.split(' ')[0].split('/')
        what_day = self.excel_analyzer.what_day()
        hour, minute = start_time.split(':')
        start_time_datetime = datetime(int(year), int(month), int(day), int(hour), int(minute))
        hour, minute = end_time.split(':')
        end_time_datetime = datetime(int(year), int(month), int(day), int(hour), int(minute))
        if what_day != 'work':
            if not start_time and not end_time:
                return {'dead': True, 'reason': what_day, 'date': self.excel_analyzer.current_date,
                        'elaboration_text': elaboration_text}
            elif not start_time:
                return {'dead': True, 'reason': what_day, 'end_date': end_time_datetime, 'elaboration_text': elaboration_text}
            elif not end_time:
                return {'dead': True, 'reason': what_day, 'start_date': start_time_datetime, 'elaboration_text': elaboration_text}
        else:
            if not start_time and not end_time:
                return {'dead': True, 'reason': what_day, 'date': self.excel_analyzer.current_date,
                        'elaboration_text': elaboration_text}
            elif not start_time:
                return {'dead': True, 'end_date': end_time_datetime, 'elaboration_text': elaboration_text}
            elif not end_time:
                return {'dead': True, 'start_date': start_time_datetime, 'elaboration_text': elaboration_text}
        if what_day != 'work':
            time_left = self.convert_hours_and_minutes_to_int(end_time) - self.convert_hours_and_minutes_to_int(
                start_time)
            hours = int(time_left / 60)
            minutes = int(time_left % 60)
            return {'reason': what_day, 'date': start_time_datetime, 'hour': hours, 'minute': minutes,
                    'elaboration_text': elaboration_text}
        return {'start_date': start_time_datetime, 'end_date': end_time_datetime, 'elaboration_text': elaboration_text}

    def get_all_days(self):
        days = list()
        days.append(self.get_day())
        while self.excel_analyzer.next_day_exists():
            self.excel_analyzer.go_next_line()
            days.append(self.get_day())
        return days


if __name__ == '__main__':
    pass
