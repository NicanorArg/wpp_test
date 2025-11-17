from machine.send_message import send_message
from typing import TYPE_CHECKING
from machine.states_enum import States
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

PLACEHOLDER_MESSAGE = "Agregando item a tu orden"
PLACEHOLDER_MESSAGE_1 = "Volviendo al menu, cuando quieras pedir tu orden, escribí 'orden'"

def listen_item(sm: "StateMachine"):
    if sm.text.lower() == "si":
        send_message(sm.number, PLACEHOLDER_MESSAGE, sm.wam_id, sm.whatsapp_token)
    
    send_message(sm.number, PLACEHOLDER_MESSAGE_1, sm.wam_id, sm.whatsapp_token)
    sm.change_state(States.CATEGORIES, True)
    sm.execute_action()