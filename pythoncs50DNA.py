import csv
import sys

# TODO: Check for command-line usage


def main():
    if len(sys.argv) == 3:
        sequence = sys.argv[1]
        subsequence = sys.argv[2]
        database_rows, headers = opendatabase(sequence)
        DNAinq = openDNA(subsequence)
        STR_dict = STRcount(database_rows, DNAinq, headers)
        result = DBmatch(STR_dict, database_rows)
        print(result)
    else:
        print("Wrong command line arguments.")
    # TODO: Read database file into a variable


def opendatabase(filename):
    rows = []
    headers = []
    with open(filename) as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        for row in reader:
            rows.append(row)
        return rows, headers

    # TODO: Read DNA sequence file into a variable


def openDNA(filename):
    rows_DNA = []
    with open(filename) as file:
        reader = file.read()
        rows_DNA.append(reader)
    return rows_DNA

    # TODO: Find longest match of each STR in DNA sequence


def STRcount(sequence, rows_DNA, headers):
    STR_dict = {}
    STRs = headers[1:]

    for j in STRs:
        max_strcount = 0
        for i in range(len(rows_DNA)):
            subsequence = j
            current_sequence = rows_DNA[i]
            longest_run = longest_match(current_sequence, subsequence)
            if longest_run > max_strcount:
                max_strcount = longest_run
        STR_dict[j] = max_strcount

    return STR_dict

    # TODO: Check database for matching profiles


def DBmatch(STR_dict, rows):
    for person in rows:
        match = True
        for STR, count in STR_dict.items():
            if int(count) != int(person[STR]):
                match = False
                break
        if match:
            return person['name']
    return "No match"


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
