from link import Link
from matchedprobe import MatchedProbe
import math


linkData = "C:/Masters/university/GeoVV/HW2/Data/Partition6467LinkData.csv"
matchedpointsData = "C:/Masters/university/GeoVV/HW2/Data/MatchedPointsOutput.csv"
slopeData = "C:/Masters/university/GeoVV/HW2/Data/slope.csv"
evaluated_data = "C:/Masters/university/GeoVV/HW2/Data/evaluated.csv"

AVG_EARTH_RADIUS = 6367


def calculate_distance(long1, latt1, long2, latt2):
    long1, latt1, long2, latt2 = list(map(math.radians, [long1, latt1, long2, latt2]))
    distance_long, distance_lat = long2 - long1 , latt2 - latt1
    a = math.sin(distance_lat/2)**2 + math.cos(latt1) * math.cos(latt2) * math.sin(distance_long/2)**2
    kilometers = AVG_EARTH_RADIUS * 2 * math.asin(math.sqrt(a))
    return kilometers


def calculate_slope():

    link_data = []
    file_line_count = 0

    # Reading link file
    with open(linkData) as street_data:
        for line in street_data:
            link_data.append(Link(line))


    # Reading matched probe data
    with open(matchedpointsData) as matched_data:
        result_data = open(slopeData, 'w')

        prev_probe = None
        print("Calculating slope for each mapped probe")

        for line in matched_data:
            probe = MatchedProbe(line)

            # Check for link
            if not prev_probe or probe.linkID != prev_probe.linkID:
                probe.slope = ''
            else:
                try:
                    # Calculating slope
                    start, end = list(map(float, [probe.longitude, probe.latitude])), list(map(float, [prev_probe.longitude, prev_probe.latitude]))

                    # calculating hypotenuse
                    hypotenuse = calculate_distance(start[0], start[1], end[0], end[1]) / 1000
                    opposite = float(probe.altitude) - float(prev_probe.altitude)
                    probe.slope = (2 * math.pi * math.atan(opposite / hypotenuse)) / 360

                except ZeroDivisionError:
                    probe.slope = 0.0

                # check for same linkID with current probe data matched link
                for link in link_data:
                    if probe.linkID == link.linkID and link.slopeInfo != '':
                        print("Inside Check for same LinkID")
                        link.ProbePoints.append(probe)
                        break

            # Increment line number
            file_line_count += 1
            result_data.write(probe.toString())

            prev_probe = probe

        result_data.close()

    return link_data



'''
    Calculating Mean of both given abnd calculating slope for the same link
'''
def evaluate_slope(link_data):
    print("Evaluating Slope: ")

    evaluated_data = open(evaluated_data, 'a')
    evaluated_data.write('linkID,  Given Slope, Calculated Slope' + "\n")

    for link in link_data:
        # check for link has matched point
        if len(link.ProbePoints) > 0.0:
            print("inside IF")
            sum_given_slope = 0.0

            # Calculating the mean of given slope info for the link
            givenSlope = link.slopeInfo.strip().split('|')
            for gslope in givenSlope:
                print("1 for loop")
                sum_given_slope += float(gslope.strip().split('/')[1])

            given_slope = sum_given_slope / len(givenSlope)

            sum_calculated_slope, non_zero_probe_count = 0.0, 0

            # Calculating the mean of calculated slope info for the link
            for probe in link.ProbePoints:
                print("2 for loop")
                if probe.direction == "T":
                    probe.slope = -probe.slope

                if probe.slope != '' and probe.slope != 0:
                    sum_calculated_slope += probe.slope
                    non_zero_probe_count += 1

            calculated_slope = sum_calculated_slope / non_zero_probe_count if non_zero_probe_count != 0 else 0

            evaluated_data.write('{}, {}, {}\n'
                                  .format(link.linkID,
                                          given_slope,
                                          calculated_slope))

    evaluated_data.close()




link_data = calculate_slope()
evaluate_slope(link_data)