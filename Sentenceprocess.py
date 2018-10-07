
class Sentenceprocess:

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

    def sentence2word(self, text):
        result = []
        for line in text:
            temp_word_token = self.my_tokenize(line)
            for word in temp_word_token:
                result.append(word)
        return result
