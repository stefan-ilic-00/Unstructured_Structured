import cv2
import imutils
from imutils.video import VideoStream

# May Modules
from comms_wrapper import *
import marker_cup_detection

"SETTINGS AND VARIABLES ________________________________________________________________"

# resolution the video capture will be resized to, smaller sizes can speed up detection
video_resolution = (640, 480)

vs = VideoStream(src="http://128.179.193.202:8080/video",
                 resolution=video_resolution,
                 framerate=13,
                 meter_mode="backlit",
                 exposure_mode="auto",
                 shutter_speed=8900,
                 exposure_compensation=2,
                 rotation=0).start()
time.sleep(0.2)

"""Main Loop ____________________________________________________________________"""

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=video_resolution[0], height=video_resolution[1])

    # detected markers are in pixels
    detected_markers, field_corners = marker_cup_detection.findArUcoMarkers(frame)
    # convert to real values
    detected_markers = marker_cup_detection.getRealCoordinates(frame, field_corners, detected_markers)

    cv2.imshow('RobotCamera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.stream.release()
cv2.destroyAllWindows()

# Get Cup Coordinates in robot base reference frame
listCups_data = marker_cup_detection.getCupCoordinates(detected_markers)
