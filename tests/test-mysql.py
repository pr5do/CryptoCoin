from database_manager import store_user
import getpass

user = input("Provide your username: ").replace(" ", "")

passwd = getpass.getpass("Provide your password: ").replace(" ", "")

store_user(user, passwd)