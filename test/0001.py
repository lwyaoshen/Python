#问题描述：第 0001 题：做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？


import random

def gen_code(length = 6):
    code_list = [];
    for i in range(10):
        code_list.append(str(i));
    for i in range(65,91):
        code_list.append(chr(i));
    for i in range(97,123):
        code_list.append(chr(i));
    return (''.join(random.sample(code_list,length)))

if __name__ =='__main__':
    for i in range (199):
        print(gen_code());



