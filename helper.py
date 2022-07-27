from os import sep
import emoji
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['contact'] == selected_user]
    
    # fetch number of messages
    num_messages = df.shape[0]

    # fetch number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
    
    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # fetch links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['contact'].value_counts().head()
    df = round((df['contact'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'contact': 'percent'})
    return x,df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['contact'] == selected_user]
    
    df = df[df['contact'] != 'group_notification']
    df = df[df['message']!= "<Media omitted>"]
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['contact']==selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['contact'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['contact'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['contact'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['contact'] == selected_user]

    return df['month'].value_counts()

def find_sentiment(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['contact'] == selected_user]

    df = df[df['contact'] != 'group_notification']
    df = df[df['message']!= "<Media omitted>"]

    sentiments = SentimentIntensityAnalyzer()
    df['positive'] = [sentiments.polarity_scores(i)["pos"] for i in df['message']]
    df['negative'] = [sentiments.polarity_scores(i)["neg"] for i in df['message']]
    df['neutral'] = [sentiments.polarity_scores(i)["neu"] for i in df['message']]

    a = sum(df['positive'])
    b = sum(df['negative'])
    c = sum(df['neutral'])

    if a>b and a>c:
        return "POSITIVE"
    elif b>a and b>c:
        return "NEGATIVE"
    else:
        return "NEUTRAL"





