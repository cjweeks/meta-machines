//
// Created by cjweeks on 01/11/16.
//

#ifndef META_MACHINES_DFA_H
#define META_MACHINES_DFA_H

#include "common.h"

// general case DFA
template<
        int num_states,
        typename accepting_states,
        int current_state,
        template<int, int> typename transitions,
        typename input>
struct Dfa {
    enum {
        result = Dfa<
                num_states,
                accepting_states,
                transitions<current_state, input::value>::next_state,
                transitions,
                typename input::next>::result

    };
};

// base case DFA
template <
        int num_states,
        typename accepting_states,
        int current_state,
        template<int, int> typename transitions>
struct Dfa<num_states, accepting_states, current_state, transitions, NullType> {
    enum {
        result = contains<accepting_states, current_state>::result
    };
};

#endif //META_MACHINES_DFA_H
