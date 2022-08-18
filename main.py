import numpy as np
import math
import random
import time
from IPython.display import display, clear_output

GROUND_SIZE = (51, 51)
SHEEP_SIGHT = (5, 5)

INITIAL_DOG_POSITION = (50, 50)
INITIAL_SHEEP_POSITION = (20, 35)

CENTER = (GROUND_SIZE[0] // 2, GROUND_SIZE[1] // 2)
DOOR = (CENTER[0], CENTER[1] - 2)

def is_sheep_can_see_dog(state):
    SHEEP_POSITION = state.SHEEP_POSITION
    DOG_POSITION = state.DOG_POSITION
    if math.fabs(SHEEP_POSITION[0] - DOG_POSITION[0]) <= SHEEP_SIGHT[0] // 2 and math.fabs(SHEEP_POSITION[1] - DOG_POSITION[1]) <= SHEEP_SIGHT[0] // 2:
        return True
    return False

def sheep_move(state):
    if state.SHEEP_POSITION == DOOR:
        state.DOG_STATE = 'WAITING'
        state.SHEEP_POSITION = CENTER
        state.GAME_STATE = 'END'
        return
    if is_sheep_can_see_dog(state) == True:
        _x = state.DOG_POSITION[0] - state.SHEEP_POSITION[0]
        _y = state.DOG_POSITION[1] - state.SHEEP_POSITION[1]
        if math.fabs(_x) > math.fabs(_y):
            if _x > 0:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0] + 1, state.SHEEP_POSITION[1])
                return
            elif _x < 0:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0] - 1, state.SHEEP_POSITION[1])
                return
        elif math.fabs(_x) < math.fabs(_y):
            if _y > 0:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0], state.SHEEP_POSITION[1] + 1)
                return
            elif _y < 0:
                state.SHEEP_POSITION = (state.SHEEP_POSITION[0], state.SHEEP_POSITION[1] - 1)
                return
        elif math.fabs(_x) == math.fabs(_y):
            if (state.DOG_PRV_POSITION[0] - state.SHEEP_POSITION[0]) ** 2 + (state.DOG_PRV_POSITION[1] - state.SHEEP_POSITION[1]) ** 2 == 1:
                state.SHEEP_POSITION = state.DOG_PRV_POSITION
                return
            else:
                direction = random.randint(0, 1)
                if direction == 0:
                    if _x > 0:
                        state.SHEEP_POSITION = (state.SHEEP_POSITION[0] + 1, state.SHEEP_POSITION[1])
                        return
                    elif _x < 0:
                        state.SHEEP_POSITION = (state.SHEEP_POSITION[0] - 1, state.SHEEP_POSITION[1])
                        return
                else:
                    if _y > 0:
                        state.SHEEP_POSITION = (state.SHEEP_POSITION[0], state.SHEEP_POSITION[1] + 1)
                        return
                    elif _y < 0:
                        state.SHEEP_POSITION = (state.SHEEP_POSITION[0], state.SHEEP_POSITION[1] - 1)
                        return

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

def check_dog_status(state):
    if is_sheep_can_see_dog(state) == True:
        if (state.DOG_POSITION[0] - state.SHEEP_POSITION[0]) ** 2 + (state.DOG_POSITION[1] - state.SHEEP_POSITION[1]) ** 2 == 1:
            state.DOG_STATE = 'LEADING'
        else:
            state.DOG_STATE = 'WAITING'

def dog_move(state):
    state.DOG_PRV_POSITION = state.DOG_POSITION
    if state.DOG_STATE == 'TRACKING':
        min_length = math.inf
        candidate_point = None
        for i in range(state.DOG_POSITION[0] - 1, state.DOG_POSITION[0] + 2):
            for j in range(state.DOG_POSITION[1] - 1, state.DOG_POSITION[1] + 2):                
                if CENTER[0] - 1 <= i <= CENTER[0] + 1 and CENTER[1] - 1 <= j <= CENTER[1] + 1:
                    continue
                _length = (i - state.SHEEP_POSITION[0]) ** 2 + (j - state.SHEEP_POSITION[1]) ** 2
                if _length < min_length and 0 <= i <= GROUND_SIZE[0] and 0 <= j <= GROUND_SIZE[1]:
                    min_length = _length
                    candidate_point = (i, j)
        if candidate_point == None:
            print('Error!')
        else:
            state.DOG_POSITION = candidate_point
        if is_sheep_can_see_dog(state) == True:
            state.DOG_STATE = 'WAITING'
    elif state.DOG_STATE == 'LEADING':
        candidate_points = []
        candidate_points.append((state.DOG_POSITION[0] + 1, state.DOG_POSITION[1]))
        candidate_points.append((state.DOG_POSITION[0] - 1, state.DOG_POSITION[1]))
        candidate_points.append((state.DOG_POSITION[0], state.DOG_POSITION[1] + 1))
        candidate_points.append((state.DOG_POSITION[0], state.DOG_POSITION[1] - 1))
        min_length = math.inf
        candidate_point = None
        for pt in candidate_points:
            if (pt[0] == state.SHEEP_POSITION[0] and pt[1] == state.SHEEP_POSITION[1]) or (CENTER[0] - 1 <= pt[0] <= CENTER[0] + 1 and CENTER[1] - 1 <= pt[1] <= CENTER[1] + 1):
                continue
            _length = (pt[0] - DOOR[0]) ** 2 + (pt[1] - DOOR[1]) ** 2
            if _length < min_length:
                min_length = _length
                candidate_point = pt
        if candidate_point == None:
            print('Error!')
        else:
            state.DOG_POSITION = candidate_point

class State:
    def __init__(self, GROUND_SIZE, SHEEP_POSITION, DOG_POSITION):
        self.GAME_STATE = 'START'
        self.DOG_STATE = 'TRACKING'
        self.GROUND_SIZE = GROUND_SIZE
        self.SHEEP_POSITION = SHEEP_POSITION
        self.DOG_POSITION = DOG_POSITION
        self.DOG_PRV_POSITION = DOG_POSITION
        self.GROUND_PRINTED = False
    def info(self):
        print('>>>>>>>>>>>>>>>>STATE-INFO>>>>>>>>>>>>>>>>')
        print('SHEEP: ', self.SHEEP_POSITION)
        print('DOG: ', self.DOG_POSITION)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    def print_ground(self):
        clear_output(wait = True)
        for i in range(-1, self.GROUND_SIZE[1] + 1):
            row_print_str = ''
            for j in range(-1, self.GROUND_SIZE[0] + 1):
                if i == state.SHEEP_POSITION[1] and j == state.SHEEP_POSITION[0]:
                    row_print_str += 'SP'
                elif i == state.DOG_POSITION[1] and j == state.DOG_POSITION[0]:
                    row_print_str += 'DG'
                elif i == -1 or i == self.GROUND_SIZE[1]:
                    row_print_str += '##'
                elif j == -1 or j == self.GROUND_SIZE[0]:
                    row_print_str += '##'
                elif CENTER[1] - 1 <= i <= CENTER[1] + 1 and (j == CENTER[0] - 1 or j == CENTER[0] + 1):
                    row_print_str += '##'
                elif i == CENTER[1] + 1 and j == CENTER[0]:
                    row_print_str += '##'
                else:
                    row_print_str += '  '
            display(row_print_str)


state = State(GROUND_SIZE, INITIAL_SHEEP_POSITION, INITIAL_DOG_POSITION)

for i in range(100):
    dog_move(state)
    sheep_move(state)
    check_dog_status(state)
    state.print_ground()
    if state.GAME_STATE == 'END':
        break
    time.sleep(.5)