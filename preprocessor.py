import re
import pandas as pd

# Extract the Date time
def date_time(s):
    pattern='^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result=re.match(pattern, s)
    if result:
        return True
    return False 

# Extract contacts
def find_contact(s):
    s=s.split(":")
    if len(s)==2:
        return True
    else:
        return False
    
# Extract Message
def getMassage(line):
    splitline=line.split(' - ')
    datetime= splitline[0];
    date, time= datetime.split(', ')
    message=" ".join(splitline[1:])
    
    if find_contact(message):
        splitmessage=message.split(": ")
        author=splitmessage[0]
        message=splitmessage[1]
    else:
        author=None
    return date, time, author, message

def convert(obj):
    if obj == None:
        return 'group_notification'
    else:
        return obj

def preprocess(contents):
    data=[]
    messageBuffer=[]
    date, time, contact= None, None, None
    for line in contents:
        line=line.strip()
        if date_time(line):
            if len(messageBuffer) >0:
                data.append([date, time, contact, ''.join(messageBuffer)])
            messageBuffer.clear()
            date, time, contact, message=getMassage(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)
    df=pd.DataFrame(data, columns=["date", "time", "contact", "message"])
    df['date']=pd.to_datetime(df['date'])

    df['contact'] = df['contact'].apply(convert)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df