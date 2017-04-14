# Submitter: brookedl(Ly, Brooke)
# Partner  : jcapulet(Capulet, Kim)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    dic = defaultdict(set)
    #lines = file.readlines()
    for l in file:
        new = l.rstrip().split(';')
        start = new[0]
        destin_nodes = new[1:]
        dic[start].update(destin_nodes)
    
    return dic 

def graph_as_str(graph : {str:{str}}) -> str:
    j = '' 
    for k, v in sorted(graph.items()):
        #print('k', k, 'v', v)
        listed = list(v)
        j = j + '  {} -> {}\n'.format(k, sorted(listed)) 
    return j
    

        
def reachable(graph : {str:{str}}, start : str) -> {str}:
    reached_nodes, exploring_list = set(), list(start) 
    for v in exploring_list:
        
        graph.get(start)
    





if __name__ == '__main__':
    # Write script here
    file = input('Enter the name of a file with a graph: ')
    graph = read_graph(open(file)) 
    print('Graph: source -> {destination} edges')
    print(graph_as_str(graph))
    starting_node = input('Enter the name of a starting node: ')
    r = reachable(graph, starting_node)
    print('From {} the reachable nodes are {}'.format(starting_node, r))
    
    
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
