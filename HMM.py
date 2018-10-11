import Readfile
import Dictionarysearch
import Sentenceprocess

path_train = 'brown.train.tagged.txt'
path_test = 'brown.test.txt'
path_test_result = 'brown.test.tagged.txt'

ds = Dictionarysearch.Dictionarysearch()
sp = Sentenceprocess.Sentenceprocess()
r1 = Readfile.Readfile(path_train)
r1.sentence_process(r1.hmm_index)
test_file = open(path_test)
test_line = []
test_tagged_file = open(path_test_result)
test_tagged_line = []


for line in test_file:
    test_line.append(line)

for line in test_tagged_file:
    test_tagged_line.append(line)

index = 0
success = 0
total_words = 0
total_unknown = 0
total_index = len(test_line)
percent = total_index/10

for line in test_line:

    tok_word = sp.my_tokenize(line)
    tok_word_tag = sp.my_tokenize(test_tagged_line[index])
    result = ds.hmm_probability_count(tok_word, r1.tag_set, r1.hmm_tag_dictionary, r1.tag_dictionary,
                                   r1.word_dictionary, r1.tag_count_dictionary, r1.total_words)

    index += 1
    result_tag = sp.my_tokenize(result)
    for time in range(len(result_tag)):
        total_words += 1
        if tok_word_tag[time].count(result_tag[time]):
            success += 1
    if index > percent:
        print(str(percent/total_index*100) + "% has been tested")
        percent += total_index / 10


print(str(success / total_words * 100) + "%")



