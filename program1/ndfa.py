import goody
from collections import defaultdict 

def read_ndfa(file : open) -> {str:{str:{str}}}:
    dic = dict()
    for line in file:
        inner = defaultdict(set)  #for the inner dictionary 
        line = line.rstrip().split(';')
        #print(line)
        for (digit, state) in zip(line[1::2], line[2::2]):
            print('----', state, digit)
            inner[digit].add(state)
        dic[line[0]] = inner
    
    #print(dic)
    return dic
    

def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    j = ''
    for k, v in sorted(ndfa.items()): 
        #print(v.items())
        if v == {}:
            tup = []
            j += '  {} transitions: {}\n'.format(k, tup)

        else:    
            li = []
            for x, y in sorted(v.items()):
                l = list(y)
                tup = (x, sorted(l))
                li.append(tup)
                
            j += '  {} transitions: {}\n'.format(k, li)
    
    #print(j)
    return j
    
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
#    lst = [state]
#     current_state = [state]
#     for x in inputs: 
#         new = set()
#         for state in current_state:
#             if x in ndfa[state]:
#                 for trans in ndfa[state][x]:
#                     new.add(trans)
#         if x in ndfa[state]:
#             lst.append((x,new))
#             current_state = list(new)
#    
#     return lst
    lst = [state]
    current_state = set([state])
    for x in inputs:
        possible_states = set()
        for state in current_state:
            if x in ndfa[state]:
                for trans in ndfa[state][x]:
                    possible_states.add(trans) 
        lst.append((x,possible_states))
        
        if possible_states == set(): #if the set is empty the returned list should be just the state
            return lst
        current_state = possible_states
    return lst
        

def interpret(result : [None]) -> str:
    ndfa_str = 'Start state = ' + str(result[0]) + '\n'
    for x in (result[1:]):
        if x[1] == None: 
            ndfa_str += '  Input = ' + x[0] +'; illegal input: simulation terminated\n'
            break
        else: 
            ndfa_str += '  Input = ' + x[0] + '; new possible states = ' + str(x[1]) + '\n' 
    ndfa_str += 'Stop state = ' + str(list(x[1])) + '\n'
    return ndfa_str




if __name__ == '__main__':
    # Write script here
    file = input('Enter the name of a file with a non-deterministic finite automaton: ')
    ndfa = (read_ndfa(open(file)))
    print('Non-Deterministic Finite Automaton')
    print(ndfa_as_str(ndfa))
    input_file = input('Enter the name of a file with the start-state and input: ')
     
    for line in open(input_file):
        input_line = line.strip().split(';')
        process_line = process(ndfa, input_line[0], input_line[1:])
        print('Starting new stimulation \n' + interpret(process_line))
                            
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
