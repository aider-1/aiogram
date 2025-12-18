from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..database.models import Date
from ..database.requests import get_contractors, get_contractors_count, get_contractors_page, get_dates_by_year_month, is_year, get_date_with_noload, get_available_contractors_for_date_count, get_available_contractors_for_date_page
from ..database.models import Contractor, Date
from pytz import timezone
from datetime import datetime
import calendar
from app.utils.generate import MONTHS, DATE_WEEK
from app.utils.config import tz_name as tz_str

tz = timezone(tz_str)

def start_menu():
    buttons = [
        [InlineKeyboardButton(text="👥 Контрагенты", callback_data="list_contractors"), InlineKeyboardButton(text="📅 Календарь", callback_data="calendar_years")],
        # [],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="faq")],
        [InlineKeyboardButton(text="Журнал сообщений", callback_data="logs")]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def contractor_list_buttons(page: int = 0):
    PER_PAGE = 30
    total = await get_contractors_count()
    pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = max(0, min(page, pages - 1))
    items = await get_contractors_page(limit=PER_PAGE, offset=page * PER_PAGE)

    b = InlineKeyboardBuilder()
    for c in items:
        b.button(text=c.name, callback_data=f"cont_{c.id}")
    b.adjust(2)

    # пагинация
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"contpage:{page-1}"))
        nav.append(InlineKeyboardButton(text=f"{page+1}/{pages}", callback_data="noop"))
    if page < pages-1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"contpage:{page+1}"))
    if nav:
        b.row(*nav, width=len(nav))
    
    b.row(
        InlineKeyboardButton(
            text="◀️ Назад", callback_data="back_start"
        ),
        InlineKeyboardButton(
            text="➕👤Создать контрагента", callback_data="create_contractor"
        ), width=2
    )
    
    return b.as_markup()

def contractor_buttons(contractor_id: int):
    buttons = [
        [
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f'del_{contractor_id}'),
            InlineKeyboardButton(text="◀️ Назад", callback_data=f'list_contractors')
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def date_buttons(date: Date):
    builder = InlineKeyboardBuilder()
    contractors = date.contractors
    if contractors:
        for cont in contractors:
            builder.row(
                InlineKeyboardButton(
                    text=cont.name,
                    callback_data=f'cl_{date.id}_{cont.id}' #добавить функционал для date-contractor
                )
            )
    
    s_year = date.date.isoformat().split('-')[0]
    s_month = date.date.isoformat().split("-")[1]
    
    builder.row(
        InlineKeyboardButton(
            text='📝 Добавить',
            callback_data=f'from_{date.id}'
        ),
        InlineKeyboardButton(
            text="◀️ Назад", callback_data=f"mth_{s_year}_{s_month}"
        ),
        InlineKeyboardButton(
            text="🗑️ Удалить дату", callback_data=f"deldate_{date.id}_{s_year}_{s_month}"
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()

async def add_contractor_by_date_buttons(date_id: int, page=0):
    PER_PAGE = 30
    total = await get_available_contractors_for_date_count(date_id=date_id)
    pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    page = max(0, min(page, pages - 1))
    items = await get_available_contractors_for_date_page(date_id=date_id, limit=PER_PAGE, offset=page * PER_PAGE)

    b = InlineKeyboardBuilder()
    for c in items:
        b.button(text=c.name, callback_data=f'add_{date_id}_{c.id}')
    b.adjust(2)

    # пагинация
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"addpage:{date_id}:{page-1}"))
        nav.append(InlineKeyboardButton(text=f"{page+1}/{pages}", callback_data="noop"))
    if page < pages-1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"addpage:{date_id}:{page+1}"))
    if nav:
        b.row(*nav, width=len(nav)) 

    b.row(
        InlineKeyboardButton(
            text="◀️ Назад", callback_data=f'dtid_{date_id}'
        )
    )

    return b.as_markup()

def show_years():
    this_year = datetime.now(tz=tz).year
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=str(this_year),
            callback_data=f"yr_{this_year}"
        ),
        InlineKeyboardButton(
            text=str(this_year+1),
            callback_data=f"yr_{this_year+1}"
        ),
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="back_start"
        )
    )
    
    
    builder.adjust(2)
    return builder.as_markup()

def show_months(*, year):
    builder = InlineKeyboardBuilder()
    tod = datetime.now(tz=tz).date()
    
    for key, value in MONTHS.items():
        if int(key) < tod.month and tod.year == year:
            continue
        builder.row(
            InlineKeyboardButton(
                text=value,
                callback_data=f"mth_{year}_{key}"
            )
        )
    
    builder.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data="calendar_years"
        )
    )
    
    builder.adjust(4)
    return builder.as_markup()
#✅
async def show_dates(*, month: str, year: str):
    days = calendar.Calendar(0).itermonthdates(year=int(year), month=int(month))
    dates = await get_dates_by_year_month(year=int(year), month=int(month))
    date_map = {d.date: d.id for d in dates}
    
    builder = InlineKeyboardBuilder()
    for day in days:
        if day.month != int(month):
            text = "❌"
            callback = "no_date"
        elif day in date_map:
            text = f"✅{day.day}"
            callback = f"dtid_{date_map[day]}"
        else:
            text = str(day.day)
            callback = f"dt_{day.isoformat()}"
        
        builder.row(
            InlineKeyboardButton(
                text=text,
                callback_data=callback
            )
        )
        
    builder.row(InlineKeyboardButton(text="◀️ Назад", callback_data=f"yr_{year}"))
    
    builder.adjust(7)
    return builder.as_markup()
    
def generate_date_buttons(*, raw_date: str):
    builder = InlineKeyboardBuilder()
    s_year = raw_date.split('-')[0]
    s_month = raw_date.split('-')[1]
    
    builder.row(
        InlineKeyboardButton(
            text="📝 Заполнить дату",
            callback_data=f"create_date_{raw_date}"
        )
    )
    
    builder.row(
        InlineKeyboardButton(
            text="◀️ Назад",
            callback_data=f"mth_{s_year}_{s_month}"
        )
    )
    
    builder.adjust(2)
    return builder.as_markup()
    