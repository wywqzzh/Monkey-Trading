import src.util as util
import random


class Q_learning_agent:
    def __init__(self, alpha, epsilon, gamma):
        self.QValues = util.Counter()
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.lastState = None
        self.lastAction = None
        self.state_list = set()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        return self.QValues[state, action]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        values = [self.getQValue(state, action) for action in state.getLegalActions()]
        if (values):
            return max(values)
        else:
            return 0.0

    def getValue(self, state):
        return self.computeValueFromQValues(state)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legal_actions = state.getLegalActions()  # all the legal actions

        value = self.getValue(state)
        for action in legal_actions:
            if (value == self.getQValue(state, action)):
                return action

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = state.getLegalActions()
        if len(legalActions) == 0:
            return None

        if (util.flipCoin(self.epsilon)):
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state)
        self.doAction(state, action)
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        newQValue = (1 - self.alpha) * self.getQValue(state, action)  # new Qvalue
        newQValue += self.alpha * (reward + (self.discount * self.getValue(nextState)))
        self.QValues[state, action] = newQValue

    def observeTransition(self, state, action, nextState, deltaReward):
        """
            Called by environment to inform agent that a transition has
            been observed. This will result in a call to self.update
            on the same arguments

            NOTE: Do *not* override or call this function
        """
        self.update(state, action, nextState, deltaReward)

    def observationFunction(self, state, reward):
        """
            This is where we ended up after our last action.
            The simulation should somehow ensure this is called
        """
        if not self.lastState is None:
            self.observeTransition(self.lastState, self.lastAction, state, reward)

    def doAction(self, state, action):
        """
            Called by inherited class when
            an action is taken in a state
        """
        self.lastState = state
        self.lastAction = action
