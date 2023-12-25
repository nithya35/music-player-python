import subprocess as sbp
from ast import Interactive
import time 
from pygame import mixer as mx
import random
import os 
import sys 
import urllib.request
import os
import re
import sqlite3 as sq3
mx.init()
con=sq3.connect("songs.db")
cur=con.cursor()



def search_video(query):
    search_query = query.split()

    url = "http://www.youtube.com/results?search_query="

    for word in search_query:
        url += word + "+"
    url+="lyrics"
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    final_vds_id=[]
    for x in video_ids:
        final_vds_id.append("https://www.youtube.com/watch?v="+x)
    return final_vds_id[0]


def play_mp3(song_name):
    mx.music.load(f"{song_name}")
    mx.music.play()
    while mx.music.get_busy():
        time.sleep(1)



def download(q1,id):
    l=os.listdir()
    print("wait as we download your required song")
    l2=["yt-dlp","--format","bestaudio","--extract-audio","--audio-format","mp3",id]
    l1=sbp.run(l2)
    lp=os.listdir()
    s1=set(l)
    s2=set(lp)
    l4=list(s2.difference(s1))
    c1=f"""INSERT INTO song VALUES("{q1}","{l4[0]}");"""
    cur.execute(c1)
    con.commit()
    # play_mp3(l4[0])




def check(name):
    c1=f"""select * from song where nn="{name}";"""
    a1=cur.execute(c1)
    c2=a1.fetchall()
    # print(c2)
    if len(c2)==0:
        return False,False 
    else:
        return True,c2[0]



def play_playlist(name):
    print(f"now playing the playlist {name}!")
    c1=f"""select * from {name};"""
    a1=cur.execute(c1)
    l1=[]
    a2=a1.fetchall()
    for x in a2:
        print(x)
        l1.append(x[1])
    random.shuffle(l1)
    print(l1)
    for x in l1:
        print(f"now playing {x}")
        play_mp3(x)



def create_playlist(name):
    c1=f"""create table {name}(nn text,an text);"""
    cur.execute(c1)
    con.commit()


def get_actual_name(name):
    c1=f"""select * from song;"""
    a1=cur.execute(c1)
    a2=a1.fetchall()
    # print(a1.fetchall())
    d1=dict()
    for i in range(len(a2)):
        d1[a2[i][0]]=a2[i][1]
    
    if name in d1.keys():
        return d1[name]
    else:
        download(name,search_video(name))
        return get_actual_name(name)


def insert_into_playlist(name,song_name):
    l1=get_actual_name(song_name)
    c1=f"""insert into {name} values("{song_name}","{l1}");"""
    cur.execute(c1)
    con.commit()



while True:
    print("A Quick tour with what you can do with this:\n 1.want to play in an interactive mode press 1\n 2.want to play playlist press 2\n 3.want to create a new playlist press 3\n 4.add songs in your playlist\n")
    a1=input("now enter your choice: ")
    if a1=='1':
        q1=input("enter the song: ").strip().lower()
        a,b=check(q1)
        if a:
            play_mp3(b[1])
        if a:
            continue 
        download(q1,search_video(q1))
        c=get_actual_name(q1)
        play_mp3(c)
    elif a1=='3':
        print("you pressed 3 now enter the name of the playlist")
        name_of_playlist=input("enter the name of the playlist: ")
        create_playlist(name_of_playlist)
        print("playlist created successfully if you want to add songs press 5")
        a2=input("enter 5 if want to add new songs else anything : ").strip()
        if a2=="5":
            print("keep entering the name of the songs and if you want to exit press -1")
            while True:
                a3=input("enter here: ")
                if a3=="-1":
                    break
                else:
                    insert_into_playlist(name_of_playlist,a3)
            print("entering successfull now if you want to play the current playlist enter YES")
            a4=input("enter YES or NO: ").upper()
            if a4=="YES":
                play_playlist(f"{name_of_playlist}")
    elif a1=="4":
        name_playlist=input("enter the name of the playlist: ").strip()
        print("keep entering the name of the songs you want to add and then enter -1 to exit")
        while True:
            song_name=input("enter the name of the song: ")
            if song_name=="-1":
                break;
            insert_into_playlist(name_playlist,song_name)

        print("entering into the database successfull!")
        print("if you want to play the current playlist press YES other wise NO")
        s1=input("enter your choice: ").upper().strip()
        if s1=="YES":
            play_playlist(name_playlist)
    else:
        print("you entered 2 now enter the name of playlist: ")
        a5=input("enter the name of the playlist: ")
        play_playlist(a5)
