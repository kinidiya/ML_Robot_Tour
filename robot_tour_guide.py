import sys
import signal
import time
import os
from joblib import dump, load  # To get the model to the robot

from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.neural_network import MLPClassifier

from mbot_bridge.api import MBot
from utils.camera import CameraHandler
from utils.robot import plan_to_pose, turn_to_theta
from waypoint_writer import read_labels_and_waypoints

# TODO: Update PATH_TO_MODEL.
PATH_TO_MODEL = "model1.joblib"

robot = MBot()


def signal_handler(sig, frame):
    print("Stopping...")
    robot.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def main():
  ch = CameraHandler()  # Initialize the camera

  # NOTE: This code will fail if you have not updated PATH_TO_MODEL above.
  assert os.path.exists(PATH_TO_MODEL), f"Model file {PATH_TO_MODEL} does not exist."
  model = load(PATH_TO_MODEL)
  
  # TODO: Either uncomment and modify the hard coded definitions for
  # waypoints and labels below or run waypoint_writer.py to write
  # waypoints and labels for your current map to output/waypoints.txt.
  #
  # You must handle the case where your model detects a label which is not part of the
  # given course.

  labels, waypoints = read_labels_and_waypoints()  # Load from waypoints.txt

  #labels = [0, 1, 3, 4]
  #waypoints = [[0.12764711678028107, -0.680280864238739, 0.11740349978208542], [0.16826844215393066, -1.213011622428894, -0.10609026998281479], [0.06286311149597168, -0.017251618206501007, -0.04573632404208183], [0.13540320098400116, -1.8279627561569214, 0.12308650463819504]]


  # NOTE: To get the cropped image of a post-it from the camera, do:
  #
  frame = ch.get_processed_image()
  #
  # If a post-it is not detected, frame will be None. Make sure you check for this
  # case. To save the image to the folder "output", pass `save=True` to this
  # function. It will be the last image labeled 08_bordered_frame_X.jpg. Check out
  # the previous images to understand how the preprocessing step works. This might 
  # slow down execution slightly. 
  
  
  # NOTE: To plan a path to a goal position (x and y, in meters), do:
  #
  #     plan_to_pose(x, y, robot)
  #
  # To turn to a given angle (theta, in radians), do:
  #
  #     turn_to_theta(theta, robot)
  #
  # You must turn to the theta after x, y location is reached.
  

  # TODO: Your code here!
  # Write your code to detect the label on a poster at a given waypoint, and use
  # the result to determine which waypoint to visit next. You will need to use the
  # "labels" and "waypoints" variables! When the robot reads a poster with label "0",
  # it should return to the start position (0, 0, 0) and the program should exit.
  #y_pred = -1
  #while(y_pred != 0):
   #   frame = ch.get_processed_image()
    #  y_pred = model.predict([frame])[0]
     # if y_pred == None:
 #         continue
 #     index = 0
  #    for i in (0,3):
   #       if y_pred == labels[i]:
    #         index = i
     #        break
 #     waypoint = waypoints[index]
  #    plan_to_pose(waypoint[0], waypoint[1], robot)
  #    turn_to_theta(waypoint[2], robot)

  while True:
    frame = ch.get_processed_image()
    y_pred = model.predict([frame])[0]

    for i in range(0, len(labels)):
        if (y_pred == None):
            print("no label, quitting")
            quit
        if(y_pred == 0):
            print("returning to start")
            plan_to_pose(0,0,robot)
            turn_to_theta(0,robot)
            quit
        if(y_pred == labels[i]):
            plan_to_pose(waypoints[i][0], waypoints[i][1],robot)
            turn_to_theta(waypoints[i][2], robot)
        

if __name__ == '__main__':
    main()
