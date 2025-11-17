from machine.send_message import send_message
from typing import TYPE_CHECKING
from machine.states_enum import States
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

def show_item(sm: "StateMachine"):
    send_message(sm.number, "Mostrando item, desea agregarlo a su orden?", sm.wam_id, sm.whatsapp_token)
    sm.change_state(States.LISTEN_ITEM, True)