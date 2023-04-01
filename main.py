import numpy as np

from swarmtronics.video_processor import VideoProcessor
import swarmtronics.two_dimensional_statistics as tds



def main():
    VP = VideoProcessor()
    # VP.set_filename('Tests/test_videos/02_95_[65_bots_PWM_1_exp_2].MP4')
    # kinematics = VP.extract_cartesian_kinematics(65, 1, 200, 1, (), (1, 0))
    # metric_constant = VP.get_metric_constant(3, (1, 0))
    # print(kinematics)
    #VP.set_filename('Tests/test_videos/test_video.MP4')
    #kinematics = VP.extract_cartesian_kinematics(65, 1, 200, 1, (), (1, 0))
    kinematics = np.load("Tests/test_videos/test_kinematics.npy", allow_pickle=True).tolist()

    center = (0,0)
    #extended_kinematics = VP.extend_kinematics(kinematics, center)
    answer = tds.get_cluster_dynamics(kinematics)
    # answer = tds.get_chi_4(60, 100, kinematics)
    print(answer)
    answer_save = np.array(answer, dtype=object)
    np.save("Tests/test_videos/get_cluster_dynamics_truth.npy", answer_save, allow_pickle=True)


if __name__ == '__main__':
    main()

