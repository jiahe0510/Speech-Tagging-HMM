import Readfile
import Dictionarysearch
import Sentenceprocess
import Rules

path_train = 'brown.train.tagged.txt'
path_test = 'brown.test.txt'
path_test_result = 'brown.test.tagged.txt'

ds = Dictionarysearch.Dictionarysearch()
sp = Sentenceprocess.Sentenceprocess()
r1 = Readfile.Readfile(path_train)
r1.sentence_process(r1.tag_index)
rules = Rules.Rules()
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


# build a confusion matrix
tag_set = r1.tag_set

tag_array = []
for word in tag_set:
    tag_array.append(word)
tag_array.append('UNK')
confusion_dictionary = {}
confusion_matrix = []
for word in tag_array:
    confusion_dictionary[word] = {}
    for word2 in tag_array:
        confusion_dictionary[word][word2] = 0

# use rules
result_array = []
for word in word_array:

    result = (ds.find_most_frequent_tag(word, r1.tag_dictionary))

    tagged_result = word_tagged_array[index]
    tag = ds.cut_the_tag(tagged_result)
    result = rules.rule(result_array, result)
    if tag.count(result):
        success += 1
    index += 1
    if result.count('UNK'):
        total_unknown += 1
    if tag not in confusion_dictionary[result]:
        continue
    confusion_dictionary[result][tag] += 1
    result_array.append(result)

print(str(success/index*100)+"%")
print("Three are %i unknown words." % total_unknown)

# Print confusion matrix

for row in range(len(tag_array)):
    confusion_matrix.append([])
    for col in range(len(tag_array)):
        confusion_matrix[row].append(confusion_dictionary[tag_array[row]][tag_array[col]])
print("%9s" % "", end='')
for word in tag_array:
    print("%9s" % str(word), end='')
new_index = 0
for row in confusion_matrix:
    start = 1
    while start > 0:
        print()
        start -= 1
    print("%9s" % str(tag_array[new_index]), end='')
    for num in row:
        print("%9s" % num, end='')
    new_index += 1

