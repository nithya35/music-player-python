import subprocess as sbp
import sqlite3 as sq3
import platform
if platform.system()=="Linux":   
    c1=["touch","songs.db"]
    sbp.run(c1)
    con=sq3.connect("songs.db")
    cur=con.cursor()
    c2=["pip","install","yt-dlp"]
    c3=["pip","install","pygame"]
    c4=["sudo","apt-get","install","ffmpeg"]
    sbp.run(c2)
    sbp.run(c3)
    sbp.run(c4)
    c1="""create table song (nn text,an text);"""
    cur.execute(c1)
    print("init successfull! now you can run app.py!")
else:
    print("only linux version released now for more information please visit https://www.github.com/g-nitin-1")