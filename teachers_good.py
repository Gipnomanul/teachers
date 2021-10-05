import sqlite3 as sl
from sqlite3 import OperationalError     #Для обработки ошибки ненахождения БД

con = sl.connect('teachers.db')
flag = True

def command():
	if flag == True:
		print('''\nВыберите команду:
			1. Список учителей
			2. Добавить учителя
			3. Добавить предмет существующему учителю
			4. Изменить ФИО учителя
			5. Изменить существующий предмет у учителя
			6. Удалить учителя или предмет
			7. Найти учителя
			8. Статистика школы
			9. Информация о программе
			0. Выход из программы''')
		try:
			s = int(input("\nВведите номер команды: "))
			if s < 0 or s > 9:
				print("Неизвестная команда. Введите команду еще раз.")
				command()
			else:
				if s == 1:
					view_all()
				elif s == 2:
					add_teacher()
				elif s == 3:
					add_lesson()
				elif s == 4:
					edit_teacher()
				elif s == 5:
					edit_lesson()
				elif s == 6:
					delete()
				elif s == 7:
					find_teacher()
				elif s == 8:
					stats()
				elif s == 9:
					info()
				elif s == 0:
					print("\nПрограмма закрывается...")
		except ValueError:
			print("Неизвестная команда. Введите команду еще раз.")
			command()

def again():
	try:
		s = int(input("\nПродолжить работать в программе? 1-Да, 2-Нет: "))
		if s < 1 or s > 2:
			print("Неизвестная команда. Введите команду еще раз.")
			again()
		else:
			if s == 1:
				command()
			else:
				print("\nПрограмма закрывается...")
				flag = False
	except ValueError:
		print("Неизвестная команда. Введите команду еще раз.")
		again()

def view_all():
	with con:
		try:
			print("\n--------------------------------------------------------------")
			print("  ID  |         NAME         |   EXP  |        LESSON        |")
			print("--------------------------------------------------------------")
			data = con.execute("SELECT * FROM TEACHERS_LESSONS_BLANK")
			for row in data:
				print(row)
			print("--------------------------------------------------------------")
			again()
		except OperationalError:
			print("Таблица в базе данных не найдена!!")
			again()
		
def add_teacher():
	print("\nДобавление учителя!")
	name = input("\nВведите ФИО учителя: ")
	exp = int(input("\nВведите опыт учителя: "))
	subject = input("\nВведите предмет, который преподает учитель: ")
	print("\nБудет добавлен учитель", name, ", ведущий предмет", subject, ", его опыт работы:", exp)
	try:
		conf = int(input("\n1 - Подтвердить, 2 - Изменить введенные данные, 3 - Выйти из окна добавления учителя "))
		if conf < 1 or conf > 3:
			print("Неизвестная команда. Введите команду еще раз.")
			add_teacher()
		else:
			if conf == 1:
				maxid = con.execute("SELECT MAX(ID) FROM TEACHERS")
				maxid = maxid.fetchone()[0]    #Нахождение максимального идентификатора в существующей таблице
				maxid += 1
				sql = 'INSERT INTO TEACHERS (id, name, expirience) values(?, ?, ?)'
				data = [(maxid, name, exp)]
				with con:
					con.executemany(sql, data)
				maxidles = con.execute("SELECT MAX(ID) FROM LESSONS")
				maxidles = maxidles.fetchone()[0]
				maxidles += 1
				sql = 'INSERT INTO LESSONS (id, teacher_id, lesson) values(?, ?, ?)'
				data = [(maxidles, maxid, subject)]
				with con:
					con.executemany(sql, data)
				#con.execute("commit")
				print("Пользователь добавлен!")
				again()
			elif conf == 2:
				add_teacher()
			elif conf == 3:
				again()
	except ValueError:
		print("Неизвестная команда. Введите команду еще раз.")
		add_teacher()

def add_lesson():
	print("\nДобавление предмета учителя!")
	with con:
		try:
			print("\n--------------------------------------------------------------")
			print("  ID  |         NAME         |   EXP  |        LESSON        |")
			print("--------------------------------------------------------------")
			data = con.execute("SELECT * FROM TEACHERS_LESSONS_BLANK")
			for row in data:
				print(row)
			print("--------------------------------------------------------------")
			inp_id = int(input("\nВведите id учителя, которому Вы хотите добавить предмет! "))
			teach = con.execute(f"SELECT NAME FROM TEACHERS WHERE ID = {inp_id}")
			teach = teach.fetchone()[0]
			print("\nБудет добавлен предмет учителю", teach)
			les = input('\nВведите предмет, который ведет учитель. Для возврата в главное меню введите "q": ');
			if les == 'q':
				again()
			else:
				print("\nБудет добавлен предмет", les, "учителю", teach)
				try:
					conf = int(input("\n1 - Подтвердить, 2 - Выбрать другой предмет или учителя, 3 - Выйти из окна добавления предмета "))
					if conf < 1 or conf > 3:
						print("Неизвестная команда. Введите команду еще раз.")
						add_lesson()
					elif conf == 1:
						maxidles = con.execute("SELECT MAX(ID) FROM LESSONS")
						maxidles = maxidles.fetchone()[0]
						maxidles += 1
						sql = 'INSERT INTO LESSONS (id, teacher_id, lesson) values(?, ?, ?)'
						data = [(maxidles, inp_id, les)]
						with con:
							con.executemany(sql, data)
						print("\nПредмет добавлен!")
						again()
					elif conf == 2:
						add_lesson()
					elif conf == 3:
						again()
				except ValueError:
					print("Неизвестная команда. Введите команду еще раз.")
					add_teacher()
		except OperationalError:
			print("Таблица в базе данных не найдена!!")
			again()

def edit_teacher():
	print("\nИзменение учителя!")
	with con:
		try:
			print("\n--------------------------------------------------------------")
			print("  ID  |         NAME         |   EXP  |        LESSON        |")
			print("--------------------------------------------------------------")
			data = con.execute("SELECT * FROM TEACHERS_LESSONS_BLANK")
			for row in data:
				print(row)
			print("--------------------------------------------------------------")
			#maxid = con.execute("SELECT MAX(ID) FROM USER")
			#maxid = maxid.fetchone()[0]
			inp_id = int(input("\nВведите id учителя, которого хотите изменить "))
			teach = con.execute(f"SELECT NAME FROM TEACHERS WHERE ID = {inp_id}")
			teach = teach.fetchone()[0]
			print("\nБудет изменен учитель", teach)
			try:
				conf = int(input("\n1 - Подтвердить и ввести новое имя, 2 - Выбрать другого учителя, 3 - Выйти из окна изменения учителя "))
				if conf < 1 or conf > 3:
					print("Неизвестная команда. Введите команду еще раз.")
					edit_teacher()
				else:
					if conf == 1:
						new_teach = input("\nВведите ФИО нового учителя! ")
						con.execute(f"UPDATE TEACHERS SET NAME = '{new_teach}' WHERE ID = {inp_id}")
						con.execute("commit")
						print('\nУчитель изменен!')
						again()
					elif conf == 2:
						edit_teacher()
					elif conf == 3:
						again()
			except ValueError:
				print("Неизвестная команда. Введите команду еще раз.")
				edit_teacher()
		except OperationalError:
			print("Таблица в базе данных не найдена!!")
			again()

def edit_lesson():
	print("\nИзменение предмета учителя!")
	with con:
		try:
			print("\n--------------------------------------------------------------")
			print("  ID  |         NAME         |   EXP  |        LESSON        |")
			print("--------------------------------------------------------------")
			data = con.execute("SELECT * FROM TEACHERS_LESSONS_BLANK")
			for row in data:
				print(row)
			print("--------------------------------------------------------------")
			#maxid = con.execute("SELECT MAX(ID) FROM USER")
			#maxid = maxid.fetchone()[0]
			inp_id = int(input('\nВведите id учителя, предмет которого Вы хотите изменить '))
			print()
			data = con.execute(f"SELECT ID, LESSON FROM LESSONS WHERE TEACHER_ID = {inp_id}")
			for row in data:
				print(row)
			inp_les_id = int(input('\nВведите id предмета, который Вы хотите изменить '))
			teach = con.execute(f"SELECT NAME FROM TEACHERS WHERE ID = {inp_id}")
			teach = teach.fetchone()[0]
			les = con.execute(f"SELECT LESSON FROM LESSONS WHERE ID = {inp_les_id}")
			les = les.fetchone()[0]
			print("\nБудет изменен предмет ", les, "у учителя", teach)
			try:
				conf = int(input("\n1 - Подтвердить изменение, 2 - Выбрать другого учителя или предмет, 3 - Выйти из окна изменения предмета "))
				if conf < 1 or conf > 3:
					print("Неизвестная команда. Введите команду еще раз.")
					edit_lesson()
				else:
					if conf == 1:
						new_les = input("\nВведите новое название предмета, либо нажмите q для отмены ")
						if new_les =='q':
							again()
						else:
							con.execute(f"UPDATE LESSONS SET LESSON = '{new_les}' WHERE ID = {inp_les_id}")
							con.execute("commit")
							print('\nПредмет изменен!')
							again()
					elif conf == 2:
						edit_lesson()
					elif conf == 3:
						again()
			except ValueError:
				print("Неизвестная команда. Введите команду еще раз.")
				edit_lesson()
		except OperationalError:
			print("Таблица в базе данных не найдена!!")
			again()

def delete():
	print("\nУдаление!")
	with con:
		try:
			print("\n--------------------------------------------------------------")
			print("  ID  |         NAME         |   EXP  |        LESSON        |")
			print("--------------------------------------------------------------")
			data = con.execute("SELECT * FROM TEACHERS_LESSONS_BLANK")
			for row in data:
				print(row)
			print("--------------------------------------------------------------")
			#maxid = con.execute("SELECT MAX(ID) FROM USER")
			#maxid = maxid.fetchone()[0]
			ch = int(input("Введите 1 для удаления учителя, 2 для удаления предмета, 3 для выхода в главное меню "))
			if ch < 1 or ch > 3:
				print("Неизвестная команда. Введите команду еще раз.")
				delete()
			elif ch == 1:
				print("\nУдаление учителя! ")
				inp_id = int(input("\nВведите id учителя, которого хотите удалить "))
				teach = con.execute(f"SELECT NAME FROM TEACHERS WHERE ID = {inp_id}")
				teach = teach.fetchone()[0]
				print("\nБудет удален учитель", teach)
				try:
					conf = int(input("\n1 - Подтвердить, 2 - Выбрать другого учителя, 3 - Выйти из окна удаления учителя "))
					if conf < 1 or conf > 3:
						print("Неизвестная команда. Введите команду еще раз.")
						edit_teacher()
					else:
						if conf == 1:
							#sql = f'DELETE FROM USER WHERE ID = {inp_id}'
							con.execute(f"DELETE FROM TEACHERS WHERE ID = {inp_id}")
							con.execute(f"DELETE FROM LESSONS WHERE TEACHER_ID = {inp_id}")
							con.execute("commit")
							print('\nУчитель удален!')
							again()
						elif conf == 2:
							delete_teacher()
						elif conf == 3:
							again()
				except ValueError:
					print("Неизвестная команда. Введите команду еще раз.")
					delete()
			elif ch == 2:
				print("\nУдаление предмета!")
				inp_id = int(input('\nВведите id учителя, предмет которого Вы хотите удалить '))
				print()
				data = con.execute(f"SELECT ID, LESSON FROM LESSONS WHERE TEACHER_ID = {inp_id}")
				for row in data:
					print(row)
				inp_les_id = int(input('\nВведите id предмета, который Вы хотите удалить '))
				teach = con.execute(f"SELECT NAME FROM TEACHERS WHERE ID = {inp_id}")
				teach = teach.fetchone()[0]
				les = con.execute(f"SELECT LESSON FROM LESSONS WHERE ID = {inp_les_id}")
				les = les.fetchone()[0]
				print("\nБудет удален предмет ", les, "у учителя", teach)
				try:
					conf = int(input("\n1 - Подтвердить удаление, 2 - Выбрать другого учителя или предмет, 3 - Выйти из окна изменения предмета "))
					if conf < 1 or conf > 3:
						print("Неизвестная команда. Введите команду еще раз.")
						edit_lesson()
					else:
						if conf == 1:
							con.execute(f"DELETE FROM LESSONS WHERE ID = {inp_les_id}")
							con.execute("commit")
							print('\nПредмет удален!')
							again()
						elif conf == 2:
							delete()
						elif conf == 3:
							again()
				except ValueError:
					print("Неизвестная команда. Введите команду еще раз.")
					delete()
			else:
				again()
		except OperationalError:
			print("Таблица в базе данных не найдена!!")
			again()

def find_teacher():
	print("\nПоиск учителя!")
	with con:
		try:
			query = input("Введите текст, будет произведен поиск ПО ФИО или по предмету, содержащими данный текст ")
			data = con.execute(f"SELECT * FROM TEACHERS_LESSONS WHERE NAME LIKE '%{query}%' OR LESSON LIKE '%{query}%'")
			if data == '':
				print(f"Учителя и предметы, включающие в себя {query}, не найдены.")
			else:
				for row in data:
					print(row)
			again()
		except OperationalError:
			print("Таблица в базе данных не найдена!!")
			again()

def stats():
	try:
		print("\nСтатистика количества предметов")
		data = con.execute("SELECT * FROM STATS")
		for row in data:
			print(row)
		again()
	except OperationalError:
		print("Таблица в базе данных не найдена!!")
		again()
			
def info():
	print('''\nПрограмма 'Учителя', версия 0.2
	Разработчик программы - Алексей Сизов.
	Тестовый проект базы данных учителей из школы.
	Программа имеет возможность редактирования, добавления и удаления учителей в базе данных школы, также поиск и статистика.
	По всем вопросам и предложениям пишите на рабочий адрес gipno2009@yandex.ru''')
	again()
	
print("Добрый день, Вас приветствует программа 'Учителя', версия 0.2\nРазработчик программы - Алексей Сизов.")
command()


	

#with con:
    # con.execute("""
        # CREATE TABLE USER2 (
            # id INTEGER NOT NULL PRIMARY KEY,
            # name TEXT,
            # subject text
        # );
    # """)
#sql = 'INSERT INTO USER (id, name, subject) values(?, ?, ?)'
#data = [(1, 'Alice', 'Math'), (2, 'Bob', 'Russian Language'), (3, 'Chris', 'IT')]

#with con:
#    con.executemany(sql, data)
