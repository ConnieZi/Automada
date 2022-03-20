import sys

def main():
    filename1 = sys.argv[1]
    in_file = open(filename1,'r')
    filename2 = sys.argv[2]

    '''
        Construct NFA's transitions. This will include the empty sets that've been ignored.
    '''

    num_states = int(in_file.readline()) 
    alphabet = list(in_file.readline().strip())
    #append epsilon
    alphabet.append('e')

    transitions = {}
    start_state = ''
    accept_states = []
    lines = list()

    for line in in_file:
        lines.append(line)

    i = 0
    for line in lines:
        #split every line into a list that has 3 items, [3,'d',4]
        transition_list = line.strip().split(' ')

        # the borderline contains only a '\n'
        if(len(transition_list) > 2):
            i += 1
            curr_state = int(transition_list[0])
            symbol = transition_list[1].strip("\'")
            dest_state = int(transition_list[2])

            #keep this structure:{3:{d:(destination set),g:(       )},2:{d:(   ),g:(    )},5:....     }
            if curr_state not in transitions.keys():
                transitions[curr_state] = dict()   #construct dic for transitions --> destinations
                #For every new state, and for every alphabet character, 
                # we move to an empty set at first, and fill it in the follwing steps.
                #Also, when we construct DFA, we need to unite these empty sets with others sets.
                for character in alphabet:
                    transitions[curr_state][character] = set()
                transitions[curr_state][symbol].add(dest_state)  #transitions --> destinations(set)
                transitions[curr_state]['e'].add(curr_state)  #every state itself is in its own epsilon closure set
            else:
                transitions[curr_state][symbol].add(dest_state)
        else:
            break

    #Note that the first chars of the entries in nfa.txt do not list all the states of the NFA!!
    for unlisted_state in range(1, num_states+1):
        if unlisted_state not in transitions.keys():
            transitions[unlisted_state] = dict()
            for character in alphabet:
                transitions[unlisted_state][character] = set()
            transitions[unlisted_state]['e'] = {unlisted_state}  # special case when 'e' is the transition

    start_state = int(lines[i + 1].strip())
    accept_states = list(map(int, lines[i + 2].strip().split(' ')))

    in_file.close()  

    '''
        convert the NFA to an DFA. Epsilon the result of union, and add this state as a new state into DFA's dictionary
    '''
    
    dfa_start = epsilon({start_state},transitions)    #The epsilon closure of NFA start state, and only tuples are hashable!!
    dfa_transitions = {}   #DFA's transition table
    dfa_states = [dfa_start]     #Q
    dfa_accept_states = set()
    alphabet.remove('e')

    queue = [dfa_start]  # a FIFO queue that stores the new states created.
    
    while queue:
        dfa_start = queue[0]
        dfa_transitions[dfa_start] = dict()
        for character in alphabet:
            T = set()   # T will represent a new state
            for state in dfa_start:
                T = T.union(transitions[state][character])     #union the result of every state in the tuple
                T = T.union(set(epsilon(T, transitions)))    # do epsilon closure on the result set

            dfa_transitions[dfa_start][character] = tuple(T)   # after the union, T is then immutable
            new_state = tuple(T)
            if new_state not in dfa_states:
                dfa_states.append(new_state)
                queue.append(new_state)
        queue.pop(0)

    # DFA accept states
    for tuples in dfa_transitions:
        for state in tuples:
            if state in accept_states:
                dfa_accept_states.add(tuples)
     
    dfa_start = epsilon({start_state},transitions)       #restore dfa_start!!
    
    '''
        Write the output DFA to a file
    '''
    
    out_file = open(filename2, 'w')

    # output number of states
    out_file.write(str(len(dfa_states))+ "\n")

    #output the alphabet
    s = ""
    for symbol in alphabet:
        symbol = symbol.strip("\'")
        s += symbol
    out_file.write(s + "\n")


    #output the transitions
    for key in dfa_states:
        # print(dfa_states.index(key))
        for symbol in alphabet:
            s = ""
            s = s + str(dfa_states.index(key) + 1) + ' ' + "'" + symbol + "'" + ' ' + str(dfa_states.index(dfa_transitions[key][symbol]) + 1)
            out_file.write(s + "\n")
    
    #output the start state
    out_file.write(str(dfa_states.index(dfa_start) + 1) + "\n")

    #output the accept states
    dfa_accept_states = list(dfa_accept_states)    # convert dfa_accept_state to a list with many tuples
    for state in dfa_accept_states:
        out_file.write(str(dfa_states.index(state) + 1) + ' ')
    out_file.write("\n")

    out_file.close()

def epsilon(states, transitions):
    new_state = states
    to_check = states
    already_check = set()

    while to_check:
        state = to_check.pop()              #it is ok to randomly pick one state from to_check set
        already_check.add(state)
        new_state = new_state.union(transitions[state]['e'])
        to_check = new_state.difference(already_check)     # after the epsilon closure, we need to omit the state itself since it's been checked
    return tuple(new_state)

if __name__ == "__main__":
    main()