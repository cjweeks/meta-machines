//
// Created by cjweeks on 01/11/16.
//

#ifndef META_MACHINES_COMMON_H
#define META_MACHINES_COMMON_H

/**
 * This value will be used for any null or invalid value
 */
#define NULL_VALUE  (-1)


/**
 * Specifies a null type, which may be used
 * to terminate a list.
 */
struct NullType {};

/**
 * This data structure specifies a recursively defined list.
 * Each element contains an integer value and a 'tail',
 * representing a list containing the next elements.
 * Fpr example, the list {1, 2, 3, 4} ,ay be defined
 * as follows: List<1, List<2, List<3, List<4, NullType> > > >
 */
template<int current, typename tail>
struct List {
    /**
     * The next sub-list, or NullList if no elemnts remain.
     */
    typedef tail next;

    enum {
        /**
         * The value of the current list element.
         */
        value = current
    };
};


/**
 * This data structure may be used to determine if
 * a guven value exists in a given List data structre.
 */
template<typename list, int value>
struct contains {
    enum {
        /**
         * Whether the list contains the given value. This is
         * calculated by performing a recursive check on each
         * sub-list.
         */
        result = (list::value == value) || contains<typename list::next, value>::result
    };
};

/**
 * Base case specification for the contains type above.
 * An empty list never contains the given value.
 */
template<int value>
struct contains<NullType, value> {
    enum {
        /**
         * Whether or not the given (empty) list contains
         * the given value: always 0.
         */
        result = 0
    };
};


#endif // META_MACHINES_COMMON_H
