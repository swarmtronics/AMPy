from swarmtronics.video_processor import VideoProcessor
from swarmtronics.two_dimensional_statistics import calculate_stcp

from matplotlib import pyplot as plt

from time import time
from tqdm import tqdm


def main():
    VP = VideoProcessor()
    VP.set_filename('Tests/test_videos/02_95_[65_bots_PWM_1_exp_2].MP4')
    kinematics = VP.extract_cartesian_kinematics(65, 1, 4000, 1, (), (1, 0))
    t = time()
    stcp, chi_4 = calculate_stcp(kinematics, 100)
    print(time() - t)
    fig, ax = plt.subplots()
    plt.plot([i for i in range(1, len(chi_4) + 1)], chi_4)
    ax.set_title('chi_4')
    plt.show()


if __name__ == '__main__':
    main()

