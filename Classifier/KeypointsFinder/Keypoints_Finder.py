import os
import cv2
import numpy as np
from scipy.ndimage.filters import gaussian_filter

import Classifier.KeypointsFinder.util as util
from Classifier.KeypointsFinder.Config_Reader import config_reader
from Classifier.KeypointsFinder.model import get_testing_model


class KeypointsFinder:
    def __init__(self):
        self.model_path = os.path.join("Classifier", "KeypointsFinder", "model.h5")
        self.colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0],
                       [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255],
                       [0, 0, 255], [85, 0, 255], [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]
        self.model = get_testing_model()
        self.model.load_weights(self.model_path)
        self.params, self.model_params = config_reader()

        self.working_all_peaks = None
        self.working_image = None
        self.canvas = None

    def find_keypoints(self, oriImg):
        """ Start of finding the Key points of full body using Open Pose."""
        self.working_image = oriImg
        multiplier = [x * self.model_params['boxsize'] / oriImg.shape[0] for x in self.params['scale_search']]
        heatmap_avg = np.zeros((oriImg.shape[0], oriImg.shape[1], 19))
        paf_avg = np.zeros((oriImg.shape[0], oriImg.shape[1], 38))
        for m in range(1):
            scale = multiplier[m]
            imageToTest = cv2.resize(oriImg, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            imageToTest_padded, pad = util.pad_right_down_corner(imageToTest, self.model_params['stride'],
                                                                 self.model_params['padValue'])
            input_img = np.transpose(np.float32(imageToTest_padded[:, :, :, np.newaxis]),
                                     (3, 0, 1, 2))  # required shape (1, width, height, channels)
            output_blobs = self.model.predict(input_img)
            heatmap = np.squeeze(output_blobs[1])  # output 1 is heatmaps
            heatmap = cv2.resize(heatmap, (0, 0), fx=self.model_params['stride'], fy=self.model_params['stride'],
                                 interpolation=cv2.INTER_CUBIC)
            heatmap = heatmap[:imageToTest_padded.shape[0] - pad[2], :imageToTest_padded.shape[1] - pad[3],
                      :]
            heatmap = cv2.resize(heatmap, (oriImg.shape[1], oriImg.shape[0]), interpolation=cv2.INTER_CUBIC)
            paf = np.squeeze(output_blobs[0])  # output 0 is PAFs
            paf = cv2.resize(paf, (0, 0), fx=self.model_params['stride'], fy=self.model_params['stride'],
                             interpolation=cv2.INTER_CUBIC)
            paf = paf[:imageToTest_padded.shape[0] - pad[2], :imageToTest_padded.shape[1] - pad[3], :]
            paf = cv2.resize(paf, (oriImg.shape[1], oriImg.shape[0]), interpolation=cv2.INTER_CUBIC)
            heatmap_avg = heatmap_avg + heatmap / len(multiplier)
            paf_avg = paf_avg + paf / len(multiplier)

        all_peaks = []  # To store all the key points which a re detected.
        peak_counter = 0

        for part in range(18):
            map_ori = heatmap_avg[:, :, part]
            map = gaussian_filter(map_ori, sigma=3)

            map_left = np.zeros(map.shape)
            map_left[1:, :] = map[:-1, :]
            map_right = np.zeros(map.shape)
            map_right[:-1, :] = map[1:, :]
            map_up = np.zeros(map.shape)
            map_up[:, 1:] = map[:, :-1]
            map_down = np.zeros(map.shape)
            map_down[:, :-1] = map[:, 1:]

            peaks_binary = np.logical_and.reduce(
                (map >= map_left, map >= map_right, map >= map_up, map >= map_down, map > self.params['thre1']))
            peaks = list(zip(np.nonzero(peaks_binary)[1], np.nonzero(peaks_binary)[0]))  # note reverse
            peaks_with_score = [x + (map_ori[x[1], x[0]],) for x in peaks]
            id = range(peak_counter, peak_counter + len(peaks))
            peaks_with_score_and_id = [peaks_with_score[i] + (id[i],) for i in range(len(id))]

            all_peaks.append(peaks_with_score_and_id)
            peak_counter += len(peaks)

        self.working_all_peaks = all_peaks

    def draw_peaks_over_canvas(self, black_image=False):
        self.set_canvas(black_image)
        for i in range(18):
            for j in range(len(self.working_all_peaks[i])):
                cv2.circle(self.canvas, self.working_all_peaks[i][j][0:2], 4, self.colors[i], thickness=-1)
                
    def set_canvas(self, black_image):
        if black_image:
            self.canvas = np.zeros((self.working_image.shape[0], self.working_image.shape[1], 3), np.uint8)
        else:
            self.canvas = self.working_image

    def test_show_image(self, black_image=False):
        self.draw_peaks_over_canvas(black_image)
        # sometimes opencv will oversize the image when using using `cv2.imshow()`. This function solves that issue.
        screen_res = 1280, 720
        scale_width = screen_res[0] / self.canvas.shape[1]
        scale_height = screen_res[1] / self.canvas.shape[0]
        scale = min(scale_width, scale_height)
        window_width = int(self.canvas.shape[1] * scale)
        window_height = int(self.canvas.shape[0] * scale)
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', window_width, window_height)
        cv2.imshow('image', self.canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
