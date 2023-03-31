from swarmtronics.video_processor import VideoProcessor
from swarmtronics.two_dimensional_statistics import get_cluster_dynamics

from matplotlib import pyplot as plt

from time import time
from tqdm import tqdm


def main():
    VP = VideoProcessor()
    VP.set_filename('Tests/test_videos/02_95_[65_bots_PWM_1_exp_2].MP4')
    #VP.set_filename('Tests/test_images/for_corr_test.jpg')
    kinematics = VP.extract_cartesian_kinematics(45, 1, 600, 1, (), (1, 0))
    print(kinematics)
    metric_constant = VP.get_metric_constant(3, (1, 0))
    print(metric_constant)
    t = time()
    c = get_cluster_dynamics(kinematics, metric_constant)
    print(time() - t)
    print(c)
    fig, ax = plt.subplots()
    plt.plot([i for i in range(1, len(c) + 1)], c)
    ax.set_title('clustering coefficient')
    plt.show()


if __name__ == '__main__':
    main()

