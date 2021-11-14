"""This module will generate data that can be used for pre-training the model used for the transform phase of the
training data pipeline. """

import random
import sys
import uuid
import numpy
import numpy as np
import cv2
import json
from multiprocessing import Process, Value, Array
import os
import os.path
import typer
import time
from os import path
import hashlib

# exepected input size of model
input_size = (256 - 64, 256)
# list of photograph sizes found in current data
photo_sizes = [(2016, 1512, 3), (4032, 3024, 3), (640, 480, 3)]


def create_fake_paper_with_writing(pix_per_mm: float, lines: int = 25, red: [] = [255, 164, 164],
                                   blue: [] = [128, 128, 255],
                                   ink: [] = [32, 32, 96], noise: float = 1):
    """Creates an image that is much like written words on ruled paper, also returns a dict of important information"""

    def get_rnd_col(col=[128, 128, 128], noise: int = 128):
        for i in range(len(col)):
            if (noise / 2) + col[i] > 255:
                col[i] = 255 - (noise / 2)

            if (noise / 2) + col[i] < 0:
                col[i] = (noise / 2)

        for i in range(len(col)):
            if (noise / 2) + col[i] > 255:
                raise ValueError
            if (noise / 2) + col[i] < 0:
                raise ValueError
            mod = random.randint(-int(noise / 2), int(noise / 2))
            col[i] = col[i] + mod
        return col

    out_dict = {}

    writing_area = {
        "top_edge": 48 * pix_per_mm,
        "left_edge": 32 * pix_per_mm,
        "right_edge": 215.9 * pix_per_mm,
        "bottom_edge": 279. * pix_per_mm
    }

    writing_area["verts_xy"] = [
        [writing_area["left_edge"], writing_area["top_edge"]],
        [writing_area["right_edge"], writing_area["top_edge"]],
        [writing_area["right_edge"], writing_area["bottom_edge"]],
        [writing_area["left_edge"], writing_area["bottom_edge"]],
    ]

    out_dict["writing_area"] = writing_area

    # randomize colors
    per_random = min(noise / 50.0, 1)
    red = get_rnd_col(col=red, noise=int(32 * per_random))
    ink = get_rnd_col(col=ink, noise=int(64 * per_random))
    blue = get_rnd_col(col=blue, noise=int(64 * per_random))
    white = get_rnd_col(col=[255, 255, 255], noise=int(32 * per_random))

    # Standard 8.5" x 11" paper
    paper_width_mm = 215.9
    paper_height_mm = 279.4

    img = np.ones((round(paper_height_mm * pix_per_mm), round(paper_width_mm * pix_per_mm), 3),
                  dtype="uint8") * np.array(white).astype("uint8")
    print(img.shape)

    def draw_box(box_corners, color: [],scale=True):
        """given the opposite corners of a box, draws a box in img of the specified color"""
        tmp = [box_corners[1], box_corners[3], box_corners[0], box_corners[2]]
        tmp = numpy.array(tmp)
        if scale:
            tmp = (tmp * pix_per_mm).astype("uint")
        else:
            tmp = tmp.astype("uint")

        img[tmp[0]:tmp[1], tmp[2]:tmp[3]] = color

    # draw blue lines, about 7.1 mm spacing between horizontal
    #
    blue_lines_spacing = (out_dict["writing_area"]["bottom_edge"] - out_dict["writing_area"]["top_edge"]) / lines
    for bl in range(lines):
        noise_val = random.random() * (noise / 200)
        blue_lines_thickness_half = .50 + noise_val

        offset = out_dict["writing_area"]["top_edge"] + (bl * blue_lines_spacing)
        blue_line_box = [0,
                         offset - blue_lines_thickness_half,
                         paper_width_mm*pix_per_mm,
                         offset + blue_lines_thickness_half
                         ]
        draw_box(blue_line_box, blue,scale=False)

    # draw ink, this simulates where writing is on the paper
    ink_lines_spacing = (out_dict["writing_area"]["bottom_edge"] - out_dict["writing_area"]["top_edge"]) / lines

    for il in range(lines):
        ink_lines_offset = out_dict["writing_area"]["top_edge"] + (il * ink_lines_spacing) + (.5 * ink_lines_spacing)
        noise_val = (random.random() - .5) * noise
        for x in range(int(32 * pix_per_mm), int(paper_width_mm * pix_per_mm)):
            # print("x: ", x, "/", int(paper_width_mm))
            ymax = int((ink_lines_spacing + (ink_lines_spacing / 2.5)) )
            for y in range(ymax):

                yy = (ink_lines_offset)
                probability_of_ink = (1 - (abs((y / ymax) - .5) * 2)) ** 8
                probability_of_ink = probability_of_ink * .5 * ((1 - (noise / 100)) + (noise_val * .01))
                if random.random() < probability_of_ink:
                    xx = x
                    tx = int(xx)
                    ty = int(yy + y - (ink_lines_spacing  / 2))
                    if ty < img.shape[0]:
                        img[ty, tx] = ink

    # draw red lines, about 32mm in from left
    num_red_lines = random.randint(1, 3)
    # print(num_red_lines)
    red_line_thickness_half = .5
    for rl in range(num_red_lines):
        offset = rl * 1.25
        red_line_box = [32 - red_line_thickness_half + offset,
                        0,
                        32 + red_line_thickness_half + offset,
                        paper_height_mm]
        draw_box(red_line_box, red)

    # draw edges of the piece of paper
    draw_box([0, 0, paper_width_mm, 3], [128, 128, 128])  # top
    draw_box([0, paper_height_mm - 3, paper_width_mm, paper_height_mm], [128, 128, 128])  # bottom
    draw_box([paper_width_mm - 3, 0, paper_width_mm, paper_height_mm], [128, 128, 128])  # right
    draw_box([0, 0, 3, paper_height_mm], [128, 128, 128])  # left
    return img, out_dict


def randomize_photo_transform(img, img_info, photo_size, noise=1):
    """takes a generated sample and transforms it to mimic the appearance of a photo taken by a camera.
    returns the modified image and the set of points
    """

    img_w = img.shape[1]
    img_h = img.shape[0]
    photo_h = photo_size[0]
    photo_w = photo_size[1]
    photo_img = np.ones(shape=(photo_h, photo_w, 3), dtype="uint8") * 164

    pts1 = np.float32([[0, 0], [img_w, 0], [img_w, img_h], [0, img_h]])

    rnd_pts = np.random.rand(8) * (10 * noise)
    pts2 = np.float32([[0 + rnd_pts[0], 0 + rnd_pts[1]],
                       [photo_w - rnd_pts[2], 0 + +rnd_pts[3]],
                       [photo_w - rnd_pts[4], photo_h - rnd_pts[5]],
                       [0 + rnd_pts[6], photo_h - rnd_pts[7]]
                       ])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    cv2.warpPerspective(img, matrix, dsize=(photo_w, photo_h), dst=photo_img, borderMode=cv2.BORDER_TRANSPARENT)

    writing_pts = img_info["writing_area"]["verts_xy"]

    out_writing_pts = []
    for pt in writing_pts:
        src = np.array([[[pt[0], pt[1]]]]).astype("float32")
        out_writing_pts.append( (cv2.perspectiveTransform(src, matrix) - 1).reshape((2)))

    return photo_img, out_writing_pts


def create_one_and_save_it(noise: float = 1, set_name: str = ""):
    """
    function to create a useful sample and save it to the local disk, given an amount of noise and a name for the
    set that it is part of
    """
    if set_name != "":
        set_name = set_name + "\\"

    file_name_base = str(uuid.uuid4())
    file_name_img_X_input = os.path.dirname(__file__) + "\\data\\" + set_name + file_name_base + ".X_input.png"
    file_name_data = os.path.dirname(__file__) + "\\data\\" + set_name + file_name_base + ".json"
    file_name_img_y_label = os.path.dirname(__file__) + "\\data\\" + set_name + file_name_base + ".y_label.png"

    os.makedirs(os.path.dirname(file_name_img_X_input), exist_ok=True)

    img, img_info = create_fake_paper_with_writing(5, 25, noise=noise)
    img2, pts = randomize_photo_transform(img, img_info, photo_sizes[0], noise=noise)
    img3 = cv2.resize(img2, input_size, interpolation=cv2.INTER_AREA)
    scaleX = input_size[0] / photo_sizes[0][1]
    scaleY = input_size[1] / photo_sizes[0][0]
    typer.echo(pts)
    pts = np.array(pts)
    pts[:, 0] = pts[:, 0] * scaleX
    pts[:, 1] = pts[:, 1] * scaleY
    img3 = cv2.cvtColor(img3, cv2.COLOR_RGB2BGR)

    cv2.imwrite(file_name_img_X_input, img3)
    img_hash = hashlib.md5(open(file_name_img_X_input, 'rb').read()).hexdigest()

    img_y_label = cv2.resize(img, input_size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(file_name_img_y_label, cv2.cvtColor(img_y_label, cv2.COLOR_RGB2BGR))

    data = {"y_label_points": pts.tolist(),
            "y_label_image_file": path.basename(file_name_img_y_label),
            "X_input_image_file": path.basename(file_name_img_X_input),
            "X_input_file_hash": img_hash
            }

    with open(file_name_data, 'w') as f:
        json.dump(data, f)


def create_bunch(how_many: int, noise: float = 1, cores: int = 4, noise_start: int = -1, noise_end: int = -1,
                 noise_step: int = -1):
    """function to create many synthetic samples, given a noise level and how many to create."""
    # creates a list of processes waiting to be started and completed.
    if noise_start == -1:
        processes = [Process(target=create_one_and_save_it, args=(noise, "" + str(noise))) for i in
                     range(0, how_many)]
    else:
        processes = []
        noise_range = noise_end - noise_start
        samples_per_step = how_many
        how_many = (noise_range / noise_step) * how_many

        for current_noise in range(noise_start, noise_end, noise_step):
            for sample_i in range(samples_per_step):
                processes.append(
                    Process(target=create_one_and_save_it, args=(current_noise, "" + str(current_noise)))
                )

    # start the initial group
    for i in range(min(cores, len(processes))):
        p = processes[i]
        p.start()

    # monitor list of processes to find opportunities to start no processes and start them, while removing old procs
    todo = how_many
    while todo != 0:
        todo = 0
        free = 0
        for i, p in enumerate(processes):
            if p is not None:
                if p.exitcode is None:
                    todo += 1
                if p.is_alive():
                    # print ("is alive")
                    pass
                if p.exitcode == 0:
                    free += 1
                    processes[i] = None
        started = []

        for i in range(free):
            for i, p in enumerate(processes):
                if p is not None:
                    if p.exitcode is None:
                        if not p.is_alive():
                            if i not in started:
                                print("starting: ", i, "<->", started)
                                started.append(i)
                                p.start()
                                break
        print(todo)
        time.sleep(.10)


# when executed this will be ran, currently creates 10 different noise value sets of 50 each.


if __name__ == "__main__":
    print(os.path.dirname(__file__))
    cores_to_use = max(os.cpu_count() - 2, 1)
    cores_to_use = min(cores_to_use, 12)

    if int(sys.argv[1]) > 1:
        typer.run(create_bunch)
    else:
        create_one_and_save_it(noise=25)
