from game_501 import Game501

class ScoringStateMachine:
    def __init__(self) -> None:
        self.state = 'SELECT_GAME'
        self.transitions = {
            'SELECT_GAME' : {'game' : 'IDLE_TURN'},
            'IDLE_TURN' : {'turn' : 'NEW_DART'},
            'NEW_DART' : {'dart' : 'WAIT_DART'},
            'WAIT_DART' : {'dart_found' : 'UPDATE_GAME'},
            'UPDATE_GAME' : {'not_done' : 'IDLE_TURN'},
            'UPDATE_GAME' : {'done' : 'FINISH_GAME'}
        }
        self.game = Game501()

    def get_action(self):
        return self.action

    def transition(self, action):
        if action in self.transitions[self.state]:
            self.state = self.transitions[self.state][action]

    def run_state(self):
        print(self.state)
        if self.state == 'SELECT_GAME':
            self.selectGame()
        elif self.state == 'IDLE_TURN':
            self.idleTurn()
        elif self.state == 'NEW_DART':
            self.newDart()
        elif self.state == 'WAIT_DART':
            self.waitDart()
        elif self.state == 'UPDATE_GAME':
            self.updateGame()
        elif self.state == 'FINISH_GAME':
            self.finishGame()

    def selectGame(self):
        input('Select Game:')
        self.action = 'game'

    def idleTurn(self):
        # Set transition
        self.action = 'turn'

    def newDart(self):
        # Set transition
        self.action = 'dart'

    def waitDart(self):
        self.number = 20
        self.ring = 'A'
        # Set transition
        self.action = 'dart_found'

    def updateGame(self):
        score = self.game.update(number=self.number, ring=self.ring)
        self.action = 'done'

    def finishGame(self):
        exit(0)

if __name__ == '__main__':
    sm = ScoringStateMachine()
    while True:
        sm.run_state()
        sm.transition(action=sm.get_action())

# EOF
