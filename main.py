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
BORDER = '#'

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
ACTIONS = [UP, DOWN, LEFT, RIGHT]

REWARD_BORDER = -2
REWARD_GOAL = 1
REWARD_EMPTY = 0


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
            if self.__states[new_state] in [BORDER, START]:
                reward = REWARD_BORDER
            elif self.__states[new_state] == GOAL:
                reward = REWARD_GOAL
            else:
                reward = REWARD_EMPTY

            agent.update(new_state, reward)


class Agent:
    def __init__(self, environment: Environment):
        self.__state = environment.start
        self.__score = 0
        self.__last_action = None

    def update(self, state: str, reward: int):
        self.__state = state
        self.__score += reward

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score


if __name__ == "__main__":
    env = Environment(MAZE)
    print(env.states)

    agent = Agent(env)
    print(agent.state, agent.score)
    env.apply(agent, DOWN)
    print(agent.state, agent.score)