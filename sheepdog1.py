import numpy as np
import math
import random
import time
from IPython.display import display, clear_output
import time
import csv
from tqdm import tqdm

GROUND_SIZE = (51, 51)
SHEEP_SIGHT = (5, 5)

INITIAL_DOG_POSITION = (50, 50)
INITIAL_SHEEP_POSITION = (0, 0)

CENTER = (GROUND_SIZE[0] // 2, GROUND_SIZE[1] // 2)
DOOR = (CENTER[0], CENTER[1] - 2)

def sheep_move(state):
    while True:
        direction = random.randint(0, 3)
        if direction == 0:
            if 0 <= state.SHEEP_POSITION[0] - 1:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0] - 1, state.SHEEP_POSITION[1])
                return
        elif direction == 1:
            if state.SHEEP_POSITION[0] + 1 < GROUND_SIZE[0]:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0] + 1, state.SHEEP_POSITION[1])
                return
        elif direction == 2:
            if 0 <= state.SHEEP_POSITION[1] - 1:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0], state.SHEEP_POSITION[1] - 1)
                return
        elif direction == 3:
            if state.SHEEP_POSITION[1] + 1 < GROUND_SIZE[1]:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0], state.SHEEP_POSITION[1] + 1)
                return

def dog_move(state):
    min_steps = math.inf
    candidate_point = None
    for i in range(state.DOG_POSITION[0] - 1, state.DOG_POSITION[0] + 2):
        for j in range(state.DOG_POSITION[1] - 1, state.DOG_POSITION[1] + 2):                
            if CENTER[0] - 1 <= i <= CENTER[0] + 1 and CENTER[1] - 1 <= j <= CENTER[1] + 1:
                continue
            if 0 <= i < GROUND_SIZE[0] and 0 <= j < GROUND_SIZE[1]:
                if i == state.SHEEP_POSITION[0] and j == state.SHEEP_POSITION[1]:
                    state.DOG_POSITION = (i, j)
                    return
                _steps = calculate_T((i, j), state.SHEEP_POSITION)
                if _steps < min_steps:
                    min_steps = _steps
                    candidate_point = (i, j)
    state.DOG_POSITION = candidate_point

class State:
    def __init__(self, SHEEP_POSITION, DOG_POSITION):
        self.SHEEP_POSITION = SHEEP_POSITION
        self.DOG_POSITION = DOG_POSITION

    def info(self):
        print('SHEEP: ', self.SHEEP_POSITION)
        print('DOG: ', self.DOG_POSITION)


def go_around(tar, state_space, depth, candidates):
    new_candidates = []
    for candidate in candidates:
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_candidate = (candidate[0] + i, candidate[1] + j)
                
                if new_candidate[0] < 0 or new_candidate[0] > 50 or new_candidate[1] < 0 or new_candidate[1] > 50:
                    continue
                if 24 <= new_candidate[0] <= 26 and 24 <= new_candidate[1] <= 26:
                    continue
                if state_space[new_candidate[0]][new_candidate[1]] == 1:
                    continue
                if new_candidate[0] == tar[0] and new_candidate[1] == tar[1]:
                    return depth + 1
                
                new_candidates.append(new_candidate)
                state_space[new_candidate[0]][new_candidate[1]] = 1
    return go_around(tar, state_space, depth + 1, new_candidates)

def calculate_T(src, tar):
    candidates = []
    state_space = np.zeros(GROUND_SIZE)
    state_space[src[0]][src[1]] = 1
    candidates.append(src)
    return go_around(tar, state_space, 0, candidates)

def generator_state_T_pairs(count):
    with open('generator.csv', 'w', encoding = 'UTF8', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['Index', 'DogX', 'DogY', 'SheepX', 'SheepY', 'T', 'BestActionX', 'BestActionY'])

        for i in tqdm(range(count)):
            while True:
                sheep_pos = np.random.randint(0, 51, size=(1, 2))[0]
                if 24 <= sheep_pos[0] <= 26 and 24 <= sheep_pos[1] <= 26:
                    continue
                break

            while True:
                dog_pos = np.random.randint(0, 51, size=(1, 2))[0]
                if 24 <= dog_pos[0] <= 26 and 24 <= dog_pos[1] <= 26:
                    continue
                if sheep_pos[0] == dog_pos[0] and sheep_pos[1] == dog_pos[1]:
                    continue
                break
            
            c_t = calculate_T(dog_pos, sheep_pos)

            min_steps = math.inf
            action = None
            flag = False
            for i in range(dog_pos[0] - 1, dog_pos[0] + 2):
                for j in range(dog_pos[1] - 1, dog_pos[1] + 2):                
                    if CENTER[0] - 1 <= i <= CENTER[0] + 1 and CENTER[1] - 1 <= j <= CENTER[1] + 1:
                        continue
                    if 0 <= i < GROUND_SIZE[0] and 0 <= j < GROUND_SIZE[1]:
                        if i == sheep_pos[0] and j == sheep_pos[1]:
                            action = (i - dog_pos[0], j - dog_pos[1])
                            flag = True
                            break
                        _steps = calculate_T((i, j), sheep_pos)
                        if _steps < min_steps:
                            min_steps = _steps
                            action = (i - dog_pos[0], j - dog_pos[1])
                if flag == True:
                    break

            writer.writerow([i + 1, dog_pos[0], dog_pos[1], sheep_pos[0], sheep_pos[1], c_t, action[0], action[1]])



# state = State(INITIAL_SHEEP_POSITION, INITIAL_DOG_POSITION)

# start_time = time.time()

# while True:
#     sheep_move(state)
#     dog_move(state)
#     # state.info()
#     if state.DOG_POSITION[0] == state.SHEEP_POSITION[0] and state.DOG_POSITION[1] == state.SHEEP_POSITION[1]:
#         print('Catched!')
#         break

# print('Execution time: ', time.time() - start_time)

generator_state_T_pairs(500000)
