from datetime import datetime, timedelta

from config import timetable
from sheets_parser import parse


def col_to_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


def get_lessons(day):
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
    if day in days:
        if day != 'среда':
            response_text = 'Расписание уроков на день: ' + days[days.index(day)] + '\n\n' + timetable[days.index(day)]
            return response_text
        else:
            sheet_days = parse('17srZM8Y2ZH02ASGfC7J-yYRND2Iyztv7uxs9_NQiBgM', '\'2019-2020 у.г.\'!1:1')[0]
            sheet_days = list(filter(None, sheet_days))
            closest_wednesday = datetime.today()
            while closest_wednesday.weekday() != 2:
                closest_wednesday += timedelta(days=1)
            day_index = 'C'
            closest_wednesday = datetime.strftime(closest_wednesday, '%d.%m')
            day_found = 0
            for num, sheet_day in enumerate(sheet_days):
                if closest_wednesday in sheet_day:
                    day_index = col_to_string(num + 3)
                    day_found = 1
                    break
            if day_found:
                day_lessons = parse('17srZM8Y2ZH02ASGfC7J-yYRND2Iyztv7uxs9_NQiBgM',
                                    '\'2019-2020 у.г.\'!' + day_index + '59:' + day_index + '64')
                response_text = 'Расписание уроков на день: ' + days[days.index(day)] + '\n\n'
                for day_lesson in day_lessons:
                    response_text += str(day_lesson[0]) + '\n'

                return response_text
            else:
                return 'Нужного дня ещё нет в расписании.'
    else:
        return 'На этот день расписания нет.'
