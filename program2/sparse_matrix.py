class Sparse_Matrix:

    # I've written str(...) because it is used in the bsc.txt file and
    #   it is a bit subtle to get correct. This function does not depend
    #   on any other method in this class being written correctly, although
    #   it could be simplified by writing self[...] which calls __getitem__.   
    
    def __init__(self, rows , cols, *args ):
        assert type(rows) ==int and type(cols) ==int
        assert rows > 0
        assert cols > 0
        self.rows = rows
        self.cols = cols
        self.args = args
        #print(self.args)
        self.matrix = dict()
        l = [] 
        for x in self.args:
            l.append(x)
        for x in l:
            tot = l.count(x)
            if tot > 1:
                raise AssertionError
        for tup in args:
            assert type(tup[2]) == int or type(tup[2]) == float             
            if tup[2] != 0: 
                tupl = (tup[0], tup[1])
                self.matrix[tupl] = tup[2]
            if tup[0] == self.rows:
                raise AssertionError
            else:   
                pass        
         
    def size(self):
        return '({}, {})'.format(self.rows, self.cols)
    
    def __str__(self):
        size = str(self.rows) + 'x' + str(self.cols)
        width = max(len(str(self.matrix.get((r,c),0))) for c in range(self.cols) for r in range(self.rows))
        return size+':['+('\n'+(2+len(size))*' ').join ('  '.join('{num: >{width}}'.format(num=self.matrix.get((r,c),0),width=width) for c in range(self.cols))\
                                                                                             for r in range(self.rows))+']'
    def __repr__(self):
        rs = 'Sparse_Matrix(' + str(self.rows) + ',' + str(self.cols) 
        for x in self.args:
            rs += ',' + str(x)
        return rs + ')'
            
    def __len__(self):
        return self.rows * self.cols #multiplying the cols and rows gives back the number of matrices 
    
    def __bool__(self):
        if len(self.matrix) == 0:
            return False
        else:
            return True
    
    def __getitem__(self, item):
        if type(item) == tuple and len(item) == 2 and type(item[0]) == int and type(item[1]) == int and (0 <= item[0] < self.rows) and (0 <= item[1] < self.cols):
            return self.matrix.get(item, 0)
        else:
            raise TypeError

    def __setitem__(self, item, value ):
        if type(item) == tuple and len(item) == 2 and type(item[0]) == int and type(item[1]) == int and (0 <= item[0] < self.rows) and (0 <= item[1] < self.cols) and type(value) == int or type(value) == float:
            if value == 0:
                try:
                    self.matrix.pop((item[0], item[1]))  
                except:
                    pass
            else:
                self.matrix[(item[0], item[1])] = value  
        else:            
            raise TypeError
    
    def __delitem__(self, item):
        if type(item) == tuple and len(item) == 2 and type(item[0]) == int and type(item[1]) == int and (0 <= item[0] < self.rows) and (0 <= item[1] < self.cols):
            for k in self.matrix.keys():
                if k == item:
                    self.matrix[k] = 0 
    
    def row(self, n):
        l = []
        assert type(n) == int and (0 <= n < self.rows)
        for x in range(self.rows):
            for y in range(self.cols):
                if x == n:
                    l.append(self.matrix.get((x, y), 0))
        return tuple(l)
        
    def col(self, n):
        l = []
        assert type(n) == int and (0 <= n < self.cols)
        for x in range(self.rows):
            for y in range(self.cols):
                if y == n:
                    l.append(self.matrix.get((x,y), 0))
        return tuple(l)
    
    def details(self):
        rs = str(self.rows) +'x'+ str(self.cols) +' -> ' + str(self.matrix) + ' -> ' 
        r = []
        for i in range(self.rows): 
            r.append(self.row(i))
            
        return rs + str(tuple(r))
    
    def __call__(self, rows, cols):
        assert rows > 0 and cols > 0
        l = []
        another = self.matrix.copy()
        for k in another:
            if k[0] >= rows or k[1] >= cols: 
                self.matrix.pop(k)
        self.__dict__['rows'] = rows
        self.__dict__['cols'] = cols       
        
        for x in self.matrix:
            l.append((x[0], x[1], self.matrix[x]))
            
        print(Sparse_Matrix(rows, cols, *l)) 
        return Sparse_Matrix(rows,cols, *l)
    
    def __iter__(self):
        s = sorted(self.matrix, key = self.matrix.get )
        for x in range(len(s)):
            s[x] = (s[x][0], s[x][1], self.matrix[s[x]])
        for y in s: 
            yield y
            
            
    def __pos__(self):
        l = []
        for k in self.matrix:
            l.append((k[0], k[1], (self.matrix[k])))
        return Sparse_Matrix(self.rows, self.cols, *l)
    
    def __neg__(self):
        l = []
        for k in self.matrix:
            l.append((k[0], k[1], -(self.matrix[k])))
        return Sparse_Matrix(self.rows, self.cols, *l)
    
    def __abs__(self):
        l = []
        for k in self.matrix:
            if self.matrix[k] < 0:
                l.append((k[0], k[1], abs(self.matrix[k])))
            else:
                l.append((k[0], k[1], self.matrix[k]))
        return Sparse_Matrix(self.rows, self.cols, *l)   
    
    def __add__(self, right):
        l = []
        if type(right) == Sparse_Matrix and Sparse_Matrix.size(right) == Sparse_Matrix.size(self):
            for k in self.matrix:
                for k2 in right.matrix:
                    if k == k2:
                        l.append((k[0], k[1], (self.matrix[k] + right.matrix[k2])))        
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif type(right) == int or type(right) == float:
            for k in self.matrix:
                l.append((k[0], k[1], (self.matrix[k] + right) ))
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif type(right) == Sparse_Matrix and len(right.matrix) ==0:
            raise AssertionError
        else:
            raise TypeError
        
    def __radd__(self, left):
        l = []
        if type(left) == int:
            for k in self.matrix:
                l.append((k[0], k[1], (self.matrix[k] + left)  ))
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif type(left) == str:
            raise TypeError
        
    def __sub__(self, right):    
        l = []
        if type(right) == Sparse_Matrix and Sparse_Matrix.size(right) == Sparse_Matrix.size(self):
            for k in self.matrix:
                for k2 in right.matrix:
                    if k == k2:
                        l.append((k[0], k[1], (self.matrix[k] - right.matrix[k2])))        
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif type(right) == int or type(right) == float:
            for k in self.matrix:
                l.append((k[0], k[1], (self.matrix[k] - right) ))
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif type(right) == Sparse_Matrix and len(right.matrix) ==0:
            raise AssertionError
        else:
            raise TypeError
    
    def __rsub__(self, left):
        l = []
        if type(left) == int:
            for k in self.matrix:
                l.append((k[0], k[1], (left - self.matrix[k] )  ))
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif type(left) == str:
            raise TypeError
    
    def __mul__(self, right):
        rl = []
        l = []
        if type(right) == Sparse_Matrix and (self.cols == right.rows):
            for r in range(self.rows): 
                for c in range(right.cols): 
                    l =[]
                    for i  in range(len(self.row(r))):
                        for j in range(len(right.col(c))):
                            if i == j:
                                l.append((self.row(r)[i]) * (right.col(c)[j]))
                    rl.append((r,c,sum(l)))
            return Sparse_Matrix(self.rows, right.cols, *rl) 
        elif type(right) == int:
            for k in self.matrix:
                l.append((k[0], k[1], (self.matrix[k]*right )   ))
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif right == self:
            raise AssertionError
        else:
            raise TypeError
        
    def __rmul__(self, left):
        l = []
        if type(left) == int:
            for k in self.matrix:
                l.append((k[0], k[1], (self.matrix[k]*left )   ))
            return Sparse_Matrix(self.rows, self.cols, *l)
        elif type(left) != Sparse_Matrix or type(left) != int:
            raise TypeError
        
    def __pow__(self, right):
        l = []
        if type(right) == str or type(right) == Sparse_Matrix:
            raise TypeError
        elif type(right) == int:
            if right <= 0:
                raise AssertionError
            else:
                if len(self.matrix) == 0:
                    raise AssertionError
                else:    
                    for k in self.matrix:
                        l.append((k[0], k[1], (self.matrix[k]**right)))
                    return Sparse_Matrix(self.rows, self.cols, *l)            

    def __eq__(self,right):
        if type(right)  == Sparse_Matrix:
            try:
                return self.size() == right.size() and (all(right.matrix[x] == self.matrix[x] for x in right.matrix)) and (all(self.matrix[x] == right.matrix[x] for x in self.matrix))
            except:
                return False 
        elif type(right) == int:
            if right == 0:
                return len(self.matrix) == 0
            else:
                return (len(self.matrix) == self.__len__()) and all(x[2] == right for x in self.args)
        else: 
            return False
        
    def __setattr__(self, name, value):
        
        if name in self.__dict__:
            raise AssertionError
        self.__dict__[name] = value
    
    
        
        
if __name__ == '__main__':
    #Simple tests before running driver
#     print('Printing')
#     m = Sparse_Matrix(3,3, (0,0,1),(1,1,3),(2,2,1))
#     print(m)
#     print(repr(m))
#     print(m.details())
#   
#     print('\nsize and len')
#     print(m.size(),len(m))
#     
#     print('\ngetitem and setitem')
#     print(m[1,1])
#     m[1,1] = 0
#     m[0,1] = 2
#     print(m.details())
# 
#     print('\niterator')
#     for r,c,v in m:
#         print((r,c),v)
#     
#     print('\nm, m+m, m+1, m==m, m==1')
#     print(m)
#     print(m+m)
#     print(m+1)
#     print(m==m)
#     print(m==1)
#     print()
    
    #driver tests
    import driver
    driver.default_file_name = 'bsc2.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
