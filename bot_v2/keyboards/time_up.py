from vkwave.bots import Keyboard, ButtonColor


TIME = Keyboard()
TIME.add_text_button(text=":(", payload={"command": "time_up"}, color=ButtonColor.NEGATIVE)
