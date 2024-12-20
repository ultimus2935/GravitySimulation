import numpy as np

RUNNING = False

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
ORIGIN = np.array([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])

FULLSCREEN = True
ZOOM_FACTOR = np.array([2, 2])

SYSTEM_FILE_PATH = "systems/sun_earth_moon.csv"

dt = 0.01