CURRENT_YEAR = '#Header1_MonthAndYearBrowser1_spnYear'  # last 2 numbers. (for example 19)
CURRENT_MONTH = '#Header1_MonthAndYearBrowser1_spnMonth'  # as hebrew text (נובמבר)
PREVIOUS_MONTH = '#Header1_MonthAndYearBrowser1_imgbtnPrevMonth'
NEXT_MONTH = '#Header1_MonthAndYearBrowser1_imgbtnNextMonth'
ADD_REPORT_TABLE = 'table td[valign=top] > table:not(.main_grid)'  # for easy selection of children inside it
REPORT_HOURS_FRAME = '#mainFrameSet'

# select best practice: https://stackoverflow.com/a/28613320/7320123
DROPDOWN_CUSTOMER = 'select[name="ddlCustomers"]'
DROPDOWN_PROJECT = 'select[name="ddlProjects"]'
DROPDOWN_TASK = 'select[name="ddlTasks"]'

TEXT_ELABORATION = 'textarea[name=txtElaboration]'  # פירוט
OPTIONAL_DAYS = 'td.calDay'  # returns all the possible days to select in the moths, without the selected day.
SELECTED_DAY = '#tdSelectedDay'

START_HOURS_INPUT = '#txtFromHours'
START_MINUTES_INPUT = '#txtFromMinutes'
END_HOURS_INPUT = '#txtToHours'
END_MINUTES_INPUT = '#txtToMinutes'

SAVE_HOURS_REPORT = 'input[name=btnSaveNew]'
