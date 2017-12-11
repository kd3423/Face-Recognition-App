import dlib
import scipy.misc
import numpy as np
import os
import time
import json
# Face recognition function
def recognize(test_filename):
	start = time.time()
	face_detector = dlib.get_frontal_face_detector()
	end = time.time()
	elapsed = end - start
	print('calling dlib function '+str(elapsed))
	start = time.time()
	# load the pose predictor from dlib
	shape_predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')
	# This lets us detect landmark points on the faces along with the pse/angle of the face.
	end = time.time()
	elapsed = end - start
	print('Time taken to load shape weights '+str(elapsed))

	start = time.time()
	# Get the face encodings
	face_recognition_model = dlib.face_recognition_model_v1('./dlib_face_recognition_resnet_model_v1.dat')
	end = time.time()
	elapsed = end - start
	print('Time taken to load dlib face resnet model '+str(elapsed))
	# Tolerance level for face comparison
	TOLERANCE = 0.55

	# This function takes a list of known faces
	def compare_face_encodings(known_faces, face):
		return (np.linalg.norm(known_faces - face, axis=1) <= TOLERANCE)

	# Below function returns the face encodings through neural network
	def get_face_encodings(path_to_image):
		image = scipy.misc.imread(path_to_image)
		# Detect faces using the face detector
		detected_faces = face_detector(image, 1)
		# print(detected_faces)
		# This allows the neural network to be able to produce similar numbers for faces of the same people, regardless of camera angle and/or face positioning in the image
		shapes_faces = [shape_predictor(image, face) for face in detected_faces]
		# computing the face encodings
		return [np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1)) for face_pose in shapes_faces]

	# This function returns the name of the person whose image matches with the given face else 'Not Found'
	def find_match(known_faces, names, face):
	    matches = compare_face_encodings(known_faces, face)
	    count = 0
	    for match in matches:
	        if match:
	            return names[count]
	        count += 1
	    return 'Not Found'

	def getResultsofRecognition(path_to_image):
		face_encodings_in_image = get_face_encodings(path_to_image)
		print("Number of Faces: "+str(len(face_encodings_in_image)))
		# Make sure there's exactly one face in the image
		# if len(face_encodings_in_image) != 1:
		#     print("Please change image: " + path_to_image + " - it has " + str(len(face_encodings_in_image)) + " faces; it can only have one")
		#     exit()	
		final_match = []
		# Find match for the face encoding found in this test image
		for fa in face_encodings_in_image:
			# print(face_encodings)
			match = find_match(face_encodings, names, fa)
			final_match.append(match)
		# Print the path of test image and the corresponding match
		ak = "No"
		nm = "No"
		if len(face_encodings_in_image) == 0:
			# print(path_to_image, 'No faces in the image')
			d={"Face Present": "No", "Narendra Modi": "No", "Arvind Kejriwal": "No"}
			return d
		else:
			if 'AK' in final_match:
				ak = "Yes"
			if 'NM' in final_match:
				nm = "Yes"
			# print(path_to_image,final_match)
			d = {"Face Present": "Yes", "Narendra Modi": nm, "Arvind Kejriwal": ak}
			return d

	start = time.time()
	if not os.path.exists('weights.out') or not os.path.exists('classes.txt'):
	# Training-------------------------------------------------------------------------
		# Get path to all the known images
		# Filtering on .jpg extension - so this will only work with JPEG images ending with .jpg
		image_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('images/'))
		# Sort in alphabetical order
		image_filenames = sorted(image_filenames)
		# Get full paths to images
		paths_to_images = ['images/' + x for x in image_filenames]
		# List of face encodings we have
		face_encodings = []
		# Loop over images to get the encoding one by one
		for path_to_image in paths_to_images:
		    # Get face encodings from the image
		    face_encodings_in_image = get_face_encodings(path_to_image)
		    # Make sure there's exactly one face in the image
		    if len(face_encodings_in_image) != 1:
		        print("Please change image: " + path_to_image + " - it has " + str(len(face_encodings_in_image)) + " faces; it can only have one")
		        exit()
		    # Append the face encoding found in that image to the list of face encodings we have
		    face_encodings.append(get_face_encodings(path_to_image)[0])
		np.savetxt('weights.out', np.array(face_encodings).view(float))
		np.savetxt('classes.txt', image_filenames, delimiter=" ", fmt="%s") 
	else:
	# Loading weights and class labels
		f = open('classes.txt','r')
		image_filenames = []
		for line in f:
			image_filenames.append(line.rstrip())
		f.close()
		face_encodings = np.loadtxt('weights.out')

	# print(face_encodings)
	# print(image_filenames)
	end = time.time()
	elapsed = end - start
	print('Time taken to Train '+str(elapsed))


	names = [x[:-4] for x in image_filenames]
	return getResultsofRecognition(test_filename)

	# # Testing---------------------------------------------------------------------------
	# # Get path to all the test images
	# # Filtering on .jpg extension - so this will only work with JPEG images ending with .jpg
	# test_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('testArvind/'))
	# # Get full paths to test images
	# paths_to_test_images = ['testArvind/' + x for x in test_filenames]
	# # Get list of names of people by eliminating the .JPG extension from image filenames
	# names = [x[:-4] for x in image_filenames]
	# # Iterate over test images to find match one by one
	# print('Testing on Arvind')
	# for path_to_image in paths_to_test_images:
	# 	print(path_to_image)
	# 	# Get face encodings from the test image
	# 	getResultsofRecognition(path_to_image)

	# print('----------------------------------------------------------------------')
	# print('----------------------------------------------------------------------')
	# test_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('testNarendra/'))
	# # Get full paths to test images
	# paths_to_test_images = ['testNarendra/' + x for x in test_filenames]
	# # Get list of names of people by eliminating the .JPG extension from image filenames
	# names = [x[:-4] for x in image_filenames]
	# # Iterate over test images to find match one by one
	# print('Testing on Narendra')
	# for path_to_image in paths_to_test_images:
	# 	# Get face encodings from the test image
	# 	getResultsofRecognition(path_to_image)

	# print('----------------------------------------------------------------------')
	# print('----------------------------------------------------------------------')
	# test_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('testBoth/'))
	# # Get full paths to test images
	# paths_to_test_images = ['testBoth/' + x for x in test_filenames]
	# # Get list of names of people by eliminating the .JPG extension from image filenames
	# names = [x[:-4] for x in image_filenames]
	# # Iterate over test images to find match one by one
	# print('Testing on Both')
	# for path_to_image in paths_to_test_images:
	# 	# Get face encodings from the test image
	# 	getResultsofRecognition(path_to_image)

	# print('----------------------------------------------------------------------')
	# print('----------------------------------------------------------------------')
	# test_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir('testNone/'))
	# # Get full paths to test images
	# paths_to_test_images = ['testNone/' + x for x in test_filenames]
	# # Get list of names of people by eliminating the .JPG extension from image filenames
	# names = [x[:-4] for x in image_filenames]
	# # Iterate over test images to find match one by one
	# print('Testing on None')
	# for path_to_image in paths_to_test_images:
	# 	# Get face encodings from the test image
	# 	getResultsofRecognition(path_to_image)

# print(json.dumps(recognize('abcde.jpg')))
