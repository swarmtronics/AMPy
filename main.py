import numpy as np

from amtoolkit.processing import Processor
import amtoolkit.statistics3d as tds



def main():
    VP = Processor()
    # VP.set_filename('tests/test_videos/02_95_[65_bots_PWM_1_exp_2].MP4')
    # kinematics = VP.extract_cartesian_kinematics(65, 1, 200, 1, (), (1, 0))
    # metric_constant = VP.get_metric_constant(3, (1, 0))
    # print(kinematics)
    #VP.set_filename('tests/test_videos/test_video.MP4')
    #kinematics = VP.extract_cartesian_kinematics(65, 1, 200, 1, (), (1, 0))
    kinematics = np.load("tests/test_statistics3d_files/test_kinematics.npy", allow_pickle=True).tolist()
    VP.cartesian_kinematics(bots_number=45,
                            )
    answer = tds.velocity_correlation(kinematics, 200, 200)
    answer_save = np.array(answer, dtype=object)
    np.save("tests/test_statistics3d_files/velocity_correlation_truth.npy", answer_save, allow_pickle=True)


if __name__ == '__main__':
    main()

