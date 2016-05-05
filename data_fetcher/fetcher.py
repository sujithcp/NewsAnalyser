'''
This program returns the main contents of a web page giving the url of the site

'''


from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


class GetTextFromUrl:
    LANGUAGE = "english"
    SENTENCE_COUNT = 100

    def __init__(self, url):
        self.url = url

    def getText(self, sentence_count=None):
        if sentence_count:
            self.SENTENCE_COUNT = sentence_count
        parser = HtmlParser.from_url(self.url, Tokenizer(self.LANGUAGE))
        # or for plain text files
        # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
        stemmer = Stemmer(self.LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(self.LANGUAGE)
        text_list = []

        for sentence  in summarizer(parser.document, self.SENTENCE_COUNT):
            text_list.append(str(sentence))
        return "\n".join(text_list)
