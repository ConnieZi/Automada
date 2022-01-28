import sys


filename = sys.argv[1]
in_file = open(filename,'r')

num_states = int(in_file.readline())
alphabet_input = in_file.readline().strip()
transitions = []
start_state = ''
accept_states = []

'''
    construct transitions
'''
for i in range(num_states):
    #every state has a dictionary containing (input:next state) pair
    transitions.append(dict())

for j in range(num_states*len(alphabet_input)): 
    #split every line into a list that has 3 items, [1,'0',4]
    transition_list = in_file.readline().strip().split(' ')
    #[{"'0'": 4, "'1'": 2}, {"'0'": 4, "'1'": 3}, {"'0'": 3, "'1'": 3}, {"'0'": 4, "'1'": 5}, {"'0'": 4, "'1'": 6}, {"'0'": 4, "'1'": 6}]
    transitions[int(transition_list[0])-1][transition_list[1].strip("\'")] = int(transition_list[2])

start_state = int(in_file.readline().strip())       

accept_states = list(map(int, in_file.readline().strip().split(' ')))
# accept_states = in_file.readline().strip().split(' ')
# accept_states = [int(i) for i in accept_states]

'''
    test strings
'''
for read_line in in_file:
    line = read_line.strip()
    current_state = start_state
    for symbol in line[0:len(line)]:
        current_state = transitions[current_state - 1][symbol]
    if current_state in accept_states:
        print('Accept')
    else:
        print('Reject')

in_file.close() 




