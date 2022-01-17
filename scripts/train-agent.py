from src.agents import Q_learning_agent
from src.game import Game
import copy


def update(state, action, nextState, reward, agent):
    if action != None:
        agent.update(state, action, nextState, reward)


def train(agent, game):
    T = 1000
    last_state = None
    last_action = None
    reward = 0
    for t in range(T):
        update(last_state, last_action, game, reward, agent)
        action = agent.getAction(game)
        last_state = copy.deepcopy(game)
        last_action = action
        reward = game.application(action)


def test(agent, game):
    T = 100
    for t in range(T):
        action = agent.getAction(game)
        print(game.remain_coins,action)
        game.application(action)


if __name__ == '__main__':
    agent = Q_learning_agent(0.1, 0.2, 0.8)
    game = Game(1, 1, 1, 10)
    train(agent, game)
    game = Game(1, 1, 1, 10)
    test(agent, game)

