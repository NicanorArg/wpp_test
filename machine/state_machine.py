#posibles estados
#posibles transiciones
#metodo para transicionar entre estados

from machine.states_enum import States
from machine.InvalidTransitionException import InvalidTransitionException
from machine.send_message import send_message

from machine.actions.welcome_user import welcome_user
from machine.actions.show_categories import show_categories
from machine.actions.show_items import show_items
from machine.actions.show_item import show_item
from machine.actions.show_order import show_order
from machine.actions.wait_user import wait_user
from machine.actions.route_user import route_user
from machine.actions.give_bill import give_bill


from machine.listeners.listen_categories import listen_categories
from machine.listeners.listen_items import listen_items
from machine.listeners.listen_item import listen_item
from machine.listeners.listen_order import listen_order
from machine.listeners.listen_route import listen_route
from machine.listeners.listen_await import listen_await

class StateMachine:
    
    def __init__(self, number, text, session, wam_id, whatsapp_token):
        self.number = number
        self.text = text
        self.state = session["state"]
        self.wam_id = wam_id
        self.whatsapp_token = whatsapp_token

        self.transition_origins = {
            States.CATEGORIES: [
                States.WELCOME,
                States.CATEGORIES,
                States.ITEMS,
                States.ITEM,
                States.ORDER,
                States.ROUTE
            ],
            States.ITEMS: [States.CATEGORIES, States.ITEMS, States.ITEM],
            States.ITEM: [States.ITEMS, States.ITEM],
            States.ORDER: [States.CATEGORIES, States.ITEMS, States.ITEM, States.ORDER],
            States.AWAIT: [States.ORDER, States.ROUTE],
            States.ROUTE:[States.AWAIT],
            States.BILL: [States.ROUTE, States.BILL, States.CATEGORIES]
            
        }

        self.state_actions ={
            States.WELCOME: welcome_user,
            States.CATEGORIES: show_categories,
            States.ITEMS: show_items,
            States.ITEM: show_item,
            States.ORDER: show_order,
            States.AWAIT: wait_user,
            States.ROUTE: route_user,
            States.BILL: give_bill,

            States.LISTEN_AWAIT: listen_await,
            States.LISTEN_CATEGORIES: listen_categories,
            States.LISTEN_ITEMS: listen_items,
            States.LISTEN_ITEM: listen_item,
            States.LISTEN_ORDER: listen_order,
            States.LISTEN_ROUTE: listen_route
        }

    def change_state(self, new_state, forced=False):
        if forced or (self.state in self.transition_origins.get(new_state, [])):
            self.state = new_state
        else:
            raise InvalidTransitionException
        
    def execute_action(self):
        print(self.state.value)
        action = self.state_actions.get(self.state)
        if action:
            action(self)
        else:
            raise RuntimeError("State doesn't have defined method")
    
