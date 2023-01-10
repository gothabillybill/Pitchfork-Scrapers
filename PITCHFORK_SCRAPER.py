import re
import urllib.request
from bs4 import BeautifulSoup
import os.path
import sqlite3
import pickle
#import concurrent.futures

def maketable(conn):
    c = conn.cursor()
    c.execute('CREATE TABLE PitchforkData(ID, Artist, Number_of_Albums, Avg_Album_Score)')
    conn.commit()
    c.close()
def makesoup(url):
    openurl = urllib.request.urlopen(url)
    html = openurl.read()
    soupdata = BeautifulSoup(html, features='lxml')
    return soupdata
def createconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
def pforkscrape(number, conn):
    reviewdict = {}
    numalbums = {}
    _id_ = 0
#finds home page and review link
    for _ in range(1, number):
        c = conn.cursor()
        soup = makesoup('https://pitchfork.com/reviews/albums/?page=' + str(_))
        link = soup.find_all(class_="review__link")
        for record in link:
            c = conn.cursor()
#finds album page with artist and album score
            soup2 = makesoup('https://pitchfork.com' + record.get('href'))
            artistlist = soup2.find_all('a', href=re.compile('^/artists/\w'))
            scorelist = soup2.find_all(class_='score')
            if len(artistlist) > len(scorelist):
                for i in artistlist:
                    c = conn.cursor()
                    artist = i.text
                    score = scorelist[0].text
                    if artist not in reviewdict:
                        _id_ += 1
                        reviewdict.update({artist: score})
                        numalbums.update({artist: 1})
                        insert_query = '''INSERT INTO PitchforkData 
                        (ID, Artist, Number_of_Albums, Avg_Album_Score) 
                        VALUES 
                        (?, ?, ?, ?);'''
                        data_tuple = (_id_, artist, numalbums[artist], score)
                        c.execute(insert_query, data_tuple)
                        conn.commit()
                        print(artist, score)
                        c.close()
                    else:
                        numalbums[artist] += 1
                        numfactors = numalbums[artist]
                        avgscore = format((float(reviewdict[artist])*(numfactors-1)+float(score))/numfactors, '.2f')
                        reviewdict[artist] = avgscore
                        update_query = '''UPDATE PitchforkData 
                        SET Avg_Album_Score = ?, Number_of_Albums = ? WHERE Artist = ?;'''
                        data_tuple = (avgscore, numfactors, artist)
                        c.execute(update_query, data_tuple)
                        conn.commit()
                        print(artist, score)
                        c.close()
            else:
                for i, e in zip(artistlist, scorelist):
                    c = conn.cursor()
                    artist = i.text
                    score = e.text
                    if artist not in reviewdict:
                        _id_ += 1
                        reviewdict.update({artist: score})
                        numalbums.update({artist: 1})
                        insert_query = '''INSERT INTO PitchforkData 
                                           (ID, Artist, Number_of_Albums, Avg_Album_Score) 
                                           VALUES 
                                           (?, ?, ?, ?);'''
                        data_tuple = (_id_, artist, numalbums[artist], score)
                        c.execute(insert_query, data_tuple)
                        conn.commit()
                        print(artist, score)
                        c.close()
                    else:
                        numalbums[artist] += 1
                        numfactors = numalbums[artist]
                        avgscore = format((float(reviewdict[artist])*(numfactors-1)+float(score))/numfactors, '.2f')
                        reviewdict[artist] = avgscore
                        update_query = '''UPDATE PitchforkData 
                                            SET Avg_Album_Score = ?, Number_of_Albums = ? WHERE Artist = ?;'''
                        data_tuple = (avgscore, numfactors, artist)
                        c.execute(update_query, data_tuple)
                        conn.commit()
                        print(artist, score)
                        c.close()
    return reviewdict


#inserts pitchfork data into sql database

if os.path.isfile('./Pitchfork_Data.db') is False:
    conn = createconnection('Pitchfork_Data.db')
    maketable(conn)
else:
    conn = createconnection('Pitchfork_Data.db')

print('How many pages do you intend to scrape?')
numpages = int(input())

reviewdict = pforkscrape(numpages, conn)

with open('pitchforkDict.txt', 'wb') as p:
    pickle.dump(reviewdict, p, protocol=-1)
    p.close()

