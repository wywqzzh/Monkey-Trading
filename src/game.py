"""

"""
import copy

WAIT_TIME = 6
PENALTY_WRONG = -5
PENALTY_WAIT = -1 / 6
TAU = 2

"""
    简单的game state,剩余金币数为唯一属性，状态空间为2 (0,1) 
"""


class State_sample:
    def __init__(self, remain_coins=0):
        """
        state初始化
        :param remain_coins: 剩余金币数
        """
        self.remain_coins = remain_coins

    def getLegalActions(self):
        """
        获取动作空间
        :return: 动作list
        """
        actions = [1, 0]
        return actions


class Game_sample:
    def __init__(self, labor_coins=1, consume_coins=1, consume_reward=1, remain_coins_max=20):
        """
        :param labor_coins: 每次劳动获得金币数
        :param consume_coins: 每次消费花费金币数
        :param consume_reward: 每次消费获得奖励值
        :param remain_coins_max: 最大金币数
        """
        self.state = State_sample()
        self.reward = 0
        self.labor_coins = labor_coins
        self.consume_reward = consume_reward
        self.remain_coins_max = remain_coins_max
        self.consume_coins = consume_coins
        self.action_num = 2

    def application(self, state, action):
        state = copy.deepcopy(state)
        reward = 0
        if action == 0:
            state.remain_coins = min(self.labor_coins + state.remain_coins, self.remain_coins_max)
            reward = 0
        elif action == 1:
            if state.remain_coins < self.consume_coins:
                reward = PENALTY_WRONG
            else:
                state.remain_coins -= self.consume_coins
                self.reward += self.consume_reward
                reward = self.consume_reward
        return state, reward

    def generateSuccessor(self, agent, action):
        state, reward = self.application(self.state, action)
        for t_state in agent.state_list:
            if type(t_state) == type(state) and t_state.remain_coins == state.remain_coins:
                state = t_state
                break
        agent.state_list.add(state)
        return state, reward


class State:
    def __init__(self, remain_coins=0, wait_earning_time=0):
        self.remain_coins = remain_coins
        self.wait_earning_time = wait_earning_time

    def getLegalActions(self):
        if self.wait_earning_time <= 0:
            return [1, 0]
        else:
            return [1]


class Game:
    def __init__(self, labor_coins=1, consume_coins=1, consume_reward=1, remain_coins_max=20):
        """

        :param labor_coins: 每次劳动获得金币数
        :param consume_coins: 每次消费花费金币数
        :param consume_reward: 每次消费获得奖励值
        """
        self.state = State()
        self.reward = 0
        self.labor_coins = labor_coins
        self.consume_reward = consume_reward
        self.remain_coins_max = remain_coins_max
        self.consume_coins = consume_coins
        self.earning_state = True
        self.action_num = 2

    def application(self, state, action):
        state = copy.deepcopy(state)
        reward = 0
        if action == 0:
            state.remain_coins = min(self.labor_coins + state.remain_coins, self.remain_coins_max)
            reward = 0
            self.earning_state = True
        elif action == 1:
            if state.remain_coins < self.consume_coins:
                reward = PENALTY_WRONG
            else:
                state.remain_coins -= self.consume_coins
                self.reward += self.consume_reward
                reward = self.consume_reward
            if self.earning_state == True:
                state.wait_earning_time = TAU
                self.earning_state = False
            else:
                state.wait_earning_time = max(0, state.wait_earning_time - 1)

        return state, reward

    def generateSuccessor(self, agent, action):
        state, reward = self.application(self.state, action)
        for t_state in agent.state_list:
            if type(t_state) == type(
                    state) and t_state.remain_coins == state.remain_coins and t_state.wait_earning_time == state.wait_earning_time:
                state = t_state
                break
        agent.state_list.add(state)
        return state, reward


class State_complex:
    def __init__(self, remain_coins=0, wait_earning_time=0):
        self.remain_coins = remain_coins
        self.wait_earning_time = wait_earning_time

    def getLegalActions(self):
        if self.wait_earning_time <= 0:
            return [1, 0, 2]
        else:
            return [1, 2]


class Game_complex:
    def __init__(self, labor_coins=1, consume_coins=1, consume_reward=1, remain_coins_max=20):
        """

        :param labor_coins: 每次劳动获得金币数
        :param consume_coins: 每次消费花费金币数
        :param consume_reward: 每次消费获得奖励值
        """
        self.state = State_complex()
        self.reward = 0
        self.labor_coins = labor_coins
        self.consume_reward = consume_reward
        self.remain_coins_max = remain_coins_max
        self.consume_coins = consume_coins
        self.earning_state = True
        self.action_num = 3

    def application(self, state, action):
        state = copy.deepcopy(state)
        reward = 0
        if action == 0:
            state.remain_coins = min(self.labor_coins + state.remain_coins, self.remain_coins_max)
            reward = 0
            self.earning_state = True
        elif action == 1:
            if state.remain_coins < self.consume_coins:
                reward = PENALTY_WRONG
            else:
                state.remain_coins -= self.consume_coins
                self.reward += self.consume_reward
                reward = self.consume_reward
            if self.earning_state == True:
                state.wait_earning_time = TAU
                self.earning_state = False
            else:
                state.wait_earning_time = max(0, state.wait_earning_time - 1)
        else:
            reward = PENALTY_WAIT
            state.wait_earning_time = max(0, state.wait_earning_time - 1)
        return state, reward

    def generateSuccessor(self, agent, action):
        state, reward = self.application(self.state, action)
        for t_state in agent.state_list:
            if type(t_state) == type(
                    state) and t_state.remain_coins == state.remain_coins and t_state.wait_earning_time == state.wait_earning_time:
                state = t_state
                break
        agent.state_list.add(state)
        return state, reward
