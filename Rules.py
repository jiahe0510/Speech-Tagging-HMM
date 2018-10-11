
class Rules:

    @staticmethod
    def rule(array, result):

        '''
        :param array: tag array of previous predictions
        :param result: result before apply the rules
        :return: result after apply the rules
        '''

        index = len(array) - 1
        # Rule 1
        if result == 'UNK':
            result = 'nn'
        # Rule 2: If previous tag is TO, and current tag is NN. Change it to VB
        if index > 0:
            if array[index - 1] == 'to' and result == ('nn', 'UNK'):
                result = 'vb'
        # Rule 3: If one of previous three tag is MD, and current is VBP. Change it to VB.
        if index > 2:
            if result == 'vbp':
                if 'md' == (array[index - 1], array[index - 2], array[index - 3]):
                    result = 'vb'
        # Rule 4: If one of previous two tag is MD, and current is NN. Change it to VB.
        if index > 1:
            if result == 'nn':
                if 'md' == (array[index - 1], array[index - 2]):
                    result = 'vb'
        # Rule 5: If one of the previous 3 tags is HV, and current is VBD, change it to VBN
        if index > 2:
            if result == 'vbd':
                if 'hv' == (array[index - 1], array[index - 2], array[index - 3], array[index - 4]):
                    result = 'vbn'


        return result
