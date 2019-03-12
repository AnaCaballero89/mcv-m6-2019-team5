from typing import Iterator

import cv2

from model import Video, Frame
from operations.find_boxes import find_boxes
from operations.gaussian_model import get_background_model, gaussian_model_adaptive, PixelValue
from operations.morphological_operations import closing, opening
from utils import read_detections


def week2_adaptive_hsv(video: Video) -> Iterator[Frame]:
    model_mean, model_std = get_background_model(video, int(2141 * 0.25), total_frames=int(2141 * 0.25),
                                                 pixel_value=PixelValue.HSV)

    ground_truth = read_detections('../datasets/AICity_data/train/S03/c010/gt/gt.txt')

    frame_id = int(2141 * 0.25)
    roi = cv2.cvtColor(cv2.imread('../datasets/AICity_data/train/S03/c010/roi.jpg'), cv2.COLOR_BGR2GRAY)
    for mask in gaussian_model_adaptive(video, int(2141 * 0.25), model_mean, model_std, total_frames=int(2141 * 0.10),
                                        pixel_value=PixelValue.HSV, alpha=1.75, rho=0.4):
        mask = mask & roi
        mask = opening(mask, 3)
        mask = closing(mask, 35)
        mask, detections = find_boxes(mask)

        frame = Frame(frame_id)
        frame.detections = detections
        frame.ground_truth = ground_truth[frame_id]

        mask2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        for detection in detections:
            cv2.rectangle(mask2,
                          (int(detection.top_left[1]), int(detection.top_left[0])),
                          (int(detection.get_bottom_right()[1]), int(detection.get_bottom_right()[0])),
                          (0, 255, 0), 5)
        cv2.imshow('f', mask2)
        cv2.waitKey()

        yield frame

        frame_id += 1
