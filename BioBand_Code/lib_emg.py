from libemg.gui import GUI
from libemg.data_handler import OnlineDataHandler

from libemg import streamers

#Create Folders for data collection
import os
from datetime import datetime

import time  # For the timer

def main():
   # Create data handler and streamer
   streamer, smm = streamers.sifi_bioarmband_streamer(emg_notch_freq=50,
                                                      name="BioArmband",
                                                      ecg=False, emg=True, eda=False, imu=True, ppg=False)
   odh = OnlineDataHandler(smm)   
   odh.analyze_hardware()

   exit()
   current_time = datetime.now()
   folder_name = current_time.strftime("%m%d%H%M")
   folder_path = os.path.join("Data\\orientation_3", folder_name)
   os.makedirs(folder_path, exist_ok=True)
   print(folder_path)
   odh.log_to_file(file_path=(folder_path+'\\'),timestamps=False)
   
   # Set timer for 'time_in_minutes'
   time_in_minutes = 3  # Set your desired duration in minutes
   time.sleep(time_in_minutes * 60)  # Sleep for the specified time

   # Stop the program after the timer expires
   print("Time's up! Exiting program.")
   odh.stop_all()
   
if __name__ == "__main__":
   main()
