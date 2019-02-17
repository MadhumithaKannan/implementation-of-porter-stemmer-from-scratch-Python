from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

nltk.download('punkt')


class porter:

    def isvowel(self, l):
        letter = l.lower()
        if (letter == 'a' or letter == 'e' or letter == 'o' or letter == 'i' or letter == 'u'):
            return True
        else:
            return False

    def iscons(self, l):
        return (not self.isvowel(l))

    def form(self, word):
        pattern = []
        fstr = ''
        for i in range(0, len(word)):
            if self.isvowel(word[i]):
                pattern.append('V')
            else:
                pattern.append('C')
        for j in pattern:
            fstr += j
        return fstr

    def m_count(self, word):
        form_string = self.form(word)
        count = form_string.count('VC')
        return (count)

    def get_base(self, word, suf):
        suflen = word.rfind(suf)
        base = word[:suflen]
        return base

    def replacer(self, word, suf1, suf2):
        base = self.get_base(word, suf1)
        base += suf2
        return base

    # *s
    def endswith_s(self, stem):
        if stem.endswith('s'):
            return True
        else:
            return False

    # *v*
    def contains_vowel(self, stem):
        for i in range(0, len(stem)):
            if self.isvowel(stem[i]):
                return True
        return False

    # *d
    def CC(self, stem):
        pattern = self.form(stem)
        if pattern[-1] == 'C' and pattern[-2] == 'C':
            return True
        else:
            return False

    # *o
    def CVC(self, stem):
        stem = stem.lower()
        pattern = self.form(stem)
        if pattern[-1] == 'C' and pattern[-2] == 'V' and pattern[-3] == 'C' and stem[-1] not in 'xyz':
            return True
        else:
            return False

    def step_1a(self, word):
        word = word.lower()
        new_word = word
        if word.endswith('sses'):
            # suflen=word.rfind('sses')
            # base=word[:suflen]
            new_word = self.replacer(word, 'sses', 'ss')
            # print(new_word)
        elif word.endswith('ies'):
            new_word = self.replacer(word, 'ies', 'i')
        elif word.endswith('ss'):
            new_word = word
        elif word.endswith('s'):
            new_word = self.replacer(word, 's', '')
        return (new_word)

    def step_1b(self, word):
        new_word = word
        if word.endswith('eed'):
            # print('ends with eed')
            suflen = len('eed')
            base = word[:suflen]
            if self.m_count(base) > 0:
                new_word = self.replacer(word, 'eed', 'ee')
                # return(new_word)
        elif word.endswith('ed'):
            suflen = word.rfind('ed')
            base = word[:suflen]
            if self.contains_vowel(base):
                new_word = word[:suflen]
                new_word = self.part_1b(new_word)
                # return(new)
        elif word.endswith('ing'):
            suflen = word.rfind('ing')
            base = word[:suflen]
            if self.contains_vowel(base):
                new_word = word[:suflen]
                print(new_word)
                new_word = self.part_1b(new_word)
                # return(new)
        return (new_word)

    def part_1b(self, word):
        # print("func called")
        if (word.endswith('at') or word.endswith('bl') or word.endswith('iz')):
            # print("first if")
            word += 'e'
            print(word)
        elif self.CC(word) and not word.endswith('s') and not word.endswith('z') and not word.endswith('l'):
            # print("YES")
            word = word[:-1]
        elif self.m_count(word) == 1 and self.CVC(word):
            word += 'e'
        return (word)

    def step_1c(self, word):
        if self.contains_vowel(word) and word.endswith('y'):
            return (self.replacer(word, 'y', 'i'))
        else:
            return (word)

    def step_2(self, word):
        if word[-2] == 'a':
            if word.endswith('ational'):
                base = self.get_base(word, 'ational')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'ational', 'ate')
            elif word.endswith('tional'):
                base = self.get_base(word, 'tional')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'tional', 'tion')
        elif word[-2] == 'c':
            if word.endswith('enci'):
                base = self.get_base(word, 'enci')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'enci', 'ence')
            elif word.endswith('anci'):
                base = self.get_base(word, 'anci')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'anci', 'ance')
        elif word[-2] == 'z':
            if word.endswith('izer'):
                base = self.get_base(word, 'izer')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'izer', 'ize')
        elif word[-2] == 'l':
            if word.endswith('abli'):
                base = self.get_base(word, 'abli')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'abli', 'able')
            elif word.endswith('alli'):
                base = self.get_base(word, 'alli')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'alli', 'al')
            elif word.endswith('entli'):
                base = self.get_base(word, 'entli')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'entli', 'ent')
            elif word.endswith('eli'):
                base = self.get_base(word, 'eli')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'eli', 'e')
            elif word.endswith('ousli'):
                base = self.get_base(word, 'ousli')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'ousli', 'ous')
        elif word[-2] == 'o':
            if word.endswith('ation'):
                base = self.get_base(word, 'ation')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'ation', 'ate')
            elif word.endswith('ization'):
                base = self.get_base(word, 'ization')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'ization', 'ize')
            elif word.endswith('ator'):
                base = self.get_base(word, 'ator')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'ator', 'ate')
        elif word[-2] == 's':
            if word.endswith('alism'):
                base = self.get_base(word, 'alism')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'alism', 'al')
            elif word.endswith('iveness'):
                base = self.get_base(word, 'iveness')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'iveness', 'ive')
            elif word.endswith('fulness'):
                base = self.get_base(word, 'fulness')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'fulness', 'ful')
            elif word.endswith('ousness'):
                base = self.get_base(word, 'ousness')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'ousness', 'ous')
        elif word[-2] == 't':
            if word.endswith('aliti'):
                base = self.get_base(word, 'aliti')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'aliti', 'al')
            elif word.endswith('iviti'):
                base = self.get_base(word, 'iviti')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'iviti', 'ive')
            elif word.endswith('biliti'):
                base = self.get_base(word, 'biliti')
                if self.m_count(base) > 0:
                    word = self.replacer(word, 'biliti', 'ble')
        return (word)

    def step_3(self, word):
        if word.endswith('icate'):
            base = self.get_base(word, 'icate')
            if self.m_count(base) > 0:
                word = self.replacer(word, 'icate', 'ic')
        elif word.endswith('ative'):
            base = self.get_base(word, 'ative')
            if self.m_count(base) > 0:
                word = self.replacer(word, 'ative', '')
        elif word.endswith('alize'):
            base = self.get_base(word, 'alize')
            if self.m_count(base) > 0:
                word = self.replacer(word, 'alize', 'al')
        elif word.endswith('iciti'):
            base = self.get_base(word, 'iciti')
            if self.m_count(base) > 0:
                word = self.replacer(word, 'iciti', 'ic')
        elif word.endswith('ful'):
            base = self.get_base(word, 'ful')
            if self.m_count(base) > 0:
                word = self.replacer(word, 'ful'), ''
        elif word.endswith('ness'):
            base = self.get_base(word, 'ness')
            if self.m_count(base) > 0:
                word = self.replacer(word, 'ness', '')
        return word

    def step_4(self, word):
        suffixes = ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement', 'ment', 'ent', 'ou', 'ism', 'ate',
                    'iti', 'ous', 'ive', 'ize']
        for suffix in suffixes:
            if word.endswith(suffix):
                base = self.get_base(word, suffix)
                if self.m_count(base) > 1:
                    word = self.replacer(word, suffix, '')
        if word.endswith('ion'):
            base = self.get_base(word, 'ion')
            if self.m_count(base) > 1 and base.endswith('s') or base.endswith('t'):
                word = self.replacer(word, 'ion', '')
        return word

    def step_5a(self, word):
        if word.endswith('e'):
            base = self.get_base(word, 'e')
            if self.m_count(base) > 1 or (self.m_count(base) == 1 and not self.CVC(base)):
                word = self.replacer(word, 'e', '')
        return word

    def step_5b(self, word):
        if self.CC(word) and word.endswith('l') and self.m_count(word) > 1:
            word = word[:-1]
        return word


p = porter()

text = "Natural language processing (NLP) is a field " + \
       "of computer science, artificial intelligence " + \
       "and computational linguistics concerned with " + \
       "the interactions between computers and human " + \
       "(natural) languages, and, in particular, " + \
       "concerned with programming computers to " + \
       "fruitfully process large natural language " + \
       "corpora. Challenges in natural language " + \
       "processing frequently involve natural " + \
       "language understanding, natural language" + \
       "generation frequently from formal, machine" + \
       "-readable logical forms), connecting language " + \
       "and machine perception, managing human-" + \
       "computer dialog systems, or some combination " + \
       "thereof."

sentences = sent_tokenize(text)  # split para into sentences
words = word_tokenize(text)
ps = PorterStemmer()
count = 0
wordcount = 0

for wordz in words:
    if len(wordz) > 2:
        word = p.step_1a(wordz)
        # print(word)
        word = p.step_1b(word)
        # print(word)
        word = p.step_1c(word)
        # print(word)
        word = p.step_2(word)
        # print(word)
        word = p.step_3(word)
        # print(word)
        word = p.step_4(word)
        # print(word)
        word = p.step_5a(word)
        # print(word)
        word = p.step_5b(word)
        print("MY PORTER OUTPUT", word) #output1
        print("NLTK PORTER OUTPUT", ps.stem(wordz)) #output2
        wordcount += 1  # NUMBER OF WORDS PASSING THROUGH STEMMER
        if ps.stem(wordz) == word:
            count += 1  # NUMBER OF WORDS STEMMED CORRECTLY

print("ACCURACY OF STEMMER", (count / wordcount) * 100)










