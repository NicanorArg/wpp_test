from machine.send_message import send_message
from typing import TYPE_CHECKING
from machine.states_enum import States
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

PLACEHOLDER = "ORDEN PEDIDA"
PLACEHOLDER_1 = "VOLVIENDO AL MENU"
PLACEHOLDER_2 = "No te entendi, responder si o no"
def listen_order(sm: "StateMachine"):
    text = sm.text.lower()
    if text == "si":
        send_message(sm.number, PLACEHOLDER, sm.wam_id, sm.whatsapp_token)
        sm.change_state(States.ROUTE, True)
        sm.execute_action()
    elif text == "no":
        send_message(sm.number, PLACEHOLDER_1, sm.wam_id, sm.whatsapp_token)
        sm.change_state(States.CATEGORIES, True)
        sm.execute_action()
    else:
        send_message(sm.number, PLACEHOLDER_2, sm.wam_id, sm.whatsapp_token)
        sm.change_state(States.LISTEN_ORDER, True)
        