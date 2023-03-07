from swarmtronics.three_dimensional_statistics import get_position_correlation, get_orientation_correlation, get_velocity_correlation
from swarmtronics.video_processor import VideoProcessor
import cv2
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from time import time
from tqdm import tqdm


def main():
    VP = VideoProcessor()

    VP.set_filename('Tests/test_videos/02_95_[65_bots_PWM_1_exp_2].MP4')
    kinematics = VP.extract_cartesian_kinematics(65, 1, 600, 1, (), (1, 0))
    t = time()
    pc_matrices = get_position_correlation(kinematics, 400, 400)

    print(time() - t)

    result = [[0 for x in range(400)] for y in range(400)]
    for m in pc_matrices:
        for y in range(400):
            for x in range(400):
                result[y][x] += m[y][x]

    fig, ax = plt.subplots()
    im = ax.imshow(result, cmap='hot')
    fig.colorbar(im, ax=ax)
    ax.set_title('Position correlation')
    plt.show()

    t = time()
    oc_matrices = get_orientation_correlation(kinematics, 400, 400)

    print(time() - t)

    result = [[0 for x in range(400)] for y in range(400)]
    for m in oc_matrices:
        for y in range(400):
            for x in range(400):
                result[y][x] += m[y][x]

    fig, ax = plt.subplots()
    im = ax.imshow(result, cmap='hot')
    fig.colorbar(im, ax=ax)
    ax.set_title('Orientation correlation')
    plt.show()

    t = time()
    vc_matrices = get_velocity_correlation(kinematics, 400, 400)

    print(time() - t)

    result = [[0 for x in range(400)] for y in range(400)]
    for m in vc_matrices:
        for y in range(400):
            for x in range(400):
                result[y][x] += m[y][x]

    fig, ax = plt.subplots()
    im = ax.imshow(result, cmap='seismic')
    fig.colorbar(im, ax=ax)
    ax.set_title('Velocity correlation')
    plt.show()


if __name__ == '__main__':
    main()

