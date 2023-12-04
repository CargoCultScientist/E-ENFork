# The script events2timesurfaces is designed to process event data from text files and convert them into time surface images. 
# A time surface is a visual representation of spatio-temporal event data, commonly used in the analysis of data from 
# event-based sensors like Dynamic Vision Sensors (DVS). 
# The script includes a main function events2timesurfaces and utilizes helper functions and classes like Event_txt_loader and 
# event_timesurface from the read_txt module. 

# Overview:
# The script processes event data files located in a specified directory.
# Each file is read and processed to generate a time surface image, which is a 2D representation of the event data.
# The time surfaces are saved as PNG images in a designated directory.
# This process can be useful in analyzing data from event-based vision systems, where traditional frame-based methods are not suitable.
# Dependencies:
# numpy: Used for numerical operations on arrays.
# cv2 (OpenCV): Used for image processing and saving images.
# read_txt: A module containing the Event_txt_loader class and event_timesurface function, which are essential for reading the event data and generating time surfaces.
# tqdm: A library for displaying progress bars in loops.
# This script is particularly relevant in the field of neuromorphic engineering and event-based computer vision, 
# where it provides a means to visualize and analyze high-speed, sparse visual information captured by event cameras.

# Function: events2timesurfaces
# This function processes a series of event data files and converts them into time surface images.


import numpy as np
import cv2
import os
from read_txt import Event_txt_loader, event_timesurface
from tqdm import tqdm

# Function to convert event data into time surface images
def events2timesurfaces(source_path, fps=30):
    path = source_path + '/events'  # Path where the event data files are stored
    path_list = os.listdir(path)  # List of files in the directory
    path_list.sort(key=lambda x: int(x[6:-4]))  # Sorting the files numerically

    events_finish = dict()  # Dictionary to store the final event data
    j = 0  # Counter to track the first iteration
    img_height, img_width = 480, 640  # Dimensions for the time surface images
    n = 0  # Counter for naming output image files

    for i in tqdm(path_list):  # Iterate over the files with a progress bar
        filename = path + '/' + i  # Full path to the event file
        event2ts_save_path = source_path + '/event2ts'  # Path to save time surface images

        # Create the directory for saving time surface images if it doesn't exist
        if not os.path.exists(event2ts_save_path):
            os.mkdir(event2ts_save_path)

        # Load event data from the file
        events_loader = Event_txt_loader(filename)
        
        # Select the first current time from the first file
        if j == 0:
            current_time = events_loader.begin_time
            event_formal = dict()
            j = 1
        
        while True:
            # Handle the case for the first iteration
            if j == 1 and current_time < events_loader.begin_time:
                event_formal = event_formal
            else:
                event_formal = dict()
            
            # Load event data for a specific time interval
            events, current_time = events_loader.files_load_delta_t(1 / fps, current_time)

            # Check if all events have been processed
            if events_loader.done:
                event_formal = events
                break

            # Combine the current and previous events
            if event_formal:
                combined_keys = event_formal.keys() | events.keys()
                combined_keys.remove('size')
                events = {key: np.hstack((event_formal[key], events[key])) for key in combined_keys}
            
            # Generate a time surface image from the events and save it
            img = event_timesurface(events, img_height, img_width)
            cv2.imwrite(event2ts_save_path + '/%06d.png' % n, img)
            n += 1

    cv2.destroyAllWindows()  # Close all OpenCV windows
    print('To Timesurfaces Done')  # Print completion message
