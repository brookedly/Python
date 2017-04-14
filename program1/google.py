import prompt 
from goody       import safe_open,irange
from collections import defaultdict # Use defaultdict for prefix and query


def all_prefixes(fq : (str,)) -> {(str,)}:
    s = set() 
    for x in range(len(fq)):
        s.add(fq[:x+1])

    #print(s)         
    return s    


def add_query(prefix : {(str,):{(str,)}}, query : {(str,):int}, new_query : (str,)) -> None:
    new_set = all_prefixes(new_query)
    #print('new_set', new_set)
    for pre in new_set:
        prefix[pre].add(new_query)
        #print('pre', pre)
        #print('preffixxxxx', prefix)
    query[new_query] += 1
    
    #print(new_set)
    #print(prefix) #empty defaultdict(set)
    #print('query', query ) #empty defaultdict(int) 
    return None 


def read_queries(open_file : open) -> ({(str,):{(str,)}}, {(str,):int}):
    p,q = defaultdict(set), defaultdict(int)

    for line in open_file:
        line = tuple(line.split())
#         ns = all_prefixes(line)
#         for pre in ns:
#             p[pre].add(line)
#         q[line] += 1
        add_query(p, q, line)
        
    
    return (p,q) 
        


def dict_as_str(d : {None:None}, key : callable=None, reverse : bool=False) -> str:
    j = ''
    for k in sorted(d.keys(), key=key, reverse=reverse):
        j = j + '  {} -> {}\n'.format(k, d.get(k))
    return j 
    

def top_n(a_prefix : (str,), n : int, prefix : {(str,):{(str,)}}, query : {(str,):int}) -> [(str,)]:
    l = []
    for x in prefix[a_prefix]:
        l.append(x)
        l.sort(key = lambda x: (-query[x], x))
    
    return l[:n]
    #want to grab a_prefix from the correct dictionary and append them 
#     for key, value in prefix.items():
#         if a_prefix == key:  
#             lst.append(prefix[key])
            #print(lst)
#             for x in lst:
#                 for thing in x:
#                     print('thing', thing)
#                     #print('x', x)
#                     l.append(query.get(thing))
#                     l = sorted(l, reverse = True)
#                     print('llllllllll', l)
#                     for x in l:
#                         for k2 in query.keys():
#                             if query.get(k2) == x:
#                                 lis.append(k2)
            
    #return lis[:n]
    #print('----------', lis)
    #return lis 
    #add the top 2 

# Script

if __name__ == '__main__':
    # Write script here
    file = input('Enter the name of a file with the full queries: ')
    infile = read_queries(open(file))  
    p, q = infile
    while True:
        print('Prefix dictionary: ')
        print(dict_as_str(p))  
        print('Query dictionary: ')
        print(dict_as_str(q))
        Aprefix = input('Enter a prefix (or quit): ')
        if Aprefix.strip() == 'quit':
            break
        else: 
            print('Top 3 (at the most) full queries = ')
            print(top_n(Aprefix, 3, p, q))
        full_query = input('Enter a full query (or quit): ')
        if full_query == 'quit':
            break 
        else:
            add_query(infile[0], infile[1], tuple(full_query.split()))
            
            
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
