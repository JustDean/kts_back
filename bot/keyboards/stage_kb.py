from random import shuffle
from vkwave.bots import Keyboard, ButtonColor


def get_stage_kb(stage_info, fin):
    if fin:
        payload = {"command": "finish"}
    else:
        payload = {"command": "next_stage"}

    shuffled = [stage_info.answer_1, stage_info.answer_2, stage_info.answer_3, stage_info.correct_answer]
    shuffle(shuffled)

    STAGE_KB = Keyboard()
    STAGE_KB.add_text_button(text=shuffled[0], payload=payload,
                             color=ButtonColor.PRIMARY)

    STAGE_KB.add_row()
    STAGE_KB.add_text_button(text=shuffled[1], payload=payload,
                             color=ButtonColor.PRIMARY)

    STAGE_KB.add_row()
    STAGE_KB.add_text_button(text=shuffled[2], payload=payload,
                             color=ButtonColor.PRIMARY)

    STAGE_KB.add_row()
    STAGE_KB.add_text_button(text=shuffled[3], payload=payload,
                             color=ButtonColor.PRIMARY)

    STAGE_KB.add_row()
    STAGE_KB.add_text_button(text="Закончить", payload={"command": "finish"},
                             color=ButtonColor.NEGATIVE)

    return STAGE_KB
