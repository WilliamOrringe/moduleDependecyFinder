import requests
import re
def main():
    url = 'https://intranet.exeter.ac.uk/emps/studentinfo/subjects/computerscience/programmes/2019new/?programmeId=2943'
    r = requests.get(url)
    counter = 0
    stage = 0
    new_val = []
    for i in range(10):
        new_val.append([])
    f_one = open("Stage1.txt", "w+")
    f_two = open("Stage2.txt", "w+")
    f_three = open("Stage3.txt", "w+")
    f_four = open("Stage4.txt", "w+")
    for line in enumerate(r):
        if counter != 0 or '''class="stage"''' in str(line):
            if stage == 0:
                f_one.write(str(line))
            elif stage == 1:
                f_two.write(str(line))
            elif stage == 2:
                f_three.write(str(line))
            elif stage == 3:
                f_four.write(str(line))
            if '</div>' in str(line) and counter != 0:
                counter = 1
                stage += 1
                new_val[stage].append(str(line))
            else:
                counter = 1
                new_val[stage].append(str(line))
def cleanup():
    ext = []
    names = []
    for i in range(4):
        file_o = open("Stage" + str(i+1) + ".txt", "r")
        contents = file_o.read()
        x = re.split('''../../modules/2019/*''', contents)
        extensions = []
        chuck = []
        for index, dull in enumerate(x):
            extensions_l = []
            for char in x[index]:
                if char == '''"''':
                    break
                extensions_l.append(char)
            new_ext = ''.join(extensions_l)
            #new_ext = re.sub("[0-9][0-9][0-9]", '', new_ext)
            new_ext = new_ext.replace("(", "").replace(")", "")
            new_ext = re.sub(", b'", '', new_ext)
            new_ext = new_ext.replace("'", "")
            new_ext = re.sub("^[0-9][0-9][0-9]", "", new_ext)
            new_ext = new_ext.replace("/", "")
            new_ext = new_ext[:7]
            extensions.append(new_ext)
            y = re.split('''">*''',x[index])
            #print("==========" + str(y[1]))
            z = re.split('''</a></td>''', str(y[1]))
            for index, item in enumerate(z):
                if "stage" in item or item == []:
                    del z[index]
                    continue
                if "td" in item:
                    new_indexl = 0
                    new_indexr = 0
                    for indexs, char in enumerate(item):
                        if char == ">":
                            new_indexl = indexs + 1
                            break
                    for indexs, char in enumerate(item):
                        if char == "<" and indexs > new_indexl:
                            new_indexr = indexs
                            break
                    new_str = item[new_indexl:new_indexr]
                    new_str = re.sub("[0-9][0-9][0-9]", '', new_str)
                    new_str = new_str.replace("(", "").replace(")", "")
                    new_str = re.sub("', b'", '', new_str)
                    if "<" not in new_str:
                        chuck.append(new_str)
        del extensions[0]
        ext.append(extensions)
        names.append(chuck)
    next_stage(ext, names)
#############################################################

def next_stage(ext, names):
    dependencies = []
    deps = []
    for index in range(4):
        dependencies.append([])
        deps.append([])
        for index_l, naas in enumerate(names[index]):
            print(str(names[index][index_l]) + " : " + str(ext[index][index_l]))
    url = 'https://intranet.exeter.ac.uk/emps/studentinfo/subjects/computerscience/modules/2019/index.php/?moduleCode='
    for index in range(4):
        for module_code in range(len(ext[index])):
            r = requests.get(url+str(ext[index][module_code]))
            #print(ext[index][module_code])
            new_vals = re.search(r"PRE-REQUISITE.MODULES</th>.(<td>)*(([A-Z][A-Z][A-Z][0-9|A-Z][0-9][0-9][0-9])(,.)*)+</td>+", r.text)
            if new_vals is not None:
                new_vals = re.findall(r"[A-Z][A-Z][A-Z][0-9|A-Z][0-9][0-9][0-9]", str(new_vals))
                deps[index].append(new_vals)
                #print(new_vals)
            else:
                deps[index].append("None")
                r.close()

    print(list(deps))
    print(str(len(deps[0]) + len(deps[1]) + len(deps[2]) + len(deps[3])))
    file_w = open("toDraw.txt", "w+")
    for indexs in range(4):
        for count in range(len(ext[indexs])):
            try:
                file_w.write(str(names[indexs][count])+":"+str(ext[indexs][count]) + \
                ":"+str(deps[indexs][count][0]))
                if deps[indexs][count] != "None":
                    try:
                        file_w.write(":" + str(deps[indexs][count][1])+"@")
                    except:
                        file_w.write("@")
                else:
                    file_w.write("one@")
            except:
                print("COUNTER" + str(count * index))

####################################################

if __name__ == "__main__":
    main()
    cleanup()
