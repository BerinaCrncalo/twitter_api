🐦 Twitter Sentiment Analyzer & Liker

This Python script interacts with the Twitter API to fetch tweets, analyze sentiment, generate visual insights, and optionally like tweets that mention a specific keyword.

✨ Features

 ✅ Authenticate using OAuth 2.0 (Bearer) and OAuth 1.0a.  
 ✅ Fetch recent tweets based on keyword search.  
 ✅ Analyze sentiment using Hugging Face transformers.  
 ✅ Like tweets that mention a specific keyword (requires Elevated access).  
 ✅ Handle API rate limits and errors gracefully.  
 ✅ Store sentiment data in both CSV and SQLite.  
 ✅ Visualize sentiment trends over time.  
 ✅ Generate word clouds and perform topic modeling (LDA).  
 ✅ (Bonus) Placeholders for multilingual sentiment and Reddit comparison.  

🚀 Setup Instructions

 1. Clone the Repository

git clone https://github.com/BerinaCrncalo/twitter_api.git

 2. Install Dependencies

Make sure you're using Python 3.7+  
Install required packages via pip:
bash
pip install r requirements.txt

If requirements.txt is not provided, install manually:
pip install tweepy pythondotenv transformers matplotlib wordcloud scikitlearn


 🔐 3. Create a .env File

Create a file named .env in the project root and add your Twitter API credentials:

env
TWITTER_BEARER_TOKEN=your_bearer_token  
TWITTER_API_KEY=your_api_key  
TWITTER_API_SECRET_KEY=your_api_secret_key  
TWITTER_ACCESS_TOKEN=your_access_token  
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret  
> ⚠️ Keep this file private. Do not share your real credentials publicly.  


 ▶️ Running the Script

Run the script from your terminal:

python main.py

 ❗ Notes on Liking Tweets

> 🛑 Liking tweets using POST /2/users/:id/likes (or via Tweepy v1.1) requires Elevated or Premium access on the [Twitter Developer Platform](https://developer.x.com/en/portal/product).  
> If you're using a free (Essential) account, this action will fail with a 403 Forbidden error, which is caught and logged by the script.



 📊 Output

 Visualizations will pop up (sentiment trend, word cloud).  
 A sentiment_report.csv file will be created.  
 A local SQLite database sentiment.db stores sentiment trends.  
 Topic modeling results are printed in the terminal.  



 🧠 Future Work

 🌍 Multilingual sentiment analysis  
 👾 Reddit comparison and analysis  
 📈 Realtime tweet streaming and dashboard  



 📧 Contact

Made by Berina 💙  

Let me know if you want this as a downloadable file or want to tweak anything like GitHub link or contact!