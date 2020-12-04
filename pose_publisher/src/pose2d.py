import numpy as np

class Pose2D:
    def __init__(self, x=0, y=0, theta=0, tmat=None):
        if tmat is None:
            self.tmatrix = np.array([[np.cos(theta), -np.sin(theta), x],
                                     [np.sin(theta), np.cos(theta), y],
                                     [0, 0, 1]])
            np.set_printoptions(precision=4, suppress=True)
            print(f"create pose: \n{self.tmatrix}")
        else:
            self.tmatrix = tmat

    def __str__(self):
        x, y, theta = self.get_params()
        return f"x={x:.3f}, y={y:.3f}, theta={theta:.4f}"

    def get_params(self):
        x, y = self.tmatrix[:2, 2]
        cosine, sine = self.tmatrix[:2, 0]
        theta = np.arctan2(sine, cosine)
        return x, y, theta

    def move(self, rel_pose):
        moved_tmat = np.dot(self.tmatrix, rel_pose.tmatrix)
        moved_pose = Pose2D(tmat=moved_tmat)
        return moved_pose

    def motion_to(self, other_pose):
        rel_tmat = np.dot(np.linalg.inv(self.tmatrix), other_pose.tmatrix)
        rel_pose = Pose2D(tmat=rel_tmat)
        return rel_pose

    def inv_transform(self, point):
        # to homogenous coordinates
        point = np.append(point[:2], 1)
        tfm_point = np.dot(np.linalg.inv(self.tmatrix), point)
        return tfm_point

    def transform(self, point):
        # to homogenous coordinates
        point = np.append(point[:2], 1)
        tfm_point = np.dot(self.tmatrix, point)
        return tfm_point