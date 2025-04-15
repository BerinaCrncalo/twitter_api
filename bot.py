import tweepy
import os
import csv
import datetime
from transformers import pipeline
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from wordcloud import WordCloud
import sqlite3
import requests
from tweepy.errors import TooManyRequests, Unauthorized, Forbidden, TweepyException

# Load environment variables from .env
load_dotenv()

# Set up Twitter API client using Bearer Token
client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

# OAuth 2.0 for write actions like liking
auth = tweepy.OAuth1UserHandler(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET_KEY'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)
api = tweepy.API(auth)

# Load sentiment pipeline
sentiment_analysis = pipeline("sentiment-analysis")

# Database setup
def init_db():
    conn = sqlite3.connect("sentiment.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sentiment_trend (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            positive INTEGER,
            neutral INTEGER,
            negative INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_to_db(date, positive, neutral, negative):
    conn = sqlite3.connect("sentiment.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sentiment_trend (date, positive, neutral, negative)
        VALUES (?, ?, ?, ?)
    ''', (date, positive, neutral, negative))
    conn.commit()
    close_db_connection(conn)

def close_db_connection(conn):
    if conn:
        conn.close()

def plot_sentiment_trend():
    conn = sqlite3.connect("sentiment.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, positive, neutral, negative FROM sentiment_trend ORDER BY date")
    rows = cursor.fetchall()
    close_db_connection(conn)

    if rows:
        dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') for row in rows]
        positives = [row[1] for row in rows]
        neutrals = [row[2] for row in rows]
        negatives = [row[3] for row in rows]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, positives, label='Positive', color='green', marker='o')
        plt.plot(dates, neutrals, label='Neutral', color='blue', marker='o')
        plt.plot(dates, negatives, label='Negative', color='red', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.title('Sentiment Over Time')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()

# 🔒 NOTE:
# The like_tweet(tweet_id) feature below uses a POST request to the "like" endpoint.
# This requires Elevated or Premium access on the Twitter/X Developer Platform.
# If you're using a free (Essential) developer account, you'll receive a 403 Forbidden error.
# To enable this functionality, upgrade your access level: https://developer.x.com/en/portal/product
# Twitter API requirement: attempt to like tweet.
# Current access level may block this; error is handled gracefully.
def like_tweet(tweet_id):
    try:
        api.create_favorite(tweet_id)
        print(f"✅ Successfully liked tweet with ID: {tweet_id}")
    except Forbidden as e:
        print(f"❌ Forbidden error: Unable to like tweet with ID: {tweet_id}. Access level might be limited. {e}")
    except Unauthorized as e:
        print(f"❌ Unauthorized: Check your credentials or token. {e}")
    except TooManyRequests as e:
        print(f"❌ Rate limit exceeded while liking tweet {tweet_id}. {e}")
    except Exception as e:
        print(f"❌ Unexpected error liking tweet with ID {tweet_id}: {e}")

# Analyze sentiment
def analyze_sentiment(tweet_text):
    try:
        result = sentiment_analysis(tweet_text)
        return result[0]['label']
    except Exception as e:
        print(f"Sentiment analysis failed: {e}")
        return 'NEUTRAL'

# Workaround for geolocation search
def fetch_tweets_by_location_workaround(keyword="Swift", max_results=20):
    query = f"{keyword} -is:retweet lang:en"
    while True:
        try:
            tweets = client.search_recent_tweets(query=query, max_results=max_results)
            return tweets
        except TooManyRequests as e:
            reset_time = e.response.headers.get('x-rate-limit-reset')
            if reset_time:
                sleep_time = int(reset_time) - int(time.time())
                print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds...")
                time.sleep(max(sleep_time + 5, 0))
            else:
                return None
        except Exception as e:
            print(f"Failed fetching tweets: {e}")
            return None

# Word cloud
def generate_wordcloud(texts):
    all_text = ' '.join(texts)
    wc = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Tweets')
    plt.show()

# Topic modeling
def perform_topic_modeling(texts, num_topics=3):
    try:
        vectorizer = CountVectorizer(stop_words='english')
        doc_term_matrix = vectorizer.fit_transform(texts)
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(doc_term_matrix)

        print("\nTop Words per Topic:")
        for i, topic in enumerate(lda.components_):
            top_words = [vectorizer.get_feature_names_out()[index] for index in topic.argsort()[-5:]]
            print(f"Topic {i + 1}: {', '.join(top_words)}")
    except Exception as e:
        print(f"Error during topic modeling: {e}")

# Placeholder for multilingual sentiment
def analyze_multilang_sentiment(text, lang='en'):
    return analyze_sentiment(text)  # In real case, handle translation

# Placeholder for social media comparison
def compare_with_reddit():
    print("Reddit comparison coming soon...")

# Main function with updates for error handling
def main():
    init_db()
    tweets = fetch_tweets_by_location_workaround()

    if tweets and tweets.data:
        texts = []
        pos, neu, neg = 0, 0, 0
        liked_tweets = set()  # To store already liked tweet IDs

        for tweet in tweets.data:
            text = tweet.text
            texts.append(text)
            sentiment = analyze_sentiment(text)
            if sentiment == 'POSITIVE':
                pos += 1
            elif sentiment == 'NEGATIVE':
                neg += 1
            else:
                neu += 1

            # Like tweet if 'swift' is mentioned and not already liked
            if 'swift' in text.lower() and tweet.id not in liked_tweets:
                like_tweet(tweet.id)
                liked_tweets.add(tweet.id)

        # Timestamp for sentiment report
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save to CSV
        with open("sentiment_report.csv", mode='a', newline='') as f:
            writer = csv.writer(f)
            if os.stat("sentiment_report.csv").st_size == 0:
                writer.writerow(["Date", "Positive", "Neutral", "Negative"])
            writer.writerow([now, pos, neu, neg])

        # Save to DB
        save_to_db(now, pos, neu, neg)

        # Visualizations
        plot_sentiment_trend()
        generate_wordcloud(texts)
        perform_topic_modeling(texts)
    else:
        print("❌ No tweets found. Please check your query or Twitter API status.")

if __name__ == "__main__":
    main()
