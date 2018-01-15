import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import matplotlib 
import cv2

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

#if tf.__version__ != '1.4.0':
#  raise ImportError('Please upgrade your tensorflow installation to v1.4.0!')

from utils import label_map_util

from utils import visualization_utils as vis_util

#matplotlib.use('Agg') 
# What model to download.
#MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
#MODEL_NAME = 'faster_rcnn_nas_coco_2017_11_08'
#MODEL_FILE = MODEL_NAME + '.tar.gz'
#DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
workpath = os.getenv("WORKPATH")

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = workpath + '/exportModel/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = workpath + '/img/tielu_label_map.pbtxt'

NUM_CLASSES = 1

correctImagePath = workpath + "/img/correctIg"

#opener = urllib.request.URLopener()
#opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
#tar_file = tarfile.open(MODEL_FILE)
#for file in tar_file.getmembers():
#  file_name = os.path.basename(file.name)
#  if 'frozen_inference_graph.pb' in file_name:
#    tar_file.extract(file, os.getcwd())


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  print "len of image.data is ", (image.getdata()[0])
  print "im_height is ", im_height
  print "im_width is ", im_width
  newdata = [(i,i,i) for i in image.getdata()]
  #newdata = image.getdata()
  return np.array(newdata).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = workpath + '/img/testImages'
TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, img) for img in os.listdir(PATH_TO_TEST_IMAGES_DIR)]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

correctImageDescriptor = open(correctImagePath + "/correctImageDescriptor1","w")
allTestedScores = []
with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    for image_path in TEST_IMAGE_PATHS:
      image = Image.open(image_path)
      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
      image_np = load_image_into_numpy_array(image)
      print "1111111111111111111111"
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection.
      (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      print "boxes is ", boxes
      print "scores is ", scores
      print "num_detections is ", num
      print "detection_classes is ", classes
      print "np.squeeze(boxes) is ", np.squeeze(boxes)
      print "np.squeeze(classes).astype(np.int32) ", np.squeeze(classes).astype(np.int32)
      print "np.squeeze(scores) is ", np.squeeze(scores)
      print "boxes[0] is ", boxes[0][0]
      print "boxes[0].tolist()", boxes[0][0].tolist()
      print "tuple(boxes[0].tolist())", tuple(boxes[0][0].tolist())
      ymin, xmin, ymax, xmax = tuple(boxes[0][0].tolist())
      im_height = image.size[1]
      im_width = image.size[0]
      (left, right, top, bottom) = (int(xmin * im_width), int(xmax * im_width),
                                  int(ymin * im_height),int(ymax * im_height))
      correctImageDescriptor.write(image_path.split("/")[-1] + ":correct:" + str((left, top,  right, bottom)) + ":" + str(im_width) + ":" + str(im_height) +  "\n")
      allTestedScores.append(scores[0][0])
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          min_score_thresh=0.03,
          use_normalized_coordinates=True,
          line_thickness=8)
      print "222222222222222222222222"
      # plt.figure(figsize=IMAGE_SIZE)
      #plt.imshow(image_np)
      #plt.savefig(image_path.split('.')[0] + '_labeled.jpg')  
      print "image_path is ", image_path
      cv2.imwrite(image_path[:-4] + '_labeled.jpg',image_np)
      print "Done"
    correctImageDescriptor.close()
    allTestedScores.sort()
    print allTestedScores
