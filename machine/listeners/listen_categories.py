from machine.send_message import send_message
from typing import TYPE_CHECKING
from machine.states_enum import States
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

def listen_categories(sm: "StateMachine"):
    if sm.text.lower() == "orden":
        sm.change_state(States.ORDER, True)
        sm.execute_action()
    else:
        send_message(sm.number, f"mostrando categoria {sm.text}", sm.wam_id, sm.whatsapp_token)
        sm.change_state(States.ITEMS, True)
        sm.execute_action()