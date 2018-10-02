from nltk import word_tokenize, sent_tokenize


class Readfile:


    def __init__(self, path):
        self.text = []
        self.word_tok = []
        self.sent_token = []
        input_file = open(path)
        for lines in input_file:
            self.text.append(lines)


    def __sent_token(self):
        for lines in self.text:
            temp = sent_tokenize(lines)
            for line in temp:
                self.sent_token.append(line)

    def sentence_process(self):
        self.__sent_token()