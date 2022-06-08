import rtde_receive
import rtde_control
import numpy as np
import time
import sys

# Robot setup
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.1.20")
rtde_c = rtde_control.RTDEControlInterface("192.168.1.20")

def robot_read(q, file_record):
    dt = 1 / 500.0
    rtde_r.startFileRecording(file_record, variables=['actual_q', 'actual_TCP_pose'])
    i = 0
    print('Press Enter stop Teach (Freedrive) mode...')
    while q.empty() == True:
        start = time.time()
        if i % 10 == 0:
            sys.stdout.write("\r")
            sys.stdout.write("{:3d} samples.".format(i))
            sys.stdout.flush()
        end = time.time()
        duration = end - start
        if duration < dt:
            time.sleep(dt - duration)
        i += 1
    rtde_r.stopFileRecording()