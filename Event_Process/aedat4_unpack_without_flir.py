# The script is a utility for handling event-based data, specifically from .aedat4 files. 
# It unpacks this data into a more accessible format and provides an option to visualize the event data as time surfaces, 
# which can be useful in applications like neuromorphic computing, where event-based sensors like Dynamic Vision Sensors (DVS) are used.
# The provided script is designed to unpack event data from .aedat4 files and optionally visualize the data as time surfaces. 
# It is organized into two main functions: unpack and unpack_events_file. 



from dv import AedatFile
import os
import numpy as np
from event_visualize import events2timesurfaces
from os.path import dirname, abspath



### Main Function: unpack
# This function iterates through files in a specified directory (data_path), 
# processes each .aedat4 file, and saves the unpacked data in a designated location (save_path).

# Function to unpack event data files and optionally visualize them as time surfaces
def unpack(data_path: object, save_path: object, if_visualize: object = True) -> object:
    file_type_list = ['aedat4']  # List of supported file types
    os.chdir(data_path)  # Change the current working directory to the data_path
    aedatfiles = os.listdir()  # List all files in the directory

    for filename in aedatfiles:  # Iterate through each file in the directory
        file_type = filename.split('.')[-1]  # Extract the file extension
        # Process files of the specified type
        if file_type in file_type_list:
            os.chdir(data_path)  # Ensure the current directory is set correctly
            unpack_events_file(filename, save_path)  # Unpack the event data from the file

            # Visualize the data as time surfaces, if enabled
            if if_visualize:
                file_name = os.path.basename(filename).split('.')[0]
                files = save_path + '/' + file_name
                events2timesurfaces(files, fps=30)

    print('All Done')



## Helper Function: unpack_events_file
# This function reads event data from a single .aedat4 file 
# and saves the unpacked data in a structured format in the specified directory.

# Function to unpack a single event data file
def unpack_events_file(file_path, save_path):
    file_name = os.path.basename(file_path).split('.')[0]  # Extract the base name of the file
    print(file_name)

    # Create directories for saving unpacked data, if they don't already exist
    if not os.path.exists(save_path + '/' + file_name):
        os.mkdir(save_path +  '/' + file_name)
    if not os.path.exists(save_path + '/' + file_name + '/events'):
        os.mkdir(save_path + '/' + file_name + '/events')

    # Process and save the event data
    i = 0  # Index for naming saved files
    with AedatFile(file_path) as f:  # Open the .aedat4 file
        for e in f['events'].numpy():  # Iterate through events in the file
            # Convert event data to a numpy array and transpose
            events = np.array([e['timestamp'] / 1e6, e['x'], e['y'], e['polarity']]).T
            # Write event data to a file
            event_file = open(save_path + '/' + file_name + '/events' + '/events{}.txt'.format(i), 'w+')
            for j in range(len(events)):
                event_file.write('%f %d %d %d\n' % (events[j, 0], events[j, 1], events[j, 2], events[j, 3]))
            event_file.close()
            i += 1
    print('To Events Done')


## Execution Block
# The script execution starts here, setting up the data paths and invoking the unpack function.


if __name__ == '__main__':
    # Determine the base path of the script
    path = dirname(dirname(abspath(__file__)))
    # Set up the paths for source data and saving the unpacked data
    data_path = path + '/Events/Raw'
    save_path = path + '/Events/Unpacked'
    # Call the unpack function
    unpack(data_path, save_path)
