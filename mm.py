import sys
import os
import re


keywords = ('type', 'alphabet', 'states', 'transitions', 'inputs')
machine_types = ['dfa']

INPUT_FILE_ERROR = 1
FILE_FORMAT_ERROR = 2

COMMENT_SYMBOL = '#'
KEYWORD_SUFFIX = ':'

TYPE_KEYWORD = 'type'
NUM_STATES_KEYWORD = 'states'
ACCEPT_KEYWORD = 'accept'
ALPHABET_KEYWORD = 'alphabet'
TRANSITIONS_KEYWORD = 'transitions'
INPUTS_KEYWORD = 'inputs'


def main():
    # check if an input file was provided
    if len(sys.argv) < 2:
        print 'Usage: python ' +  sys.argv[0] + '<input-file>'
        sys.exit(INPUT_FILE_ERROR)
    # check if the the given input file exists
    input_file_path = sys.argv[1]
    if not os.path.exists(input_file_path):
        print 'Could not read file:', input_file_path
        sys.exit(INPUT_FILE_ERROR)
    # open the input file and combine it into one string
    with open(input_file_path) as input_file:
        # strip the space from each line and concatenate the lines into one string
        # remove blank lines and comment lines
        input_string = '\n'.join(re.sub('[\s+]', '', line) for line in input_file
                                 if len(line.strip()) > 0 and line.strip()[0] != COMMENT_SYMBOL)

        print input_string
        # parse the file string to obtain the required fields
        machine_type = ''
        num_states = 0
        accepting_states = []
        alphabet = []
        transitions = []

        # detect the type of the machine
        try:
            machine_type = re.search(TYPE_KEYWORD + KEYWORD_SUFFIX + '([^\s]*)', input_string).group(1)
            if machine_type not in machine_types:
                print 'Error: invalid value for machine type'
                sys.exit(FILE_FORMAT_ERROR)
        except AttributeError:
            print 'Error: machine type not specified'
            sys.exit(FILE_FORMAT_ERROR)

        # detect the number of states in the machine
        try:
            num_states = int(re.search(NUM_STATES_KEYWORD + KEYWORD_SUFFIX + '([0-9]*)', input_string).group(1))
            if num_states < 1:
                raise ValueError

        except AttributeError:
            print 'Error: number of states not specified'
            sys.exit(FILE_FORMAT_ERROR)
        except ValueError:
            print 'Error: invalid number of states'
            sys.exit(FILE_FORMAT_ERROR)

        # detect the accepting states
        try:
            accepting_string = re.search(ACCEPT_KEYWORD + KEYWORD_SUFFIX + '([^\s]*)', input_string).group(1)
            accepting_states = [int(accepting_state_string) for accepting_state_string in accepting_string.split(',')]

            # check for duplicates
            if len(accepting_states) != len(set(accepting_states)):
                print 'Error: duplicates exist in accepting states'
                sys.exit(FILE_FORMAT_ERROR)
            # check for invalid values
            if len([state for state in accepting_states if state < 0 or state > num_states - 1]) > 0:
                raise ValueError
        except AttributeError:
            print 'Error: accepting states not specified'
            sys.exit(FILE_FORMAT_ERROR)
        except ValueError:
            print 'Error: invalid states in list of accepting states'
            sys.exit(FILE_FORMAT_ERROR)

        # detect the alphabet
        try:
            alphabet_string = re.search(ALPHABET_KEYWORD + KEYWORD_SUFFIX + '([^\s]*)', input_string).group(1)
            alphabet = alphabet_string.split(',')

            # check for duplicates
            if len(alphabet) != len(set(alphabet)):
                print 'Error: duplicates exist in alphabet specification'
                sys.exit(FILE_FORMAT_ERROR)
            # check for invalid values
            for symbol in alphabet:
                # require that each symbol be composed of only one character
                if len(symbol) != 1:
                    print 'Error: alphabet symbols are limited to one character'
                    sys.exit(FILE_FORMAT_ERROR)
        except AttributeError:
            print 'Error: alphabet not specified'
            sys.exit(FILE_FORMAT_ERROR)

        print num_states
        print machine_type
        print accepting_states
        print alphabet


if __name__ == '__main__':
    main()
        

