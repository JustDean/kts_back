from vkwave.bots import Keyboard, ButtonColor


WELCOME_KB = Keyboard()
WELCOME_KB.add_text_button(text="Начать", payload={"command": "start"}, color=ButtonColor.POSITIVE)
WELCOME_KB.add_row()
WELCOME_KB.add_text_button(text="Помощь", payload={"command": "help"}, color=ButtonColor.SECONDARY)
