# The ENF_match_GUI.py script seems to be a graphical user interface (GUI) application for matching event-based 
# Electric Network Frequency (E-ENF) data with a reference. This script uses the Tkinter library for the GUI, 
# SoundFile library for audio file processing, and other libraries for signal processing and visualization.


import tkinter as tk
from tkinter.filedialog import askdirectory
import soundfile as sf
import numpy as np
from scipy import signal
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TDMF import TDMF
from find_reference_wav_filename import date_wav_filename
from AccurateSTFT import AccurateSTFT
from scipy.stats import pearsonr
from DV_data import event_files_sampling
# #####################################################
# ################ Generate task

# Function to select the directory of the event data files
def Select_file():
    global filenames
    filenames = askdirectory()  # Opens a dialog to choose directory
    file.set(filenames)  # Updates the text entry with the chosen directory

# Function to select the directory of the ENF reference files
def Select_reference_path():
    global folernames
    folernames = askdirectory()  # Opens a dialog to choose directory
    path.set(folernames)  # Updates the text entry with the chosen directory

# Function to start the ENF matching process
def start_program_button():
    # Configuration constants for the STFT processing
    ConstFs = 1000  # Sampling frequency
    AWindowLength = 16 * ConstFs  # Window length for STFT
    AStepSize = ConstFs  # Step size for STFT
    NFFT = 200 * ConstFs  # Number of FFT points

    # Extracting information from the filename to find the corresponding reference file
    file_path = filenames

    FILENAME = filenames.split('/')[-2]
    ENF_Year, ENF_Month = FILENAME[7:11], FILENAME[12:14]
    ENF_date_Begin = ENF_date_End = FILENAME[15:17]
    ENF_Hour_Begin, ENF_Hour_End = FILENAME[18:20], str(int(FILENAME[18:20]) + 1)
    ENF_second = int(FILENAME[21:23]) * 60 + int(FILENAME[24:26])

    # Finding the reference WAV file
    Ref_filename = date_wav_filename(ENF_Year, ENF_Month, ENF_date_Begin, ENF_date_End, ENF_Hour_Begin, ENF_Hour_End)
    Reference = folernames + '/' + Ref_filename + '.wav'
    data_ref, frequency = sf.read(Reference)

    # Processing the event data files
    Use_data = event_files_sampling(file_path, ConstFs)

    # Bandpass filter to isolate 100Hz component
    b, a = signal.butter(4, [(98 * 2 / ConstFs), (102 * 2 / ConstFs)], 'bandpass')
    data_after_fir = signal.filtfilt(b, a, Use_data)

    # Applying STFT and TDMF to the filtered data
    IFtest1 = np.array(AccurateSTFT(data_after_fir, AWindowLength, AStepSize, ConstFs, NFFT))
    IFtest1 = np.array(TDMF(IFtest1, 21, 0.02))

    # Processing the reference ENF data
    IF = IFtest1 / 2
    if len(IF) + ENF_second > 3600:
        Ref_filename2 = date_wav_filename(ENF_Year, ENF_Month, ENF_date_Begin, ENF_date_End, str(int(ENF_Hour_Begin) + 1), str(int(ENF_Hour_End) + 1))
        Reference2 = folernames + '/' + Ref_filename2 + '.wav'
        data_ref2, frequency = sf.read(Reference2)
        data_ref = np.append(data_ref, data_ref2)

    # STFT processing for reference data
    ConstFs2 = frequency
    AWindowLength2 = 16 * ConstFs2
    AStepSize2 = ConstFs2
    NFFT2 = 200 * ConstFs2
    IF_ref_total = AccurateSTFT(data_ref, AWindowLength2, AStepSize2, ConstFs2, NFFT2)

    # Extracting the relevant portion of the reference ENF
    IF_ref = IF_ref_total[ENF_second:ENF_second + len(IF)]

    # Calculating similarity and Mean Absolute Error (MAE) between the recorded and reference ENFs
    corr = pearsonr(IF, IF_ref)[0] * 100
    MAE = np.sum(np.absolute(IF - IF_ref)) / len(IF)
    titlename = 'Similarity:  ' + '%0.2f' % corr + '%' + '    ' + 'MAE: ' + '%f' % MAE

    # Plotting the results using Matplotlib
    matplotlib.use('TkAgg')
    fig = plt.Figure(figsize=(5, 4), dpi=80)
    draw_set = FigureCanvasTkAgg(fig, master=window)
    ax = fig.add_subplot(111)
    ax.plot(IF, label='record')
    ax.legend(loc='upper right')
    ax.plot(IF_ref, label='reference')
    ax.legend(loc='upper right')
    ax.set_ylim(49.95, 50.05)
    ax.set(title=titlename, ylabel='Frequency (Hz)', xlabel='Time (s)')
    fig.savefig(FILENAME + '.eps', dpi=80, format='eps', bbox_inches='tight')
    draw_set.get_tk_widget().place(x=100, y=100, height=420, width=480)

# Setting up the main window using Tkinter
window = tk.Tk()
window.title('Event-based ENF (E-ENF)')
window.geometry('680x550')

# GUI Components
pixelVirtual = tk.PhotoImage(width=1, height=1)
btn = tk.Button(window, text="Unpacked Events :", image=pixelVirtual, height=20, width=140, compound="c", command=Select_file)
btn.place(x=15, y=20)
file = tk.StringVar()
folder = tk.Entry(window, textvariable=file)
folder.place(x=170, y=23, width=420)

btn2 = tk.Button(window, text="ENF_Reference Folder :", image=pixelVirtual, height=20, width=140, compound="c", command=Select_reference_path)
btn2.place(x=15, y=55)
path = tk.StringVar()
folder = tk.Entry(window, textvariable=path)
folder.place(x=170, y=58, width=420)

start_pro = tk.Button(window, text="Start", image=pixelVirtual, height=50, width=50, compound="c", command=start_program_button)
start_pro.place(x=600, y=22)
window.mainloop()  # Starting the GUI event loop

# This annotated code explains the process of loading event data, selecting reference files, 
# processing the data to extract ENF information, and finally comparing it with the reference ENF data. 
# The results are displayed in a plot, showing the similarity and mean absolute error between the recorded and reference ENF signals. 
# The GUI facilitates easy interaction with the application, allowing users to select files and initiate the processing.