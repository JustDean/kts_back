from vkwave.bots import Keyboard, ButtonColor


AGREED_KB = Keyboard(one_time=True)
AGREED_KB.add_text_button(text="Понял!", color=ButtonColor.POSITIVE)