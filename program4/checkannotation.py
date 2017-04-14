# Submitter: brookedl(Ly, Brooke)
# Partner  : knquinta(Quintana, Kimberly)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
from goody import type_as_str
import inspect
from collections import defaultdict

class Bag:
    def __init__(self,values=[]):
        self.counts = defaultdict(int)
        for v in values:
            self.counts[v] += 1
    
    def __str__(self):
        return 'Bag('+', '.join([str(k)+'['+str(v)+']' for k,v in self.counts.items()])+')'

    def __repr__(self):
        param = []
        for k,v in self.counts.items():
            param += v*[k]
        return 'Bag('+str(param)+')'

    def __len__(self):
        return sum(self.counts.values())
        
    def unique(self):
        return len(self.counts)
        
    def __contains__(self,v):
        return v in self.counts
    
    def count(self,v):
        return self.counts[v] if v in self.counts else 0

    def add(self,v):
        self.counts[v] += 1
    
    def remove(self,v):
        if v in self.counts:
            self.counts[v] -= 1
            if self.counts[v] == 0:
                del self.counts[v]
        else:
            raise ValueError('Bag.remove('+str(v)+'): not in Bag')
        
    def __eq__(self,right):
        if type(right) is not Bag or len(self) != len(right):
            return False
        else:
            for i in self.counts:
                # check not it to avoid creating count of 0 via defaultdict
                if i not in right or self.counts[i] != right.counts[i]:
                    return False
            return True
        
    @staticmethod
    def _gen(x):
        for k,v in x.items():
            for i in range(v):
                yield k  
                
    def __iter__(self):
        return Bag._gen(dict(self.counts))
    
    #define this method to implement the check annotation protocol
    #The check parameter refers to the check function in Check_Annotation,
    #  so that it can be called from here
    def __check_annotation__(self, check, param, value, text_history):
        pass

class Check_All_OK:
    """
    Check_All_OK class implements __check_annotation__ by checking whether each
      annotation passed to its constructor is OK; the first one that
      fails (by raising AssertionError) prints its problem, with a list of all
      annotations being tried at the end of the check_history.
    """
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_All_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value,check_history):
        for annot in self._annotations:
            check(param, annot, value, check_history+'Check_All_OK check: '+str(annot)+' while trying: '+str(self)+'\n')

class Check_Any_OK:
    """
    Check_Any_OK implements __check_annotation__ by checking whether at least
      one of the annotations passed to its constructor is OK; if all fail 
      (by raising AssertionError) this classes raises AssertionError and prints
      its failure, along with a list of all annotations tried followed by the
      check_history.
    """
    def __init__(self,*args):
        self._annotations = args
        
    def __repr__(self):
        return 'Check_Any_OK('+','.join([str(i) for i in self._annotations])+')'

    def __check_annotation__(self, check, param, value, check_history):
        failed = 0
        for annot in self._annotations: 
            try:
                check(param, annot, value, check_history)
            except AssertionError:
                failed += 1
        if failed == len(self._annotations):
            assert False, repr(param)+' failed annotation check(Check_Any_OK): value = '+repr(value)+\
                         '\n  tried '+str(self)+'\n'+check_history                 

class Check_Annotation():
    # set name to True for checking to occur
    checking_on  = True
  
    # self._checking_on must also be true for checking to occur
    def __init__(self,f):
        self._f = f
        self.checking_on = True
        
    # Check whether param's annot is correct for value, adding to check_history
    #    if recurs; defines many local function which use it parameters.  
    def check(self,param,annot,value,check_history=''):        
        def list_check():
            #print(param, ';', annot, ';', value) 
            if type(annot) == list:
                assert isinstance(value, list)
            elif type(annot) == tuple:
                assert isinstance(value, tuple)

            if len(annot) == 1:
                for v in value:
                    self.check(param, annot[0], v)
            else:
                assert len(value) == len(annot)
                for x in range(len(annot)):
                    self.check(param, annot[x], value[x])

        def dict_check():
            assert isinstance(value, dict)
            assert len(annot.items()) == 1
            for k, v in annot.items():
            
                for k2, v2 in value.items():
                    
                    self.check(param, k, k2)
                    self.check(param, v, v2)
                    
                    
        def set_check():
            if type(annot) == set:
                assert isinstance(value, set)
            elif type(annot) == frozenset:
                assert isinstance(value, frozenset)
            for a in annot:
                for x in value:
                    assert isinstance(x, a)
    
        def lambda_check():
            #print(annot, ';', value, ';', param)
            #print('-----', annot.__code__.co_varnames)
            assert len(annot.__code__.co_varnames) == 1
            try: 
                assert annot(value)
            except:
                raise AssertionError
            
        def str_check():
            try: 
                assert eval(annot, self._parameters)
            except:
                assert False
        # Define local functions for checking, list/tuple, dict, set/frozenset,
        #   lambda/functions, and str (str for extra credit)
        # Many of these local functions called by check, call check on their
        #   elements (thus are indirectly recursive)

        # Decode the annotation here and check it 
        #print(annot, ';', value)

        if annot == None:
            pass
        elif type(annot) == type:
            assert isinstance(value, annot)
        elif type(annot) == list or type(annot) == tuple:
            list_check()
        elif isinstance(annot, dict):
            dict_check()
        elif isinstance(annot, set) or isinstance(annot, frozenset):
            set_check()
        elif inspect.isfunction(annot):
            lambda_check()
        elif type(annot) == str:
            str_check()
        else:
            try: 
                annot.__check_annotation__()
            except:
                raise AssertionError
            
    # Return result of calling decorated function call, checking present
    #   parameter/return annotations if required
    def __call__(self, *args, **kargs):
        # Return a dictionary of the parameter/argument bindings (actually an
        #    ordereddict, in the order parameters occur in the function's header)
        def param_arg_bindings():
            f_signature  = inspect.signature(self._f)
            bound_f_signature = f_signature.bind(*args,**kargs)
            for param in f_signature.parameters.values():
                if param.name not in bound_f_signature.arguments:
                    bound_f_signature.arguments[param.name] = param.default
            return bound_f_signature.arguments
        
        if self.checking_on == True and Check_Annotation.checking_on == True:
            pass
        else:
            return self._f(*args, **kargs)
 
        self._parameters = param_arg_bindings()
        #print('-----', self._parameters)
        annot = self._f.__annotations__
        #print('******', annot)
        # If annotation checking is turned off at the class or function level
        #   just return the result of calling the decorated function
        # Otherwise do all the annotation checking
        
        try:
            # Check the annotation for every parameter (if there is one)
            for k in self._parameters.keys():
                if k in annot:
                    self.check(k, annot[k], self._parameters[k])
                else:
                    pass
            # Compute/remember the value of the decorated function
            remember_val = self._f(*args, **kargs)
            # If 'return' is in the annotation, check it
            if 'return' in annot:
                self._parameters['_return'] = remember_val
                self.check('return', annot['return'], remember_val)
            return remember_val
            # Return the decorated answer
            
    #remove after adding real code in try/except
            
        # On first AssertionError, print the source lines of the function and reraise 
        except AssertionError:
#             print(80*'-')
#             for l in inspect.getsourcelines(self._f)[0]: # ignore starting line #
#                 print(l.rstrip())
#             print(80*'-')
            raise

if __name__ == '__main__':     
    # an example of testing a simple annotation  
#     def f(x:int): pass
#     f = Check_Annotation(f)
#     f(3)
#     f('a')
           
    import driver
    driver.driver()
