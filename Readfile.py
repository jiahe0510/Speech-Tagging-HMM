class Readfile:

    import nltk

    def __init__(self):
        self.text = []




    def readtxt(self, path):
        input_file = open(path)
        for lines in input_file:
            self.text.append(lines)
