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
    city = input ('\nPlease select for which city you want to see the data. \nYou can choose between Chicago, New York City or Washington:')
    city = city.casefold()
    if city not in CITY_DATA:
        city = input('Unfortunately your input is invalid. Please try again!')
        city = city.casefold()


    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    month = input('\nPlease select for which month from january to june you want to see the data. \nIf you want so see the data from every month type "all": ')
    month = month.casefold()

    if month not in months:
        month = input('Unfortunately your input is invalid. Please try again!')
        month = month.casefold()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('\nPlease select for which day of week you want to see the data. \nIf you want so see the data from every day type "all": ')
    day = day.casefold()
    if day not in days:
        day = input('Unfortunately your input is invalid. Please try again!')
        day = day.casefold()

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
    # Loading the data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])


    # Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # Extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # Filtering the data by month if applicable
    if month != 'all':
        # Useing the index of the months list to get corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filtering the data by month to create new dataframe
        df = df[df['month'] == month]


    # Filtering the data by day of week if applicable
    if day != 'all':
        # Filtering by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('\nFor the selected filter, the most common month is:')
    print(df['month'].mode()[0])

    # TO DO: display the most common day of week
    print('\nFor the selected filter, the most common day of week is:')
    print(df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    print('\nFor the selected filter, the most common start hour is:')
    print(df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station: ', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('The most commonly used end station: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of start and end station trips:\n',df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total trip duration:', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Mean trip duration:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print("No gender data available in this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest year of birth is:', df['Birth Year'].min())
        print('The most recent year of birth is:', df['Birth Year'].max())
        print('The most common year of birth is:', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays raw data when the user wants to see it. Otherwise the user can start the query again."""

    print(df.head())
    next = 0
    while True:
        raw_data = input('\nWould you like to see next five row of raw data? Please type yes or no.\n')
        if raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            raw_data = input('\nWould you like to see five lines of raw data? Please type yes or no.\n')
            if raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Alright, have a nice day!')
            break

if __name__ == "__main__":
    main()
