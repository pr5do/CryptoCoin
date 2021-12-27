import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="4kD1F,MjK-)ZScYTa4En@4EO5[&piX}w1_jv",
    database="cryptocoin"
)

mycursor = db.cursor()

mycursor.execute('desc login')

for x in mycursor:
    print(x)
