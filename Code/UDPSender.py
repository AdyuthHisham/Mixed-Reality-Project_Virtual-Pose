import socket
import time
import math
import random

# IP of the Meta Quest and port to send to
quest_ip = '192.168.0.100'  # Replace with your Quest IP
port = 9050

TOGGLE_ARMBAND = True  # Set to True to enable sending real armband data

if TOGGLE_ARMBAND:
    import numpy as np
    from libemg import streamers
    from libemg.data_handler import OnlineDataHandler

# Read latest quaternion from the BioArmband or generate a random one if data is not available
def armband_quat(odh):
    time.sleep(0.1)
    data, count = odh.get_data(N=10)
    imu = data.get('imu', None)

    if imu is None or imu.shape[0] == 0:
        return "0,0,0,0"

    quat = imu[-1, 3:7]  # [w, x, y, z]
    norm = np.linalg.norm(quat)
    if norm == 0 or np.isnan(norm):
        return "0,0,0,0"

    quat_norm = quat / norm
    # Formatting to a readable string with 4 decimal places
    return ",".join(f"{x:.4f}" for x in quat_norm)


def random_quaternion_string():
    q = [random.uniform(-1, 1) for _ in range(4)]
    norm = math.sqrt(sum(x * x for x in q))
    q_norm = [x / norm for x in q]
    return ",".join(f"{x:.4f}" for x in q_norm)


def start():
    # Initialize the UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if TOGGLE_ARMBAND:
        # Initialize the BioArmband streamer
        streamer, smm = streamers.sifi_bioarmband_streamer(
            emg_notch_freq=50,
            name="BioArmband",
            ecg=False, emg=True, eda=False, imu=True, ppg=False
        )
        odh = OnlineDataHandler(smm)
        odh.reset()
        time.sleep(2)  # Let stream initialize
        return odh, sock
    return None, sock


if __name__ == "__main__":
    odh, sock = start()
    try:
        while True:
            if TOGGLE_ARMBAND:
                message = armband_quat(odh)
            else:
                message = random_quaternion_string()

            sock.sendto(message.encode(), (quest_ip, port))
            # print("Sent:", message)
            time.sleep(0.05)  # 20 Hz
    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print("Error:", e)
    finally:
        sock.close()
        print("Socket closed.")
