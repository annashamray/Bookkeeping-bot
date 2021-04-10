from telebot import TeleBot, types

from src.settings import BOT_TOKEN
from src.sheets import sheets

bot = TeleBot(BOT_TOKEN)


def create_markup_with_buttons(iterable, row_width=3):
    markup = types.ReplyKeyboardMarkup(row_width=row_width)
    buttons = [types.KeyboardButton(group) for group in iterable]
    button_groups = (
        buttons[pos : pos + row_width] for pos in range(0, len(buttons), row_width)
    )
    for buton_group in button_groups:
        markup.add(*buton_group)
    return markup


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(message.chat.id, "This is the expanse tracking bot")


@bot.message_handler(regexp=".* *[0-9]+\,?[0-9]*")
def input_expense(message):
    try:
        name, value = message.text.rsplit(" ", 1)
    except ValueError:
        bot.send_message(message.chat.id, "input must be formatted like: <name> <sum>")
        return

    groups = sheets.get_expense_groups()
    markup = create_markup_with_buttons(list(groups.keys()))
    msg = bot.send_message(
        message.chat.id, "Choose the expense group", reply_markup=markup
    )
    bot.register_next_step_handler(msg, process_group_step, name, value)


def process_group_step(message, name, value):
    group = message.text
    groups = sheets.get_expense_groups()
    subgroups = groups[group]

    if not subgroups:
        sheets.add_expense(name, value, group, group)
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Done", reply_markup=markup)

    else:
        markup = create_markup_with_buttons(subgroups)
        msg = bot.send_message(
            message.chat.id, "Choose the expense subgroup", reply_markup=markup
        )
        bot.register_next_step_handler(msg, process_subgroup_step, name, value, group)


def process_subgroup_step(message, name, value, group):
    sheets.add_expense(name, value, group, message.text)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Done", reply_markup=markup)
