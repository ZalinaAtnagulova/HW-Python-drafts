MODULE = 'C:\Python27\Lib\site-packages\pattern-2.6'
import sys
import re
from itertools import islice, tee
if MODULE not in sys.path: sys.path.append(MODULE)
from pattern.web import Wikipedia, plaintext
import math
from unittest import TestCase

class WikiParser:
    def __init__(self):
        pass
    
    def get_articles(self, start):
        list_of_strings = []
        article = Wikipedia().article(start).plaintext()
        list_of_strings.append(self.plain_text(article))
        for link in Wikipedia().article(start).links:
            if Wikipedia().article(link).language is 'en':
                list_of_strings.append(self.plain_text(link))
        return list_of_strings
    
    def plain_text(self, article):
        corrected = article.lower()
        corrected = re.sub('\n', ' ', corrected)
        while re.search('  ', corrected) != None:
            corrected = re.sub('  ', ' ', corrected)
        return corrected

class TextStatistics:
    def __init___(self, articles):
        pass

    def clean_text(self, text):
        text = re.sub('\n', ' ', text)
        text = re.sub('[.,?!:;*\'-_"\(\)\]\[]', '', text)
        while re.search('  ', text) != None:
            text = re.sub('  ', ' ', text)
        return text
    
    def make_ngrams(self, text):
        big_dict = {}
        ngrams = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(text, 3))))
        ngrams = [''.join(x) for x in ngrams]
        for gram in ngrams:
            if gram in big_dict:
                big_dict[gram] += 1
            else:
                big_dict[gram] = 0
        return big_dict

    def count_words(self, text):
        big_dict = {}
        words = text.split(' ')
        for word in words:
            if word in big_dict:
                big_dict[word] += 1
            else:
                big_dict[word] = 0
        return big_dict

    def get_top_ngrams(self, n, use_idf = False):
        list_of_3grams_in_descending_order_by_freq = []
        list_of_their_corresponding_freq = []
        sentences = []
        number_of_sentences = 0
        for text in articles:
            sentences = text.split('. ')
            big_dict = make_ngrams(self.clean_text(text))
        if use_idf:
            for ngram in big_dict:
                for sentence in sentences:
                    if ngram in sentence:
                        number_of_sentences += 1
                idf = self.idfs(len(sentences), number_of_sentences)
                big_dict[ngram] = big_dict[ngram]*idf
        for ngram in sorted(big_dict, key=lambda n: big_dict[n], reverse=True):
            list_of_3grams_in_descending_order_by_freq.append(ngram)
            list_of_their_corresponding_freq.append(big_dict[ngram])
        return (list_of_3grams_in_descending_order_by_freq[:n], list_of_their_corresponding_freq)[:n]

    def get_top_words(self, n, use_idf = False):
        list_of_words_in_descending_order_by_freq = []
        list_of_their_corresponding_freq = []
        number of texts = 0
        number_of_sentences = 0
        number_of_words = 0
        for text in articles:
            big_dict = count_words(self.clean_text(text))
        if use_idf:
            for word in big_dict:
                for text in texts:
                    if word in text:
                        number_of_texts += 1
                idf = self.idfs(len(articles), number_of_texts)
                big_dict[word] = big_dict[word]*idf
        for word in sorted(big_dict, key=lambda n: big_dict[n], reverse=True):
            list_of_words_in_descending_order_by_freq.append(word)
            list_of_their_corresponding_freq.append(big_dict[word])
        return (list_of_words_in_descending_order_by_freq[:n], list_of_their_corresponding_freq[:n])

    def idfs(self, num_all, num_corresponding):
        return math.log(num_all/num_corresponding)

    def test_double_space(self):
        for article in articles:
            self.assertNotIn('  ', article)

    def test_double_space_ngram(self):
        for article in articles:
            biq_dict = self.make_ngrams(article)
            for key in big_dict:
                self.assertNotIn('  ', key)

    def test_idfs(self):
        idf = self.idfs(32, 2)
        self.assertAlmostEqual(idf, 2.77, 2)

    def test_idf_words(self):
        tuple_lists = self.get_top_words(5, use_idf = True)
        freqs = tuple_lists[1]
        for freq in freqs:
            idf = self.idfs(100, 5)
            self.assertAlmostEqual(idf, -1, 2)
    
class Experiment:
    def __init___(self, articles):
        pass

    def show_results(self):
        start = 'Natural language processing'
        articles = WikiParser().get_articles(start)
        top_20_ngr = TextStatistics().get_top_ngrams(20)
        top_20_words = TextStatistics().get_top_ngrams(20)
        print 'Top-20 3grams in article', start, 'and all the artickes it refers to:', top_20_ngr
        print 'Top-20 words in article', start, 'and all the artickes it refers to:', top_20_words
        start_only = WikiParser().get_articles(start)
        top_5_ngr_in_start = TextStatistics().get_top_ngrams(5)
        top_5_words_in_start = TextStatistics().get_top_words(5)
        print 'Top-5 3grams in article', start, top_5_ngr_in_start
        print 'Top-5 words in article', start, top_5_words_in_start
        
Experiment().show_results()
