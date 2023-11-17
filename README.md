<h1> Brand Sentiment Analysis </h1>
<p>This goal of this project is to analyze a brand’s sentiment based on their social media and internet and get a base score or sentiment score. Then when the user search for the same brand it will increment or decrement the score based on different criteria and send an email to the user informing about the same.</p>
<ol>
  <a href="#apporach"><li>Approach</li></a>
  <a href="#process_flow_diagram"><li>Process Flow Diagram</li></a>
  <a href="#technology_used"><li>Technologies Used</li></a>
  <a href="#direction"><li>Directions to Use</li></a>
</ol>

<h2 id="approach">Approach</h2>
<p>At first, we’ve to collect the brand’s Facebook comments from many posts using Selenium WebDriver and a package called facebook_scraper in Python and save it into a text file. We can also choose other Social media like Twitter or Instagram but it requires API to access their data and the API is very hard to get so for the sake of simplicity we’ve chosen Facebook platform to analyze the brand’s sentiment. Then we read the data from the text file and preprocess it. For the preprocessing part we’ve first converted the whole data into lower cases, then removed punctuations and unwanted emojis from the data. Then we’ve imported all the stop words (Stop words are words like ‘I’, ‘are’ which adds no meaning to the sentence) and make a hash set to compare and remove stop words from our data in O(1) time complexity. Then we can compare and analyze different emotions from our data and show it to the user using Matplotlib bar chart. For the analysis part we’ve used Sentiment Intensity Analyzer from nltk.sentiment.vader module. It uses a collection of predefined emotions and their meanings in the sentence to analyze the sentiment from the given text. Then it returns a base score, positive score and a negative score. If the positive score is greater than the negative score then we can say that the overall sentiment of the brand is positive and if the negative score is greater than the negative score then we can say that the overall sentiment is negative. Then we’ve to save the brand name, base score, positive score, negative score, and overall sentiment so that we can get the existing base score later and increment or decrement it based on our criteria. We also have to save the user’s basic information (name and email) and the brand he has searched for onto our database so that when  the user search again on the next day we can know that the user has searched for this brand previously, analyze the brand and increment or decrement the existing scores and send email to the user informing about the same. For the database, we’ve used MongoDB and for emailing we’ve used the SMTP library in Python. At last, we’ve used the Tkinter library to build a user-friendly graphical-user-interface in python. </p>
<h2 id="process_flow_diagram">Process Flow Diagram</h2>
<img src="https://www.shoppirate.com/blog/wp-content/uploads/2023/11/Brand-Sentiment-Analysis.png">
<h2 id="technology_used">Technologies Used</h2>
<ul>
<li><strong>Programming Language :-</strong> Python</li>
<li><strong>Libraries :- </strong>Selenium, NumPy, Pandas, matplotlib, nltk, tkinter, smtplib</li>
<li><strong>Database :- </strong>MongoDB</li>
</ul>
<h2>Directions to Use</h2>
<p>Install all the packages that are mentioned in the main.py file and then run the file using python. I'm also working on converting this project into an EXE file but it will take some time. 
1. You will see a tkinter window pop up. Enter your name, email, brand name in the boxes.
  <br></br>
<img src="https://www.shoppirate.com/blog/wp-content/uploads/2023/11/Search-Information-17-11-2023-16_18_18.png" />
<br></br>
2. After clicking the search button, the comment scraping process will start. It will take some time.
<br></br>
<img src="https://www.shoppirate.com/blog/wp-content/uploads/2023/11/facebook_comment_sentiment_analyzer-–-main.py-17-11-2023-16_21_24.png" />
<br></br>
3. You can see public sentiment about your brand in a bar chart for greater analysis
<br></br>
<img src="https://www.shoppirate.com/blog/wp-content/uploads/2023/11/Figure-1-17-11-2023-16_19_23.png" />
<br></br>
4. Another window will pop up and show the brand's base score, positive score, negative score, and overall sentiment
<br></br>
<img src="https://www.shoppirate.com/blog/wp-content/uploads/2023/11/Search-Information-17-11-2023-16_20_51.png" />
<br></br>
</p>
