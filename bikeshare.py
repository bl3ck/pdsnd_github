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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\n\nWhat city do you intend to filter by? New York City, Chicago, Washington or all?\n").lower()
    ### The following checks will ensure that the user inputs one of the expected cities.
    while(True):
        if city not in('chicago', 'new york city', 'washington', 'all'):
            city = input('Please enter a city from the option provided\n').lower()
            continue
        else:
            print('You have chosen to filter by {}'.format(city))
            break
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('\n\nWhich of the following months will you want to filter by? January, February, March, April, May, or June?\n').lower()
    # Here we validate user input for month to ensure that it is one of the expected values.
    while(True):
        if(month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'all'):
            print('You have chosen to filter by {}'.format(month))
            break
        else:
            month = input('Please Enter a valid month\n').lower()
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day =  input('Which or the following days ? monday, tuesday, wednesday, thursday, friday, saturday , sunday or all will you want to display the data for?\n').lower()
    # Ensuring that the correct value is inputted for day of the week.
    while(True):
        
        if(day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all'):
            print('You have chosen to filter by {}'.format(day))
            break
        else:
            day = input('Enter Correct day: ').lower()

    
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
    start_time = time.time()
    
    # loads the data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert start time to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    
    # Separating date time components to month, week, day and hour from start time creating new columns
    
    # Months,  1 - 12
    df['month'] = df['Start Time'].dt.month  
    
    # day of week 1 - 7
    df['day_of_week'] = df['Start Time'].dt.dayofweek      
    
    # hour 0 - 23
    df['hour'] = df['Start Time'].dt.hour

    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # filtering by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1       

        df = df[df['Start Time'].dt.month == month]

    # filtering by day of week using the start time
    if day != 'all': 
        df = df[df['Start Time'].dt.weekday_name == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The Most Common Month: ', common_month)

    # TO DO: display the most common day of week
    print('The Most common day of the week: ' + str(df['Start Time'].dt.weekday_name.value_counts().idxmax()))


    # TO DO: display the most common start hour
    print('The Most common start hour:  ' + str(df['Start Time'].dt.hour.value_counts().idxmax()))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    commonly_start_station = df['Start Station'].value_counts().idxmax()
    print('The Most used start station was:',commonly_start_station)


    # TO DO: display most commonly used end station
    commonly_end_station = df['End Station'].value_counts().idxmax()
    print('The Most Commonly used end station was:', commonly_end_station)


    # TO DO: display most frequent combination of start station and end station trip
    freq_combination_station = (df['Start Station'].astype(str) + " to " + df['End Station'].astype(str)).value_counts().idxmax()
    
    print('\n The Most commonly used combination of start and end station: {}\n'.format(freq_combination_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The Total travel time: ', sum(df['Trip Duration'])/(24*60*60), " Days")


    # TO DO: display mean travel time
    df['Trip Duration'].mean()

    print('The mean travel time :', df['Trip Duration'].mean()/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User Types:\n', df['User Type'].value_counts())


    # TO DO: Display counts of gender
    try:
      gender = df['Gender'].value_counts()
      print('\nGender Types:\n', gender)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")


    # TO DO: Display earliest, most recent, and most common year of birth
    if('Birth Year' in df):
        most_common_year = df['Birth Year'].value_counts().idxmax()
        
        earliest_year = df['Birth Year'].min()
        
        most_recent_year = df['Birth Year'].max()
        
        print('\n Oldest Birth Year is {}\n Youngest Birth Year is {}\n Most popular Birth Year is {}\n'.format(int(earliest_year), int(most_recent_year), int(most_common_year)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):    
    """Displays five raw stats at a time, displaying 5 each time and requesting user if they want to view more"""    
    count = 0
    user_input = input('\nDo you want to see 5 lines of raw data? Enter yes or no.\n').lower() 
    while True :
        if user_input == 'yes':
            print(df.iloc[count : count + 5])
            count += 5
            user_input = input('\nDo you want to see more raw data? Enter yes or no.\n')
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

# Starting my program.
if __name__ == "__main__":
	main()
