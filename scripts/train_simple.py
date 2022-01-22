from src.agents import Q_learning_agent
from src.game import Game_sample
import copy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def update(state, action, nextState, reward, agent):
    if action != None:
        agent.update(state, action, nextState, reward)


def train(agent, game):
    state = game.state
    for t_state in agent.state_list:
        if type(t_state) == type(state) and t_state.remain_coins == state.remain_coins:
            state = t_state
            break
    agent.state_list.add(state)
    game.state = state
    reward = 0
    Q_table_ = []
    while game.reward < 10:
        Q_table_.append(copy.deepcopy(agent.QValues))
        agent.observationFunction(game.state, reward)
        action = agent.getAction(game.state)
        game.state, reward = game.generateSuccessor(agent, action)
    xx = 0
    keys = [key for key in agent.QValues]
    Q_table = np.zeros((2, game.remain_coins_max + 1))
    for key in keys:
        action = key[1]
        remain = key[0].remain_coins
        Q_table[action][remain] = agent.getQValue(key[0], action)
    return Q_table, Q_table_


def test(agent, game):
    state = game.state
    for t_state in agent.state_list:
        if type(t_state) == type(state) and t_state.remain_coins == state.remain_coins:
            state = t_state
            break
    agent.state_list.add(state)
    game.state = state
    num = 0
    total = 0
    while game.reward < 600:
        total += 1
        action = agent.getAction(game.state)
        if game.state.remain_coins <= 0 and action == 1:
            num += 1
        print(game.state.remain_coins, action)
        game.state, reward = game.generateSuccessor(agent, action)
    print(total * 0.05 / 2, num)


def plot_Q_tables(Q_tables, filename=None):
    fig = plt.figure(figsize=(16, 5), dpi=200)
    data = np.array(Q_tables)
    for i in range(data.shape[2]):
        plt.subplot(2, 6, i + 1)
        plt.plot(data[:, 0, i])
        plt.plot(data[:, 1, i])
        plt.legend(["labour", "cnsume"])
        plt.xlabel("state " + str(i))
    plt.tight_layout()
    if filename != None:
        plt.savefig("../results/imgs_simple/" + filename + ".pdf")
    plt.show()
    pass


def heatMap(data, filename=None):
    state = [i for i in range(data.shape[1])]
    actions = ["labour", "consume"]
    heatMap = data.T

    heatMap = pd.DataFrame(heatMap, columns=actions,
                           index=state)
    # sns_plot = sns.heatmap(heatMap)
    plt.figure(figsize=(6, 5), dpi=100)
    plt.style.use('ggplot')
    # 处理中文乱码
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    # 坐标轴负号的处理
    plt.rcParams['axes.unicode_minus'] = False
    sns.heatmap(data=heatMap,  # 指定绘图数据
                cmap='PuBuGn',  # 指定填充色
                linewidths=.1,  # 设置每个单元格边框的宽度
                annot=True,  # 显示数值
                )
    plt.xlabel("action")
    plt.ylabel("state")
    if filename != None:
        plt.savefig("../results/imgs_simple/QTables-" + str(filename) + ".pdf")
    else:
        plt.savefig("../results/imgs_simple/QTables.pdf")
    plt.show()


if __name__ == '__main__':
    agent = Q_learning_agent(0.01, 0.2, 1)
    game = Game_sample(1, 1, 1, 10)
    num_train = 200
    Q_tables = []
    Q_tables_ = []
    for i in range(num_train):
        if i == 99:
            xxx = 0
        # agent.epsilon = max((0.7 - 0.012 * i), 0.1)
        agent.epsilon = 0
        agent.lastAction = None
        agent.lastState = None
        Q_table, Q_table_ = train(agent, copy.deepcopy(game))
        Q_tables.append(Q_table)
        Q_tables_.append(Q_table_)
        x = [a for a in agent.QValues]
        y = [a[0].remain_coins for a in x]
    plot_Q_tables(Q_tables, "convergence")
    heatMap(Q_tables[-1])
    game = Game_sample(1, 1, 1, 10)
    agent.epsilon = 0.05
    test(agent, game)
