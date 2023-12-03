import numpy as np  # Import the NumPy library for numerical operations
from scipy.fftpack import fft  # Import the FFT function from SciPy library

def AccurateSTFT(Signal, Window, StepPoints, Fs, NFFT):
    # Initialization and Signal Padding
    FrameSize = Window  # Set the frame size to the specified window size
    Signal2 = np.zeros(int(FrameSize / 2) * 2 + len(Signal))  # Create an array to hold the padded signal
    Signal2[int(FrameSize / 2):int(FrameSize / 2) + len(Signal)] = Signal # Pad the original signal with zeros to match the frame size
    WindowPositions = range(1, len(Signal2) - int(FrameSize) + 2, StepPoints) # Calculate positions for overlapping windows
    
    IF0 = np.zeros(len(WindowPositions))  # Initialize an array to store instantaneous frequencies

    # Loop through each window position
    for i in range(len(WindowPositions)):
        B = np.array(fft(Signal2[WindowPositions[i]:WindowPositions[i] + int(FrameSize)], NFFT))  # Perform FFT on the windowed signal
        HalfTempFFT = B[:int(len(B) / 2)]  # Extract the first half of the FFT
        absHalfTempFFT = abs(HalfTempFFT)  # Compute the absolute values of the FFT coefficients

        # Find the peak frequency in the FFT
        PeakLoc = np.argmax(absHalfTempFFT)  # Find the index of the maximum value
        ValueLeft = HalfTempFFT[PeakLoc - 1]  # Value to the left of the peak
        ValueCenter = HalfTempFFT[PeakLoc]  # Value at the peak
        ValueRight = HalfTempFFT[PeakLoc + 1]  # Value to the right of the peak

        # Calculate correction coefficient for more accurate peak frequency estimation
        CorrectionCoef = -((ValueRight - ValueLeft) / (2 * ValueCenter - ValueRight - ValueLeft)).real # Compute the correction coefficient
        IF0[i] = (PeakLoc + CorrectionCoef - 1) * Fs / NFFT  # Calculate and store the instantaneous frequency

    return IF0  # Return the array of instantaneous frequencies
