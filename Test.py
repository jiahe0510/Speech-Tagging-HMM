import Readfile

path1 = 'brown.train.tagged.txt'
r1 = Readfile.Readfile(path1)
r1.sentence_process()
for line in r1.sent_token:
    print(line)
