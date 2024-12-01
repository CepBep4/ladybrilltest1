import pickle
import pymysql.cursors
import datetime
import traceback
import pprint as pp
from random import randint
import os
import cryptography

class errorLogin(BaseException): ...
class errorPassword(BaseException): ...
class errorConnectionBase(BaseException): ...
class errorDeleteUser(BaseException): ...

def wrt_logg(text):
    with open('logg.txt','a') as file:
        file.write(f'\n{text}')

class DataBase:
    def connection_base(self):
        try:
            self.connection = pymysql.connect(host='188.225.46.105',
                user='gen_user',
                password='Oksana380838',
                db='default_db',
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=20,
                write_timeout=20,
                read_timeout=20)
        except Exception as error:
            raise errorConnectionBase(error)

    def regestration_new_user(self, login: str, password: str, admin=False):
        self.login=str(login)
        self.password=str(password)
        
        if self.login is None: raise errorLogin('Логин не может быть пустым')
        if self.password is None or len(self.password)>8 and admin==False: raise errorPassword('Пароль должен состоять из восьми символов')

        DataBase.connection_base(self)
        if admin==False:
            try:
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO `users` VALUES ('{}', '{}', '{}', 'None')".format(str(self.login),str(self.password),f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}')
                    cursor.execute(sql)
                    self.connection.commit()
            except Exception as error:
                raise error
            finally:
                self.connection.close()
        else:
            try:
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO `users` VALUES ('{}', '{}', '{}', 'ADMIN')".format(str(self.login),'913750380838',f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}')
                    cursor.execute(sql)
                    self.connection.commit()
            except Exception as error:
                raise error
            finally:
                self.connection.close()
    def check_user(self, login: str, password: str):
        try:
            self.connection = pymysql.connect(host='188.225.46.105',
                user='gen_user',
                password='Oksana380838',
                db='default_db',
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=20,
                write_timeout=20,
                read_timeout=20
            )

            self.login=str(login)
            self.password=str(password)


            with self.connection.cursor() as cursor:
                sql_date = "UPDATE `usersfont` SET `date_online` = '{}' WHERE `login`='{}'".format(f'{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}',self.login)
                cursor.execute(sql_date)
                sql = "SELECT `password` FROM `usersfont` WHERE `login`='{}'".format(self.login)
                cursor.execute(sql)
                self.connection.commit()
                result = cursor.fetchone()

                if result['password']==self.password:
                    sql = "SELECT `id` FROM `usersfont` WHERE `login`='{}'".format(self.login)
                    cursor.execute(sql)				
                    r=cursor.fetchone()
                    if not r['id']:
                        idu=str(randint(99999,999999))
                        sql_u = "UPDATE `usersfont` SET `id` = '{}' WHERE `login`='{}'".format(idu,self.login)
                        cursor.execute(sql_u)
                        self.connection.commit()
                        return idu
                    else:
                        return r["id"]
                            
                else:
                    return False
                
                
        except Exception as error:
            wrt_logg(str(error))

        finally:
            self.connection.close()	

def check_auth(login: str, password: str):
    try:
        return DataBase().check_user(login, password)
    except Exception as error:
        wrt_logg(str(error))
        return False
    
def get(uid):
    with open(f'static/userbase/{uid}.pickle', 'rb') as file:
        return pickle.load(file)

def add(uid):
    if not os.path.exists(f'static/userbase/{uid}.pickle'):
        with open(f'static/userbase/{uid}.pickle', 'wb') as file:
            #print('Новый добавлен')
            pickle.dump({'user_id': uid}, file)

def save(uid, params):
    with open(f'static/userbase/{uid}.pickle', 'wb') as file:
        wrt_logg(f'Сохранено - {params}')
        #print(f'Сохранено - {params}')
        pickle.dump(params, file)

if __name__=='__main__':
    pass