from .base import BaseKinematics
from ..utils.icr_handler import IcrHandler
import numpy as np


class CarLike(BaseKinematics):
    def __init__(self, config_path=None, config_override=None):
        mode="car_like"
        self._icr_handler = IcrHandler(mode=mode, config_path=config_path, config_override=config_override)
        self._icr_handler.initialize()
        super().__init__(mode=mode, config_path=config_path, config_override=self._icr_handler.config)
        

    def _constrainIcr(self, x, y):
        #Here we apply the Car-Like constraint
        self._last_computed_icr = np.array([x, y,0])
        self._icr_handler.validateIcr([x,y])
        x_icr,y_icr = self._icr_handler.getProjectedIcr()
        return (x_icr, y_icr)


    def _preprocessHighLevelSpeeds(self, high_level_speed):
        high_level_speed = super()._preprocessHighLevelSpeeds(high_level_speed)
        if high_level_speed[0] == 0:
            high_level_speed[0] = 1e9
        if high_level_speed[1] == 0:
            high_level_speed[1] == 0
        
        return high_level_speed
    def show(self, plot=True, show_frame=False, draw_wheels_arrows=False, draw_computed_wheel_lin_speed=False):
        return super().show(plot=plot, show_frame=show_frame, draw_wheels_arrows=draw_wheels_arrows, draw_computed_wheel_lin_speed=draw_computed_wheel_lin_speed)


if __name__ == '__main__':
    car = CarLike()
    #car.computeInverseKinematics([0.0,0,0.0])
    car.kinematicsStep([0,0,-10])
    print(car._current_wheel_speed)
    car.show(True)

