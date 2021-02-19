from vkwave.bots import Keyboard, ButtonColor


ROUND_KB = Keyboard(one_time=True)
ROUND_KB.add_text_button(text="Ответить", payload={"command": "answer"}, color=ButtonColor.POSITIVE)
