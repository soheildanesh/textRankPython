from os import walk

f = []
for (dirpath, dirnames, filenames) in walk("/Users/soheildanesh/GitHub/cam"):
    f.extend(filenames)
    break
print(f)