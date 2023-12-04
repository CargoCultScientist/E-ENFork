# The TDMF function in the provided script appears to be a custom implementation of a smoothing and detrending function, 
# possibly a form of the Temporal Derivative Median Filter (TDMF). 
# This filter is commonly used to smooth a signal while preserving its edges, and it can be particularly effective in reducing noise and outliers. 
# Functionality:
# Padding: The function first pads the input signal at both ends to ensure that the filtering window fits within the range of the input data, even at the boundaries.
# Median Filtering: For each point in the input signal, a segment of the signal (of length specified by Order) centered around that point is extracted,
# sorted, and the median value of this segment is computed. This step helps to smooth out the signal.
# Detrending: The filtered signal is subtracted from the original signal to detect significant deviations
# Thresholding: If the absolute value of the detrended signal at a particular point is less than or equal to the specified threshold, 
# the original signal value is retained; otherwise, the filtered (median) value is used. 
# This step helps to preserve the signal's original characteristics while smoothing out large deviations likely caused by noise or outliers.


import math

# Function for smoothing and detrending a signal
def TDMF(Input, Order, Threshold):
    # Length of the input signal
    InputLength = len(Input)
    
    # Initialize arrays for the filtered input and the final output
    FilteredInput = [None] * InputLength
    Output = [None] * InputLength

    # Calculate padding length based on the filter order
    PaddingLength = int((int(Order) - 1) / 2)

    # Create padding for the beginning and end of the signal
    Oneline = [1] * PaddingLength
    PadInput = [Oneline[i] * Input[0] for i in range(PaddingLength)]
    PadInput[PaddingLength:PaddingLength + InputLength] = Input
    PadInput[PaddingLength + InputLength:PaddingLength * 2 + InputLength] = [Oneline[i] * Input[-1] for i in range(PaddingLength)]

    # Apply the median filter to the input signal
    for i in range(InputLength):
        Seg = PadInput[i: i + Order]  # Extract the segment for filtering
        Seg.sort()  # Sort the segment
        # Pick the median value from the sorted segment
        FilteredInput[i] = Seg[math.ceil((Order - 1) / 2)]

    # Detrend the input signal by subtracting the filtered signal from the original signal
    DetrendedInput = [FilteredInput[ii] - Input[ii] for ii in range(InputLength)]

    # Apply thresholding to determine the final output
    for i in range(InputLength):
        if abs(DetrendedInput[i]) <= Threshold:
            Output[i] = Input[i]  # Keep original value if within the threshold
        else:
            Output[i] = FilteredInput[i]  # Use filtered value if outside the threshold

    return Output
