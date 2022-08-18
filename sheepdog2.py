import numpy as np
import math
import random
import time
from IPython.display import display, clear_output
import time
import csv
from tqdm import tqdm
import pandas as pd
import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

df = pd.read_csv('generator.csv')

train_x = df[['DogX', 'DogY', 'SheepX', 'SheepY']]

train_y = df['T']

train_x = train_x.to_numpy()
train_y = train_y.to_numpy()

train_x = train_x / 51.0

def one_hot(x, n_classes):
    res = []
    for xx in x:
        _xx = np.zeros(n_classes)
        _xx[xx - 1] = 1.
        res.append(_xx)
    return np.array(res)

train_y = one_hot(train_y, 102)

model = Sequential()
model.add(layers.Dense(units = 128, activation = 'relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units = 64, activation = 'relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units = 32))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(units = 102, activation = 'softmax'))

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

model.build((None, 4))

model.summary()

model.fit(train_x, train_y, validation_split = 0.2, epochs = 10, batch_size = 32)

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
                _steps = np.argmax(model.predict([[i / 51.0, j / 51.0, state.SHEEP_POSITION[0] / 51.0, state.SHEEP_POSITION[1] / 51.0]], verbose = 0))
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


state = State(INITIAL_SHEEP_POSITION, INITIAL_DOG_POSITION)

print('Start to catch')
start_time = time.time()

while True:
    sheep_move(state)
    dog_move(state)
    state.info()
    if state.DOG_POSITION[0] == state.SHEEP_POSITION[0] and state.DOG_POSITION[1] == state.SHEEP_POSITION[1]:
        print('Catched!')
        break

print('Execution time: ', time.time() - start_time)

