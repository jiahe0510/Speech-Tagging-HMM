import numpy as np


class Dictionarysearch:

    @staticmethod
    def find_most_frequent_tag(word, dictionary):
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

    def hmm_probability_count(self, sentence, tag_set, hmm_dictionary, tag_dictionary, word_dictionary, tag_count_dictionary, total_words):
        sentence_length = len(sentence)
        tag_list = list(tag_set)

        tag_length = len(tag_list)
        start_word = sentence[0]
        matrix = np.zeros((tag_length, sentence_length))
        small = 0.00000001
        result = []
        for row in range(tag_length):
            current_tag = tag_list[row]
            if start_word in tag_dictionary:
                if current_tag in tag_dictionary[start_word]:
                    if current_tag in hmm_dictionary['start']:
                        matrix[row][0] = tag_dictionary[start_word][current_tag] / word_dictionary[start_word] * \
                                           hmm_dictionary['start'][current_tag] / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
                    else:
                        matrix[row][0] = tag_dictionary[start_word][current_tag] / word_dictionary[start_word] * small / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
                else:
                    if current_tag in hmm_dictionary['start']:
                        matrix[row][0] = small / word_dictionary[start_word] * hmm_dictionary['start'][current_tag] / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
                    else:
                        matrix[row][0] = small / word_dictionary[start_word] * small / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
            else:
                matrix[row][0] = small / total_words * small / tag_count_dictionary[current_tag]
                result.append([str(current_tag) + ' '])

#       The following part is starting from second word of a sentence.

        for col in range(1, sentence_length):
            next_word = sentence[col]
            for row in range(tag_length):
                current_tag = tag_list[row]
                self.max_probability(col, row, next_word, current_tag, matrix, result,
                                     hmm_dictionary, tag_dictionary, word_dictionary, tag_count_dictionary,
                                     tag_list, total_words, small)

        result_string = result[0][sentence_length-1]
        temp_max = matrix[0][sentence_length-1]
        for index in range(1, tag_length):
            if matrix[index][sentence_length-1] > temp_max:
                temp_max = matrix[index][sentence_length-1]
                result_string = result[index][sentence_length-1]
        return result_string

    @staticmethod
    def max_probability(col, row, word, tag, matrix, result, hmm, one, word_dctionary, tag_count_dictionary, tag_list, total, small):
        maximum = 0
        index_tag = 0
        for index in range(len(tag_list)):
            previous_tag = tag_list[index]
            if word in one:
                if tag in one[word]:
                    if tag in hmm[previous_tag]:
                        temp_probability = one[word][tag] / word_dctionary[word] * hmm[previous_tag][tag] / tag_count_dictionary[tag] * matrix[index][col-1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
                    else:
                        temp_probability = one[word][tag] / word_dctionary[word] * small / tag_count_dictionary[tag] * matrix[index][col - 1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
                else:
                    if tag in hmm[previous_tag]:
                        temp_probability = small / word_dctionary[word] * hmm[previous_tag][tag] / tag_count_dictionary[tag] * matrix[index][col - 1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
                    else:
                        temp_probability = small / word_dctionary[word] * small / tag_count_dictionary[tag] * matrix[index][col - 1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
            else:
                temp_probability = small / total * small / tag_count_dictionary[tag] * matrix[index][col - 1]
                if temp_probability > maximum:
                    maximum = temp_probability
                    matrix[row][col] = temp_probability
                    index_tag = index
        result[row].append(result[index_tag][col-1] + str(tag) + ' ')

# The following methods implements beam algorithm in Vertibi algorithm
    def hmm_probability_count_beam(self, sentence, tag_set, hmm_dictionary, tag_dictionary, word_dictionary, tag_count_dictionary, total_words, beam):
        sentence_length = len(sentence)
        tag_list = list(tag_set)

        tag_length = len(tag_list)
        start_word = sentence[0]
        matrix = np.zeros((tag_length, sentence_length))
        small = 0.00000001
        result = []
        for row in range(tag_length):
            current_tag = tag_list[row]
            if start_word in tag_dictionary:
                if current_tag in tag_dictionary[start_word]:
                    if current_tag in hmm_dictionary['start']:
                        matrix[row][0] = tag_dictionary[start_word][current_tag] / word_dictionary[start_word] * \
                                           hmm_dictionary['start'][current_tag] / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
                    else:
                        matrix[row][0] = tag_dictionary[start_word][current_tag] / word_dictionary[start_word] * small / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
                else:
                    if current_tag in hmm_dictionary['start']:
                        matrix[row][0] = small / word_dictionary[start_word] * hmm_dictionary['start'][current_tag] / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
                    else:
                        matrix[row][0] = small / word_dictionary[start_word] * small / tag_count_dictionary[current_tag]
                        result.append([str(current_tag) + ' '])
            else:
                matrix[row][0] = small / total_words * small / tag_count_dictionary[current_tag]
                result.append([str(current_tag) + ' '])

#       The following part is starting from second word of a sentence.

        for col in range(1, sentence_length):
            next_word = sentence[col]
            t_set = self.beam_search(beam, tag_dictionary, next_word)
            for row in range(tag_length):
                current_tag = tag_list[row]
                if current_tag not in t_set:
                    result[row].append(' ')
                    continue
                self.max_probability_beam(col, row, next_word, current_tag, matrix, result,
                                     hmm_dictionary, tag_dictionary, word_dictionary, tag_count_dictionary,
                                     tag_list, total_words, small)

        result_string = ''
        temp_max = 0
        for index in range(tag_length):

            if matrix[index][sentence_length-1] >= temp_max:
                temp_max = matrix[index][sentence_length-1]
                result_string = result[index][sentence_length-1]
        return result_string

    @staticmethod
    def max_probability_beam(col, row, word, tag, matrix, result, hmm, one, word_dctionary, tag_count_dictionary, tag_list, total, small):
        maximum = 0
        index_tag = 0
        for index in range(len(tag_list)):
            if matrix[index][col-1] == 0:
                continue
            previous_tag = tag_list[index]
            if word in one:
                if tag in one[word]:
                    if tag in hmm[previous_tag]:
                        temp_probability = one[word][tag] / word_dctionary[word] * hmm[previous_tag][tag] / tag_count_dictionary[tag] * matrix[index][col-1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
                    else:
                        temp_probability = one[word][tag] / word_dctionary[word] * small / tag_count_dictionary[tag] * matrix[index][col - 1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
                else:
                    if tag in hmm[previous_tag]:
                        temp_probability = small / word_dctionary[word] * hmm[previous_tag][tag] / tag_count_dictionary[tag] * matrix[index][col - 1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
                    else:
                        temp_probability = small / word_dctionary[word] * small / tag_count_dictionary[tag] * matrix[index][col - 1]
                        if temp_probability > maximum:
                            maximum = temp_probability
                            matrix[row][col] = temp_probability
                            index_tag = index
            else:
                temp_probability = small / total * small / tag_count_dictionary[tag] * matrix[index][col - 1]
                if temp_probability > maximum:
                    maximum = temp_probability
                    matrix[row][col] = temp_probability
                    index_tag = index

        result[row].append(result[index_tag][col-1] + str(tag) + ' ')

    @staticmethod
    def beam_search(beam, dictionary, word):
        result = []
        tag_result = set()
        if word not in dictionary:
            return set('nn')
        for tag in dictionary[word]:
            result.append(dictionary[word][tag])
        result = sorted(result)
        length = len(result)
        start = length-1
        while start >= 0 and beam >= 0:
            for tag in dictionary[word]:
                if dictionary[word][tag] == result[start]:
                    tag_result.add(tag)
            start -= 1
            beam -= 1
        return tag_result
