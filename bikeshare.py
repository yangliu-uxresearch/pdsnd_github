#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import calendar 
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

# Step 1. Define get_filters
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print(" "*40)
    
    # Get the name of the city
    while True:
        city = input("Please enter the city you would like to explore into, from this list: New York City, Chicago, or Washington.\n")
        if city.title() not in ('New York City', 'Chicago', 'Washington'): 
            print ("***Sorry please try again. Pay attention to the spelling.")
            continue
        else: 
            print ("Thanks for picking the city:", city.title())
            print(" "*40)
            break 

    # Get the month filter, and day-of-week filter 
    while True:
        month = input("Next, please enter the month you would like to explore into, from this list: January, February, March, April, May, June, or All Months.\n")
        if month.title() not in ('January', 'February', 'March', 'April', 'May', 'June', 'All Months'):
            print("***Sorry please try again. Pay attention to the spelling.")
            continue
        else:
            print ("Thanks for picking the month:", month.title())
            print(" "*40)
            break

    # Get the day-of-week filter 
    while True:
        day = input("Last, please enter a weekday you would like to explore into, from this list: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All Days.\n")
        if day.title() not in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All Days'):
            print("***Sorry please try again. Pay attention to the spelling.")
            continue
        else:
            print ("Thanks for picking the day:", day.title())
            print(" "*40)
            break

    # End step 1
    print("The data you've selected is for:", (city.title(), month.title(), day.title()))
    print('\nLoading the results of analysis...\n')
    print('_'*40)
    return city, month, day

    
# Step 2. Define load_data 
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
    # load data for the specified city and filters by month and day    
    df = pd.read_csv(CITY_DATA[city.title()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month.title() != 'All Months':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day.title() != 'All Days':
        df = df[df['day_of_week'] == day.title()]
    
    return df

    
# Step 3. Define time_stats
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    
    # display most common month/day of week/start hour
    session_start_time = time.perf_counter()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour 
    popular_month = df['month'].mode()[0]
    popular_month = calendar.month_abbr[popular_month]
    popular_day = df['day_of_week'].mode()[0]
    popular_hour = df ['hour'].mode()[0]
    print('The most common month for bikeshare is %s.' % popular_month)
    print('The most common day of week for bikeshare is %s.' % popular_day)
    print('The most common start hour for bikeshare is %s.' % popular_hour)
    print(" "*40)
    
    duration = time.perf_counter() - session_start_time
    print("This took %s seconds." % duration) 
    print("_"*40)

    
# Step 4. Define station_stats 
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
   
    # display most commonly used start station 
    session_start_time = time.perf_counter()      
    start_station_by_order = df['Start Station'].value_counts()
    most_popular_start_station = start_station_by_order.idxmax()
    popularity_start_station = start_station_by_order.max()
    print("The most popular start station is %s." % most_popular_start_station)
    print("It's been used for %s times." % popularity_start_station)
    print(" "*40)
    
    # dispaly most commonly used end station
    end_station_by_order = df['End Station'].value_counts()
    most_popular_end_station = end_station_by_order.idxmax()
    popularity_end_station = end_station_by_order.max()
    print("The most popularend station is %s." % most_popular_end_station)
    print("It's been used for %s times." % popularity_end_station)
    print(" "*40)
    
    # display most frequent combination of start station and end station trip 
    df['start2end_stations'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    trip_by_order = df['start2end_stations'].value_counts()
    most_popular_trip = trip_by_order.idxmax()
    popularity_trip = trip_by_order.max()
    print("The most popular combination of start station and end station is %s." % most_popular_trip)
    print("It's been taken for %s times." % popularity_trip)
    print(" "*40)
          
    duration = time.perf_counter() - session_start_time
    print("This took %s seconds." % duration) 
    print("_"*40)


# Step 5. Define trip_duration_stats 
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
     
    #display total travel time and mean travel time
    session_start_time = time.perf_counter()

    total_trip_duration = df['Trip Duration'].sum()
    total_trip_duration_in_days = total_trip_duration/60/60/24
    mean_trip_duration = df['Trip Duration'].mean()
    mean_trip_duration_in_hours = mean_trip_duration/60/60 
    print("Total travel time is {} seconds, that is, {} days.".format(total_trip_duration, total_trip_duration_in_days)) 
    print("Mean travel time is {} second, that is, {} hours.". format(mean_trip_duration, mean_trip_duration_in_hours ))
    print(" "*40)

    duration = time.perf_counter() - session_start_time
    print("This took %s seconds." % duration) 
    print("_"*40) 

# Step 6. Define user_stats 
# Note: for Washington, no data for gender and year of bith.
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    # Display counts of user types; counts of gender; and earliest, most recent, and most common year of birth

    session_start_time = time.perf_counter()

    user_type_count = df['User Type'].value_counts() 
    user_type_count_frame = user_type_count.to_frame()
    subscriber_count = user_type_count_frame.at['Subscriber', 'User Type']
    customer_count = user_type_count_frame.at['Customer', 'User Type']
    print("There are {} subscribers, and {} customers.". format(subscriber_count, customer_count))

    if df.columns[7] == 'Gender': 

        gender_count = df['Gender'].value_counts() 
        gender_count_frame = gender_count.to_frame()
        male_count = gender_count_frame.at['Male', 'Gender']
        female_count = gender_count_frame.at['Female', 'Gender']
        print("There are {} male users, and {} female users.". format(male_count, female_count))    
        
    else:
        print("This city doesn't have data on user gender.")
    
    if df.columns[8] == 'Birth Year': 
    
        df['Birth Year'] = round(df['Birth Year'])
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print("The ealiest year of birth is %s." % int(earliest_year))
        print("The most recent year of birth is %s." % int(most_recent_year))
        print("The most common year of birth is %s." % int(most_common_year))
          
    else:
        print("This city doesn't have data on user birth year.")
        print(" "*40)
    
    duration = time.perf_counter() - session_start_time
    print(" "*40)
    print("This took %s seconds." % duration) 

    print("_"*40) 
    

# Step 7. Display raw data til user says no 
def display_data(df):  
    """Displays raw data on individual trips on user request."""
    
    #Get user input for checking rows 1 to 5 
    while True: 
        user_input = input("Now you can also check the raw data on individual trips!\n"
                           "Would you like to check out some raw data? Enter Yes, or No.\n")
        if user_input.title() not in ("Yes", "Y", "Ye", "No", "Not", "N"):  
            print ("Sorry please try again. Pay attention to the spelling.")
            continue 
        if user_input.title() in ("No", "Not", "N"):
            print("You've selected No.\n")
            break 
        if user_input.title() in ("Yes", "Y", "Ye"): 
            print("You've selected Yes.\n")
            print(""*40)
            print("Here are 5 lines of raw data on your request:\n")
            print(""*40)
            start_row = 0 
            next_start_row = start_row + 5 
            print(df.iloc[start_row:next_start_row])
            print("_"*40)
            #Get user input for checking next 5 rows 
            while True: 
                user_prompt = input("Would you like to see more data? Enter Yes, or No.\n")
                if user_prompt.title() not in ("Yes", "Y", "Ye", "No", "Not", "N"):  
                    print ("Sorry please try again. Pay attention to the spelling.")
                    continue 
                if user_prompt.title() in ("Yes", "Y", "Ye"): 
                    print("You've selected Yes.\n")
                    print(""*40)
                    print("Here are 5 more lines of raw data on your request:\n")
                    print(""*40)
                    start_row = next_start_row
                    next_start_row = start_row + 5 
                    print(df.iloc[start_row:next_start_row])
                    print("_"*40)
                    continue 
                if user_prompt.title() in ("No", "Not", "N"):
                    print("You've selected No.\n")
                    break
            break 


# Step 8. The 'Restart' option  
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

if __name__ == "__main__":
	main()


# In[ ]:




