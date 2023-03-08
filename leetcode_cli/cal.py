
import calendar
import datetime

# Get the date 365 days ago from today
today = datetime.date.today()
one_year_ago = today - datetime.timedelta(days=365)

# Create a TextCalendar object
cal = calendar.TextCalendar()

# Loop through each day of the past year and print the calendar for each month in groups of 4 per row
for year in range(one_year_ago.year, today.year+1):
    for month in range(1, 13, 4):
        if year == one_year_ago.year and month < one_year_ago.month:
            continue
        if year == today.year and month > today.month:
            continue
        month_calendars = []
        for i in range(4):
            if month + i <= 12:
                month_calendars.append(cal.formatmonth(year, month+i))
        print('\n'.join([month_calendars[i] + ' ' * 5 for i in range(len(month_calendars))]))
    print('\n')
