
content = open("F://code/filter.txt",'r');
filter = [];
for line in content.readlines():
    filter.append(line);

input = input("input your words:");
for i in range(len(filter)):
    if input.find(filter[i].strip())>-1:
        print("yes");
        break;
    else:
        continue;

