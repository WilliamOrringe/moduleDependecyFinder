import requests
import re
def main():
    print("Selecting modules from source link...")
    url = 'https://intranet.exeter.ac.uk/emps/studentinfo/subjects/computerscience/programmes/2019new/?programmeId='
    #module_code = "2812" #CompSCI Master
    module_code = "2943" # CompSCI Maths Master
    url += module_code
    r = requests.get(url)
    new_contents = str(r.text)
    new_array = []
    for x in range(70):
        x = re.search(r'''(<tr class="orGroup"><td class="first">)((<a href="../../modules/2019/.......">.......</a>)|[.]*)[A-Z|a-z| ]*(</td><td>)([|A-Z|a-z| ]*[|:]*[|-]*[0-9]*)*''', new_contents)
        if x is not None:
            new_contents = re.sub(r'''(<tr class="orGroup"><td class="first">)((<a href="../../modules/2019/.......">.......</a>)|[.]*)[A-Z|a-z| ]*(</td><td>)([|A-Z|a-z| ]*[|:]*[|-]*[0-9]*)*''', "",new_contents,1)
            new_array.append(x.group())
        else:
            x = re.search(r'''(<tr class=""><td class="first">)((<a href="../../modules/2019/.......">.......</a>)|[.]*)[A-Z|a-z| ]*(</td><td>)([|A-Z|a-z| ]*[|:]*[|-]*[0-9]*)*''', new_contents)
            if x is None:
                break
            new_array.append(x.group())
            new_contents = re.sub(r'''(<tr class=""><td class="first">)((<a href="../../modules/2019/.......">.......</a>)|[.]*)[A-Z|a-z| ]*(</td><td>)([|A-Z|a-z| ]*[|:]*[|-]*[0-9]*)*''', "",new_contents,1)
    print("Finished selecting modules from source link...")
    cleanup(new_array)
def cleanup(new_array):
    print("Selecting names and codes of modules...")
    ext = []
    names = []
    new_vals = []
    for x in new_array:
        new_vals = x.split(">")
        del new_vals[0]
        del new_vals[0]
        names.append(new_vals[len(new_vals)-1])
        if "<" in new_vals[0][0]:
            del new_vals[0]
        strX = new_vals[0]
        strX = strX.split("<")
        ext.append(strX[0])
    print("Finished selecting names and codes of modules...")
    next_stage(ext, names)
#############################################################
def next_stage(ext, names):
    print("Selecting the dependencies of the modules")
    deps = []
    url = 'https://intranet.exeter.ac.uk/emps/studentinfo/subjects/computerscience/modules/2019/index.php/?moduleCode='
    for module_code in range(len(ext)):
        r = requests.get(url+str(ext[module_code]))
        new_vals = re.search(r"PRE-REQUISITE.MODULES</th>.(<td>)*(([A-Z][A-Z][A-Z][0-9|A-Z][0-9][0-9][0-9])(,.)*)+</td>+", r.text)
        if new_vals is not None:
            new_vals = re.findall(r"[A-Z][A-Z][A-Z][0-9|A-Z][0-9][0-9][0-9]", str(new_vals))
            deps.append(new_vals)
        else:
            deps.append("None")
            r.close()
    file_w = open("static/toDraw.txt", "w+")
    for count in range(len(ext)):
        try:
            file_w.write(str(names[count])+")"+str(ext[count]) + \
            ")"+str(deps[count][0]))
            if deps[count] != "None":
                try:
                    file_w.write(")" + str(deps[count][1])+"@")
                except:
                    file_w.write("@")
            else:
                file_w.write("one@")
        except:
            print(str(count))
    print("Finished selecting the dependencies of the modules")
####################################################
if __name__ == "__main__":
    main()
