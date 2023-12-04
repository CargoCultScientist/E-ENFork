# This function takes an integer representing a month (e.g., 1 for January, 2 for February, etc.) and 
# returns its string representation with two digits. This is useful for formatting dates in a consistent manner, 
# especially for file naming or data processing where a standardized format is required.


# Function to convert a month's integer value to its string representation
def get_month_str(E_month):
    # Dictionary mapping month integers to their string representations
    month_str = {
        1 : '01',  # January
        2 : '02',  # February
        3 : '03',  # March
        4 : '04',  # April
        5 : '05',  # May
        6 : '06',  # June
        7 : '07',  # July
        8 : '08',  # August
        9 : '09',  # September
        10: '10',  # October
        11: '11',  # November
        12: '12'   # December
    }
    # Return the string representation of the month
    return month_str[E_month]


# This function converts an integer representing a day of the week (e.g., 0 for Monday, 1 for Tuesday, etc.) 
# into its corresponding three-letter string abbreviation. 
# This is typically used for formatting or representing dates where the day of the week is needed in a short form.

# Function to convert a week's integer value to its string abbreviation
def get_week_str(E_week):
    # Dictionary mapping week integers to their string abbreviations
    week_str = {
        0: 'Mon',  # Monday
        1: 'Tue',  # Tuesday
        2: 'Wed',  # Wednesday
        3: 'Thu',  # Thursday
        4: 'Fri',  # Friday
        5: 'Sat',  # Saturday
        6: 'Sun',  # Sunday
    }
    # Return the string abbreviation of the weekday
    return week_str[E_week]

# In summary, these functions serve as utility tools for converting date-related numerical values 
# into standardized string formats, likely for use in file naming, data logging, or any other process
# where dates need to be represented consistently and clearly.