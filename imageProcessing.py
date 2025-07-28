import cv2
import numpy as np
import base64
import math

def image_to_matrix(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, 0)

    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [c for c in contours if 1000 < cv2.contourArea(c) < 50000]

    def contour_center(cnt):
        M = cv2.moments(cnt)
        if M['m00'] == 0:
            return (0, 0)
        return (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

    centers = [contour_center(cnt) for cnt in contours]
    sorted_centers = []

    for cent in centers:
        cv2.circle(img, cent, 5, (255, 0, 0), 10)

    cv2.imshow("Img", img)
    cv2.waitKey(0)

    coordinates_threshold = 10
    while len(centers) > 0:
        top_left = min(centers, key=lambda x: x[0] + x[1])

        condition = lambda x: math.fabs(x[1] - top_left[1]) < coordinates_threshold
        extracted = []

        for center in centers[:]:
            if condition(center):
                extracted.append(center)
                centers.remove(center)

        sorted_centers.extend(sorted(extracted, key=lambda x: x[0]))

    grid = [(center, gray[center[1], center[0]]) for center in sorted_centers]

    N = math.floor(math.sqrt(len(sorted_centers)))

    i = 0
    j = 0

    board = [[0 for _ in range(N)] for _ in range(N)]

    for cell in grid:
        i += j // N
        j = j % N
        board[i][j] = cell
        j += 1

    return board

def crop_the_chess_board(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)

    _, threshold = cv2.threshold(edges, 127, 255, 0)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    biggest_coutour = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # Filter small contours
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4 and cv2.isContourConvex(approx):
                if area > max_area:
                    biggest_coutour = approx
                    max_area = area

    x, y, w, h = cv2.boundingRect(biggest_coutour)
    cropped = img[y:y + h, x:x + w]

    return cropped

def place_queens(img, coordinates):
    queen_img = cv2.imread("resources/queen_image.png", cv2.IMREAD_UNCHANGED)

    original_height, original_width = queen_img.shape[:2]
    ratio = (img.shape[:1][0] / len(coordinates)) / max(original_width, original_height) * 0.9
    resized_queen = cv2.resize(queen_img, (int(original_width * ratio), int(original_height * ratio)),
                               interpolation=cv2.INTER_AREA)

    h, w = resized_queen.shape[:2]
    resized_queen = cv2.resize(queen_img, (w // 2 + w // 2, h // 2 + h // 2))

    queen_img = resized_queen[..., :3]
    queen_mask = resized_queen[..., 3:] / 255.0  # Normalize alpha to [0,1]

    for (x, y) in coordinates:
        # Region of interest in background
        roi = img[y - h // 2: y + h // 2, x - w // 2: x + w // 2]

        # Blend the images
        blended = (queen_mask * queen_img + (1 - queen_mask) * roi).astype(np.uint8)

        img[y - h // 2: y + h // 2, x - w // 2: x + w // 2] = blended
