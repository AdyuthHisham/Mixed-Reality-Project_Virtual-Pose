# from libemg.gui import GUI
from libemg.data_handler import OnlineDataHandler
from libemg import streamers
import os
from datetime import datetime
import time
import csv

""" (Old Code - Only for reference) Script to collect and log IMU data from the BioArmband with labels for training. """
def main():
   # Create data handler and streamer
   streamer, smm = streamers.sifi_bioarmband_streamer(emg_notch_freq=50,
                                                   name="BioArmband",
                                                   ecg=False, emg=True, eda=False, imu=True, ppg=False)
   odh = OnlineDataHandler(smm)
   odh.reset()   
   odh.analyze_hardware()

   # Create folders for data collection
   current_time = datetime.now()
   folder_name = current_time.strftime("%m%d%H%M")
   folder_path = os.path.join("Data\\orientation_train", folder_name)
   os.makedirs(folder_path, exist_ok=True)
   print(f"Data folder created at: {folder_path}")
   odh.log_to_file(file_path=(folder_path+'\\'),timestamps=False)
   # Set the file path for CSV logging
   csv_file_path = os.path.join(folder_path, "labels.csv")

   # Write headers to the CSV file
   with open(csv_file_path, mode='w', newline='') as csv_file:
      writer = csv.writer(csv_file)
      writer.writerow(["timestamp", "label"])

   # Start logging labels and timestamps
   time_in_minutes = 0.2  # Set your desired duration in minutes
   end_time = time.time() + (time_in_minutes * 60)

   # Define the label sequence and sleep durations
   sequence = [
      (20, "left", 1)
      # (15, "default", 0),
      # (20, "right", 2),
      # (15, "default", 0),
      # (20, "forward jerk", 7),
      # (15, "default", 0),
      # (20, "END", 0)
   ]

   print(f"default: LABEL 0")
   # Start the timer loop
   #  while time.time() < end_time:
   for duration, label, label_value in sequence:
      # Sleep for the specified duration
      time.sleep(duration)

      # Print the label to the console
      print(f"{label}: LABEL {label_value}")

      # Log the label and timestamp to the CSV
      with open(csv_file_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([datetime.now().strftime("%H:%M:%S"), label_value])

   # Stop the program after the timer expires
   print("Time's up! Exiting program.")
   odh.stop_all()

if __name__ == "__main__":
    main()
