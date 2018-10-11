from nltk import sent_tokenize


class Readfile:

    def __init__(self, path):
        self.text = []
        self.word_tok = []
        self.sent_token = []
        self.total_words = 0
        self.tag_dictionary = {} #count tag for each word appear how many times
        self.hmm_tag_dictionary = {'start': {}} #tag bigram
        self.word_dictionary = {} #count each word appear how many times
        self.tag_set = set()
        self.tag_count_dictionary = {} #count each tag appear how many times
        self.tag_index = 1
        self.hmm_index = 2
        self.start_tag = 'start'
        input_file = open(path)
        for lines in input_file:
            self.text.append(lines)

    def __sent_token(self):
        for lines in self.text:
            self.sent_token.append(lines)

    def __sent_token_nltk(self):
        for lines in self.text:
            self.sent_token.append(lines)


    def __sentence_to_word(self):
        for line in self.sent_token:
            temp_word_token = self.my_tokenize(line)
            temp_array = []
            for word in temp_word_token:
                temp_array.append(word)
            if len(temp_array) > 0:
                self.word_tok.append(temp_array)

    @staticmethod
    def my_tokenize(line):
        array = []
        start = 0
        end = 0
        length = len(line)
        while end < length:
            if line[end] != " ":
                end += 1
            else:
                string = line[start:end]
                array.append(string)
                start = end + 1
                end += 1

        return array

    def __put_tag_in_book(self, word_with_tag):
        length = len(word_with_tag)
        start = length - 1
        while start >= 0:
            if word_with_tag[start] == "/":
                break
            else:
                start -= 1
        word = word_with_tag[0:start]
        tag = word_with_tag[start+1:]
        self.tag_set.add(tag)
        if tag in self.tag_count_dictionary:
            self.tag_count_dictionary[tag] += 1
        else:
            self.tag_count_dictionary[tag] = 1

        if word in self.word_dictionary:
            self.word_dictionary[word] += 1
        else:
            self.word_dictionary[word] = 1

        if word in self.tag_dictionary:
            if tag in self.tag_dictionary[word]:
                self.tag_dictionary[word][tag] += 1
            else:
                self.tag_dictionary[word][tag] = 1
        else:
            self.tag_dictionary[word] = {tag: 1}

    def __build_token_dictionary(self):
        for line in self.word_tok:
            for word in line:
                self.total_words += 1
                self.__put_tag_in_book(word)

    def sentence_process(self, index):
        if index == self.tag_index:
            self.__sent_token()
        else:
            self.__sent_token_nltk()
        self.__sentence_to_word()
        self.__build_token_dictionary()
        if index == self.hmm_index:
            self.__hmm_dictionary()

    def __hmm_dictionary(self):
        for line in self.word_tok:
            length = len(line)
            start = 0
            start_word = line[start]
            t0 = self.cut_the_tag(start_word)
            if t0 not in self.hmm_tag_dictionary[self.start_tag]:
                self.hmm_tag_dictionary[self.start_tag][t0] = 1
            else:
                self.hmm_tag_dictionary[self.start_tag][t0] += 1
            while start < length - 1:
                first = line[start]
                second = line[start + 1]
                t1 = self.cut_the_tag(first)
                t2 = self.cut_the_tag(second)
                if t1 in self.hmm_tag_dictionary and t2 in self.hmm_tag_dictionary[t1]:
                    self.hmm_tag_dictionary[t1][t2] += 1
                else:
                    if t1 in self.hmm_tag_dictionary:
                        self.hmm_tag_dictionary[t1][t2] = 1
                    else:
                        self.hmm_tag_dictionary[t1] = {t2: 1}
                start += 1

    @staticmethod
    def cut_the_tag(word_with_tag):
        tag = ""
        length = len(word_with_tag)
        start = length - 1
        while start >= 0:
            if word_with_tag[start] == "/":
                tag = word_with_tag[start + 1:]
                break
            else:
                start -= 1
        return tag