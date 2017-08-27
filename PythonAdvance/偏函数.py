#转换为二进制数
import functools


def int2(x, base=2):
    return int(x, base)
'''
functools.partial就是帮助我们创建一个偏函数的，不需要我们自己定义int2()，可以直接使用下面的代码创建一个新的函数int2：
'''
int2 = functools.partial(int, base=2)
'''
所以，简单总结functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。
'''