import numpy as np
from scipy.signal import find_peaks

from components.Calibration import Calibration

class Peak:
    def __init__(self, name, x, height, center, width, skew) -> None:
        self.name = name
        self.x = x
        self.height = height
        self.center = center
        self.width = width
        self.skew = skew
        self.y = self.create_peak()
        self.area = 0
        self.start_idx = 0
        self.stop_idx = 0
        self.concentration = 0
        self.unit = "ppm"
        self.calibration = Calibration()

    def create_peak(self):
        # current formula with skewness does not draw with width = 0
        # set to minimal sharp value to improve UX and not have peaks disappearing
        if self.width == 0:
            self.width = 0.1
        # https://www.desmos.com/calculator/gokr63ciym
        return self.height * np.exp(-0.5 * ((self.x - self.center) / (self.width + (self.skew * (self.x - self.center))))**2)
        # https://www.desmos.com/calculator/k5y9glwjee   ??
        # https://math.stackexchange.com/questions/3605861/what-is-the-graph-function-of-a-skewed-normal-distribution-curve
        # https://cremerlab.github.io/hplc-py/methodology/fitting.html
    
    def clear_integration(self):
        self.area = 0
        self.start_idx = 0
        self.stop_idx = 0