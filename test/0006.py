
import os

for filename in os.listdir("F://code"):
    print(filename);
test = 'F://code';
test = open(os.path.join(test,"test3.txt"),'w');

test.write("学好Python,立此为证，为了一年后离职。");
test.close();
