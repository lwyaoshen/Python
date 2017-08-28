'''
对于类的方法，装饰器一样起作用。Python内置的@property装饰器就是负责把一个方法变成属性调用的：


'''

class Screen(object):
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self,value):
        if not isinstance(value, int):
            raise ValueError('width must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('width must between 0 ~ 100!')
        self.__width = value

    @property
    def height(self):
        return self.__width

    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            raise ValueError('height must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('height must between 0 ~ 100!')
        self.__height = value

s = Screen()
s.width = 30
print(s.width)
