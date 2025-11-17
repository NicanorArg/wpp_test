from queue import Queue
import time
from machine.state_machine import StateMachine, States

def process_queue(queue: Queue, sessions: dict, wam_id, whatsapp_token):
    #cargar llm
    # from machine.micro_llm.get_intent import get_intent
    # from machine.send_message import send_message

    # import pickle
    # import os

    # path = "machine/micro_llm"

    # vectorizer_filename = os.path.join(path, "intent_vectorizer.pkl")
    # with open(vectorizer_filename, 'rb') as f:
    #     vectorizer = pickle.load(f)
        
    # classifier_filename = os.path.join(path, "intent_classifier.pkl")
    # with open(classifier_filename, 'rb') as f:
    #     clf = pickle.load(f)


    while True:
        number, text = queue.get()
        if number and text:
            print(f"Procesando mensaje de {number}: {text}")

            # recuperar o crear sesion
            session = sessions.get(number, {"history":[], 
                                            "state": States.WELCOME,}) #default 
            session["last_message"] = text
            session["history"].append(text)

            print("process_queue state: " + session["state"].value)

            machine = StateMachine(number, text, session, wam_id, whatsapp_token)
            machine.execute_action()
            session["state"] = machine.state

            sessions[number] = session

            # intent = get_intent(text, vectorizer, clf)
            # send_message(number, intent, wam_id, whatsapp_token)

        queue.task_done()
        time.sleep(0.2)
