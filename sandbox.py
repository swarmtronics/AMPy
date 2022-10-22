import cv2
from matplotlib import pyplot as plt
from swarmtronics.video_processor import VideoProcessor
#1111
vp = VideoProcessor()
filename = 'C0412.MP4'
vp.set_filename(filename)
kin, raw = vp.extract_cartesian_kinematics(45,
                                      0,
                                      10000,
                                      5,
                                      (),
                                      (1,0))
print(len(kin))
print(min([len(el) for el in kin]), max([len(el) for el in kin]))
print(kin)
print(len(raw))
print(min([len(el) for el in raw]), max([len(el) for el in raw]))
print(raw)

#290
# filename = "D:/YandexDisk.Files/SECOND_SET/00_61_[45_bots_PWM_2_ex_236].MP4"
# cap = cv2.VideoCapture(filename)
# cap.set(cv2.CAP_PROP_POS_FRAMES, 200)
# success, image = cap.read()
# plt.imshow(image)
# cv2.imwrite('Tests/test_images/image2.png', image)
# plt.show()
# print(cap.get(cv2.CAP_PROP_FRAME_COUNT))