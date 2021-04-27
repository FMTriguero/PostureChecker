#! /Users/carterash/.local/share/virtualenvs/PostureChecker-3vBRJ410/bin/python3

# Posture Checker Program

# TODO:
# 1. Import the model's code
# 2. Test that the model works with single image.
# 3. Test that the model works with live stream images.
# 4. Make custom start and stop for program.
# 5. Build trigger to take 100 photos over a period of 10 mins calculat % good posture

from Classifier.Classifier import Classifier

# 1. Import the model's code


class PostureChecker:
    def __init__(self, classifier=None):
        self.classifier = classifier
        self.prediction = None

    def test_image(self):
        path_to_picture = "/Users/carterash/PostureChecker/.gitignore/Test_img.jpg"
        self.prediction = self.classifier.testing(image_path=path_to_picture)

    def analyze_results(self):
        if self.prediction[0][0] > self.prediction[0][1]:
            return print("Thumbs up!")
        return print("Thumbs down!")

    def testing(self):
        self.test_image()
        self.analyze_results()


def main():
    classifier = Classifier()
    postureChecker = PostureChecker(classifier=classifier)
    postureChecker.testing()


if __name__ == "__main__":
    main()
