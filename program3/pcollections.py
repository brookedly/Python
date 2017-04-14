# Submitter: brookedl(Ly, Brooke)
# Partner  : knquinta(Quintana, Kimberly)
# We certify that we worked cooperatively on this programming
#   assignment, according to the rules for pair programming
import re, traceback, keyword
default = '^[A-Za-z]\w*$'
default2 = '\s*[,]\s*|\s+'

def pnamedtuple(type_name, field_names, mutable=False):
    def show_listing(s):
        for i, l in enumerate(s.split('\n'),1):
            print('{num: >3} {txt}'.format(num=i, txt=l.rstrip()))
  
    def legal_typename(type_name):
        if type(type_name) == str and type_name not in keyword.kwlist and re.match(default, type_name):
            return True #therefore it matches 
        else:
            raise SyntaxError
        
    legal_typename(type_name)
    legal = re.compile(default2)
    
    if type(field_names) not in [str, list]:
        raise SyntaxError
    elif type(field_names) == list:
        field_names = field_names
    else:
        field_names = legal.split(field_names)
    
    field_args = []
    for name in field_names:
        if re.match(default, name) is None or name in keyword.kwlist:
            raise SyntaxError
        field_args.append(name)
    # put your code here
    # bind class_definition (used below) to the string constructed for the class
    class_template = 'class {}:'.format(type_name)

    init_template = '''
    def __init__(self, {}):    
        {}
        self._fields = {}
        self._mutable = {} 
    ''' 
    repr_temp = '''
    def __repr__(self):
        return '{}({})'.format({})
    '''
    
    accessor_temp = '''
    def get_{}(self):
        return self.{}
    '''
    temp = ''
    for arg in field_args:
        temp += accessor_temp.format(arg, arg) +'\n'   
    
    getitem_temp = '''
    def __getitem__(self, index):
#         print('-----', self._fields)
#         print(self.__dict__)
#         for k, v in self.__dict__.items():
#             print('k', k, 'v', v)
        values = []
        if type(index) == int:
            if index < len(self._fields):
                for k, v in sorted(self.__dict__.items()):
                    if len(k)  == 1:
                        values.append(v)
                return values[index]
            else:
                raise IndexError 
        elif type(index) == str:
            if index in self._fields:
                return self.__dict__[index]
            else: 
                raise IndexError
        else:
            raise IndexError 
    '''
        
    equal_temp = ''' 
    def __eq__(self, right):
        if type(self) == type(right) and self.__dict__ == right.__dict__:
            return True
        else:
            return False
    '''
    
    replace_temp = '''
    def _replace(self, **kargs):
        #print('kargs', kargs) 
        for k, v in kargs.items():
            if k not in self._fields:
                raise TypeError 
        if self._mutable == True:
            for k, v in kargs.items():
                for k2, v2 in self.__dict__.items():
                    if k == k2:
                        self.__dict__[k] = v
        else:
            d = dict()
            l = []
            for k, v in self.__dict__.items():
                if k != '_fields' and k != '_mutable':
                    if k in kargs:
                        d[k] = kargs[k]
                    else:
                        d[k] = v 
            for a,b in d.items():
                l.append(b)
            return {}(*l)
        '''
    
    setattr_temp = '''
    def __setattr__(self, name, value):
        if name in self.__dict__:
            if self._mutable == True:
                self.__dict__[name] = value
            else:
                raise AttributeError
        else:
            self.__dict__[name] = value
    '''
    
    # For initial debugging, always show the source code of the class
    #show_listing(class_definition)
    class_definition = class_template.format(type_name)
    class_definition += init_template.format(', '.join(name for name in field_args),'\n        '.join(['self.{} = {}'.format(name, name) for name in field_args]), list(name for name in field_args), mutable)
    class_definition += repr_temp.format(type_name,','.join(['{}={{}}'.format(name) for name in field_args]),', '.join(['self.{}'.format(name, name) for name in field_args]))
    class_definition += temp
    class_definition += getitem_temp
    class_definition += equal_temp
    class_definition += replace_temp.format(type_name)
    class_definition += setattr_temp
    # Execute the class_definition string in a local namespace and bind the
    #   name source_code in its dictionary to the class_defintion; return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict(__name__='pnamedtuple_{type_name}'.format(type_name=type_name))
    try:
        exec(class_definition, name_space)
        name_space[type_name].source_code = class_definition
    except(SyntaxError, TypeError):
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]
    
if __name__ == '__main__':
    import driver
    driver.driver()
