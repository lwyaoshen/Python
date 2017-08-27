from functools import reduce
'''
map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回。
再看reduce的用法。reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算，其效果就是：reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
'''



def normalize(name):
    return name.capitalize()

def prod(L):
    def a(x,y):
        return x*y
    return reduce(a, L)
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))



def str2float(s):
    def a(x,y):
        return x*10+y
    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    return reduce(a,map(char2num,s.replace('.','')))/(pow(10,len(s.split('.')[1])))
print(type(str2float('123.456')))