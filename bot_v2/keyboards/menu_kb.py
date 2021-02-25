from vkwave.bots import Keyboard, ButtonColor


MENU_KB = Keyboard()
MENU_KB.add_text_button(text="Начать", payload={"command": "game_menu"}, color=ButtonColor.POSITIVE)
MENU_KB.add_row()
MENU_KB.add_text_button(text="Инструкция", payload={"command": "help"}, color=ButtonColor.PRIMARY)
MENU_KB.add_row()
MENU_KB.add_text_button(text="Прошлая игра", payload={"command": "previous_game"}, color=ButtonColor.SECONDARY)
