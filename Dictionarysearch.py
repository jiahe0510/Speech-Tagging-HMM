

class Dictionarysearch:

    def find_most_frequent_tag(self, word, dictionary):
        temp_tag = ''
        temp_probability = 0
        if word in dictionary:
            for tag in dictionary[word]:
                if dictionary[word][tag] > temp_probability:
                    temp_probability = dictionary[word][tag]
                    temp_tag = tag
            return temp_tag
        else:
            return 'UNK'

