from enum import Enum
from ask_user import get_arguments_from_user, ask_user_bin, ask_user_main_menu_task, is_exit_response
from retrieval import retrieve, detect_files

class MenuState(Enum):
    RETRIEVAL = "retrieval"
    MAIN_MENU = "main menu"
    EXIT = None

class Menu():
    
    def __init__(self, parser, config):
        self.state = MenuState.RETRIEVAL
        self.run_state = {
            MenuState.RETRIEVAL: self.run_retrieval_state(),
            MenuState.MAIN_MENU: self.run_main_menu_state()
        }
        
        self.parser = parser
        self.config = config
        
        self.main_menu_actions = {
        'h': self.parser.print_help,
        'i': self.config.print_info,
        'a': self.config.addrac,
        's': self.config.supprac,
        }
        
    
    def run_retrieval_state(self):
        user_arguments = get_arguments_from_user()
        if is_exit_response(user_arguments[0]):
            return MenuState.MAIN_MENU 
        
        self.config.set_retrieval_params(*user_arguments) 
        self.config.verify_inputs()
        
        detect_files(self.config)
        retrieve(self.config)
        
        if not ask_user_bin("Voulez-vous effectuer une recherche ? (y/n)"):
            return MenuState.MAIN_MENU
    
    def run_main_menu_state(self):
        task = ask_user_main_menu_task()
            
        if is_exit_response(task):
            return MenuState.EXIT
            
        elif task == "r":
            return MenuState.RETRIEVAL  # avant je faisais return self.set_state('retrieval') mais ça fait un appel récursif
        else:
            if action := self.main_menu_actions.get(task, None):
                action()
                return MenuState.MAIN_MENU
            return MenuState.EXIT
        
    def run(self):
        while self.state:
            self.state = self.run_state[self.state]
            # J'avais tenté self.state=self.state_actions[self.state]["next state"].get(new_state, None) avec niveaux -1, 0, 1
            
        