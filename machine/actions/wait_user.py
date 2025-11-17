from machine.send_message import send_message
from typing import TYPE_CHECKING
from machine.states_enum import States
if TYPE_CHECKING:
    from machine.state_machine import StateMachine


PLACEHOLDER = "Esperando"
def wait_user(sm: "StateMachine"):
    send_message(sm.number, PLACEHOLDER, sm.wam_id, sm.whatsapp_token)
    