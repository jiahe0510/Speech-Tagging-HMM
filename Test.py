import Readfile

r1 = Readfile.Readfile()
path1 = 'brown.train.tagged.txt'
r1.readtxt(path1)
print(r1.text)