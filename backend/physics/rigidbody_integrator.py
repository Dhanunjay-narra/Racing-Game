import math
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __add__(self, o): return Vector3(self.x + o.x, self.y + o.y, self.z + o.z)
    def __sub__(self, o): return Vector3(self.x - o.x, self.y - o.y, self.z - o.z)
    def __mul__(self, s: float): return Vector3(self.x * s, self.y * s, self.z * s)
    def length(self) -> float: return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    def normalized(self):
        l = self.length()
        return Vector3(self.x/l, self.y/l, self.z/l) if l > 1e-6 else Vector3(0,0,0)


class RK4Integrator:
    @staticmethod
    def integrate_linear(pos: Vector3, vel: Vector3, force: Vector3, mass: float, dt: float) -> Tuple[Vector3, Vector3]:
        # k1
        a1 = force * (1.0 / mass)
        v1 = vel
        
        # k2
        v2 = vel + a1 * (0.5 * dt)
        a2 = force * (1.0 / mass)
        
        # k3
        v3 = vel + a2 * (0.5 * dt)
        a3 = force * (1.0 / mass)
        
        # k4
        v4 = vel + a3 * dt
        a4 = force * (1.0 / mass)
        
        # Integration
        next_pos = pos + (v1 + v2 * 2.0 + v3 * 2.0 + v4) * (dt / 6.0)
        next_vel = vel + (a1 + a2 * 2.0 + a3 * 2.0 + a4) * (dt / 6.0)
        
        return next_pos, next_vel
