import inspect
import sys

'''
The threshold used to see if the given attribute is numerical or nominal.
In order to be nominal, the data must have >= this many instances of a attribute.
'''
NUM_THRESH = 20


def write_attributes(write_to: str, data: {}):
    '''
    Gets the Weka attributes based on the given data. Only differentiates numerical or nominal.
    '''
    x = open(write_to, "a")
    attrib_num = 0
    while attrib_num < len(data):
        if len(data[attrib_num]) >= NUM_THRESH:
            x.write(f"@ATTRIBUTE A{attrib_num+1} numeric\n")
        else:
            classes = "{"
            for values in data[attrib_num].keys():
                classes += (values+", ")
            classes += "}"
            classes = classes.replace(", }", "}")
            x.write(f"@ATTRIBUTE A{attrib_num+1} {classes}\n")
        attrib_num += 1

    x.close()


def convert_to_arff(path_name: str):
    '''
    Converts the given file to arff form.
    '''
    # String without file extension
    stripped = path_name.rsplit(".", 1)[0]
    try:

        with open(f"{stripped}.arff", "w") as new_file:
            new_file.write(f"@RELATION {stripped}\n\n")

        data = extract_data(path_name)
        write_attributes(f"{stripped}.arff", data)

        with open(f"{stripped}.arff", "a") as new_file:
            new_file.write("\n\n@DATA\n")
            with open(path_name, "r") as data_file:
                new_file.writelines(data_file.readlines())

        # Makes the arff name equal to that of the path name; sans '.arff'
    except FileNotFoundError:
        sys.exit(f"Couldn't read from {path_name} or create {stripped}.arff")


def extract_data(path_name: str) -> {}:
    '''
    Gets the data from a given data file, in comma separated values where
    each entry/entity is on a new line.
    '''

    # Open up the file from the path
    x = open(path_name, 'r')
    # Get all the lines from the file
    lines = x.readlines()
    # Close the open file
    x.close()
    if len(lines) < 1:
        exit("No data found!")

    # A list of dictionaries keeping track of occurences of attributes.
    data = []
    # The number of attributes.
    attrib_num = lines[0].count(',')
    # Cycle through every line.
    for line in lines:
        line = line.replace('\n', '')
        # Take apart the lines by each comma.
        split = line.split(',')
        # Keep track of what attribute is being iterated through
        attrib_num = 0
        # Iteration
        while attrib_num < len(split):
            # The current attribute
            attrib = split[attrib_num]
            # If the number of the attribute isn't in the data, make the dictionary for it.
            if attrib_num >= len(data):
                data.append({})
            # Increment the occurence, or create it
            data[attrib_num][split[attrib_num]
                             ] = 1 if attrib not in data[attrib_num] else data[attrib_num][attrib] + 1
            # Iteration increment
            attrib_num += 1
    return data


# Only input file to convert; not where to.
output = input("File to read: ") if len(sys.argv) < 2 else sys.argv[1]
# Output is now the file to write to.
try:
    # created = open(output, "w")
    # This creates a file for writing, creating if necessary.
    convert_to_arff(output)
except FileNotFoundError:
    sys.exit("Specified file not found.")
