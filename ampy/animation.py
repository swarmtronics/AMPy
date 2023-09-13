"""
Module provides the dashboard with evolution of system's parameters
"""
import math
from tqdm import tqdm
from copy import deepcopy

import matplotlib.gridspec as gridspec
import numpy as np
import cv2
from cv2 import aruco
from celluloid import Camera
from matplotlib import pyplot as plt


# parameter for the ArUco recognition & processing

size_of_marker = 0.03
mtx = np.array(
    [
        [2.12753367e03, 0.00000000e00, 7.24147082e02],
        [0.00000000e00, 2.12169339e03, 7.65231051e02],
        [0.00000000e00, 0.00000000e00, 1.00000000e00],
    ]
)

dist = np.array(
    [
        [-4.76057214e01],
        [3.72141657e03],
        [-1.18878543e-02],
        [9.99370683e-03],
        [2.23865999e03],
        [-4.89979090e01],
        [3.86516794e03],
        [-6.64583433e02],
        [0.00000000e00],
        [0.00000000e00],
        [0.00000000e00],
        [0.00000000e00],
        [0.00000000e00],
        [0.00000000e00],
    ]
)

ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11,
}


def get_video(filename, begin_frame, end_frame, get_each):
    """
        Returns a list with the frames of the input video

        :param filename: the path
        :param bots_number: number of bots in video
        :param begin_frame: frame to begin the processing
        :param end_frame: frame to end the processing
        :param get_each: frames decimation frequency
        :return: list with the frames of the input video
    """

    video_capture = cv2.VideoCapture(filename)

    if begin_frame < 1: # pragma: no cover
        start_frame = 1
    else:
        start_frame = begin_frame

    frames_number = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    if end_frame > frames_number: # pragma: no cover
        finish_frame = frames_number
    else:
        finish_frame = end_frame

    frames = []
    raw_cart_kin = []
    for current_frame in tqdm(range(start_frame, finish_frame + 1, get_each)):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 1)
        success, frame = video_capture.read()
        if success: # pragma: no cover
            frames.append(frame)
    return frames

def save_video(output_name: str, frames: list, framerate: int = 50) -> None:
    """
       Saves a list with the frames os a video file
        :param output_name: name of the output file
        :param frames: list of the frames from the get_video method output
        :param framerate: frames per second
    """
    frame_size = frames[0].shape[0:2][::-1]

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_name, fourcc, framerate, frame_size)
    for frame in frames:
        out.write(frame)
    out.release()

    print(f"Video saved as {output_name}")

def create_dashboard(video: list,
                  output_name:str,
                  cart_disp:list,
                  boo:list,
                  stcp:list, 
                  cl_coeff:list,
                  distance:list,
                  angle:list,
                  angle_abs:list,
                  fps:int,
                 ) -> None:
    """
    Creates .gif with simulteneous evolution of the system parameters along with еру original video

    :param video: list of the frames from the get_video method output
    :param output_name: name of the output file
    :param cart_disp: cartesian displacement
    :param boo: bond orientational order parameter
    :param stcp: spatio-temporal correlation parameter
    :param cl_coeff: clustering coefficient
    :param distance: mean distance from the center
    :param angle: mean polar angle
    :param angle_abs: absolute value of the mean polar angle
    :param fps: frames per second
    """
    
    fig, ax = plt.subplots()
    fig = plt.figure(layout="constrained", figsize = (12,8))
    
    gs = gridspec.GridSpec(4, 4, figure=fig)
    
    ax1 = fig.add_subplot(gs[:3, :3])
    ax2 = fig.add_subplot(gs[:1, -1])
    ax3 = fig.add_subplot(gs[1:2, -1])
    ax4 = fig.add_subplot(gs[2:3, -1])
    ax5 = fig.add_subplot(gs[3:4, -1])
    ax6 = fig.add_subplot(gs[-1, 0])
    ax7 = fig.add_subplot(gs[-1, 1])
    ax8 = fig.add_subplot(gs[-1, 2])

    camera = Camera(fig)
    
    time = [i for i in range(len(cart_disp))]

    for i in tqdm(range(len(video))):

        ax1.imshow(video[i])
        ax1.text(x = 10, y = 30, s=f'Frame {i}, {round(i/fps, 2)} sec', color ='white')

        ax1.set_title('Source video')

        ax2.set_title('Cartesian displacement')

        ax3.set_title('Bond orientation parameter')

        ax4.set_title('S-t correlation parameter')

        ax5.set_title('Clustering coefficient')

        ax6.set_title('Mean distance from the center')

        ax7.set_title('Mean polar angle')

        ax8.set_title('Mean polar angle path')

        axs = [ax2, ax3, ax4, ax5, ax6, ax7, ax8]
        data = [cart_disp, boo, stcp, cl_coeff, distance, angle, angle_abs]

        for d, ax in zip(data, axs):
            ax.plot(time[0:i], d[0:i], color="blue")
            ax.axis(xmin = min(time), xmax = max(time), ymin = min(d), ymax = max(d) + 
                 (max(d) - min(d))/10)

        camera.snap()

    animation = camera.animate()
    animation.save(output_name)

def draw_markers(frames: list,
                 marker_type: str = "DICT_7X7_1000"
                 ) -> list:
    """
        Returns the list with the frames and highlighted markers.

        :param frames: list of the frames from the get_video method output
        :param marker_type: Mmrker type of robots
    """
    frames_altered = deepcopy(frames)
    for j in tqdm(range(len(frames_altered))):
        image = frames_altered[j]
        arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[marker_type])
        arucoParams = cv2.aruco.DetectorParameters_create()

        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            image, arucoDict, parameters=arucoParams
        )

        rvecs, tvecs, trash = aruco.estimatePoseSingleMarkers(
            corners, size_of_marker, mtx, dist
        )

        if len(corners) != 0:

            for k in range(len(corners)):
                markerCorner = corners[k]
                markerID = ids[k]
                (topLeft, topRight, bottomRight, bottomLeft) = markerCorner.reshape(
                    (4, 2)
                )

                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                contour = np.array(
                    [
                        list(topLeft),
                        list(bottomLeft),
                        list(bottomRight),
                        list(topRight),
                    ],
                    dtype=np.int32,
                )

                triangle = np.array(
                    [
                        [
                            (list(topLeft)[0] + 3 * list(topRight)[0]) / 4,
                            (list(topLeft)[1] + 3 * list(topRight)[1]) / 4,
                        ],
                        [
                            (list(bottomRight)[0] + 3 * list(topRight)[0]) / 4,
                            (list(bottomRight)[1] + 3 * list(topRight)[1]) / 4,
                        ],
                        list(topRight),
                    ],
                    dtype=np.int32,
                )

                cv2.fillPoly(image, pts=[contour], color=(179, 0, 0))
                cv2.fillPoly(image, pts=[triangle], color=(255, 179, 0))

                cX, cY = int((topLeft[0] + bottomRight[0]) / 2.0), int((topLeft[1] + bottomRight[1]) / 2.0)

                angle = math.atan2(topRight[0] - cX, topRight[1] - cY)
                if angle < 0:
                    angle = 2 * np.pi + angle
                angle = np.degrees(angle)

                font = cv2.FONT_HERSHEY_DUPLEX
                textsize = cv2.getTextSize(str(markerID), font, 1, 2)[0]
                textX = int((cX - textsize[0] / 4.5))
                cv2.putText(
                    image, str(markerID), (textX, cY + 5), font, 0.5, (255, 255, 255), 2
                )
    return frames_altered