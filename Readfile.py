
class Readfile:

    def __init__(self, path):
        self.text = []
        self.word_tok = []
        self.sent_token = []
        self.total_words = 0
        self.tag_dictionary = {}
        input_file = open(path)
        for lines in input_file:
            self.text.append(lines)

    def __sent_token(self):
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
        times = 0
        start = 0
        length = len(word_with_tag)
        while start < length:
            if word_with_tag[start] == "/":
                if times == 1:
                    break
                else:
                    times += 1
            else:
                start += 1
        word = word_with_tag[0:start]
        tag = word_with_tag[start+1:]
        if word in self.tag_dictionary:
            if tag in self.tag_dictionary[word]:
                self.tag_dictionary[word][tag] += 1
            else:
                self.tag_dictionary[word] = {tag: 1}
        else:
            self.tag_dictionary[word] = {tag: 1}

    def __build_token_dictionary(self):
        for line in self.word_tok:
            for word in line:
                self.total_words += 1
                self.__put_tag_in_book(word)

    def sentence_process(self):
        self.__sent_token()
        self.__sentence_to_word()
        self.__build_token_dictionary()