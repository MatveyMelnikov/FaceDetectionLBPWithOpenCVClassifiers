import numpy as np


# In this case, the x and y coordinates are swapped.

def to_integral_image(img_arr):
    integral_image_arr = np.zeros((img_arr.shape[0] + 1, img_arr.shape[1] + 1), dtype=int)
    for x in range(img_arr.shape[1]):
        row_sum = 0

        for y in range(img_arr.shape[0]):
            value = int(img_arr[y, x])

            integral_image_arr[y + 1, x + 1] = integral_image_arr[y + 1, x] + row_sum + value

            row_sum += value

    return integral_image_arr


def to_integral_image_of_squares(img_arr):
    integral_image_of_squares = np.zeros((img_arr.shape[0], img_arr.shape[1]))
    for x in range(img_arr.shape[1]):
        row_sum = 0

        for y in range(img_arr.shape[0]):
            value_square = np.uint64(pow(img_arr[y, x], 2)) >> np.uint64(8)

            integral_image_of_squares[y, x] = \
                (integral_image_of_squares[y, x - 1] if x > 0 else 0) + \
                row_sum + value_square

            row_sum += value_square

    return integral_image_of_squares


def sum_region(integral_img_arr, rect):
    if rect.size == (1, 1):
        return integral_img_arr[rect.pos]

    top_left = (rect.pos[0], rect.pos[1])
    top_right = (rect.pos[0] + rect.size[0], rect.pos[1])
    bottom_left = (rect.pos[0], rect.pos[1] + rect.size[1])
    bottom_right = (rect.pos[0] + rect.size[0], rect.pos[1] + rect.size[1])

    return integral_img_arr[top_left] - integral_img_arr[top_right] - \
        integral_img_arr[bottom_left] + integral_img_arr[bottom_right]
