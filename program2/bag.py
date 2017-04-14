from collections import defaultdict
from goody import type_as_str
from hmac import new


class Bag:
    
    def __init__(self, letters = []):
        self.bag = defaultdict(int)
        self.letters = list(letters)
        print('-------', self.letters)
        for x in letters:
            self.bag[x] += 1
            
    def __repr__(self):
        result = []
        for x in self.bag: 
            for y in range(self.bag[x]):
                result.append(x)
        result.sort()
        return 'Bag(' + str(result) + ')'
    
    def __str__(self):
        default = 'Bag('
        if len(self.bag) == 0:
            return default + ')'
        else:
            string = ''
            for letter, value in self.bag.items():
                string += '{}[{}]'.format(letter, value)
            return 'Bag(' + string + ')'
    
    def __len__(self):
        sum = 0
        for times in self.bag.values():
            sum += times
        return sum
    
    def unique(self):
        return len(self.bag.keys())
    
    def __contains__(self, item):
        if item in self.bag.keys():
            return True
        else:
            return False
        
    def count(self, item):
        if item not in self.bag.keys():
            return 0
        else:
            return self.bag[item]
   
    def __add__(self, right):
        if type(right) == Bag:
            return Bag(list(self.letters) + list(right.letters))
#             return self.bag.update(right.bag)
        else:
            raise TypeError
    
    def add(self, item):
        if item not in self.bag.keys():
            self.bag[item] = 1
        else:
            self.bag[item] += 1
    
    def remove(self, item):
        if item in self.bag.keys():
            self.bag[item] -= 1
            if self.bag[item] == 0:
                del self.bag[item]
        else:
            raise ValueError
        
         
    def __eq__(self, right):
        if type(right) == Bag:
            for l, v in self.bag.items():
                for l2, v2 in right.bag.items():
                    if l == l2 and v == v2:
                        return True
            
                    else:
                        return False
        else:
            return False
        
    def __ne__(self, right):
        if type(right) != Bag:
            return True
        else:
            return False 
        
    def __iter__(self):
        l = []
        for k in self.bag:
            for x in range(self.bag[k]):
                l.append(k)
        #print('l', l)
        for thing in l:
            #print(thing)
            yield thing
        
        
           
if __name__ == '__main__':
    # You can put your own code to test Bags here

    print()
    import driver
    driver.default_file_name = 'bsc1.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
