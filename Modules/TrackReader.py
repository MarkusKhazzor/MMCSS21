import csv
import os.path
import string

import numpy as np

# HOW TO USE:
# last node of the track gets kicked out --> connection to first node
# supports only writing 1 track down in a track file
# form has to be 1 line of just "Track"
# then 1 Line of just the amount of the pillar points for eg "42"
# then lines with x y z for eg "4.5 2.7 5" and the delimiter is tab
# the variable "path" specifies the name of the file which is extracted next to this project file path
# Last line is not taken into account - BUT HAS TO HAVE SOME COORDINATES for example: "0   0   0"
# the algo thinks that the 1 pillar point prior the last pillar point line connects into the first pillar point line


def extract_rollercoaster_pillar_points():

    my_path = os.path.abspath(os.path.dirname(__file__))
    # self created track
    path = os.path.join(my_path, "../_MyTrack.trk")
    # provided track
    # path = os.path.join(my_path, "../_WildeMaus.trk")


    with open(path, newline='', encoding="utf8") as csv_file:
        line_list = list(csv.reader(csv_file, delimiter='\t'))  # optional setting with different delimiter --> , delimiter=','

        pillar_points = None
        track_keyword_found = False
        total_amount_of_pillar_points = None
        temp_pillar_point = 0

        for index, line in enumerate(line_list):
            if line:
                # check if empty
                line_data = [x for x in line if x.strip()]
                if not line_data:
                    continue
                
                # find where the Track starts
                if 'Track' in line and len(line[0].strip()) == 5:
                    track_keyword_found = True
                    continue
                
                # read the next line after Track as total amount
                elif track_keyword_found and total_amount_of_pillar_points is None:
                    total_amount_of_pillar_points = int(line[0].strip()) - 1
                    pillar_points = np.zeros(shape=(total_amount_of_pillar_points, 3))
                    continue
                
                # read the rest of the lines as points until total_amount_of_pillar_points is done
                elif track_keyword_found and total_amount_of_pillar_points:
                    if len(line_data) > 3:
                        raise ValueError("line has more than 3 x/ y/ z values - this is not possible in a 3D space")
                    if temp_pillar_point < total_amount_of_pillar_points:
                        for j, entry in enumerate(line_data):
                            pillar_points[temp_pillar_point][j] = float(entry)
                        temp_pillar_point += 1

        if not track_keyword_found:
            raise ValueError("No track keyword found to get where Track starts")

    return pillar_points