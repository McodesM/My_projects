from sqlite3.dbapi2 import Cursor
from nltk.featstruct import CustomFeatureValue
import praw
import text2emotion as te
import pandas as pd
import json
import sqlite3
from praw.reddit import Subreddit
import time
import email, smtplib, ssl



reddit = praw.Reddit(client_id='############################', \
                     client_secret='###########################', \
                     user_agent='#######################', \
                     username='', \
                     password='')

def reddit_run(reddit):

    subred = reddit.subreddit('CryptoCurrency')
    hot = subred.hot(limit = 11)
    top = subred.top(limit = 11)

    y = next(top)
    dir(y)

    x = next(hot)
    dir(x)

    titles = []
    for i in hot:
        titles.append(i.title)


    for i in top:
        titles.append(i.title)


        
    f = open('cryptonames.json')

    data = json.load(f)

    conn = sqlite3.connect('cryptotable.db')
    connection = conn.cursor()

    connection.execute("""CREATE TABLE IF NOT EXISTS crypto(
                                            Symbol VARCHAR(255) PRIMARY KEY,
                                            Total_appearances INTEGER);""")

    connection.execute(''' CREATE TABLE IF NOT EXISTS Post(
                                            Posts VARCHAR(2555) PRIMARY KEY);''')

    def edit_table(connection, key, value, conn, title):
        

        connection.execute('''
            INSERT INTO Post(Posts)
            VALUES (?)''', [title])
        conn.commit()

        connection.execute('''
            SELECT * FROM crypto
        ''')
        current_symbols = connection.fetchall()
        print(current_symbols)
        Found = False

        for j in range(0, len(current_symbols)):
            if (key.lower() == current_symbols[j][0].lower()) or (value.lower() == current_symbols[j][0].lower()):  
                Found = True
                connection.execute('''
                UPDATE crypto SET Total_appearances = (?) WHERE Symbol = (?)''', (current_symbols[j][1]+1, key))

                conn.commit()
        
        if Found == False:
            connection.execute('''
            INSERT INTO crypto(Symbol, Total_appearances)
            VALUES(?, ?)''', (key, 1))
            conn.commit()
        
        return current_symbols


    for i in range(0, len(titles)):  

        dictio = te.get_emotion(titles[i])
        pos_val = list(dictio.values())[0]
        neg_val = list(dictio.values())[3]
        

        if pos_val >= neg_val:
            s = titles[i]

            for key, value in data.items():
                
                if (key in s) or (value in s):
                    connection.execute('''
                        SELECT * FROM Post
                    ''')
                    checker = connection.fetchall()
                    if len(checker) == 0:
                        edit_table(connection, key, value, conn, s)
                    else:
                        found = 0
                        for j in range(0, len(checker)):
                            
                            if checker[j][0] == s:
                                
                                found += 1
                               
                        if found == 0:
                            edit_table(connection, key, value, conn, s)
    
    

    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    subject = 'Crypto scraper results'
    
    body = ""
        
    sender_email = "####################################"
    receiver_email = "####################################"


    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  

    message.attach(MIMEText(body, "plain"))

   
    text = current_symbols


    server = smtplib.SMTP_SSL('##################', 465)
    server.login("######################", "################")
    server.sendmail(
      "#########################", 
      "########################", 
      text)
    server.quit()
    #plt.show()

   


count = 0
while count == 0:
    times = str(datetime.datetime.now())
    calltimes = ['12:00']
    hourtime = times[11:16]
    print(hourtime)
    if hourtime in calltimes:
        reddit_run(reddit)
    time.sleep(3600)


