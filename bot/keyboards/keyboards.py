from aiogram import types


class KeyboardManager:
    @staticmethod
    def admin_start_inline():
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(types.InlineKeyboardButton('ℹ️File with all log', callback_data=f'all_log'))
        kb.insert(types.InlineKeyboardButton('💣File with errors ', callback_data=f'err_log'))
        kb.insert(types.InlineKeyboardButton('🔄Get Users', callback_data=f'get_users'))
        kb.insert(types.InlineKeyboardButton('‼️️Black List', callback_data=f'Black_List'))
        return kb

    @staticmethod
    def start_inline():
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton('💰Пополнить баланс💰', callback_data='refill_balance'))
        return kb
