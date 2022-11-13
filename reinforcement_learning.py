import random
import math

# 1. Q-Learning
class QLearningAgent:
    """Implement Q Reinforcement Learning Agent using Q-table."""

    def __init__(self, game, discount, learning_rate, explore_prob):
        """Store any needed parameters into the agent object.
        Initialize Q-table.
        """
        
        self.game = game
        self.discount = discount
        self.learning_rate = learning_rate
        self.explore_prob = explore_prob
        self.q_table = {} # empty dictionary as we have no q values as of now

    def get_q_value(self, state, action):
        """Retrieve Q-value from Q-table.
        For an never seen (s,a) pair, the Q-value is by default 0.
        """
        if (state, action) in self.q_table:
            return self.q_table[(state, action)]
        return 0

    def get_value(self, state):
        """Compute state value from Q-values using Bellman Equation.
        V(s) = max_a Q(s,a)
        """
        max = -math.inf
        actions = self.game.get_actions(state)
        if len(actions) == 0:
            return 0
        for action in actions:
            q_val = self.get_q_value(state, action)
            if q_val > max:
                max = q_val
        return max 
        
    def get_best_policy(self, state):
        """Compute the best action to take in the state using Policy Extraction.
        π(s) = argmax_a Q(s,a)

        If there are ties, return a random one for better performance.
        Hint: use random.choice().
        """
        best_actions = []
        best_q_val = -math.inf
        for action in self.game.get_actions(state):
            q_val = self.get_q_value(state, action)
            if q_val > best_q_val:
                best_q_val = q_val
                best_actions = [action]
            elif q_val == best_q_val:
                best_actions.append(action)                
        return random.choice(best_actions)

    def update(self, state, action, next_state, reward):
        """Update Q-values using running average.
        Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
        Where α is the learning rate, and γ is the discount.

        Note: You should not call this function in your code.
        """
        self.q_table[(state, action)] = (1 - self.learning_rate) * self.get_q_value(state, action) + self.learning_rate * (reward + self.discount * self.get_value(next_state))
    
    # 2. Epsilon Greedy
    def get_action(self, state):
        """Compute the action to take for the agent, incorporating exploration.
        That is, with probability ε, act randomly.
        Otherwise, act according to the best policy.

        Hint: use random.random() < ε to check if exploration is needed.
        """
        if random.random() >= self.explore_prob:
            return self.get_best_policy(state)
        return random.choice(list(self.game.get_actions(state)))

# 3. Bridge Crossing Revisited
def question3():
    return 'NOT POSSIBLE'
    epsilon = 0.25
    learning_rate = 0.25
    return epsilon, learning_rate
    # If not possible, return 'NOT POSSIBLE'


# 5. Approximate Q-Learning
class ApproximateQAgent(QLearningAgent):
    """Implement Approximate Q Learning Agent using weights."""

    def __init__(self, *args, extractor):
        """Initialize parameters and store the feature extractor.
        Initialize weights table."""

        super().__init__(*args)
        self.extractor = extractor
        self.weights_table = {}

    def get_weight(self, feature):
        """Get weight of a feature.
        Never seen feature should have a weight of 0.
        """
        if feature in self.weights_table: 
            return self.weights_table.get(feature)
        return 0

    def get_q_value(self, state, action):
        """Compute Q value based on the dot product of feature components and weights.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + ... + w_n * f_n(s,a)
        """
        q_val = 0
        for feature, val in self.extractor(state, action).items():
            q_val += val * self.get_weight(feature)
        return q_val

    def update(self, state, action, next_state, reward):
        """Update weights using least-squares approximation.
        Δ = R + γ V(s') - Q(s,a)
        Then update weights: w_i = w_i + α * Δ * f_i(s, a)
        """
        delta = reward + self.discount * (self.get_value(next_state)) - self.get_q_value(state, action)
        for feature, val in self.extractor(state, action).items():
            self.weights_table[feature] = self.get_weight(feature) + self.learning_rate * delta * val

