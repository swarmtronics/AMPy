import cv2
from matplotlib import pyplot as plt
from swarmtronics.video_processor import VideoProcessor

vp = VideoProcessor()
filename = 'Tests/test_images/image2.jpg'
cap = cv2.VideoCapture(filename)
success, frame = cap.read()
print(vp._get_raw_cartesian_kinematics_from_frame(frame, ignore_codes=()))


# filename = "D:/YandexDisk.Files/SECOND_SET/00_61_[45_bots_PWM_2_ex_236].MP4"
# cap = cv2.VideoCapture(filename)
# cap.set(cv2.CAP_PROP_POS_FRAMES, 200)
# success, image = cap.read()
# plt.imshow(image)
# cv2.imwrite('Tests/test_images/image2.png', image)
# plt.show()
# print(cap.get(cv2.CAP_PROP_FRAME_COUNT))