from aiogram.dispatcher.filters.state import StatesGroup, State


class Ban_Unban_state(StatesGroup):
    waiting_for_ban_id = State()
    waiting_for_unban_id = State()


class BalanceChange(StatesGroup):
    waiting_user = State()
    waiting_amount = State()

class BalanceRefill(StatesGroup):
    waiting_amount = State()