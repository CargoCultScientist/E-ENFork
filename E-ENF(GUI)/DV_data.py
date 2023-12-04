# for loading and processing event data captured by an event camera. 
# Event cameras are specialized sensors that record changes in the light intensity, providing information about the 
# timing (when), location (where), and polarity (positive or negative change) of each event. 
# This type of data is particularly useful for high-speed, high-dynamic-range imaging and is relevant to the context of Electric Network Frequency (ENF) analysis

import numpy as np
import os

class Event_txt_loader: # designed to load and process event data stored in text files.
    def __init__(self, path):
        # Loads event data from a given file path.
        # Parses the data into timestamps, x and y coordinates, and polarity.
        # Initializes some basic properties like the size and shape of the event data, 
        # and keeps track of the beginning and final times of the events.
        
        # Load events from the given file path
        self.events = np.loadtxt(path)  # Loading the event data from the file
        self.timestamp = self.events[:, 0]  # Extracting timestamps
        self.xpos = np.int32(self.events[:, 1])  # Extracting x coordinates and casting to int32
        self.ypos = np.int32(self.events[:, 2])  # Extracting y coordinates and casting to int32
        self.polarity = np.uint32(self.events[:, 3])  # Extracting polarity and casting to uint32

        self.size = len(self.timestamp)  # Total number of events
        h, w = 480, 640  # Height and width for event data processing
        self.shape = (h, w)  # Setting the shape of the event data

        # Keeping track of the time range of the events
        self.begin_time = self.timestamp[0]  # First timestamp in the data
        self.final_time = self.timestamp[-1]  # Last timestamp in the data
        self.delta_t_idx = 0  # Index to track the current position in the data
        self.done = False  # Flag to indicate if processing is complete


    def load_delta_t(self, delta_t):
        #Loads events within a given time window (delta_t) starting from the current timestamp.
        # Returns a dictionary containing timestamps, x and y coordinates, and polarity of the events within this window.
        # Load events within a time window starting from the current timestamp  It also handles cases where processing is complete or the time window extends beyond the available data.
        current_time = self.timestamp[self.delta_t_idx]  # Get the current timestamp at the delta_t index
        if self.done or current_time + delta_t > self.final_time:
            # Check if processing is done or if the current timestamp plus delta_t exceeds the final timestamp
            self.done = True  # Set the 'done' flag to True if the conditions are met
            return np.empty((0,), dtype=np.uint32)  # Return an empty NumPy array if done

        finish_time = current_time + delta_t  # Calculate the finish time of the time window
        finish_idx = np.where(self.timestamp < finish_time)[0][-1]
        # Find the index of the last event before or at the finish_time

        # Creating a dictionary to store the relevant event data
        events = dict()
        events['t'] = self.timestamp[self.delta_t_idx:finish_idx+1]  # Extract timestamps within the time window
        events['x'] = self.xpos[self.delta_t_idx:finish_idx+1]  # Extract x coordinates within the time window
        events['y'] = self.ypos[self.delta_t_idx:finish_idx+1]  # Extract y coordinates within the time window
        events['p'] = self.polarity[self.delta_t_idx:finish_idx+1]  # Extract polarity values within the time window
        events['size'] = finish_idx - self.delta_t_idx + 1  # Calculate the size of the event data
        self.delta_t_idx = finish_idx + 1  # Update the delta_t index for the next time window
        return events  # Return the dictionary containing relevant event data

        # For a given timestamp, read the events from the previous time
    def load_last_delta_t(self, time, delta_t):
        # Loads events in a given time window (delta_t) ending at a specific time.
        # Useful for processing events within a specified time range.
        # assert time <= self.final_time, 'time is out of range! Final time is {}'.format(self.final_time)
        
        # Load events in a given time window ending at a specific time
        begin_time = time - delta_t  # Calculate the start time of the time window
        if begin_time < self.begin_time:
            # Check if the calculated start time is earlier than the beginning time of available data
            begin_time = self.begin_time  # Set the start time to the beginning time if it's earlier
        if time > self.final_time:
            finish_time = self.final_time  # Set the finish time to the final time if it's later than the final time
        else:
            finish_time = time  # Otherwise, set the finish time to the specified time

        if finish_time <= begin_time:
            # Check if the finish time is earlier than or equal to the start time
            events = dict()  # Create an empty dictionary to store event data
            events['size'] = 0  # Set the size of the event data to 0
            return events  # Return the empty dictionary if no events fall within the time window

        begin_idx = np.where(self.timestamp >= begin_time)[0][0]
        # Find the index of the first event that occurs after or at the start time
        finish_idx = np.where(self.timestamp <= finish_time)[0][-1]
        # Find the index of the last event before or at the finish time
        print(begin_idx, finish_idx)
        events = dict()
        events['t'] = self.timestamp[begin_idx:finish_idx + 1]
        events['x'] = self.xpos[begin_idx:finish_idx + 1]
        events['y'] = self.ypos[begin_idx:finish_idx + 1]
        events['p'] = self.polarity[begin_idx:finish_idx + 1]
        events['size'] = finish_idx - begin_idx + 1
        return events


    def load_t(self, delta_t):
        # Similar to load_delta_t but ensures events have the same final timestamp
        current_time = self.timestamp[self.delta_t_idx]
        # Get the current timestamp at the delta_t index
        if self.done or current_time + delta_t > self.final_time:
            # Check if processing is done or if the current timestamp plus delta_t exceeds the final timestamp
            self.done = True
            # Set the 'done' flag to True if the conditions are met
            return np.empty((0,), dtype=np.uint32)
            # Return an empty NumPy array if done

        finish_time = current_time + delta_t
        # Calculate the finish time of the time window
        finish_idx = np.where(self.timestamp <= finish_time)[0][-1]
        # Find the index of the last event before or at the finish time
        sampling_time_finish = self.timestamp[finish_idx]

        # Finding the index of the beginning of the current sampling window
        sampling_begin_time_index = finish_idx
        while True:
            if(self.timestamp[sampling_begin_time_index]==sampling_time_finish):
                sampling_begin_time_index = sampling_begin_time_index -1
            else:
                break

        # Creating a dictionary to store the relevant event data
        events = dict()
        events['t'] = self.timestamp[sampling_begin_time_index+1:finish_idx+1]
        # Extract timestamps within the time window
        events['x'] = self.xpos[sampling_begin_time_index+1:finish_idx+1]
        # Extract x coordinates within the time window
        events['y'] = self.ypos[sampling_begin_time_index+1:finish_idx+1]
        # Extract y coordinates within the time window
        events['p'] = self.polarity[sampling_begin_time_index+1:finish_idx+1]
        # Extract polarity values within the time window
        self.delta_t_idx = finish_idx + 1
        # Update the delta_t index for the next time window
        return events


    def files_load_t(self, delta_t, current_time):
    # Sequentially processes event data over time, updating the current time
        if self.done or current_time + delta_t > self.final_time: # Check if processing is done or if the current timestamp plus delta_t exceeds the final timestamp
            self.done = True # Set the 'done' flag to True if the conditions are met
            return np.empty((0,), dtype=np.uint32), current_time  # Return an empty NumPy array and current time if done

        finish_time = current_time + delta_t
        if finish_time < self.begin_time:
            finish_time = self.begin_time # Ensure that finish time is not earlier than the beginning time
        finish_idx = np.where(self.timestamp <= finish_time)[0][-1] # Find the index of the last event before or at the finish time
        sampling_time_finish = self.timestamp[finish_idx]# Find the index of the last event before or at the finish time
        sampling_begin_time_index = finish_idx # Finding the index of the beginning of the current sampling window
        while True:
            if (self.timestamp[sampling_begin_time_index] == sampling_time_finish):
                sampling_begin_time_index = sampling_begin_time_index - 1
            else:
                break

        # Creating a dictionary to store the relevant event data
        events = dict()
        events['t'] = self.timestamp[sampling_begin_time_index + 1:finish_idx + 1]
        # Extract timestamps within the time window
        events['x'] = self.xpos[sampling_begin_time_index + 1:finish_idx + 1]
        # Extract x coordinates within the time window
        events['y'] = self.ypos[sampling_begin_time_index + 1:finish_idx + 1]
        # Extract y coordinates within the time window
        events['p'] = self.polarity[sampling_begin_time_index + 1:finish_idx + 1]
        # Extract polarity values within the time window
        self.delta_t_idx = finish_idx + 1
        # Update the delta_t index for the next time window
        current_time = finish_time
        return events, current_time





######## events_files #########
# This function processes multiple event files for a given source path.
# It iterates through each file in the specified directory, loading the event data using the Event_txt_loader class.
# It processes the event data at a specified frame rate (fps), likely to standardize the time intervals for analysis.
# The function collects a specific attribute from the event data (in this case, the most common polarity) and returns it as a list.
def event_files_sampling(source_path, fps):
    data = []  # Initialize an empty list to store collected data
    path = source_path  # Store the source path in a variable
    path_list = os.listdir(path)  # List all files in the source path
    path_list.sort(key=lambda x: int(x[6:-4]))  # Sort the files based on a numeric part of their names
    j = 0  # Initialize a variable for tracking the first iteration
    for i in path_list:  # Iterate through the sorted list of files
        fliename = path + '/' + i  # Create the full file path
        events_loader = Event_txt_loader(fliename)  # Initialize an event data loader for the file
        if j == 0:  # Check if it's the first iteration
            current_time = events_loader.begin_time  # Select the first current_time
            j = 1
        while True:  # Start an infinite loop for processing event data
            events, current_time = events_loader.files_load_t(1/fps, current_time) # Load events within a specified time window and update current_time
            polarity = []  # Initialize a list to store polarity values
            if events_loader.done:  # Check if all events have been processed
                break
            x, y, t, p = events['x'], events['y'], events['t'], events['p']
            # Extract x, y, t, and p (polarity) from the event data
            try:
                data.append(np.argmax(np.bincount(p)))
                # Calculate and append the most common polarity value to the data list
            except Exception:
                data.append(data[-1])  # Handle exceptions by duplicating the last value
    return data  # Return the collected data as a list


# This file seems to be part of a system that processes event data to extract relevant features for ENF estimation.
# The high temporal resolution of event cameras makes them suitable for capturing the subtle fluctuations in light intensity caused by the ENF.
# By processing this data, the system can potentially extract ENF-related information, which can then be used for various applications like electrical grid monitoring or multimedia forensics.
# Overall, DV_data.py is a key component in handling and preprocessing the high-resolution event data necessary for accurate ENF extraction.