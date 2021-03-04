import numpy as np
from pose2d import Pose2D
from pose_plotter import plot_poses, plot_point

def main():
    relative_poses = [Pose2D(1, 1, np.pi/6), Pose2D(3, 1, np.pi/6),
                      Pose2D(2, -2, -np.pi/3), Pose2D(2, -1, -np.pi/6)]
    global_point = np.array([8, 6])

    # 1. 연결된 포즈들 사이의 상대 포즈를 알 때, 모든 포즈의 전역 포즈(global pose) 계산
    # 첫 번째만 절대 포즈(전역 좌표계), 나머지는 직전 포즈 기준 상대 포즈(움직임)
    global_poses = []
    cur_pose = Pose2D()
    for rel_pose, index in zip(relative_poses, ['A', 'B', 'C', 'D']):
        # 상대 포즈를 누적해서 전역 포즈 계산
        cur_pose = cur_pose.move(rel_pose)
        global_poses.append(cur_pose)
        print(f"global pose {index}: {cur_pose}")

    # 전역 좌표계에서의 포즈들과 점 그리기
    plot_poses(global_poses, 121)
    plot_point(global_point)

    # 2. 모든 포즈의 전역 포즈를 알 때, 특정 포즈를 기준으로 다른 포즈들의 상대 포즈 계산
    # 중간 포즈를 새로운 기준 좌표계로 사용
    ref_pose = global_poses[1]
    print("reference pose:", ref_pose)
    local_poses = []
    for glo_pose, index in zip(global_poses, ['A', 'B', 'C', 'D']):
        # 기준 좌표계에서 다른 포즈의 상대 포즈 계산
        loc_pose = ref_pose.motion_to(glo_pose)
        local_poses.append(loc_pose)
        print(f"local pose {index}: {loc_pose}")

    # 기준 좌표계에서의 포즈들 그리기
    plot_poses(local_poses, 122, show=True)

    # 3. 점의 전역 좌표가 주어졌을 때 Pose A~D를 기준으로 점의 상대 좌표 계산
    relative_coords = []
    for glo_pose, index in zip(global_poses, ['A', 'B', 'C', 'D']):
        # 전역 좌표를 상대 좌표로 변환
        rel_coords = glo_pose.inv_transform(global_point)
        relative_coords.append(rel_coords)
        print(f"relative coordinates in {index}: {rel_coords}")

    # 4. 각 포즈에서 본 점의 좌표 relative_coords를 전역 좌표로 변환
    global_coords = []
    for glo_pose, rel_coords, index in zip(global_poses, relative_coords, ['A', 'B', 'C', 'D']):
        # 상대 좌표를 전역 좌표로 변환
        glo_coords = glo_pose.transform(rel_coords)
        global_coords.append(glo_coords)
        print(f"global coordinates in {index}: {glo_coords[:2]}")

if __name__ == "__main__":
    main()