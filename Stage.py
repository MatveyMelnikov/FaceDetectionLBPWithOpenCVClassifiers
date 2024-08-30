class Stage:
    # 1. list of HaarLikeFeatures, 2. float
    def __init__(self, classifiers, threshold):
        self.classifiers = classifiers
        self.threshold = threshold

    def calculate_prediction(self, integral_image, offset, scale):
        score = 0

        for classifier in self.classifiers:
            score += classifier.get_vote(integral_image, offset, scale)

        return True if score > self.threshold else False
