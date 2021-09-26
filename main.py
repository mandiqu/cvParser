REQUIRED_FIELDS = ['DESCRIPTION']
LIST_ID = "126890"

# Read in input data
input_file = open("data/Super Powers Descriptor List.txt", 'r')
# Output file
output_file = open("data/cvCommands.txt", 'w')

# Unlock the list
output_file.write("update_list\t" + LIST_ID + "\tlock=false\n")

# Process the first line as a list of headers
headers = input_file.readline().strip().split("\t")

# Loop through lines in the input file
for line in input_file:
    # For each header, place the field into a dictionary
    current_concept = {}
    line_parts = line.replace("\n", "").split("\t")
    for index in range(0, len(headers)):
        current_concept[headers[index]] = line_parts[index]

    # Validate the concept - do not output if it doesn't contain required fields
    failed_validation = False
    for field in REQUIRED_FIELDS:
        if field not in current_concept or current_concept[field].strip() == "":
            print("Could not find required field " + field + " in concept!")
            failed_validation = True
            break
    if failed_validation:
        continue

    # Create the concept
    output_file.write("create_concept\t" + current_concept['DESCRIPTION'] + "\n")
    # Set the concept type if it exists
    if 'TYPE' in current_concept and current_concept['TYPE'].strip() != "":
        output_file.write("update_concept\t$conceptId\t" + "attrs=1:" + current_concept['TYPE'] + "\n")
    # If the official term exists, create it
    if 'OFFICIAL' in current_concept and current_concept['OFFICIAL'].strip() != "":
        output_file.write("create_term\t" + current_concept['OFFICIAL'] + "\ten\tOFFICIAL\t$conceptId\n")
        output_file.write("update_list\t" + LIST_ID + "\tterms=$termId\n")
    # If an official plural term exists, create it
    if 'OFFICIAL_PLURAL' in current_concept and current_concept['OFFICIAL_PLURAL'].strip() != "":
        output_file.write("create_term\t" + current_concept['OFFICIAL_PLURAL'] + "\ten\tOFFICIAL_PLURAL\t$conceptId\n")
        output_file.write("update_list\t" + LIST_ID + "\tterms=$termId\n")
    # If an alternate term exists, create it
    if 'ALTERNATE' in current_concept and current_concept['ALTERNATE'].strip() != "":
        output_file.write("create_term\t" + current_concept['ALTERNATE'] + "\ten\tALTERNATE\t$conceptId\n")
        output_file.write("update_list\t" + LIST_ID + "\tterms=$termId\n")

# Lock the list
output_file.write("update_list\t" + LIST_ID + "\tlock=true\n")
