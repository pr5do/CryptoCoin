import mysql.connector
from termcolor import colored


def connect():
  try:
    connection = mysql.connector.connect(
    host="localhost",
    user="cryptocoin_viewer",
    passwd="pRsxCjiqu}Laq(wF[y46_>v]ugTq1[TjEiUy",
    database="cryptocoin"
    )
    return connection
  except (Exception, mysql.connector.Error) as error:
    return error


def store_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'insert into login (user, passwd) values (%s, %s)'
    record_to_insert = (user, passwd)
    cursor.execute(query, record_to_insert)
    connection.commit()
    return True
  except (Exception, mysql.connector.Error) as error:
    return error


def find_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'select * from login where user = %s and passwd = %s'
    record_to_insert = (user, passwd)
    cursor.execute(query, record_to_insert)
    response = cursor.fetchone()
    return response
  except (Exception, mysql.connector.Error) as error:
    return error
