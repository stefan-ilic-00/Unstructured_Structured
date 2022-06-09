import threading
import queue
import robot_functions as rfx
from robot_functions import rtde_r, rtde_c
import time
import csv

# Initialize Queue
q = queue.Queue()

# pH measuring flag
thread_flag = 'Stop'

t1 = threading.Thread(target=rfx.robot_read, args=(q, "positions.csv"))
t1.start()
rtde_c.teachMode()
input('Press Enter stop Teach (Freedrive) mode...')
q.put(thread_flag)  # Send Variable to Queue
t1.join()  # Close pH measurement thread
q.queue.clear()  # Clear queue
rtde_c.endTeachMode()

# Stop the RTDE control script
rtde_c.stopScript()