import string
from collections import Counter
from typing import Tuple
import re
import pymongo
from pymongo import MongoClient
import smtplib
import datetime
from email.message import EmailMessage
from facebook_scraper import get_posts
import pandas as pd
import matplotlib.pyplot as plt
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import webtext, stopwords
import send_mail
from analyse_sentiment import AnalyseSentiment
from database import MongoDatabase
from constants import CONNECTION_STRING, COOKIES, GMAIL_USER, GMAIL_PASSWORD
from facebook_comment_scraper import FacebookCommentScraper
from analyse_sentiment import AnalyseSentiment
import tkinter as tk
from tkinter import messagebox

MONGO_DB = MongoDatabase(database_name="facebook_comment_sentiment_analyzer", connection_string=CONNECTION_STRING)
USER_DB = MONGO_DB.get_database().get_collection("users")
BRAND_DB = MONGO_DB.get_database().get_collection("brands")


def analyse(user_name, user_email, brand_name):
    # If user doesn't exist in database
    if not MONGO_DB.is_user_db_exist(USER_DB, user_name):
        print("User doesn't exist")
        USER_DB.insert_one({
            "user_name": user_name,
            "user_email": user_email,
            "searched_brand": brand_name,
        })
        print(f"Saving user -> {user_name} to database")
        # If the brand searched is already in our database
        if MONGO_DB.is_brand_db_exist(BRAND_DB, brand_name):
            print(f"Brand {brand_name} exist in database")
            brand = BRAND_DB.find_one({"brand_name": brand_name})
            base_score = brand["base_score"]
            positive_score = brand["positive_score"]
            negative_score = brand["negative_score"]
            overall_sentiment = brand["overall_sentiment"]
            print(f"Brand Name -> {brand_name}\nBase Score -> {base_score}\nOverall Sentiment -> {overall_sentiment}")
            return base_score, positive_score, negative_score, overall_sentiment
        else:
            # If the brand searched isn't in our database
            print(f"{brand_name} doesn't exist in database")
            print(f"Extracting {brand_name} comments from facebook")

            # obj = FacebookCommentScraper(brandName=brand_name, cookies=COOKIES)
            #
            # comment_df = obj.get_comments(pages=3, options={'comments': True, "posts_per_page": 2})
            # preprocessed_df = obj.preprocess_data(comment_df)
            # comment_list = obj.get_comment_list(preprocessed_df)
            # obj.convert_to_text_file(comment_list)

            sentiment_analyser = AnalyseSentiment()
            text = sentiment_analyser.read_file_to_string("facebook_comments_pepsi.txt")
            preprocessed_list = sentiment_analyser.preprocess_text(text)
            emotions_list = sentiment_analyser.emotion_list(preprocessed_list)
            sentiment_analyser.show_emotions(emotions_list)
            lower_case = text.lower()
            cleaned_text = lower_case.translate(str.maketrans("", "", string.punctuation))
            base_score, positive_score, negative_score, overall_sentiment = sentiment_analyser.sentiment_analyse(
                cleaned_text)
            print(f"Base score is {base_score}")
            BRAND_DB.insert_one({
                "brand_name": brand_name,
                "base_score": base_score,
                "positive_score": positive_score,
                "negative_score": negative_score,
                "overall_sentiment": overall_sentiment
            })
            return base_score, positive_score, negative_score, overall_sentiment
    else:
        # If the user already in our database
        print(f"user -> {user_name} exist in database")
        current_user = USER_DB.find_one({"user_name": user_name})
        if current_user["searched_brand"] == brand_name:
            # If the user already searched for this brand previously
            print(f"User -> {user_name} already searched for this brand")
            # Scrap the recent facebook comment from the brand and analyse the sentiment.
            # obj = FacebookCommentScraper(brandName=brand_name, cookies=COOKIES)
            # comment_df = obj.get_comments(pages=3, options={'comments': True, "posts_per_page": 2})
            # preprocessed_df = obj.preprocess_data(comment_df)
            # comment_list = obj.get_comment_list(preprocessed_df)
            # obj.convert_to_text_file(comment_list)

            sentiment_analyser = AnalyseSentiment()
            text = sentiment_analyser.read_file_to_string("facebook_comments_pepsi.txt")
            preprocessed_list = sentiment_analyser.preprocess_text(text)
            emotions_list = sentiment_analyser.emotion_list(preprocessed_list)
            sentiment_analyser.show_emotions(emotions_list)
            lower_case = text.lower()
            cleaned_text = lower_case.translate(str.maketrans("", "", string.punctuation))
            base_score, positive_score, negative_score, overall_sentiment = sentiment_analyser.sentiment_analyse(
                cleaned_text)
            brand = BRAND_DB.find_one({"brand_name": brand_name})
            existing_base_score = brand["base_score"]
            existing_positive_score = brand["positive_score"]
            existing_negative_score = brand["negative_score"]
            user_email = current_user["user_email"]

            if overall_sentiment == "positive" and positive_score>existing_positive_score:
                print("Sentiment has changed positively! Send email to user and increment the existing base score")
                print("Updating the database with new values")
                newValues = {"$set": {"base_score": existing_base_score + 0.1,
                                      "positive_score": positive_score,
                                      "negative_score": negative_score,
                                      "overall_score": overall_sentiment}}
                BRAND_DB.update_one({"brand_name": brand_name}, newValues)
                subject = f"{brand_name}'s base score has increased"
                body = f"You have searched for {brand_name} previously. We've recently noticed that {brand_name}'s base score has increased from {existing_base_score} to {base_score}, and overall sentiment has become positive."
                print(f"Sending email to user -> {user_email}")
                send_mail.SendMail(subject, body, GMAIL_USER, user_email).send_message_to_user(GMAIL_USER, GMAIL_PASSWORD)
            elif overall_sentiment=="negative" and negative_score<existing_negative_score:
                print("Sentiment has changed negatively! Send email to user and decrement the existing base score")
                print("Updating the database with new values")
                newValues = {"$set": {"base_score": existing_base_score - 0.1,
                                      "positive_score": positive_score,
                                      "negative_score": negative_score,
                                      "overall_score": overall_sentiment}}
                BRAND_DB.update_one({"brand_name": brand_name}, newValues)
                subject = f"{brand_name}'s base score has decreased"
                body = f"You have searched for {brand_name} previously. However we've recently noticed that {brand_name}'s base score has decreased from {existing_base_score} to {base_score}, and overall sentiment has become negative."
                print(f"Sending email to user -> {user_email}")
                send_mail.SendMail(subject, body, GMAIL_USER, user_email).send_message_to_user(GMAIL_USER,GMAIL_PASSWORD)

            print(f"Brand Name -> {brand_name}\nBase Score -> {base_score}\nOverall Sentiment -> {overall_sentiment}")
            return base_score, positive_score, negative_score, overall_sentiment
        else:
            # If the user hasn't searched for this brand yet
            print(f"User -> {user_name} hasn't searched for this brand yet.\n creating new record...")
            USER_DB.insert_one({
                "user_name": user_name,
                "user_email": user_email,
                "searched_brand": brand_name,
            })
            # If the searched brand is already in our database
            if MONGO_DB.is_brand_db_exist(BRAND_DB, brand_name):
                print(f"Brand {brand_name} exist in database")
                brand = BRAND_DB.find_one({"brand_name": brand_name})
                base_score = brand["base_score"]
                positive_score = brand["positive_score"]
                negative_score = brand["negative_score"]
                overall_sentiment = brand["overall_sentiment"]
                print(
                    f"Brand Name -> {brand_name}\nBase Score -> {base_score}\nOverall Sentiment -> {overall_sentiment}")
                return base_score, positive_score, negative_score, overall_sentiment
            else:

                # If the searched brand is not in our database
                print(f"{brand_name} doesn't exist in database")
                print(f"Extracting {brand_name} comments from facebook")

                # obj = FacebookCommentScraper(brandName=brand_name, cookies=COOKIES)
                #
                # comment_df = obj.get_comments(pages=3, options={'comments': True, "posts_per_page": 2})
                # preprocessed_df = obj.preprocess_data(comment_df)
                # comment_list = obj.get_comment_list(preprocessed_df)
                # obj.convert_to_text_file(comment_list)

                sentiment_analyser = AnalyseSentiment()
                text = sentiment_analyser.read_file_to_string("facebook_comments_pepsi.txt")
                preprocessed_list = sentiment_analyser.preprocess_text(text)
                emotions_list = sentiment_analyser.emotion_list(preprocessed_list)
                sentiment_analyser.show_emotions(emotions_list)
                lower_case = text.lower()
                cleaned_text = lower_case.translate(str.maketrans("", "", string.punctuation))
                base_score, positive_score, negative_score, overall_sentiment = sentiment_analyser.sentiment_analyse(
                    cleaned_text)

                BRAND_DB.insert_one({
                    "brand_name": brand_name,
                    "base_score": base_score,
                    "positive_score": positive_score,
                    "negative_score": negative_score,
                    "overall_sentiment": overall_sentiment
                })
                return base_score, positive_score, negative_score, overall_sentiment


def main():
    # Create the main window
    root = tk.Tk()
    root.title("Search Information")

    def on_search():
        user_name = user_name_entry.get().lower()
        user_email = email_entry.get().lower()
        brand_name = brand_name_entry.get().lower()

        base_score, positive_score, negative_score, overall_sentiment = analyse(user_name, user_email, brand_name)

        info_message = f"Brand Name: {brand_name}\nBase Score: {base_score}\nPositive Score: {positive_score}\nNegative Score:{negative_score}\nOverall Sentiment:{overall_sentiment}"

        messagebox.showinfo("Search Result", info_message)

    root.geometry("400x300")

    tk.Label(root, text="User Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    user_name_entry = tk.Entry(root)
    user_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    email_entry = tk.Entry(root)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Brand Name:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    brand_name_entry = tk.Entry(root)
    brand_name_entry.grid(row=2, column=1, padx=10, pady=5)

    search_button = tk.Button(root, text="Search", command=on_search)
    search_button.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
