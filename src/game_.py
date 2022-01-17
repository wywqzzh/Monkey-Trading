"""

"""


class State:
    def __init__(self, remain_coins_max, consume_coins, remain_coins=0, reward=0):
        self.remain_coins = remain_coins
        self.remain_coins_max = remain_coins_max
        self.consume_coins = consume_coins
        self.reward = reward

    def getLegalActions(self):
        if self.remain_coins >= self.consume_coins and self.remain_coins < self.remain_coins_max:
            return [0, 1]
        elif self.remain_coins < self.consume_coins:
            return [0]
        else:
            return [1]

    def getScore(self):
        return self.reward

    def deepCopy(self):
        state = State(self.remain_coins_max, self.consume_coins)
        return state


class Game:
    def __init__(self, labor_coins=1, consume_coins=1, consume_reward=1, remain_coins_max=20):
        """

        :param labor_coins: 每次劳动获得金币数
        :param consume_coins: 每次消费花费金币数
        :param consume_reward: 每次消费获得奖励值
        """
        self.state = State(remain_coins_max, consume_coins)
        self.reward = 0
        self.labor_coins = labor_coins
        self.consume_reward = consume_reward

        self.last_earning_time = 0
        self.current_tim = 0

    def application(self, state, action):
        if action == 0:
            state.remain_coins += self.labor_coins
            state.reward = 0
        else:
            state.remain_coins -= self.state.consume_coins
            self.reward += self.consume_reward
            state.reward = self.consume_reward

    def generateSuccessor(self, agent, action):
        state = State(self.state.remain_coins_max, self.state.consume_coins, self.state.remain_coins, self.state.reward)
        self.application(state, action)
        for t_state in agent.state_list:
            if type(t_state) == type(state) and t_state.remain_coins == state.remain_coins and \
                    t_state.remain_coins_max == state.remain_coins_max and t_state.consume_coins == state.consume_coins and \
                    t_state.reward == state.reward:
                state = t_state
                break
        agent.state_list.add(state)
        return state
