import mysql.connector

def connect():
  try:
    connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="4kD1F,MjK-)ZScYTa4En@4EO5[&piX}w1_jv",
    database="cryptocoin"
    )
    return connection
  except (Exception, mysql.connector.Error) as error:
    print(error)

def store_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'insert into login (user, passwd) values (%s, %s)'
    record_to_insert = (user, passwd)
    cursor.execute(query, record_to_insert)
    connection.commit()
  except (Exception, mysql.connector.Error) as error:
    print(error)
