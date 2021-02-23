from vkwave.bots import Keyboard, ButtonColor


ROUND_KB = Keyboard()
ROUND_KB.add_text_button(text="Ответить", payload={"command": "answer"}, color=ButtonColor.POSITIVE)
