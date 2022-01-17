"""

"""


class Game:
    def __init__(self, labor_coins=1, consume_coins=1, consume_reward=1, remain_coins_max=20):
        """

        :param labor_coins: 每次劳动获得金币数
        :param consume_coins: 每次消费花费金币数
        :param consume_reward: 每次消费获得奖励值
        """
        self.remain_coins = 0
        self.last_earning_time = 0
        self.current_tim = 0
        self.reward = 0
        self.labor_coins = labor_coins
        self.consume_coins = consume_coins
        self.consume_reward = consume_reward
        self.remain_coins_max = remain_coins_max

    def getLegalActions(self):
        if self.remain_coins >= self.consume_coins and self.remain_coins < self.remain_coins_max:
            return [0, 1]
        elif self.remain_coins < self.consume_coins:
            return [0]
        else:
            return [1]

    def application(self, action):
        reward = 0
        if action == 0:
            self.remain_coins += self.labor_coins
        else:
            self.remain_coins -= self.consume_coins
            self.reward += self.consume_reward
            reward = self.consume_reward
        return reward
