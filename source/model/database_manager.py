import mysql.connector


def connect():
  try:
    connection = mysql.connector.connect(
    host="localhost",
    user="cryptocoin-viewer",
    passwd="pRsxCjiqu}Laq(wF[y46_>v]ugTq1[TjEiUy",
    database="cryptocoin"
    )
    return connection
  except (Exception, mysql.connector.Error) as error:
    return error


def store_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor(buffered=True)
    query = 'insert into login (user, passwd) values (%s, %s)'
    record_to_insert = [user, passwd]
    cursor.execute(query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  except (Exception, mysql.connector.Error) as error:
    return error


def find_user(user):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'select * from login where user = %s'
    record_to_insert = [user]
    cursor.execute(query, record_to_insert)
    response = cursor.fetchone()
    cursor.close()
    connection.close()
    return (response[1], response[2])
  except (Exception, mysql.connector.Error) as error:
    return error

def delete_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'delete from login where user = %s and passwd = %s '
    record_to_insert = [user, passwd]
    cursor.execute(query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()
    return True
  except (Exception, mysql.connector.Error) as error:
    return error