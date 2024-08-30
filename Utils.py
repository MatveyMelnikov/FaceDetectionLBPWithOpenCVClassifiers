import numpy as np
from PIL import Image
from Area import Area
import os


def load_images(path):
    result = []
    for _file in os.listdir(path):
        if _file.endswith('.jpg'):
            result.append(
                np.asarray(Image.open((os.path.join(path, _file))), dtype=np.uint8)
            )

    return result


def convert_images_to_greyscale(images):
    result = []

    for image in images:
        result.append(
            np.transpose(
                np.floor(np.dot(image[..., :3], [0.3, 0.59, 0.11]))
            )
        )

    return result


def merge(areas, min_neighbors):
    result = []
    similar_areas_indexes = [None] * len(areas)
    similar_areas = []
    number_of_similar_areas = 0

    for i in range(0, len(areas)):
        found = False
        # The higher the index, the larger the area. We prefer large areas
        for j in reversed(range(0, i)):
            if is_similar(areas[j], areas[i]):
                found = True
                similar_areas_indexes[i] = similar_areas_indexes[j]
                similar_areas[similar_areas_indexes[i]].append(
                    areas[i]
                )
                break

        if not found:
            similar_areas_indexes[i] = number_of_similar_areas
            similar_areas.append([areas[i]])

            number_of_similar_areas += 1

    for neighbours in similar_areas:
        if len(neighbours) >= min_neighbors:
            result.append(combine_neighbours(neighbours))

    return result


def is_similar(first_area, second_area):
    threshold = first_area.size * 0.2

    delta_x = first_area.x - second_area.x
    delta_y = first_area.y - second_area.y
    delta_size = second_area.size - first_area.size
    delta_size_x = second_area.size - (delta_x + first_area.size)
    delta_size_y = second_area.size - (delta_y + first_area.size)

    # Similar in position and size
    if abs(delta_x) <= threshold and abs(delta_y) <= threshold and \
            abs(delta_size) <= threshold:
        return True
    # The second area includes the first
    if delta_x >= 0 and delta_y >= 0 and delta_size_x >= 0 and delta_size_y >= 0:
        return True

    return False


def combine_neighbours(neighbours):
    result = Area()

    for neighbour in neighbours:
        result.set(
            result.x + neighbour.x,
            result.y + neighbour.y,
            result.size + neighbour.size
        )

    result.set(
        int(result.x / len(neighbours)),
        int(result.y / len(neighbours)),
        int(result.size / len(neighbours))
    )

    return result


def draw_face_area(image, face):
    pixel_size = int(min(image.size[0], image.size[1]) / 55)

    set_dot(image, face.x, face.y, pixel_size)
    set_dot(image, face.x + face.size, face.y, pixel_size)
    set_dot(image, face.x, face.y + face.size, pixel_size)
    set_dot(image, face.x + face.size, face.y + face.size, pixel_size)


def set_dot(image, x, y, size):
    image_size = image.size

    for pixel_y in range(y, y + size):
        for pixel_x in range(x, x + size):
            if pixel_x >= image_size[0] or pixel_y >= image_size[1]:
                continue

            image.putpixel((pixel_x, pixel_y), (0, 255, 0))
