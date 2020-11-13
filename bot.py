import numpy as np
import poker

X_BINSIZE = 200
Y_BINSIZE = 100
X_SCREEN = 1400
Y_SCREEN = 900

class Learner(object):

    def __init__(self):
        self.last_state = None
        self.last_action = None
        self.last_reward = None

        # We initialize our Q-value grid that has an entry for each action and state.
        # (action, rel_x, rel_y)
        self.Q = np.zeros((2, X_SCREEN // X_BINSIZE, Y_SCREEN // Y_BINSIZE))
        self.epoch = 0

    def reset(self):
        self.last_state = None
        self.last_action = None
        self.last_reward = None

    def discretize_state(self, state):
        '''
        Discretize the position space to produce binned features.
        rel_x = the binned relative horizontal distance between the monkey and the tree
        rel_y = the binned relative vertical distance between the monkey and the tree
        '''

        rel_x = int((state["tree"]["dist"]) // X_BINSIZE)
        rel_y = int((state["tree"]["top"] - state["monkey"]["top"]) // Y_BINSIZE)
        return rel_x, rel_y

    def action_callback(self, state):
        '''
        Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.
        '''

        # TODO (currently monkey just jumps around randomly)
        # 1. Discretize 'state' to get your transformed 'current state' features.
        current_state = self.discretize_state(state)

        # 2. Perform the Q-Learning update using 'current state' and the 'last state'.
        # params = [[0.1, 0.7], [0.2, 0.7], [0.4, 0.7], [0.3, 0.8], [0.3, 0.9]]
        alpha = 0.3
        gamma = 0.8
        if self.last_reward is not None:
            delQ = self.last_reward + (gamma * np.max(self.Q[:, current_state[0], current_state[1]]))
            delQ -= self.Q[self.last_action, self.last_state[0], self.last_state[1]]
            self.Q[self.last_action, self.last_state[0], self.last_state[1]] += alpha * delQ

        # 3. Choose the next action using an epsilon-greedy policy.
        self.epoch += 1
        epsilon = 0.1 * np.log(100 - self.epoch)  # decaying epsilon
        if npr.rand() < epsilon:
            new_action = int(npr.rand() < 0.1)
        else:
            new_action = np.argmax(self.Q[:, current_state[0], current_state[1]])

        self.last_action = new_action
        self.last_state = current_state
        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''
        self.last_reward = reward

def run_games(learner, hist, iters = 100, t_len = 100):
    '''
    Driver function to simulate learning by having the agent play a sequence of games.
    '''
    for ii in range(iters):
        # Make a new monkey object.
        swing = SwingyMonkey(action_callback=learner.action_callback,
                             reward_callback=learner.reward_callback)
        # Loop until you hit something.
        while swing.game_loop():
            pass
        hist.append(swing.score)  # Save score history.
        learner.reset()  # Reset the state of the learner.
    pg.quit()
    return


if __name__ == '__main__':
    agent = Learner()
    hist = []
    run_games(agent, hist, 100, 100)
    np.save('hist', np.array(hist))

class bot(player):
    def __init__(self, buy_in):
        player.__init__(self, buy_in)

    # TODO: implement reinforcement learning
    def act(self):
        pass


