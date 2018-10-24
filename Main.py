arrayOfNCDCStations = {}
arrayOfIdLatLon = {}

fileLoc = "data/asos-stations.txt"


def load_dat_file():
    with open(fileLoc, 'r') as file:
        entryCount = 0
        for line in file:
            key = line[:8]
            if key.isdigit():
                # add entry to main array with NCDCID as key
                arrayOfNCDCStations[key] = line.strip()
                # validate values and create tupple to insert into array
                # use NCDCID as key
                splitLine = line.split()
                lat = None
                lon = None
                for value in splitLine:
                    try:
                        n = float(value)
                        # if n is not None and n is a floating point value but not a whole number
                        if n and n % 1 != 0:
                            # if n falls within the limits of longitude
                            if n > -180.0 and n < 180.0:
                                if lat is None:
                                    lat = value
                                elif lon is None:
                                    lon = value
                                else:
                                    print("Error: lat/lon values already assigned! ", value)
                    except ValueError:
                        pass
                    except TypeError:
                        pass
                arrayOfIdLatLon[key] = (lat, lon)
                entryCount += 1
        print("%s file loaded, %s entries" % (fileLoc, entryCount))


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
    for key in arrayOfIdLatLon:
        # algorithm here to calculate distance between positions
        # because absolute distance is not required,
        # will use a^ b^ sum to assign a dist to each coord pair
        dist_a = abs(float(lat_lon[0])) - abs(float(arrayOfIdLatLon[key][0]))
        dist_b = abs(float(lat_lon[1])) - abs(float(arrayOfIdLatLon[key][1]))
        dist = dist_a ** 2 + dist_b ** 2
        result[key] = dist

    return sorted(result.items(), key=lambda x: x[1])


def main():
    load_dat_file()
    lat_lon = ()
    choice = ""
    while choice != "y" and choice != "Y":
        lat_lon = get_lat_lon()
        choice = input("Is this correct (y/n) >>> ")

    result = get_from_closest(lat_lon)
    for r in result:
        print(arrayOfNCDCStations[r[0]])


main()
