# Include your imports here, if any are used.

import math

# 1. Value Iteration
class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.discount = discount
        self.state_vals = {} # dictionary to hold values corresponding to each state
        for state in self.game.states: 
            self.state_vals[state] = 0 # set the value for each state to 0

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        if state not in self.state_vals.keys(): # check for the corner case where state isn't in the dict
            return 0 
        return self.state_vals.get(state) 

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        transitions = self.game.get_transitions(state, action) # obtain transitions from game
        q_val = 0
        for state_next, prob in transitions.items(): # iterate through all the next states and their respective probabilities
            reward = self.game.get_reward(state, action, state_next) # calculate reward for s, a, s'
            q_val += prob*(reward + (self.discount*self.get_value(state_next))) # sum up the q values for each next state
        return q_val

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        max = -math.inf
        for action in self.game.get_actions(state): # loop through all possible actions from a certain state
            new_q = self.get_q_value(state, action) 
            if new_q > max:
                max = new_q
                action_best = action # find the best action through max q value
        return action_best

    def iterate(self):
        """Run single value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        action_vals = dict()
        for state in self.game.states: 
            action_best = self.get_best_policy(state) # find best action for state
            q_val = self.get_q_value(state, action_best) # find q value of that action
            action_vals[state] = q_val # replace 0 value with new q value

        self.state_vals = action_vals


# 2. Policy Iteration
class PolicyIterationAgent(ValueIterationAgent):
    """Implement Policy Iteration Agent.

    The only difference between policy iteration and value iteration is at
    their iteration method. However, if you need to implement helper function or
    override ValueIterationAgent's methods, you can add them as well.
    """

    def __init__(self, game, discount):
        super().__init__(game, discount)
        self.policy = {} # create dictionary mapping each state to a certain random action (in this case first one)
        for state in game.states: 
            for action in game.get_actions(state):
                self.policy[state] = action
                break


    def iterate(self):
        """Run single policy iteration.
        Fix current policy, iterate state values V(s) until |V_{k+1}(s) - V_k(s)| < ε
        """
        epsilon = 1e-6
        
        delta = math.inf 

        while delta > epsilon: # run while the delta doesnt become greater than epsilon
            delta = -math.inf
            for state in self.game.states: # loop through all game states, checking the action stored for that state
                action = self.policy.get(state)
                q_val = self.get_q_value(state, action) # calculate the q value for that action

                if abs(q_val - self.get_value(state)) > delta: # find the MAX difference between q value and the previous q value
                    delta = abs(q_val - self.get_value(state))

                self.state_vals[state] = q_val # set the state to that maximum q value

                # this ensures that when the delta is greater than epsilon, EVERY single states q value is imoroving by that amount

        for state in self.game.states: 
            self.policy[state] = self.get_best_policy(state) # the looping leads to finding the optimal q values, which is at convergence. 

            # these are set into our original dictionary
        
