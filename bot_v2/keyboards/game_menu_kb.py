from vkwave.bots import Keyboard, ButtonColor


GAME_MENU_KB = Keyboard()
GAME_MENU_KB.add_text_button(text="Начать раунд", payload={"command": "next_round"}, color=ButtonColor.POSITIVE)
GAME_MENU_KB.add_row()
GAME_MENU_KB.add_text_button(text="Результаты", payload={"command": "game_results"}, color=ButtonColor.SECONDARY)
GAME_MENU_KB.add_row()
GAME_MENU_KB.add_text_button(text="Закончить", payload={"command": "end"}, color=ButtonColor.NEGATIVE)
