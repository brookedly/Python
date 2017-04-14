import goody
from collections import defaultdict

def read_voter_preferences(file : open):
    dic = dict()
    #lines = file.readlines() 
    for l in file:
        new = l.rstrip().split(';')
        dic[new[0]] = (new[1:])
#    print(dic)
    return dic    

def dict_as_str(d : {None:None}, key : callable=None, reverse : bool=False) -> str:
    j = ''
    for k in sorted(d.keys(), key = key, reverse=reverse):
        listed = list(d.get(k))
        j = j + '  {} -> {}\n'.format(k, d.get(k))
    return j 

def evaluate_ballot(vp : {str:[str]}, cie : {str}) -> {str:int}: 
    v = {}
    for candi in cie:
        v[candi] = int()
    
    for candidate_list in vp.values():
        for candi in candidate_list:
            if candi in cie:
                v[candi] += 1 
                break
    
    return v 

def remaining_candidates(vd : {str:int}) -> {str}:
    dic = set() 
    less_votes = min(vd.values())
    for key, v in vd.items():
        if v > less_votes:
            dic.update(key)
    
    return dic
    
def run_election(vp_file : open) -> {str}:
    
    dic = read_voter_preferences(open(vp_file))
    print('Voter Preferences')
    print(dict_as_str(dic))
    for key, value in dic.items():
        cie = value
    cie = set(cie) 
    #return set(cie)
    count_ballot = 1
    while len(cie) > 1:
        eval_ballot = evaluate_ballot(dic,cie)
        print('Vote count on ballot #{} with candidates (alphabetical order): remaining candidates = {}'.format(str(count_ballot), str(cie)))
        print(dict_as_str(dic))
        print('Vote count on ballot #{} with candidates (numerical order): remaining candidates = {}'.format(str(count_ballot), str(cie)))
        print(dict_as_str (dic))
        cie = remaining_candidates(eval_ballot)
        count_ballot += 1
    if len(cie) == 1:
        print('Winner is ',cie)
    else:
        print('No winner; the election has come to a tie between each candidates.')
    return cie
    
    
    
    
    #s = set() 
    #or you can return '{ with the str in it brackets }'
    

  
    
if __name__ == '__main__':
    # Write script here
    file = input('Enter the name of a file with voter preferences: ')

    run_election(file)
    
    #run_election(file)
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
