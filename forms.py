import psycopg2 as dbapi
import os

url = os.getenv("url")

class ShowMe:
	def Check_username(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select username FROM Users Where username=%s;"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				len_c = len(cursor_list)
				if len_c == 1:
					return False
				else:
					return True

	def User_Add(self, name, surname,gender, username, password):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """INSERT INTO Users(name,surname,gender,username,password) VALUES(%s,%s,%s,%s,%s);"""
				cursor.execute(statement,([name,surname,gender,username,password]))

	def Check_existing_user(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select username, password FROM Users Where username=%s;"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				return cursor_list
	
	def All_Users(self,username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select Name, Surname, Username,Gender, followed.id, followed.source, followed.target From Users as t1 left join followed on followed.target=t1.username where followed.source=%s 
union all
Select Name, Surname, Username,Gender, followed.id, followed.source, followed.target from Users as t2 left join followed on followed.target='NULL' where username not in (Select Username From Users as t1 left join followed on followed.target=t1.username where followed.source=%s) ;

  """
				cursor.execute(statement,([username,username]))
				cursor_list=cursor.fetchall()
				return cursor_list

	def User_key(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select Name, Surname, Username From Users;"""
				cursor.execute(statement)
				cursor_list=cursor.fetchall()
				return cursor_list

	def Follow_add(self, source, target):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """INSERT INTO Followed(source,target) VALUES(%s,%s);"""
				cursor.execute(statement,([source,target]))
	
	def Followed_users(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """ Select Name, Surname, Username, Gender, followed.id, followed.source, followed.target From Users left join followed on followed.target=users.username where followed.source=%s; """
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				return cursor_list

	def Follow_delete(self, source, target):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Delete from followed where source=%s and target=%s;"""
				cursor.execute(statement,([source,target]))
	
	def Bookmark_add(self, username, url_bookmark):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """INSERT INTO Bookmarks(username,url) VALUES(%s,%s);"""
				cursor.execute(statement,([username,url_bookmark]))
	
	def Bookmarks(self,username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select id, url From bookmarks where username=%s;"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				return cursor_list
	
	def Bookmark_delete(self,id):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Delete from bookmarks where id=%s;"""
				cursor.execute(statement,([id]))

	def About_key(self,username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select username,info from About where username=%s;"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				return cursor_list

	def About_update(self,username,info):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Update About Set info=%s where username=%s;"""
				cursor.execute(statement,([info,username]))

	def About_add(self, username, info):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Insert Into About(username,info) Values(%s,%s);"""
				cursor.execute(statement,([username,info]))
	
	def About_delete(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Delete from about where username=%s;"""
				cursor.execute(statement,([username]))
	
	def Check_about(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """Select username FROM About Where username=%s;"""
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				len_c = len(cursor_list)
				if len_c == 1:
					return False
				else:
					return True

	def Delete_account(self, username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement1 = """Delete FROM About Where username=%s;"""
				statement2 = """Delete FROM Bookmarks Where username=%s;"""
				statement3 = """Delete FROM Followed Where source=%s;"""
				statement4 = """Delete FROM Followed Where target=%s;"""
				statement5 = """Delete FROM Users Where username=%s;"""
				cursor.execute(statement1,([username]))
				cursor.execute(statement2,([username]))
				cursor.execute(statement3,([username]))
				cursor.execute(statement4,([username]))
				cursor.execute(statement5,([username]))

	def get_gender(self,username):
		with dbapi.connect(url) as connection:
			with connection.cursor() as cursor:
				statement = """ Select gender FROM Users WHERE username=%s """
				cursor.execute(statement,([username]))
				cursor_list=cursor.fetchall()
				return cursor_list