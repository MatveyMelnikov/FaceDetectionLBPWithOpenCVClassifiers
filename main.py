from FaceDetector import FaceDetector
from Utils import load_images
from Utils import convert_images_to_greyscale
from Utils import draw_face_area
from PIL import Image


def main():
    # test()

    pos_training_path = 'training_data/faces'
    neg_training_path = 'training_data/nonfaces'
    pos_testing_path = 'training_data/faces/test'
    neg_testing_path = 'training_data/nonfaces/test'

    pos_result_testing_path = 'training_data/faces/test/results/'
    neg_result_testing_path = 'training_data/nonfaces/test/results/'

    images = load_images(pos_testing_path)
    greyscale_images = convert_images_to_greyscale(images)
    face_detector = FaceDetector("classifiers/lbpcascade_frontalface.xml")

    for image_index in range(0, len(greyscale_images)):
        print(f"Image: {image_index}")
        faces = face_detector.detect(greyscale_images[image_index], 1.0, 1.1, 0.1, 3)
        image = Image.fromarray(images[image_index])

        for face in faces:
            print(f"Detect - x: {face.x}, y: {face.y}, size: {face.size}")
            draw_face_area(image, face)

        image.save(pos_result_testing_path + "test" + str(image_index) + ".png")


if __name__ == '__main__':
    main()
