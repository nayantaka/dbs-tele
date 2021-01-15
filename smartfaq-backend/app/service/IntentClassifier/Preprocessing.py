# import nltk
import string
import pickle
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

class Embedding:
    label = []
    def __init__(self, data, **argm):
        max_nb_words = 1000
        embedding_dim = 128
        clean_text = False
        if 'max_nb_words' in argm and argm['max_nb_words'] is not None:
            max_nb_words = argm['max_nb_words']

        if 'embedding_dim' in argm and argm['embedding_dim'] is not None:
            embedding_dim = argm['embedding_dim']

        if 'label' in argm and argm['label'] is not None:
            self.create_label(argm['label'])

        if 'clean_text' in argm and argm['clean_text'] is not None:
            clean_text = argm['clean_text']

        self.prepare_data(data, int(max_nb_words), int(embedding_dim), clean_text)

    def prepare_data(self, data, max_nb_words, embedding_dim, clean_text=False):
        self.MAX_NB_WORDS = int(max_nb_words)
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer(num_words = self.MAX_NB_WORDS)    
        datas = data
        if clean_text == True:
            datas = [(self.clean_text(d)) for d in data]

        self.sentence = datas
        self.tokenizer.fit_on_texts(datas)
        self.word_index = list(set(self.tokenizer.word_index))
        self.MAX_SEQUENCE_LENGHT = len(self.word_index)
        self.save()       

    def clean_text(self, sentence):
        sentence = sentence.translate(str.maketrans('', '', string.punctuation)).lower().strip()
        sentence = self.stemmer.stem(sentence.lower())
        sentence = self.stemmer.remove(sentence)
        return sentence

    def text_to_sequence(self, sentence):
        sentence = self.clean_text(sentence)
        sentence = [sentence]
        seq = self.tokenizer.texts_to_sequences(sentence)
        padded = pad_sequences(seq, maxlen = self.MAX_SEQUENCE_LENGHT)
        return padded

    def corpus_to_sequence(self, dataX):
        seq = self.tokenizer.texts_to_sequences(dataX)
        padded = pad_sequences(seq, maxlen = self.MAX_SEQUENCE_LENGHT)
        return padded

    def create_label(self, dataY):
        # creating label
        le = LabelEncoder()
        label = le.fit_transform(dataY)
        self.label = dict()
        for l in label:
            for intent in dataY:
                if l not in self.label and intent not in self.label.values():
                    self.label[l] = intent

    def save(self):
        pickle.dump({'intent': self.label, 'sentence': self.sentence}, open("data-rnn-lstm.pkl", "wb"))

class Stemmer:
    def __init__(self):
        self.stemmer()
        self.stopword()

    def stemmer(self):
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()

    def stopword(self):
        stop_factory = StopWordRemoverFactory().get_stop_words()
        more_stopword = ['diatur', 'perjodohan', 'dengan', 'ia', 'bahwa', 'oleh', 'nya']
        data = stop_factory + more_stopword
         
        stop_factory = StopWordRemoverFactory()
        dictionary = ArrayDictionary(data)
        self.stopword = StopWordRemover(dictionary)

    def stem(self, sentence = None):       
        sentence = self.stemmer.stem(sentence)

        return sentence

    def remove(self, sentence = None):
        sentence = self.stopword.remove(sentence)

        return sentence