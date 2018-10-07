import Readfile
import Dictionarysearch
import Sentenceprocess

path_train = 'brown.train.tagged.txt'
path_test = 'brown.test.txt'
path_test_result = 'brown.test.tagged.txt'

ds = Dictionarysearch.Dictionarysearch()
sp = Sentenceprocess.Sentenceprocess()
r1 = Readfile.Readfile(path_train)
r1.sentence_process()
test_file = open(path_test)
test_line = []
test_tagged_file = open(path_test_result)
test_tagged_line = []
for line in test_file:
    test_line.append(line)
for line in test_tagged_file:
    test_tagged_line.append(line)

word_array = sp.sentence2word(test_line)

word_tagged_array = sp.sentence2word(test_tagged_line)
index = 0
success = 0
total_unknown = 0
print(len(word_array))
print(len(word_tagged_array))

for word in word_array:

    result = (ds.find_most_frequent_tag(word, r1.tag_dictionary))
    if result.count('UNK'):
        total_unknown += 1
    tagged_result = word_tagged_array[index]
    if tagged_result[len(tagged_result)-len(result):].count(result):
        success += 1
    index += 1
    print(result + " | " + tagged_result[len(tagged_result)-len(result):])

print(str(success/index)+"%")
print("Three are %i unknown words." % total_unknown)


