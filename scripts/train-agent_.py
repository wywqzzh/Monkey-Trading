from src.agents_ import Q_learning_agent
from src.game_ import Game
import copy


def update(state, action, nextState, reward, agent):
    if action != None:
        agent.update(state, action, nextState, reward)


def train(agent, game):
    agent.state_list.add(game.state)
    while game.reward < 600:
        observation = agent.observationFunction(
            game.state)
        action = agent.getAction(observation)
        game.state = game.generateSuccessor(agent, action)


def test(agent, game):
    T = 100
    for t in range(T):
        action = agent.getAction(game.state)
        print(game.state.remain_coins, action)
        game.state = game.generateSuccessor(agent, action)


if __name__ == '__main__':
    agent = Q_learning_agent(0.1, 0.2, 0.8)
    game = Game(1, 1, 1, 10)
    num_train = 100
    for i in range(num_train):
        train(agent, copy.deepcopy(game))

    game = Game(1, 1, 1, 10)
    test(agent, game)
