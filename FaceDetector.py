from OpenCVClassifierParser import OpenCVClassifierParser
import IntegralImage as IntegralImage
from Area import Area
from Utils import merge


class FaceDetector:
    def __init__(self, classifiers_path):
        parser = OpenCVClassifierParser(classifiers_path)
        self.stages = parser.parse()
        self.feature_size = parser.feature_size
        self.all_scales = []

    def detect(
            self,
            image,
            base_scale,
            scale_increment,
            position_increment,
            min_neighbors
    ):
        integral_image = IntegralImage.to_integral_image(image)
        found_faces = []  # Areas

        self.calculate_scales(base_scale, scale_increment, image.shape[0], image.shape[1])

        for stage in self.stages:
            stage.calculate_scaled_features(self.all_scales)

        for scale_index in range(0, len(self.all_scales)):
            step = int(self.all_scales[scale_index] * self.feature_size * position_increment)
            size = int(self.all_scales[scale_index] * self.feature_size)

            for x in range(0, image.shape[0] - size + 1, step):
                for y in range(0, image.shape[1] - size + 1, step):
                    result = True

                    for stage in self.stages:
                        if not stage.calculate_prediction(
                                integral_image, (x, y), scale_index
                        ):
                            result = False
                            break

                    if result:
                        found_faces.append(Area(x, y, size))

        return merge(found_faces, min_neighbors)

    def calculate_scales(self, base_scale, scale_increment, width, height):
        self.all_scales = []
        max_scale = min(width, height) / self.feature_size

        scale = base_scale
        while scale < max_scale:
            self.all_scales.append(scale)
            scale *= scale_increment

        self.all_scales.append(max_scale)
