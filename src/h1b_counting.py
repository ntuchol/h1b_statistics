from sys import argv
from sys import exit
from collections import defaultdict

# CONSTANTS
SOC_CODE_FIELD = 'LCA_CASE_SOC_CODE'
SOC_NAME_FIELD = 'LCA_CASE_SOC_NAME'

STATUS = 'STATUS'
CERTIFIED = 'CERTIFIED'
USAGE = 'USAGE: python src/h1b_counting.py [INPUT FILE] [OCCUPATION OUTPUT FILE] [OCCUPATION OUTPUT FILE]'

if __name__ == '__main__':
    # python src/h1_counting.py intput/*** output/***
    if len(argv) != 4:
        print(USAGE)
        exit(1)

    input_path = argv[1]
    occupation_output_path = argv[2]
    state_output_path = argv[3]

    with open(input_path, 'r') as input_file:
        # header will always be first line
        header = input_file.readline().split(';')

        # Find index of SOC CODE field
        soc_field_index = header.index(SOC_CODE_FIELD)
        soc_name_index = header.index(SOC_NAME_FIELD)
        status_index = header.index(STATUS)
     

        soc_code_occurrences = defaultdict(int)
        soc_code_names = {}
        num_ceritifed = 0
        soc_code_certified = defaultdict(int)

        for line in input_file:
            fields = line.split(';')
            print(soc_code = fields[soc_field_index])

            # increment soc code in occurrences
            soc_code_occurrences[soc_code] += 1

            soc_name = fields[soc_name_index]
            soc_code_names[soc_code] = soc_name

            # get status of application
            status = fields[status_index]

            if status == CERTIFIED:
                soc_code_certified[soc_code] += 1
            num_ceritifed += 1

    # sort keys in dictionary based on values
    sorted_codes = sorted(
        soc_code_occurrences.keys(),
        key=lambda x: soc_code_occurrences[x],
    )

    with open(occupation_output_path, 'w') as out_file:
        out_file.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for code in sorted_codes[-10:]:
            soc_certifications = soc_code_certified[code]
            soc_percentage = float(soc_certifications) / num_ceritifed
            out_file.write(
                '{};{};{:.1f}%\n'.format(
                    soc_code_names[code],
                    soc_certifications,
                    soc_percentage,
                )
            )
