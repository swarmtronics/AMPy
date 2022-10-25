import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
import time
from swarmtronics.video_processor import VideoProcessor
from swarmtronics.two_dimensional_statistics import calculate_distance

# directory = "D:/25_10_2022/archive/"
# files = [directory + filename for filename in os.listdir(directory)]
# print(files)
# vp = VideoProcessor()
# for i in range(len(files)):
#     print(i)
#     file = files[i]
#     vp.set_filename(file)
#     kinematics = vp.extract_cartesian_kinematics(1, 1, 1E6, 1, (), (1, 0))
#     arr = np.array(kinematics, dtype=object)
#     np.save("kinematics/" + file.split("/")[-1], kinematics, allow_pickle=True)
# exit(0)

# directory = "C:/Users/Mikhail/PycharmProjects/Swarmtronics/ST_lib/kinematics/"
# files = [directory + filename for filename in os.listdir(directory)]
# for i in range(len(files)):
#     file = files[i]
#     kinematics = np.load(file, allow_pickle=True)
#     #print(len(kinematics))
#     only_bot = []
#     for i in range(len(kinematics)):
#         frame = kinematics[i]
#         for bot in frame:
#             if bot[0] in (85, 24, 68):
#                 only_bot.append([i, bot])
#                 continue
#     #print(len(only_bot))
#     np.save("only_bot/" + file.split("/")[-1][:-8], only_bot, allow_pickle=True)
#
# exit(0)

# directory = "C:/Users/Mikhail/PycharmProjects/Swarmtronics/ST_lib/only_bot/"
# files = [directory + filename for filename in os.listdir(directory)]
#
# for file in files:
#     kinematics = np.load(file, allow_pickle=True)
#     times = []
#     displacement = []
#     init_pos = kinematics[0][1][2]
#     for i in range(len(kinematics)):
#         pos = kinematics[i][1][2]
#         time = kinematics[i][0]
#         times.append(time)
#         displacement.append(calculate_distance(init_pos, pos))
#     fig, ax = plt.subplots()
#     plt.plot(times, displacement)
#     plt.show()
#     to_start, to_stop = list(map(int, input().split(" ")))
#     disps = [(times[i], displacement[i]) for i in range(len(times)) if to_start <= times[i] <= to_stop]
#     np.save("edited/" + file.split("/")[-1][:-4], np.array(disps, dtype=object), allow_pickle=True)
# exit(0)

directory = "C:/Users/Mikhail/PycharmProjects/Swarmtronics/ST_lib/edited/"
def f(filename, framerate):
    dat = np.load(directory + filename, allow_pickle=True)
    time = [(el[0] - dat[0][0]) / framerate for el in dat]
    disp = [el[1] * 0.0903 for el in dat]
    return time, disp

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
fig.set_figwidth(6.69291)
fig.set_figheight(4)

fig.suptitle('Mean square displacement')

ax1.set_title('10% Power')
ax2.set_title('20% Power')
ax3.set_title('30% Power')

ax1.set_xlabel('Time, s')
ax2.set_xlabel('Time, s')
ax3.set_xlabel('Time, s')
ax1.set_ylabel('MSD, cm')

ax1.set_xscale('log')
ax2.set_xscale('log')
ax3.set_xscale('log')
ax1.set_ylabel('log')
ax2.set_yscale('log')
ax3.set_yscale('log')
time1, disp1 = f("01_16_[PWM_1_number_1].npy", 50)
time2, disp2 = f("01_11_[PWM_1_number_2].npy", 30)
time3, disp3 = f("01_08_[PWM_1_number_3].npy", 30)
ax1.plot(time1, disp1, label="1")
ax1.plot(time2, disp2, label="2")
ax1.plot(time3, disp3, label="3")

time1, disp1 = f("01_04_[PWM_2_number_1].npy", 50)
time2, disp2 = f("02_06_[PWM_2_number_2].npy", 30)
time3, disp3 = f("01_04_[PWM_2_number_3].npy", 30)
ax2.plot(time1, disp1)
ax2.plot(time2, disp2)
ax2.plot(time3, disp3)

time1, disp1 = f("01_03_[PWM_3_number_1].npy", 50)
time2, disp2 = f("01_03_[PWM_3_number_2].npy", 30)
time3, disp3 = f("01_03_[PWM_3_number_3].npy", 30)
ax3.plot(time1, disp1)
ax3.plot(time2, disp2)
ax3.plot(time3, disp3)

ax1.legend(handlelength=1)
fig.tight_layout()
plt.savefig('MSD_loglog.pdf')
plt.show()
exit(0)
#290
# filename = "D:/YandexDisk.Files/SECOND_SET/00_61_[45_bots_PWM_2_ex_236].MP4"
# cap = cv2.VideoCapture(filename)
# cap.set(cv2.CAP_PROP_POS_FRAMES, 200)
# success, image = cap.read()
# plt.imshow(image)
# cv2.imwrite('Tests/test_images/image2.png', image)
# plt.show()
# print(cap.get(cv2.CAP_PROP_FRAME_COUNT))