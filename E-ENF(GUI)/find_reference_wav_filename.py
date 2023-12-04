# This script dynamically constructs filenames for reference WAV files based on the input date and time parameters. 
# It covers different scenarios, such as when the dates span one day, two days, or more. 
# It carefully calculates the file naming based on the year, month, day, and hour, 
# considering the weekdays and ensuring correct zero-padding for single-digit numbers.
# The find_reference_wav_filename.py script contains a function date_wav_filename that generates reference filenames for WAV files based on the date and time parameters.
# It is used in the context of Electric Network Frequency (ENF) analysis to match recorded data with the appropriate reference ENF data.

from datetime import datetime
from get_str_date import get_month_str, get_week_str

# Function to generate reference WAV filename based on date and time parameters
def date_wav_filename(ENF_Year, ENF_Month, ENF_date_Begin, ENF_date_End, ENF_Hour_Begin, ENF_Hour_End):
    # Convert date parameters to string format for processing
    begin_time_str = ENF_Year + '-' + ENF_Month + '-' + ENF_date_Begin
    end_time_str = ENF_Year + '-' + ENF_Month + '-' + ENF_date_End

    # Convert the date strings to datetime objects and get the corresponding weekdays
    begin_week_int = datetime.strptime(begin_time_str, '%Y-%m-%d').weekday()
    end_week_int = datetime.strptime(end_time_str, '%Y-%m-%d').weekday()

    # Get the string representation of the weekdays
    begin_week_str = get_week_str(begin_week_int)
    end_week_str = get_week_str(end_week_int)

    # Convert date and time parameters to integers for calculation
    ENF_Year_int = int(ENF_Year)
    ENF_Month_int = int(ENF_Month)
    ENF_date_Begin_int = int(ENF_date_Begin)
    ENF_date_End_int = int(ENF_date_End)
    ENF_Hour_Begin_int = int(ENF_Hour_Begin)
    ENF_Hour_End_int = int(ENF_Hour_End)

    # Convert month number to its string representation
    month_str = get_month_str(ENF_Month_int)

    # Generate the reference filename based on the given date and time
    # If the dates are within one day
    if ENF_date_Begin_int == ENF_date_End_int:
        Num_of_File = ENF_Hour_End_int - ENF_Hour_Begin_int
        storeFileStrings = ''
        ENF_date_str = '%02d' % ENF_date_End_int
        for ii in range(Num_of_File):
            newHour = '%02d' % (ENF_Hour_Begin_int + ii + 1)
            storeFileStrings += ENF_Year + '_' + month_str + '_' + ENF_date_str + '_' + end_week_str + '_'+ newHour + '_00_00'
    
    # If the dates are within two days
    elif ENF_date_End_int - ENF_date_Begin_int == 1:
        Num_of_File = 23 - ENF_Hour_Begin_int + ENF_Hour_End_int + 1
        storeFileStrings = ''
        ENF_date_str_B = '%02d' % ENF_date_Begin_int
        ENF_date_str_E = '%02d' % ENF_date_End_int

        for ii in range(23 - ENF_Hour_Begin_int):
            newHour = '%02d' % (ENF_Hour_Begin_int + ii + 1)
            storeFileStrings += ENF_Year + '_' + month_str + '_' + ENF_date_str_B + '_' + end_week_str + '_' + newHour + '_00_00'
        
        for ii in range(Num_of_File - 23 + ENF_Hour_Begin_int):
            newHour = '%02d' % ii
            storeFileStrings += ENF_Year + '_' + month_str + '_' + ENF_date_str_E + '_' + end_week_str + '_' + newHour + '_00_00'

    # If the dates span more than two days
    elif ENF_date_End_int - ENF_date_Begin_int > 1:
        Num_of_File = (ENF_date_End_int - ENF_date_Begin_int - 1) * 24 + 23 - ENF_Hour_Begin_int + ENF_Hour_End_int + 1
        Num_of_Full_Days = ENF_date_End_int - ENF_date_Begin_int - 1
        WeekDayStrings = ''
        for ii in range(Num_of_Full_Days + 2):
            NumOfDate = ENF_date_Begin_int + ii
            time_str = ENF_Year + '-' + ENF_Month + '-' + str(NumOfDate)
            week_int = datetime.strptime(time_str, '%Y-%m-%d').weekday()
            week_str = get_week_str(week_int)
            WeekDayStrings += week_str

        FileStringA, FileStringB, FileStringC = '', '', ''
        ENF_date_str_B = '%02d' % ENF_date_Begin_int
        ENF_date_str_E = '%02d' % ENF_date_End_int

        # Process the first and last day separately from full days in between
        for ii in range(1, 24 - ENF_Hour_Begin_int):
            newHour = '%02d' % (ENF_Hour_Begin_int + ii)
            FileStringA += ENF_Year + '_' + month_str + '_' + ENF_date_str_B + '_' + end_week_str + '_' + newHour + '_00_00'
        
        counterF = 0
        for ii in range(1, ENF_Hour_End_int + 2):
            newHour = '%02d' % counterF
            FileStringC += ENF_Year + '_' + month_str + '_' + ENF_date_str_E + '_' + end_week_str + '_' + newHour + '_00_00'
            counterF += 1

        for ii in range(1, Num_of_Full_Days + 1):
            newDate = '%02d' % (ENF_date_Begin_int + ii)
            for jj in range(1, 25):
                newHour = '%02d' % (jj - 1)
                FileStringB += ENF_Year + '_' + month_str + '_' + newDate  + '_' + WeekDayStrings[ii * 3:ii * 3 + 3] + '_' + newHour + '_00_00'
        
        storeFileStrings = FileStringA + FileStringB + FileStringC

    return storeFileStrings
