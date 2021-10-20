MAZE = """
    #.########
    #  #     #
    #  #  #  #
    #     #  #
    #  ##### #
    #  #     *
    ##########
"""

START = '.'
GOAL = '*'
WALL = '#'

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
ACTIONS = [UP, DOWN, LEFT, RIGHT]

REWARD_OUT = -5
REWARD_BORDER = -2
REWARD_GOAL = 10
REWARD_EMPTY = -1


class Environment:
    def __init__(self, maze: str):
        self.__states = {}

        lines = list(map(lambda x: x.strip(), maze.strip().split("\n")))
        for row in range(len(lines)):
            for col in range(len(lines[row])):
                self.__states[(row, col)] = lines[row][col]

                if lines[row][col] == START:
                    self.__start = (row, col)

                if lines[row][col] == GOAL:
                    self.__goal = (row, col)

    @property
    def start(self):
        return self.__start

    @property
    def goal(self):
        return self.__goal

    @property
    def states(self):
        return self.__states.keys()

    def apply(self, agent, action: str):
        state = agent.state

        if action == UP:
            new_state = (state[0] - 1, state[1])
        elif action == DOWN:
            new_state = (state[0] + 1, state[1])
        elif action == LEFT:
            new_state = (state[0], state[1] - 1)
        elif action == RIGHT:
            new_state = (state[0], state[1] + 1)

        if new_state in self.states:
            if self.__states[new_state] in [WALL, START]:
                reward = REWARD_BORDER
            elif self.__states[new_state] == GOAL:
                reward = REWARD_GOAL
            else:
                reward = REWARD_EMPTY

            state = new_state
        else:
            reward = REWARD_OUT

        agent.update(action, state, reward)
        return reward


class Agent:
    def __init__(self, environment: Environment):
        self.__state = environment.start
        self.__score = 0
        self.__last_action = None
        self.__qtable = {}
        self.__learning_rate = 1
        self.__discount_factor = 0.5

        for s in environment.states:
            self.__qtable[s] = {}

            for a in ACTIONS:
                self.__qtable[s][a] = 0.0

    def update(self, action: str, state: str, reward: int):
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * \
            (reward + self.__discount_factor *
             maxQ - self.__qtable[self.__state][action])

        self.__state = state
        self.__score += reward
        self.__last_action = action

    def best_action(self):
        rewards = self.__qtable[self.__state]
        best = None

        for a in rewards:
            if best is None or rewards[a] > rewards[best]:
                best = a

        return best

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def qtable(self):
        return self.__qtable


if __name__ == "__main__":
    env = Environment(MAZE)
    print(env.states)

    agent = Agent(env)

    i = 0

    while agent.state != env.goal:
        i += 1
        action = agent.best_action()

        reward = env.apply(agent, action)
        print(f"{i}: {agent.state} {agent.score} ({reward}) {action}")