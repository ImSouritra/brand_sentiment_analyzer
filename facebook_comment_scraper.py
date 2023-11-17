import re

from facebook_scraper import get_posts
import pandas as pd

class FacebookCommentScraper:
    def __init__(self, brandName, cookies):
        self.brandName = brandName
        self.cookies = cookies

    def get_comments(self, pages, options):
        """Returns a pandas dataframe with user-id, comments , comments-full, likes etc..
            brandName -> Name of the brand you want to get comments from
            cookies -> User cookies (required)
            pages ->  How many pages of posts to request, the first 2 pages may have no results, so try with a number greater than 2. Default is 10.
            options ->  Dictionary of options. Set options={"comments": True} to extract comments
        """
        post_df_full = pd.DataFrame()

        for post in get_posts(self.brandName, cookies = self.cookies, pages = pages, options = options):
            post_entry = post
            fb_post_df  = pd.DataFrame.from_dict(post_entry, orient='index')
            fb_post_df = fb_post_df.transpose()
            post_df_full = post_df_full.append(fb_post_df)
        return post_df_full

    def preprocess_data(self, dataFrame,columns="comments_full"):
        """Preprocess the entire dataframe, remove unwanted columns

            dataframe -> a pandas dataframe
            columns -> Columns you want to extract from the dataframe, if multiple pass a list of columns
        """

        cleaned_dataframe = pd.DataFrame(dataFrame[columns])
        cleaned_dataframe.rename(columns={"comments_full":"comment"}, inplace=True)
        cleaned_dataframe.reset_index(drop=True, inplace = True)
        return cleaned_dataframe

    def get_comment_list(self, dataFrame):
        """Make a list of comments from the dataFrame
            dataFrame -> A pandas dataFrame
        """
        facebook = []
        for i in range(len(dataFrame["comment"])):
            l = len(dataFrame["comment"][i])
            for j in range(l):
                facebook.append(self.remove_emojis(dataFrame["comment"][i][j]["comment_text"]))

        return facebook


    def remove_emojis(self, data):

        """remove emoji from data
            data -> data
        """

        emoji = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        return re.sub(emoji, '', data)

    def convert_to_text_file(self, data):
        """Convert a list of comments to a text file
            data -> data
        """
        for i in data:
            with open(f"facebook_comments.txt","a",encoding="utf-8") as f:
                f.write(i)

    def convert_to_csv(self, data):
        """Convert a list of comments to .csv file
            data -> data
        """

        dataFrame = pd.DataFrame(data,columns=["comment"])
        dataFrame.to_csv("facebook.csv")


