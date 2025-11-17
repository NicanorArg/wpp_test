from machine.send_message import send_message
from machine.states_enum import States
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

WELCOME_MESSAGE = "Hola, bienvenido a *restaurante*. Soy mesero.me, tu mesero virtual."
WELCOME_MESSAGE_1 = "Te voy a guiar en el proceso de hacer tu pedido"
    
def welcome_user(sm:"StateMachine"):
    send_message(sm.number, WELCOME_MESSAGE, sm.wam_id, sm.whatsapp_token)
    send_message(sm.number, WELCOME_MESSAGE_1, sm.wam_id, sm.whatsapp_token)
    sm.change_state(States.CATEGORIES)
    sm.execute_action()