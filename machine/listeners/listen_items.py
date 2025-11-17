from machine.send_message import send_message
from typing import TYPE_CHECKING
from machine.states_enum import States
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

def listen_items(sm: "StateMachine"):
    send_message(sm.number, f"mostrando item {sm.text}", sm.wam_id, sm.whatsapp_token)
    sm.change_state(States.ITEM, True)
    sm.execute_action()