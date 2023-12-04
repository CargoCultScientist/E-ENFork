#AccurateSTFT which appears to perform an accurate Short-Time Fourier Transform (STFT) on a given signal. 
#This is likely used to analyze the frequency components of the signal over time, crucial for ENF extraction.

import numpy as np  # Importing NumPy library for numerical operations
from scipy.fftpack import fft  # Importing FFT function from SciPy library

def AccurateSTFT(Signal, Window, StepPoints, Fs, NFFT):
   # Initialization and Signal Padding
   FrameSize = Window  # Set the frame size to the specified window size
   Signal2 = np.zeros(int(FrameSize / 2) * 2 + len(Signal))  # Create a zero-padded signal
   Signal2[int(FrameSize / 2):int(FrameSize / 2) + len(Signal)] = Signal  # Fill the padded signal with the original signal
   WindowPositions = range(1, len(Signal2) - int(FrameSize) + 2, StepPoints)  # Define window positions
   IF0 = np.zeros(len(WindowPositions))  # Initialize an array for storing instantaneous frequencies

   # Loop through each window position
   for i in range(len(WindowPositions)):
      # Perform FFT on the windowed signal
      B = np.array(fft(Signal2[WindowPositions[i]:WindowPositions[i] + int(FrameSize)], NFFT))
      HalfTempFFT = B[:int(len(B) / 2)]  # Take the first half of the FFT
      absHalfTempFFT = abs(HalfTempFFT)  # Calculate the absolute values of the FFT coefficients

      # Find the peak frequency in the FFT
      PeakLoc = np.argmax(absHalfTempFFT)  # Find the index of the peak in the absolute values
      ValueLeft = HalfTempFFT[PeakLoc - 1]  # Value to the left of the peak
      ValueCenter = HalfTempFFT[PeakLoc]  # Value at the peak
      ValueRight = HalfTempFFT[PeakLoc + 1]  # Value to the right of the peak

      # Calculate correction coefficient for more accurate peak frequency estimation
      CorrectionCoef = -((ValueRight - ValueLeft) / (2 * ValueCenter - ValueRight - ValueLeft)).real  # Calculate the correction coefficient
      IF0[i] = (PeakLoc + CorrectionCoef - 1) * Fs / NFFT  # Calculate and store the instantaneous frequency

   return IF0  # Return the array of instantaneous frequencies



#The signal is padded to ensure that each frame (window) has the same length for the Fourier Transform.
#The function loops through the signal, applying the FFT to each windowed segment.
#It then identifies the peak frequency within each FFT and applies a correction coefficient for more accurate frequency estimation.
#This could be used to track the ENF over time, as the peak frequencies are indicative of the power grid's frequency at each time step.