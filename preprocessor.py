import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    # extract date-time
    df['message_date'] = df['message_date'].str.extract(
        r'(^\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2})'
    )

    # convert to datetime
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format="%d/%m/%y, %H:%M"
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # 🔥 Extract user & message
    users = []
    messages_clean = []

    for message in df['user_message']:
        entry = re.split(r'^([^:]+):\s', message)

        if entry[1:]:
            users.append(entry[1])
            messages_clean.append(entry[2])
        else:
            users.append('group_notification')
            messages_clean.append(entry[0])

    df['user'] = users
    df['message'] = messages_clean

    df.drop(columns=['user_message'], inplace=True)

    # 🚀 Date Features
    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['day_name']= df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
        
    df['period'] = period    

    return df