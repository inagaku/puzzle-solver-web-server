from imageProcessing import *
from puzzleSolver import *

if __name__ == '__main__':
    img = cv2.imread("resources/queens_sample.png")
    cropped = crop_the_chess_board(img) # cropped colored image
    cv2.imshow("Img", cropped)
    cv2.waitKey(0)

    matrix = image_to_matrix(cropped) # 2D array where element is ((x, y), color)
    for row in matrix:
        print(row)

    coordinates = solve_queens(matrix) # a list of coordinates (x, y)

    place_queens(cropped, coordinates)

    cv2.imshow("Img", cropped)
    cv2.waitKey(0)

