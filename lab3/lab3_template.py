'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

--------------------------------------------------------------------------------
'''
import sys
import matplotlib.pylab as plt
import numpy as np
import statistics as st

# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date)
                        One list with the information from the fourth column (temperature)
    """
    wdates = []             # list of dates data
    wtemperatures = []      # list of temperarture data

    with open(infile, mode='r') as openfile:
        openfile.readline()
        for rec in openfile:
            columns = rec.split()
            wdates.append(columns[2])
            wtemperatures.append(float(columns[3]))

    return wdates, wtemperatures

def parse_data2(infile):
    """
    Function to parse weather data and find max and min temperatures
    :param infile: weather data input file
    :return: two dictionaries, one with minimum temps, one with maximum temps
    """
    wmin = {}      # list of dates data
    wmax = {}      # list of temperarture data
    with open(infile, mode='r') as openfile:
        openfile.readline()
        for rec in openfile:
            columns = rec.split()
            year = columns[2][0:4]
            if float(columns[17]) != 9999.9 and float(columns[18]) != 9999.9:
                if year in wmin:
                    wmin[year].append(float(columns[18]))
                    wmax[year].append(float(columns[17]))
                else:
                    wmin[year] = []
                    wmin[year].append(float(columns[18]))
                    wmax[year] = []
                    wmax[year].append(float(columns[17]))
    for key in wmin:
        wmin[key] = min(wmin[key])
        wmax[key] = max(wmax[key])
    return wmin, wmax


def calc_mean_std_dev(wdates, wtemp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: list with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """
    monthTemp = {'01':[],'02':[],'03':[],'04':[],'05':[],'06':[],'07':[],'08':[],'09':[],'10':[],'11':[],'12':[],}
    i = 1
    while i < len(wdates):
        monthTemp[wdates[i]].append(wtemp[i])
        i = i + 1
    means = []
    std_dev = []

    #Calculate mean and STD_DEV
    for key in monthTemp:
        means.append(st.mean(monthTemp[key]))
        std_dev.append(st.stdev(monthTemp[key], st.mean(monthTemp[key])))


    return means, std_dev



def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Year")
    plt.ylim([-20, 100])

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 100])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()      # display plot


def plot_data_task2(wmin, wmax):
    """
    Create plot for Task 2 which will plot the minimum and maximum temperature values for each year.
    :param: wmin: A dictionary with years as keys, and the minimum temperatures as the value of each.
    :param: wmax: A dictionary with years as keys, and the maximum temperatures as the value of each.
    """
    year = []
    for key in wmin:
        year.append(float(key))

    plt.xlabel('Year')
    plt.ylabel('Temperature, F')
    plt.plot(year, list(wmin.values()), "ob", label='Minimum')
    plt.plot(year, list(wmax.values()), "or", label='Maximum')
    plt.legend()
    plt.show()


def main(infile):
    weather_data = infile    # take data file as input parameter to file
    wdates, wtemperatures = parse_data(weather_data)
    wmin, wmax = parse_data2(infile)
    wyear = []
    wmonth = []
    for rec in wdates:
        wyear.append(int(rec[0:4]))
        wmonth.append(rec[4:6])
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wmonth, wtemperatures)
    # Plot data
    plot_data_task1(wyear, wtemperatures, month_mean, month_std)
    #Plot the 2nd task data
    plot_data_task2(wmin, wmax)



if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    infile = sys.argv[1]
    main(infile)
    exit(0)
