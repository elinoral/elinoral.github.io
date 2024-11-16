import csv
from os import close
import requests
import json


# Function to create file name
# Return file name list
## To edit years and tables, go to def main()
def create_filename_list(table, year_list):
    file_name_list = []
    for year in year_list:
        file_name = table + "_" + year + ".csv"
        file_name_list.append(file_name)

    return file_name_list


# Function to build a path to the data using the table, year, and geography level
# Returns path
def create_path_list(table, year_list, geography_list, key):
    path_list = []
    for year in year_list:
        if "B" in table:
            # Loop through individual geos and store in list
            for i in geography_list:
                path = "https://api.census.gov/data/" + year + "/acs/acs1?get=NAME, group(" + table + ")" + i + "&key=" + key
                path_list.append(path)
        elif "S" in table:
            for i in geography_list:
                path = "https://api.census.gov/data/" + year + "/acs/acs1/subject?get=group(" + table + ")" + i + "&key=" + key
                path_list.append(path)
        elif "DP" in table:
            # Loop through individual geos and store in list
            for i in geography_list:
                path = "https://api.census.gov/data/" + year + "/acs/acs1/profile?get=group(" + table + ")" + i + "&key=" + key
                path_list.append(path)
        else:
            print("Could not find table", table, "in year", year)

    return path_list


# Function to call the dataset and store the output
# Creates new csv files with the collected data
def get_data(path_list, file_list, year_list):
    for n in path_list:
        # Find the year corresponding to the current path
        for year in year_list:
            if year in n:
                # Find the correct file for that year
                file_index = year_list.index(year)
                output_file = file_list[file_index]

                with open(output_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    response = requests.get(n)

                    # Check the status code
                    if response.status_code == 200:
                        # Parse the JSON data
                        data = response.json()  # This converts the JSON response to a Python object

                        # Check if the parsed data is a list
                        if isinstance(data, list):
                            # Write each item in the list to the CSV file
                            for item in data:
                                writer.writerow(item)

                            print("Data has been written to", output_file)
                        else:
                            print("The content is not a list. It is a:", type(data))



# Main function puts it all together
def main():

    # collect table input
    table = input("Enter table code: ")

    # list of years to run through #
    years = ["2010", "2011","2012","2013","2014","2015","2016","2017","2018", "2019", "2021","2022","2023"]

    #list of geographies to collect data on
    geos = ["&for=us:1", "&for=state:06", "&for=county:025&in=state:06", "&for=county:029&in=state:06",
            "&for=county:037&in=state:06", "&for=county:065&in=state:06", "&for=county:071&in=state:06",
            "&for=county:059&in=state:06", "&for=county:073&in=state:06", "&for=county:111&in=state:06",
            "&for=place:44000&in=state:06", "&for=public%20use%20microdata%20area:03703&in=state:06",
            "&for=public%20use%20microdata%20area:03704&in=state:06",
            "&for=public%20use%20microdata%20area:03705&in=state:06",
            "&for=public%20use%20microdata%20area:03706&in=state:06",
            "&for=public%20use%20microdata%20area:03707&in=state:06",
            "&for=public%20use%20microdata%20area:03708&in=state:06",
            "&for=public%20use%20microdata%20area:03709&in=state:06",
            "&for=public%20use%20microdata%20area:03710&in=state:06",
            "&for=public%20use%20microdata%20area:03711&in=state:06",
            "&for=public%20use%20microdata%20area:03712&in=state:06",
            "&for=public%20use%20microdata%20area:03713&in=state:06",
            "&for=public%20use%20microdata%20area:03714&in=state:06",
            "&for=public%20use%20microdata%20area:03715&in=state:06",
            "&for=public%20use%20microdata%20area:03716&in=state:06",
            "&for=public%20use%20microdata%20area:03717&in=state:06",
            "&for=public%20use%20microdata%20area:03718&in=state:06",
            "&for=public%20use%20microdata%20area:03719&in=state:06",
            "&for=public%20use%20microdata%20area:03720&in=state:06",
            "&for=public%20use%20microdata%20area:03721&in=state:06",
            "&for=public%20use%20microdata%20area:03722&in=state:06",
            "&for=public%20use%20microdata%20area:03723&in=state:06",
            "&for=public%20use%20microdata%20area:03724&in=state:06",
            "&for=public%20use%20microdata%20area:03725&in=state:06",
            "&for=public%20use%20microdata%20area:03728&in=state:06",
            "&for=public%20use%20microdata%20area:03730&in=state:06",
            "&for=public%20use%20microdata%20area:03731&in=state:06",
            "&for=public%20use%20microdata%20area:03732&in=state:06",
            "&for=public%20use%20microdata%20area:03733&in=state:06",
            "&for=public%20use%20microdata%20area:03734&in=state:06",
            "&for=public%20use%20microdata%20area:03735&in=state:06",
            "&for=public%20use%20microdata%20area:03736&in=state:06",
            "&for=public%20use%20microdata%20area:03737&in=state:06",
            "&for=public%20use%20microdata%20area:03738&in=state:06",
            "&for=public%20use%20microdata%20area:03739&in=state:06",
            "&for=public%20use%20microdata%20area:03740&in=state:06",
            "&for=public%20use%20microdata%20area:03744&in=state:06",
            "&for=public%20use%20microdata%20area:03741&in=state:06",
            "&for=public%20use%20microdata%20area:03742&in=state:06",
            "&for=public%20use%20microdata%20area:03743&in=state:06",
            "&for=public%20use%20microdata%20area:03745&in=state:06",
            "&for=public%20use%20microdata%20area:03746&in=state:06",
            "&for=public%20use%20microdata%20area:03747&in=state:06",
            "&for=public%20use%20microdata%20area:03748&in=state:06",
            "&for=public%20use%20microdata%20area:03750&in=state:06",
            "&for=public%20use%20microdata%20area:03751&in=state:06",
            "&for=public%20use%20microdata%20area:03752&in=state:06",
            "&for=public%20use%20microdata%20area:03753&in=state:06",
            "&for=public%20use%20microdata%20area:03754&in=state:06",
            "&for=public%20use%20microdata%20area:03757&in=state:06",
            "&for=public%20use%20microdata%20area:03758&in=state:06",
            "&for=public%20use%20microdata%20area:03759&in=state:06",
            "&for=public%20use%20microdata%20area:03760&in=state:06",
            "&for=public%20use%20microdata%20area:03761&in=state:06",
            "&for=public%20use%20microdata%20area:03762&in=state:06",
            "&for=public%20use%20microdata%20area:03763&in=state:06",
            "&for=public%20use%20microdata%20area:03764&in=state:06",
            "&for=public%20use%20microdata%20area:03766&in=state:06",
            "&for=public%20use%20microdata%20area:03767&in=state:06",
            "&for=public%20use%20microdata%20area:03768&in=state:06",
            "&for=public%20use%20microdata%20area:03770&in=state:06",
            "&for=public%20use%20microdata%20area:03771&in=state:06",
            "&for=public%20use%20microdata%20area:03772&in=state:06",
            "&for=public%20use%20microdata%20area:03773&in=state:06",
            "&for=public%20use%20microdata%20area:03774&in=state:06",
            "&for=public%20use%20microdata%20area:03775&in=state:06",
            "&for=public%20use%20microdata%20area:03776&in=state:06",
            "&for=public%20use%20microdata%20area:03778&in=state:06",
            "&for=public%20use%20microdata%20area:03779&in=state:06",
            "&for=public%20use%20microdata%20area:03780&in=state:06",
            "&for=public%20use%20microdata%20area:03781&in=state:06",
            "&for=public%20use%20microdata%20area:03782&in=state:06"]

    # census API personal key
    key = "1599c160e1e6628893d0486d1068d6b06aaa5505"

    # passes table, years, geos, and key into create_path_list function
    # runs create_path_list function
    # saves path_list as list variable
    path_list = create_path_list(table, years, geos, key)

    # prints generated path list for error checking
    print(len(path_list), "paths generated:\n", path_list, "\n")

    # passes table and years into create_filename_list function
    # runs create_filename_list function
    # saves file_list as list variable
    file_list = create_filename_list(table, years)

    # prints list of files generated
    print("Working files:\n", file_list, "\n")
    print("\nWriting to files...")

    # passes path list, file list, and years into get_data function
    # runs get_data function
    # data is written directly to files
    get_data(path_list, file_list, years)

    # only when this line is printed is the code finished running
    print("Done.\nNew files:", file_list)

# Call main!
main()