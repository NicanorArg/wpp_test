from machine.send_message import send_message
from typing import TYPE_CHECKING
from machine.states_enum import States
if TYPE_CHECKING:
    from machine.state_machine import StateMachine

# cargar llm
from machine.micro_llm.get_intent import get_intent
from machine.send_message import send_message

import pickle
import os

path = "machine/micro_llm"

vectorizer_filename = os.path.join(path, "intent_vectorizer.pkl")
with open(vectorizer_filename, 'rb') as f:
    vectorizer = pickle.load(f)
    
classifier_filename = os.path.join(path, "intent_classifier.pkl")
with open(classifier_filename, 'rb') as f:
    clf = pickle.load(f)


def listen_route(sm: "StateMachine"):
    intent = get_intent(sm.text, vectorizer, clf)

    match intent:
        case "pedido":
            send_message(sm.number, "pedido: volviendo al menu", sm.wam_id, sm.whatsapp_token)
            sm.change_state(States.CATEGORIES, True)
            sm.execute_action()

        case "queja":
            send_message(sm.number, "queja: por ahora la conversacion termina aca", sm.wam_id, sm.whatsapp_token)

        case "cuenta": 
            send_message(sm.number, "cuenta: se le entregara la cuenta", sm.wam_id, sm.whatsapp_token)
            