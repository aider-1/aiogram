import calendar
from app.database.requests import tz_name
from pytz import timezone
from datetime import datetime

DATE_WEEK = ["Пн", "Вт", "Ср", "Чт", "Пт",]

MONTHS = {
    "01": "Январь",
    "02": "Февраль",
    "03": "Март",
    "04": "Апрель",
    "05": "Май",
    "06": "Июнь",
    "07": "Июль",
    "08": "Август",
    "09": "Сентябрь",
    "10": "Октябрь",
    "11": "Ноябрь",
    "12": "Декабрь",
}

# async def gen(*, year):
#     tz = timezone(tz_name)
#     tod = datetime.now(tz=tz).date()
#     res = list()
#     if tod.year != year:
#         for month in range(1, 13):
#             cal = calendar.Calendar(0).itermonthdates(year, month)
            
#             for date in cal:
#                 if date.month == month:
                    