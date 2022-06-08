import cv2
import time
import numpy as np
import cv2.aruco as aruco


# Settings

calibrationMatrix = np.load('Cam_Calibration/calibration_matrix.npy')
distortionCoefficient = np.load('Cam_Calibration/distortion_coefficients.npy')

# Environment width and height
r_width = 290
r_height = 172

def findArucoMarkers(frame, draw = True):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, rejected = aruco.detectMarkers(img_gray, arucoDict, parameters=arucoParam,
                                              cameraMatrix=calibrationMatrix, distCoeff=distortionCoefficient)

    detected_markers = list()  # Storage destination of center coordinates for all detected markers with their ID
    field_corners = np.empty((4, 2))  # detect the corner values of the "play field" ->marker ID: 0-3

    if len(bbox) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(bbox, ids): # Loop simultaneously through Bbox and marker IDs
            # Get (x, y) corner pixel positions of single aruco marker (looped for all of them)
            # Positions are returned in order: top-left, top-right, bottom-right and bottom-left
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            # Convert each of the (x, y)-coordinate pairs to integers
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))

            # Calculate Aruco Marker center points
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            # eX = int((topLeft[0] + topRight[0]) / 2.0)
            # eY = int((topLeft[1] + topRight[1]) / 2.0)


            # Save Python dictionary with all relevant information
            detected_markers.append(dict(id=markerID, cx=cX, cy=cY, ex=eX, ey=eY))
            print(detected_markers)
    if draw:
        aruco.drawDetectedMarkers(img, bbox, ids)

    return [detected_markers, field_corners]

def getRealCoordinates(frame, field_corners, detected_markers, p_width=1920, p_height=1080):

    field_corners_vect = np.float32([field_corners[0], field_corners[1], field_corners[2], field_corners[3]])
    true_coordinates = np.float32([[0, 0], [p_width, 0], [p_width, p_height], [0, p_height]])
    trans_mat = cv2.getPerspectiveTransform(field_corners_vect, true_coordinates)
    detected_true_coordinates = np.empty((len(detected_markers), 3))  # create matrix of coordinates

time.sleep(0.2)



"""Main Loop ____________________________________________________________________"""
cap = cv2.VideoCapture("http://192.168.1.36:8080/video")
while True:

    ret, img = cap.read()
    findArucoMarkers(img)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print('test')