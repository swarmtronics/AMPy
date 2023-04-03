import numpy as np

from swarmtronics.video_processor import VideoProcessor
import swarmtronics.three_dimensional_statistics as tds



def main():
    VP = VideoProcessor()
    # VP.set_filename('Tests/test_videos/02_95_[65_bots_PWM_1_exp_2].MP4')
    # kinematics = VP.extract_cartesian_kinematics(65, 1, 200, 1, (), (1, 0))
    # metric_constant = VP.get_metric_constant(3, (1, 0))
    # print(kinematics)
    #VP.set_filename('Tests/test_videos/test_video.MP4')
    #kinematics = VP.extract_cartesian_kinematics(65, 1, 200, 1, (), (1, 0))
    kinematics = np.load("Tests/test_three_dimensional_statistics_files/test_kinematics.npy", allow_pickle=True).tolist()
    VP.extract_cartesian_kinematics(bots_number=45,
                                    )
    answer = tds.get_velocity_correlation(kinematics, 200, 200)
    answer_save = np.array(answer, dtype=object)
    np.save("Tests/test_three_dimensional_statistics_files/get_velocity_correlation_truth.npy", answer_save, allow_pickle=True)


if __name__ == '__main__':
    main()

