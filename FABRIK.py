import math
import numpy as np

class FABRIK:
    def __init__(self, jointPos, tolerance: float):
        if tolerance <= 0:
            raise ValueError("Tolerance must be more than 0")
        self.joints = jointPos
        self.tolerance: float = tolerance
        self.linkLength = []

        a = jointPos[0]
        for b in jointPos[1:]:
            self.linkLength.append(np.linalg.norm(a - b))
            a = b

        if any([l <= 0 for l in self.linkLength]):
            raise ValueError("Link lengths must be positive")

        self.lengths = self.linkLength
        self.maxLen = sum(self.linkLength)
        self._has_moved = True
        self._angles = []
        _ = self.angles

    def as_length(self, vector, length):
        return vector * length / np.linalg.norm(vector)

    def angles(self):
        if not self._has_moved:
            return self._angles

        angles = [math.atan2(self.joints[1][1], self.joints[1][0])]
        previousAngle: float = angles[0]
        for i in range(2, len(self.joints)):
            p = self.joints[i] - self.joints[i - 1]
            absoluteAngle: float = math.atan2(p[1], p[0])
            angles.append(absoluteAngle - previousAngle)
            previousAngle = absoluteAngle

        self.moved = False
        self._angles = angles
        return self._angles

    def solvable(self, target):
        return self.maxLen >= np.linalg.norm(target)

    def angles_deg(self):
        angles = self.angles()
        angles = [math.degrees(val) for val in angles]
        return angles

    def move_to(self, target, tryReaching=True):
        if not self.solvable(target):
            if not tryReaching:
                return 0
            target = self.as_length(target, self.maxLen)
        return self._iterate(target)

    def _iterate(self, target):
        it: int = 0
        initPos = self.joints[0]
        last: int = len(self.joints) - 1

        while np.linalg.norm(self.joints[-1] - target) > self.tolerance:
            it += 1
            self.joints[-1] = target
            for i in reversed(range(0, last)):
                next, cur = self.joints[i + 1], self.joints[i]
                len_share = self.lengths[i] / np.linalg.norm(next - cur)
                self.joints[i] = (1 - len_share) * next + len_share * cur

            self.joints[0] = initPos
            for i in range(0, last):
                next, cur = self.joints[i + 1], self.joints[i]
                len_share = self.lengths[i] / np.linalg.norm(next - cur)
                self.joints[i + 1] = (1 - len_share) * \
                    cur + len_share * next
        return it

if __name__ == "__main__":
    c1 = list(map(int, input("1st Coordinate: ").strip().split()))[:3]
    c2 = list(map(int, input("2nd Coordinate: ").strip().split()))[:3]
    c3 = list(map(int, input("3rd Coordinate: ").strip().split()))[:3]
    c4 = list(map(int, input("4th Coordinate: ").strip().split()))[:3]
    tolerance = float(input("Tolerance: "))
    goal = list(map(int, input("Goal: ").strip().split()))[:3]

    initCoordinates = [ np.array(c1), np.array(c2), np.array(c3), np.array(c4) ]
    initPos = initCoordinates
    fab = FABRIK(initCoordinates, tolerance)

    iterations = fab.move_to(np.array(goal))
    print(f"Result\nNumber of Iterations: {iterations}\nAngles: {fab.angles_deg()}\nLink position: {fab.joints}\nGoal Position: {goal}")
