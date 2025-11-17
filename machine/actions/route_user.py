from machine.send_message import send_message
from machine.states_enum import States
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

def route_user(sm: "StateMachine"):
    PLACEHOLDER = "Desea volver a ver el menu y pedir algo mas, la cuenta, o hablar con una persona real del restaurante?"
    send_message(sm.number, PLACEHOLDER, sm.wam_id, sm.whatsapp_token)
    sm.change_state(States.LISTEN_ROUTE, True)