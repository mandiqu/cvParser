list_id = "126890"

# Read in input data
input_file = open("data/Super Powers Descriptor List.txt", 'r')
# Output file
output_file = open("data/cvCommands.txt", 'w')

# Unlock the list
output_file.write("update_list\t" + list_id + "\tlock=false\n")

# Skip the header line
skipped_headers = False

# Loop through lines in the input file
for line in input_file:
    if not skipped_headers:
        skipped_headers = True
        continue
    line_parts = line.strip().split("\t")
    # Create the concept
    output_file.write("create_concept\t" + line_parts[1] + "\n")
    # Set the concept type
    output_file.write("update_concept\t$conceptId\t" + "attrs=1:" + line_parts[0] + "\n")
    # Create the official term
    output_file.write("create_term\t" + line_parts[2] + "\ten\tOFFICIAL\t$conceptId\n")
    output_file.write("update_list\t" + list_id + "\tterms=$termId\n")
    # If an alternate term exists, create it
    if len(line_parts) > 3:
        output_file.write("create_term\t" + line_parts[3] + "\ten\tALTERNATE\t$conceptId\n")
        output_file.write("update_list\t" + list_id + "\tterms=$termId\n")

# Lock the list
output_file.write("update_list\t" + list_id + "\tlock=true\n")
