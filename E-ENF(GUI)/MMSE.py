import numpy as np  # Importing NumPy library for numerical operations
import copy

def MMSE(ConstFs, AStepSize, ENFData, IFtest, AWindowLength):
    ENFData = np.array(ENFData)  # Convert ENFData to a NumPy array
    RecordLength = len(IFtest)  # Get the length of IFtest
    ENFLength = len(ENFData)  # Get the length of ENFData
    OverFact = AStepSize / ConstFs  # Calculate the overlap factor
    MSECalibrated = np.ones(ENFLength - RecordLength)  # Initialize an array for storing mean square errors

    # Comparing segments of the reference ENF data with the test data
    if ENFLength >= RecordLength:
        for i in range(ENFLength - RecordLength):
            IF0 = ENFData[i: i + RecordLength]  # Extract a segment of reference ENF
            TempIF1 = copy.copy(IFtest)  # Create a copy of IFtest
            bbb = IF0 - TempIF1  # Calculate the difference between reference and test ENF
            MSECalibrated[i] = np.linalg.norm(bbb) / RecordLength  # Calculate mean square error

        # Finding the best match (minimum MSE)
        min_score = min(MSECalibrated)  # Find the minimum mean square error
        min_index1 = np.argmin(MSECalibrated)  # Find the index of the minimum error
        FinalIndex = min_index1  # Get the final index of the best match

        # Calculating time indices and scores
        StartTimeIndex = int(OverFact * FinalIndex)  # Calculate the start time index
        MinScore = min_score  # Get the minimum score
        EndTimeIndex = int(StartTimeIndex + OverFact * RecordLength - OverFact)  # Calculate the end time index
        StartSec = int(StartTimeIndex % 60)  # Calculate start seconds
        StartMin = (StartTimeIndex - StartSec) / 60  # Calculate start minutes
        EndSec = int(EndTimeIndex % 60)  # Calculate end seconds
        EndMin = (EndTimeIndex - EndSec) / 60  # Calculate end minutes
        CalibratedIF = ENFData[FinalIndex: FinalIndex + RecordLength]  # Extract the calibrated IF segment

    return CalibratedIF, StartMin, StartSec, EndMin, EndSec, StartTimeIndex, EndTimeIndex, MinScore
