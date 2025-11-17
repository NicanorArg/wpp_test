from machine.send_message import send_message
from machine.states_enum import States
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

MESSAGE_PLACEHOLDER = "Elija un item:\n\t" \
                                "1-test\n\t" \
                                "2-test\n\t" \
                                "3-test\n\t" \
                                "4-test\n\t" \
                                "5-test\n\t"

def show_items(sm: "StateMachine"):
    send_message(sm.number, MESSAGE_PLACEHOLDER, sm.wam_id, sm.whatsapp_token)
    sm.change_state(States.LISTEN_ITEMS, True)