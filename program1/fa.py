import goody


def read_fa(file : open) -> {str:{str:str}}:
    dic = dict()
    for line in file:
        new = line.rstrip().split(';')
        start_state = new[0]
        pairs  = zip(new[1::2], new[2::2])
        dic[start_state] = dict(pairs)
    print(dic)
    return dic


def fa_as_str(fa : {str:{str:str}}) -> str:
#     j = ''
#     for key, inner in sorted(fa.items()):
#         l = []
#         for value, state in inner.items():
#             l.append( (value, state) )
#         j += '  {} transitions: {}\n'.format(key, sorted(l))
#     
#     return j 

    j = ''
    for key, inner in sorted(fa.items()):
        l = []
        for value, state in inner.items():
            l.append( (value, state) )
        j += '  {} transitions: {}\n'.format(key, sorted(l))
     
    return j 
    
def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    lst = [state]
    current_state = state
    for x in inputs: 
        if x in fa[current_state]:
            current_state = fa[current_state][x]
            lst.append((x,current_state))
        else: 
            lst.append((x,None))
            break
   
    return lst 
        
    #for key, inner in fa.items():
        #you want to find if the state matches either state in the fa dict
        #if so then take the number in the inputs and match it to it's respective 
        #value and create a tuple and add those tuples in a list 


def interpret(fa_result : [None]) -> str:
    fa_str = 'Start state = ' + str(fa_result[0]) + '\n'
    for x in fa_result[1:]:
        if x[1] == None: 
            fa_str += '  Input = ' + x[0] +'; illegal input: simulation terminated\n'
            break
        else: 
            fa_str += '  Input = ' + x[0] + '; new state = ' + x[1] + '\n' 
    fa_str += 'Stop state = ' + str(x[1]) + '\n'
    return fa_str




if __name__ == '__main__':
    # Write script here
    file = input('Enter the name of a file with a finite automaton: ')
    fa_dict  = read_fa(open(file))
    print(fa_as_str(fa_dict))
    input_file = input('Enter the name of a file with the start-state and input: ')
    
    for line in open(input_file): 
        input_line = line.strip().split(';')
       
        process_line = process(fa_dict, input_line[0], input_line[1:])
       
        print('Starting new simulation \n' + interpret(process_line))

    
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
