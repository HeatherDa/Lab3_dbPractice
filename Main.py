import sqlite3
import traceback

db= sqlite3.connect('chainsaw_db.db') #Creates or opens database file
c=db.cursor() #Cursor object for performing operations




def display_menu():
    option=input("\n1. Display table\n2. New entry\n3. Search\n4. Update Entry\n5. Quit\nEnter selection: ")
    print("")
    if option=='1':
        view_table()
        return '1'
    elif option =='2':
        new_juggler()
        return '2'
    elif option =='3':
        print(search_db())
        return '3'
    elif option =='4':
        update_entry()
        return '4'
    elif option =='5':
        close_database()
        return '5'

def create_juggler_table():
    #Create table
    try:
        c.execute('create table if not exists chainsaw_jugglers (Chainsaw_Juggling_Record_Holder text, Country text, Number_of_catches int)')
        c.execute('SELECT * FROM chainsaw_jugglers')
        rec=c.fetchall()
        if len(rec)<3:
            contestants=[('Ian Stewart', 'Canada', 94),
                         ('Aaron Gregg', 'Canada', 88),
                         ('Chad Taylor', 'USA', 78)
                         ]
            c.executemany('INSERT INTO chainsaw_jugglers VALUES (?,?,?)', contestants)
            db.commit()  #save changes
    except sqlite3.OpterationalError:
        traceback.print_exc()
        return

    except sqlite3.Error as e:
        print('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def new_juggler():
    try:
        number=0
        name=input("Please enter the name of the competitor: ")
        country=input("Please enter the country from which the competitor came: ")
        num=input("Please enter the number of catches the competitor made: ")
        if num.isnumeric():
            number=int(num)
        c.execute('insert into chainsaw_jugglers values(?,?,?)',(name,country,number))
        db.commit()  #save changes

    except sqlite3.IntegrityError:
        print ('wrong data type?  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

    except sqlite3.Error as e:
        print('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def search_db():
    col=input("1. Chainsaw_Juggling_Record_Holder\n2. Country\n\nEnter which column to search.")
    val=input('Enter the search parameter: ')
    try:
        if col=='1':
            value=(val,)
            c.execute('SELECT * FROM chainsaw_jugglers WHERE Chainsaw_Juggling_Record_Holder=?',value)
            print (c.fetchone())
        elif col=='2':
            value=(val,)
            c.execute('SELECT * FROM chainsaw_jugglers WHERE Country=?', value)
            print (c.fetchone())
    except sqlite3.Error as e:
        print('An error occurred.')
        traceback.print_exc()

def view_table():
    print('')
    for row in c.execute('select * from chainsaw_jugglers'):
        print (row)


def delete_juggler_table():
    try:
        c.execute('drop table chainsaw_jugglers') #Delete table
        db.commit() #save changes

    except sqlite3.Error as e:
        print('An error occurred.  Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def update_entry(): #TODO FIX THIS
    name = input("Enter the name of the competitor who's record will be updated:")
    val = input("Enter the updated name of the competitor: ")
    val2 = input('Enter the new country: ')
    val3 = input('Enter the new number of catches: ')
    try:
        value = (val,)
        value2 = (val2,)
        val3=int(val3)
        value3 = (val3,)
        sql= '''UPDATE chainsaw_jugglers
                SET Chainsaw_Juggling_Record_Holder=?, Country=?, Number_of_catches=?
                WHERE Chainsaw_Juggling_Record_Holder=?'''
        c.execute(sql, (value, value2, value3, name))
        return
    except sqlite3.Error as e:
        print('An error occurred. Changes will be rolled back.')
        traceback.print_exc()
        db.rollback()

def close_database():
    db.close()

def main():
    choice=None
    #delete_juggler_table()
    create_juggler_table()
    while choice !='5':
        choice=display_menu()

main()