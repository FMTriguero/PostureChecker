#! /Users/carterash/.local/share/virtualenvs/PostureChecker-3vBRJ410/bin/python3

# Posture Checker Program

# TODO:
# 1. Import the model's code
# 2. Test that the model works with single image.
# 3. Test that the model works with live stream images.
# 4. Make custom start and stop for program.
# 5. Build trigger to take 100 photos over a period of 10 mins calculat % good posture


# 1. Import the model's code
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

def check_model(img):
		# Disable scientific notation for clarity
	np.set_printoptions(suppress=True)

		# Load the model
	model = tensorflow.keras.models.load_model('/Users/carterash/PostureChecker/.gitignore/keras_model.h5')

		# Create the array of the right shape to feed into the keras model
		# The 'length' or number of images you can put into the array is
		# determined by the first position in the shape tuple, in this case 1.
	data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

	# 2. Test that the model works with single image.
	image = Image.open(img)

		#resize the image to a 224x224 with the same strategy as in TM2:
		#resizing the image to be at least 224x224 and then cropping from the center
	size = (224, 224)
	image = ImageOps.fit(image, size, Image.ANTIALIAS)

		#turn the image into a numpy array
	image_array = np.asarray(image)

		# display the resized image
	image.show()

		# Normalize the image
	normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

		# Load the image into the array
	data[0] = normalized_image_array

		# run the inference
	pred= model.predict(data)
	return pred



def main():
	prediction = check_model("/Users/carterash/PostureChecker/.gitignore/Test_img.jpg")
	if prediction[0][0] > prediction[0][1]:
		print("Thumbs up!")
	else:
		print("Thumbs down!")


if __name__ == "__main__":
	main()

