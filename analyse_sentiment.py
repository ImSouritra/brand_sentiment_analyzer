from collections import Counter
from typing import Tuple

import matplotlib.pyplot as plt
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.corpus import webtext, stopwords


class AnalyseSentiment:

    def read_file_to_string(self, filePath):
        """Read a text file and return a string
            filePath -> absolute path to the file
        """
        try:
            with open(filePath, encoding="utf-8") as f:
                text = f.read()
            return text
        except FileNotFoundError as msg:
            print("File not found in path")

    def preprocess_text(self, text):
        """
        preprocess a string and lemmatize and vectorize it
        :param text:
        :return: A list of lemmatized and vectorized words
        """

        lower_case = text.lower()

        cleaned_text = lower_case.translate(str.maketrans("", "", string.punctuation))

        tokenized_words = word_tokenize(cleaned_text, "english")

        stop_words_set = set(stopwords.words('english'))

        # Create a hashtable (dictionary) for stopwords
        stop_words_dict = {word: True for word in stop_words_set}

        final_words = [word for word in tokenized_words if not stop_words_dict.get(word, False)]

        return final_words

    def emotion_list(self, vectorized_words):
        """
        Make a list of emotions from the given word list
        :param vectorized_words -> A list of lemmatized and vectorized words:
        :return: A list of emotions from the words
        """

        emotion_dict = {}

        with open('emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", "").replace(",", "").replace("'", "").strip()
                word, emotion = clear_line.split(":")
                emotion_dict[word] = emotion

        emotion_list = [emotion_dict[word].strip(" ") for word in vectorized_words if
                        emotion_dict.get(word) is not None]
        return emotion_list

    def show_emotions(self, emotion_list):
        """
        Show a bar graph of different emotions
        :param emotion_list:
        :return: Returns a matplotlib bar graph
        """
        emotion_count = Counter(emotion_list)
        fig, ax1 = plt.subplots()
        ax1.bar(emotion_count.keys(), emotion_count.values())
        fig.autofmt_xdate()
        plt.savefig('graph.png')
        plt.show()

    def sentiment_analyse(self, text):

        """
        Analyse sentiment from text
        :param text:
        :return: A tuple object of base_score, positive_score, negative_score, overall_sentiment
        """
        score = SentimentIntensityAnalyzer().polarity_scores(text)
        base_score = round(score['neu'] * 10,2)
        negative_score = round(score['neg'] * 10,2)
        positive_score = round(score['pos'] * 10,2)
        overall_sentiment = "positive" if positive_score > negative_score else "negative"
        return base_score, positive_score, negative_score, overall_sentiment
