from aiogram import types


class KeyboardManager:
    @staticmethod
    def admin_start_inline():
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(types.InlineKeyboardButton('ℹ️File with all log', callback_data=f'all_log'))
        kb.insert(types.InlineKeyboardButton('💣File with errors ', callback_data=f'err_log'))
        kb.insert(types.InlineKeyboardButton('🔄Get Users', callback_data=f'get_users'))
        kb.insert(types.InlineKeyboardButton('💸Change Balance', callback_data=f'change_balance'))
        kb.insert(types.InlineKeyboardButton('‼️️Black List', callback_data=f'black_List'))
        return kb

    @staticmethod
    def start_inline():
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(types.InlineKeyboardButton('💰Пополнить баланс💰', callback_data='refill_balance'))
        return kb

    @staticmethod
    def ban_unban_menu():
        kb = types.InlineKeyboardMarkup(row_width=2)
        ban = types.InlineKeyboardButton("⚠️ Ban ⚠️", callback_data='ban_user')
        unban = types.InlineKeyboardButton('❎ Unban ❎', callback_data='unban_user')
        back = types.InlineKeyboardButton('◀️ BACK ◀️', callback_data='black_List_back')
        kb.add(ban, unban, back)
        return kb

    @staticmethod
    def ban_enter():
        kb = types.InlineKeyboardMarkup(row_width=1)
        ban = types.InlineKeyboardButton("👇️ Enter the UserID or Username below to 💥BAN💥 👇",
                                         callback_data='enter_smth_not_cb')
        back = types.InlineKeyboardButton('◀️ BACK ◀️', callback_data='black_List_back')
        kb.add(ban, back)
        return kb

    @staticmethod
    def unban_enter():
        kb = types.InlineKeyboardMarkup(row_width=1)
        uban = types.InlineKeyboardButton("👇️ Enter the UserID or Username below to ❎UNBAN❎ 👇",
                                          callback_data='enter_smth_not_cb')
        back = types.InlineKeyboardButton('◀️ BACK ◀️', callback_data='black_List_back')
        kb.add(uban, back)
        return kb

    @staticmethod
    def balance_userid_enter():
        kb = types.InlineKeyboardMarkup(row_width=1)
        userid = types.InlineKeyboardButton("👇️ Enter Username to 💸change balance💸 👇",
                                            callback_data='enter_smth_not_cb')
        back = types.InlineKeyboardButton('◀️ BACK ◀️', callback_data='black_List_back')
        kb.add(userid, back)
        return kb

    @staticmethod
    def balance_amount_enter(username):
        kb = types.InlineKeyboardMarkup(row_width=1)
        balance = types.InlineKeyboardButton(f"👇️ Enter a new balance for {username} 👇",
                                             callback_data='enter_smth_not_cb')
        back = types.InlineKeyboardButton('◀️ BACK ◀️', callback_data='black_List_back')
        kb.add(balance, back)
        return kb

    @staticmethod
    def waiting_amount_refill():
        kb = kb = types.InlineKeyboardMarkup(row_width=1)
        back = types.InlineKeyboardButton('◀️ BACK ◀️', callback_data='user_back')
        kb.add(back)
        return kb

    @staticmethod
    def pay_wait(payment_url, bill_id):
        kb = kb = types.InlineKeyboardMarkup(row_width=1)
        pay = types.InlineKeyboardButton('Оплатить', url=payment_url)
        update = types.InlineKeyboardButton(text="Проверить оплату", callback_data=f'update-balance_{bill_id}')
        kb.add(pay, update)
        return kb
