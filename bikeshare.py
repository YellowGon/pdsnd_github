import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city: 
    city  = input('Please enter the name of a city (Chicago, New York City or Washington):\n').lower()
    allowable_cities = ['new york city', 'chicago', 'washington']

    #conditional check in case input is 'New York' rather than 'New York City':
    if city == 'new york':
        city = 'new york city'

    # While loop to keep prompting user for valid city input if input is incorrect:
    while city not in(allowable_cities):
        city  = input('City not valid. Please try again:\n')

    # Confirmation for user of the city they have selected:
    print('\nGreat, lets see some stats for ' + city.title() + '...\n')

    # Get user input for month: 
    month_filter_status = input('Would you like to show data for a specific month (yes/no)?\n')
    while month_filter_status not in ('Yes','yes','No','no'):
        month_filter_status = input('Please enter "Yes" or "No":\n')
    
    if month_filter_status in ('Yes','yes'):
        month_short = input('please enter a month (Jan, Feb, Mar, Apr, May, Jun):\n').lower()
        while month_short not in ('jan','feb','mar','apr','may','jun'):
            month_short = input('Please enter a valid month:\n').lower()

        month_lookup = { 'jan': 'january',
                         'feb': 'february',
                         'mar': 'march',
                         'apr': 'april',
                         'may': 'may',
                         'jun': 'june' }
        month = month_lookup[month_short]
  
    elif month_filter_status in ('No','no'):
        month = 'all'

    # Get user input for day 
    day_filter_status = input('Would you like to filter for a specific weekday (yes/no)?\n')

    while day_filter_status not in ('Yes','yes','No','no'):
        day_filter_status = input('Please enter "Yes" or "No":\n')

    if day_filter_status in ('Yes','yes'):
        day_short = input('please enter a weekday (M, Tu, W, Th, F, Sa, Su):\n')
        day_lookup = { 'M': 'Monday',
                       'Tu': 'Tuesday',
                       'W': 'Wednesday',
                       'Th': 'Thursday',
                       'F': 'Friday',
                       'Sa': 'Saturday',
                       'Su': 'Sunday'  }

        while day_short not in ('M','Tu','W','Th','F','Sa','Su'):
            day_short = input('Please enter a valid day:\n')

        day = day_lookup[day_short]

    elif day_filter_status in ('No','no'):
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
   
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]    

    return df


def time_stats(df,month,day):
    """
    Displays statistics on the most frequent times of travel.
       
    Args:
        (str) df - the filtered dataframe 
        (str) month - used to determine whether or not popular month stat is relevant
        (str) day - used to determine whether or not popular day stat is relevant
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month (only show this stat if df not filtered by month)
    if month in ('All','all'):
        popular_month_int = df['month'].mode()[0]
        months = ['January','February','March','April','May','June']
        popular_month  = months[popular_month_int-1]
        print('The Most Popular Start Month is: ', popular_month)


    # Display the most common day of week (only show this stat if df not filtered by day)
    if day in ('All','all'):
        popular_day = df['day_of_week'].mode()[0]
        print('The most Popular Start Day is: ', popular_day)


    # Display the most common start hour
    df['Start_Hour'] = df['Start Time'].dt.hour
    popular_start_hour = str(df['Start_Hour'].mode()[0])
    print('The most common start hour is: ' + popular_start_hour)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:'+ '\n' + start_station)
    
    # Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is:' + '\n' + end_station)

    # Display most frequent combination of start station and end station trip
    # Create a column that joins stat station to end station for each row first
    df['Combination'] = df['Start Station'] + ' ----> '+ df['End Station']
    combo_stations = df['Combination'].mode()[0]
    print('\nThe most common trip (Start Station to End Station) is:' + '\n' + combo_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in both seconds and then days
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_days = round((total_travel_time / (60*60*24)),2)

    print('Total travel time is: ' +str(total_travel_time) + ' seconds')

    print('In days, this total travel time is: ' + str(total_travel_time_days) + ' days')

    # Display mean travel time
    print('Mean travel time is: ' + str(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(str(df['User Type'].value_counts()))

    # Display counts of gender. Some city day does not include this column, so use error handling 
    try:
        print(str(df['Gender'].value_counts()))
    except:
        print('Sorry, no gender data for this city')
    


    # Display earliest, most recent, and most common year of birth (with error handling as per gender)
    try:
        print('The earliest birth year.... '+ str(int(df['Birth Year'].min())))
        print('The most recent birth year.... '+ str(int(df['Birth Year'].max())))
        print('The most common birth year.... '+ str(int(df['Birth Year'].mode()[0])))
    except:
        print('Sorry, no birth year data for this city')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Ask user if they want to see raw user data
    indiv_data_response = input('would you like to see individual user trip data? (yes/no)\n')

    while indiv_data_response not in ('Yes','yes','No','no'):
        indiv_data_response = input('Please enter "Yes" or "No": ')

    #count number of rows in dataframe
    max_rows = int(df.shape[0])
    printing_row_start = 1
    printing_row_end = 6

    # while loop to keep showing the next 5 rows of data until user either enters something other than yes
    # loop will also stop if the end of the dataframe is reached
    while indiv_data_response in ('Yes','yes') and printing_row_end < max_rows:
        
        print(df.iloc[printing_row_start:printing_row_start + 1,1:8].T)
        print('-----')
        print(df.iloc[printing_row_start + 1:printing_row_start + 2,1:8].T)
        print('-----')
        print(df.iloc[printing_row_start + 2:printing_row_start + 3,1:8].T)
        print('-----')
        print(df.iloc[printing_row_start + 3:printing_row_start + 4,1:8].T)
        print('-----')
        print(df.iloc[printing_row_start + 4:printing_row_start + 5,1:8].T)
        print('-----')

        printing_row_start += 5
        printing_row_end += 5
        indiv_data_response = input('would you like to see more individual user trip data? (yes/no)\n')



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
