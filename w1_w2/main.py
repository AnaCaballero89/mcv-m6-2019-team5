import argparse

import cv2
from functional import seq
from matplotlib.lines import Line2D

from methods import week2_nonadaptive, week2_adaptive, week2_soa, week2_soa_mod, week2_nonadaptive_hsv, \
    week2_adaptive_hsv
from metrics import iou_over_time, mean_average_precision
from model import Video
import matplotlib.pyplot as plt
import numpy as np

method_refs = {
    'w2_adaptive': week2_adaptive,
    'w2_nonadaptive': week2_nonadaptive,
    'w2_soa': week2_soa,
    'w2_nonadaptive_hsv': week2_nonadaptive_hsv,
    'w2_adaptive_hsv': week2_adaptive_hsv,
    'w2_soa_mod': week2_soa_mod
}


def main():
    parser = argparse.ArgumentParser(description='Search the picture passed in a picture database.')

    parser.add_argument('method', help='Method to use', choices=method_refs.keys())
    parser.add_argument('--debug', action='store_true', help='Show debug plots')

    args = parser.parse_args()

    method = method_refs.get(args.method)

    video = Video("../datasets/AICity_data/train/S03/c010/frames")

    frames = []
    for im, mask, frame in method(video, **{'debug': args.debug}):
        frames.append(frame)
        #iou = frame.get_detection_iou(ignore_classes=True)
        #print(iou)

        if not args.debug:
            plt.figure(figsize=(12, 8))
            plt.subplot2grid((2, 2), (0, 0))

            im_frame_left = np.copy(im)
            for d in frame.ground_truth:
                cv2.rectangle(im_frame_left, (int(d.top_left[1]), int(d.top_left[0])),
                              (int(d.get_bottom_right()[1]), int(d.get_bottom_right()[0])), (255, 0, 0), thickness=5)
            for d in frame.detections:
                cv2.rectangle(im_frame_left, (int(d.top_left[1]), int(d.top_left[0])),
                              (int(d.get_bottom_right()[1]), int(d.get_bottom_right()[0])), (0, 0, 255), thickness=5)

            plt.imshow(cv2.cvtColor(im_frame_left, cv2.COLOR_BGR2RGB))
            plt.axis('off')
            plt.legend([
                Line2D([0], [0], color=(0, 0, 1)),
                Line2D([0], [0], color=(1, 0, 0)),
            ], ['GT', 'Det'], loc='lower right')

            plt.subplot2grid((2, 2), (0, 1))
            m = cv2.cvtColor(np.copy(mask), cv2.COLOR_GRAY2RGB)
            for d in frame.ground_truth:
                cv2.rectangle(m, (int(d.top_left[1]), int(d.top_left[0])),
                              (int(d.get_bottom_right()[1]), int(d.get_bottom_right()[0])), (0, 0, 255), thickness=5)
            for d in frame.detections:
                cv2.rectangle(m, (int(d.top_left[1]), int(d.top_left[0])),
                              (int(d.get_bottom_right()[1]), int(d.get_bottom_right()[0])), (255, 0, 0), thickness=5)
            plt.imshow(m)
            plt.axis('off')
            plt.legend([
                Line2D([0], [0], color=(0, 0, 1)),
                Line2D([0], [0], color=(1, 0, 0)),
            ], ['GT', 'Det'], loc='lower right')

            plt.subplot2grid((2, 2), (1, 0), colspan=2)
            plt.title('IoU over time' + str(frame.id))
            iou_over_time(frames, ignore_classes=True, show=False)
            axes = plt.gca()
            axes.set_xlim((0, int(2041*.75) + 1))
            axes.set_ylim((0, 1.1))
            plt.legend()

            plt.savefig('../video/{:04d}.png'.format(frame.id))

            #plt.show()
            plt.close()

    iou_over_time(frames, ignore_classes=True)
    print('mAP:', mean_average_precision(frames, ignore_classes=True))


if __name__ == '__main__':
    main()
