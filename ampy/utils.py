"""
Module provides methods for reading/saving video data
"""
from tqdm import tqdm

import cv2

def get_video(filename:str, begin_frame:int, end_frame:int, get_each:int) -> list:
    """
        Returns a list with the frames of an input video

        :param filename: the path
        :param bots_number: number of bots in video
        :param begin_frame: frame to begin the processing
        :param end_frame: frame to end the processing
        :param get_each: frames decimation frequency
        :return: list with the frames of the input video
    """

    video_capture = cv2.VideoCapture(filename)

    if begin_frame < 1:
        start_frame = 1
    else:
        start_frame = begin_frame # pragma: no cover

    frames_number = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    if end_frame > frames_number:
        finish_frame = frames_number
    else:
        finish_frame = end_frame # pragma: no cover

    frames = []
    raw_cart_kin = []
    for current_frame in tqdm(range(start_frame, finish_frame + 1, get_each)):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame - 1)
        success, frame = video_capture.read()
        if success: # pragma: no cover
            frames.append(frame)
    return frames

def save_video(filename: str, frames: list, framerate: int = 50) -> None:
    """
       Saves a list with the frames of a video file
        :param filename: name of an output file
        :param frames: list of the frames from the *get_video* method output
        :param framerate: frames per second
    """
    frame_size = frames[0].shape[0:2][::-1]

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, framerate, frame_size)
    for frame in frames:
        out.write(frame)
    out.release()

    print(f"Video saved as {filename}")
