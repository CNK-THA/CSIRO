"""
@author Chanon Kachornvuthidej, kac016@csiro.au, chanon.kachorn@gmail.com

Extract Geolocations from the database: https://geonames.nga.mil/gns/html/namefiles.html
"""

from pathlib import Path
from GeoNames1 import *

def parse_countries2(file_name):
    """
    :param file_name: (str) directory to the countryInfo.txt file
    :return: Dictionary mapping of FIPS country code to country name e.g. "AU" = "Australia"
    """
    countries_list = {}
    with open(file_name, 'r', encoding="utf8") as countryFile:
        line_number = 0
        for line in countryFile:
            line_number += 1
            if line_number < 51:  # DATA STARTS AT LINE 51
                continue
            line_parsed = line.split('\t')
            countries_list[line_parsed[3]] = (line_parsed[4], line_parsed[8])
    return countries_list


def main():
    countries_list = parse_countries2("countryInfo.txt")
    FIPSToFHIRLevel1 = {} # countries
    FIPSToFHIRLevel2 = {}

    with open(str(Path.home()) + "/Downloads/" + "Countries.txt", 'r', encoding="utf8", errors='ignore') as dataFile:
        line_number = 0
        current_country = None
        for line in dataFile:

            line = line.split('\t') # "Queensland" in line.split('\t')[22]
            # print(line)
            # input('')
            if "Gold Coast" in line:
                input(line)
            else:
                continue

            if current_country is None or line[12] != current_country.FIPSCode:
                current_country = Region(countries_list.get(line[12])[0], line[12], None)  # Change None to continents
                FIPSToFHIRLevel1[current_country.FIPSCode] = current_country.FHIRCode
                with open("GlobalData(GeoNames3).json", 'a') as fp:
                    for element in FIPSToFHIRLevel2:
                        fp.write(FIPSToFHIRLevel2.get(element).toJSON())
                    # json.dump(FIPSToFHIRLevel2, fp, indent=4)
                FIPSToFHIRLevel2 = {}

            if line[10] == "ADM1":
                current_state = Region(line[22], line[13], current_country.FHIRCode)
                FIPSToFHIRLevel2[line[13]] = current_state
            elif line[10] == "ADMD":
                # pass
                current_suburb = Region(line[22], line[13], )
                print(line)
    print(FIPSToFHIRLevel1)
    print(FIPSToFHIRLevel2)



if __name__ == "__main__":
    main()