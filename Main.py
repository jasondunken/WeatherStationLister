import urllib
import re
import files

file_loc = "data/asos-stations.txt"
arrayOfNCDCStations = {}
arrayOfIdLatLon = {}

data_source = 'https://www.ncdc.noaa.gov/homr'
all_loc = {}
processed_loc = {}


# this method gets an array of web links to .txt files
# it assigns the locations to a class dict of all the locations without duplications
# if returns void
def load_data():
    links = files.get_data(data_source)
    entry_count = 0
    duplicate_count = 0
    for link in links:
        content = urllib.request.urlopen(link)
        for line in content:
            line = line.decode('utf-8')
            if line[:8] not in all_loc:
                all_loc[line[:8]] = line
                entry_count += 1
            else:
                duplicate_count += 1

    print("%s duplicates were not recorded" % duplicate_count)
    print("%s entries recorded" % entry_count)


# this method fills an array with each location's id, lat and lon to be used for comparing to search location lat/lon
def process_locations():
    processed_count = 0
    for entry in all_loc:
        split_entry = all_loc[entry].split()
        key = split_entry[0]
        lat = None
        lon = None
        for s in split_entry:
            if re.match('[-+]?([0-9]*\.[0-9]+)', s):
                if lat is None:
                    lat = s
                elif lon is None:
                    lon = s
                else:
                    print("Error, too many lat/lon values for id: %s" % key)
        processed_loc[key] = (lat, lon)
        processed_count += 1
    print("%s locations processed" % processed_count)


def get_lat_lon():
    prilat = None
    prilon = None
    while prilat is None:
        prilat = input("Enter search latitude >>> ")
        try:
            n = float(prilat)
            if n and n < -90.0 or n > 90.0:
                print("%s is outside latitude parameters (-90.0 ~ 90.0)" % n)
                prilat = None
            else:
                prilat = n
        except ValueError:
            prilat = None
        except TypeError:
            prilat = None

    while prilon is None:
        prilon = input("Enter search longitude >>> ")
        try:
            n = float(prilon)
            if n and n < -180.0 or n > 180.0:
                print("%s is outside longitude parameters (-180.0 ~ 180.0)" % n)
                prilon = None
            else:
                prilon = n
        except ValueError:
            prilon = None
        except TypeError:
            prilon = None
    print("You have entered latitude %s and longitude %s." % (prilat, prilon))

    return prilat, prilon


def get_from_closest(lat_lon):
    result = {}
    for key in processed_loc:
        # algorithm here to calculate distance between positions
        # because absolute distance is not required,
        # will use a^ b^ sum to assign a dist to each coord pair
        dist_a = abs(float(lat_lon[0])) - abs(float(processed_loc[key][0]))
        dist_b = abs(float(lat_lon[1])) - abs(float(processed_loc[key][1]))
        dist = dist_a ** 2 + dist_b ** 2
        result[key] = dist

    return sorted(result.items(), key=lambda x: x[1])


def main():
    load_data()
    process_locations()

    lat_lon = ()
    choice = ""
    while choice != "y" and choice != "Y":
        lat_lon = get_lat_lon()
        choice = input("Is this correct (y/n) >>> ")

    result = get_from_closest(lat_lon)
    for r in result:
        print(all_loc[r[0]])


main()
