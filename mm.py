import sys
import os
import re

INPUT_FILE_ERROR = 1
FILE_FORMAT_ERROR = 2

KEYWORDS = ('type', 'alphabet', 'states', 'transitions', 'inputs')

TYPE_DFA = 'dfa'
TYPE_NFA = 'nfa'
MACHINE_TYPES = (TYPE_DFA, TYPE_NFA)


COMMENT_SYMBOL = '#'
KEYWORD_SUFFIX = ':'
STATEMENT_SUFFIX = ';'
LIST_SEPARATOR = ','
TRANSITION_SEPARATOR = '->'

# detects any of the listed keywords along with their suffix, as well as the end of a string
KEYWORDS_REGEX = '(?:' + '|'.join(keyword + KEYWORD_SUFFIX for keyword in KEYWORDS) + '|$)'
print KEYWORDS_REGEX

TYPE_KEYWORD = 'type'
NUM_STATES_KEYWORD = 'states'
ACCEPT_KEYWORD = 'accept'
ALPHABET_KEYWORD = 'alphabet'
TRANSITIONS_KEYWORD = 'transitions'
INPUTS_KEYWORD = 'inputs'


def write_machine(machine_type, num_states, accepting_states, alphabet, transitions, inputs):
    pass


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
        input_string = ''.join(re.sub('[\s+]', '', line) for line in input_file
                                 if len(line.strip()) > 0 and line.strip()[0] != COMMENT_SYMBOL)
        print input_string
        # parse the file string to obtain the required fields
        # detect the type of the machine
        try:
            machine_type = re.search(TYPE_KEYWORD + KEYWORD_SUFFIX + '([^' + STATEMENT_SUFFIX +
                                     '\s]*?)' + STATEMENT_SUFFIX, input_string).group(1)
            if machine_type not in MACHINE_TYPES:
                print 'Error: invalid value for machine type'
                sys.exit(FILE_FORMAT_ERROR)
        except AttributeError:
            print 'Error: machine type not specified or specified incorrectly'
            sys.exit(FILE_FORMAT_ERROR)
        print machine_type
        # detect the number of states in the machine
        try:
            num_states = int(re.search(NUM_STATES_KEYWORD + KEYWORD_SUFFIX +
                                       '([0-9]+)' + STATEMENT_SUFFIX, input_string).group(1))
            if num_states < 1:
                raise ValueError
        except AttributeError:
            print 'Error: number of states not specified or specified incorrectly'
            sys.exit(FILE_FORMAT_ERROR)
        except ValueError:
            print 'Error: invalid number of states'
            sys.exit(FILE_FORMAT_ERROR)

        # detect the accepting states
        try:
            accepting_string = re.search(ACCEPT_KEYWORD + KEYWORD_SUFFIX +
                                         '([^' + STATEMENT_SUFFIX + '\s]*)' + STATEMENT_SUFFIX, input_string).group(1)
            accepting_states = [int(accepting_state_string)
                                for accepting_state_string
                                in accepting_string.split(LIST_SEPARATOR)]
            # check for duplicates
            if len(accepting_states) != len(set(accepting_states)):
                raise ValueError('Error: duplicates exist in accepting states')
            # check for invalid values
            if len([state for state in accepting_states if state < 0 or state > num_states - 1]) > 0:
                raise ValueError('Error: invalid states in list of accepting states')
        except AttributeError:
            print 'Error: accepting states not specified or specified incorrectly'
            sys.exit(FILE_FORMAT_ERROR)
        except ValueError as e:
            print e
            sys.exit(FILE_FORMAT_ERROR)

        # detect the alphabet
        try:
            alphabet_string = re.search(ALPHABET_KEYWORD + KEYWORD_SUFFIX +
                                        '([^' + STATEMENT_SUFFIX + '\s]*)' + STATEMENT_SUFFIX, input_string).group(1)
            alphabet = alphabet_string.split(LIST_SEPARATOR)
            # check for duplicates
            if len(alphabet) != len(set(alphabet)):
                raise ValueError('Error: duplicates exist in alphabet specification')
            # check for invalid values
            for symbol in alphabet:
                # require that each symbol be composed of only one character
                if len(symbol) != 1:
                    raise ValueError('Error: alphabet symbols are limited to one character')

        except AttributeError:
            print 'Error: alphabet not specified or specified incorrectly'
            sys.exit(FILE_FORMAT_ERROR)
        except ValueError as e:
            print e
            sys.exit(FILE_FORMAT_ERROR)

        # detect the transition function
        try:
            transitions = [None for i in xrange(num_states)]
            alphabet_regex = '(' + '|'.join(alphabet) + ')'
            states_regex = '(' + '|'.join(str(state) for state in xrange(num_states)) + ')'
            transition_string = re.search(TRANSITIONS_KEYWORD + KEYWORD_SUFFIX + '([^\s]*)' + KEYWORDS_REGEX,
                                          input_string).group(1)
            # iterate through each state transition specified
            for state_string in transition_string.split(STATEMENT_SUFFIX):
                regex_results = re.search('([0-9]+)' + KEYWORD_SUFFIX + '([^\s]*)', state_string)
                # determine the state for the current transition
                state = int(regex_results.group(1))
                # determine if the state is a valid state
                if state not in xrange(num_states):
                    raise ValueError('Error: transition state is not valid')
                # determine if the state has already been defined
                if transitions[state]:
                    raise ValueError('Error: more than one transition statement for a single state specified')
                transitions[state] = {}
                # determine the transitions for the given state
                state_transitions = regex_results.group(2).split(LIST_SEPARATOR)
                for transition in state_transitions:
                    transition_groups = re.search(alphabet_regex + TRANSITION_SEPARATOR + '([0-9]+)', transition)
                    symbol = transition_groups.group(1)
                    next_state = int(transition_groups.group(2))
                    if symbol in transitions[state]:
                        raise ValueError('Error: duplicate transition specified')
                    if next_state not in xrange(num_states):
                        raise ValueError('Error: invalid state in transition specification')
                    transitions[state][symbol] = next_state

        except AttributeError:
            print "Error: transitions not specified or specified incorrectly"
            sys.exit(FILE_FORMAT_ERROR)
        except ValueError as e:
            print e
            sys.exit(FILE_FORMAT_ERROR)

        # verify that the transition is valid for the specified type
        print num_states
        print machine_type
        print accepting_states
        print alphabet
        print transitions
        try:
            if machine_type == TYPE_DFA:
                for state_transition in transitions:
                    # all states must have a set of num_states transitions
                    if not state_transition:
                        raise ValueError('Error: transition specification for state not found')
                    elif len(state_transition) < len(alphabet):
                        raise ValueError('Error: transition specification for state missing transition(s)')

        except ValueError as e:
            print e
            sys.exit(FILE_FORMAT_ERROR)





if __name__ == '__main__':
    main()
        

