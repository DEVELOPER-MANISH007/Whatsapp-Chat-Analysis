from collections import Counter
import pandas as pd
import re
from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import emoji


# ================= FETCH STATS =================
def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    # media messages
    media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # links extraction
    extractor = URLExtract()
    links = []

    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, words, media, links


# ================= MOST BUSY PEOPLE =================
def most_busy_people(df):
    x = df['user'].value_counts().head()

    new_df = (
        (df['user'].value_counts() / df.shape[0]) * 100
    ).round(2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})

    return x, new_df


# ================= WORDCLOUD =================
def create_word_cloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # load stopwords
    with open('stopword.txt', 'r') as f:
        stop_words = set(f.read().split())

    # remove unwanted rows
    temp_data = df[
        (df['user'] != 'group_notification') &
        (df['message'] != '<Media omitted>\n')
    ].copy()

    def clean_message(message):
        # remove punctuation
        message = re.sub(r'[^\w\s]', '', message)

        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

        return " ".join(words)

    temp_data['clean_msg'] = temp_data['message'].apply(clean_message)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    df_wc = wc.generate(temp_data['clean_msg'].str.cat(sep=" "))

    return df_wc


# ================= MOST COMMON WORD =================
def most_common_word(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # load stopwords
    with open('stopword.txt', 'r') as f:
        stop_words = set(f.read().split())

    temp_data = df[
        (df['user'] != 'group_notification') &
        (df['message'] != '<Media omitted>\n')
    ]

    words = []

    for message in temp_data['message']:
        message = re.sub(r'[^\w\s]', '', message)

        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(
        Counter(words).most_common(20),
        columns=['Word', 'Frequency']
    )

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common())
    return emoji_df

def monthly_timeline(selected_user,df):
     if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
     timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
     time = []
     for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+str(timeline['year'][i]))
     timeline['time'] = time

     return timeline    


def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()