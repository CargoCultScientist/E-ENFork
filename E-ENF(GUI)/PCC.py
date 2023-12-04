# The PCC.py script defines a function PCC (Pearson Correlation Coefficient), 
# which is used to compare an estimated Electric Network Frequency (ENF) signal 
# (IFtest) with a reference ENF signal (ENFData). It calculates the Pearson correlation coefficient
# for different segments of the reference ENF to find the segment that best matches the estimated ENF.


import numpy as np
import copy
from scipy.stats import pearsonr
from TDMF import TDMF

# Function to find the best matching segment of the reference ENF to the estimated ENF using Pearson Correlation Coefficient
def PCC(ConstFs, AStepSize, ENFData, IFtest, AWindowLength):
    # Convert the ENF data to a NumPy array for processing
    ENFData = np.array(ENFData)
    RecordLength = len(IFtest)  # Length of the estimated ENF
    ENFLength = len(ENFData)  # Length of the reference ENF
    OverFact = AStepSize / ConstFs  # Factor to scale the index to time

    # Initialize an array to store the Pearson correlation coefficient for each segment
    Calibrated = np.ones(ENFLength - RecordLength)

    # Only proceed if the reference ENF is longer than the estimated ENF
    if ENFLength >= RecordLength:
        for i in range(ENFLength - RecordLength):
            IF0 = ENFData[i: i + RecordLength]  # Segment of the reference ENF
            TempIF1 = copy.copy(IFtest)  # Copy of the estimated ENF
            TempIF1 = np.array(TempIF1)  # Convert to a NumPy array
            # Calculate the Pearson correlation coefficient for the segment
            Calibrated[i] = pearsonr(IF0, TempIF1)[0]

        m = Calibrated  # Array of Pearson correlation coefficients
        # Find the index of the segment with the highest correlation
        max_score = m[0]
        max_index = 0
        for ii in range(ENFLength - RecordLength):
            if m[ii] > max_score:
                max_score = m[ii]
                max_index = ii

        # Determine the start and end indices of the best matching segment
        FinalIndex = max_index
        StartTimeIndex = int(OverFact * FinalIndex)
        MaxScore = max(Calibrated)
        EndTimeIndex = int(StartTimeIndex + OverFact * RecordLength - OverFact)
        StartSec = int(StartTimeIndex % 60)
        StartMin = (StartTimeIndex - StartSec) / 60
        EndSec = int(EndTimeIndex % 60)
        EndMin = (EndTimeIndex - EndSec) / 60
        # Extract the best matching segment of the reference ENF
        CalibratedIF = ENFData[FinalIndex: FinalIndex + RecordLength]

    # Return the best matching segment and its corresponding start and end times, along with the maximum correlation score
    return CalibratedIF, StartMin, StartSec, EndMin, EndSec, StartTimeIndex, EndTimeIndex, MaxScore
