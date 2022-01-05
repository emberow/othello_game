# db.py
import mysql.connector
from datetime import datetime

con = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    database="pygame"
)
 
cursor = con.cursor()

#make a function to access the db
def get_10_record():
    try:
        cursor.execute("SELECT * FROM `record` ORDER BY `record`.`time` DESC LIMIT 10")
        return (cursor.fetchall())
    except:
        return False

def upload_record(player1, player2, player1_score, player2_score):
    try:
        
        print("已存進資料庫", player1, player2, player1_score, player2_score)
        time = datetime.now()
        cursor.execute("INSERT INTO `record` (`player1`, `player2`, `player1_score`, `player2_score`, `time`) VALUES ('{}', '{}', '{}', '{}', '{}');".format(player1, player2, player1_score, player2_score, time))
        # 提交到資料庫執行
        con.commit()
        return True
        
    except:
        return False
