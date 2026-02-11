import sqlite3
from tkinter import *
from tkinter import messagebox

# Creating Database
class Mosque:
    def __init__(self, ID, name,type,address,coordinates,imam):
        self.ID = ID
        self.name = name
        self.type = type
        self.address = address
        self.coordinates = coordinates
        self.imam = imam

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("mosques.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mosq(
        ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        Coordinates TEXT,
        Imam TEXT
        )            
        """)
        self.conn.commit()

    def display(self):
        self.cursor.execute("SELECT * FROM Mosq")
        return self.cursor.fetchall()

    def search(self,name):
        self.cursor.execute("SELECT * FROM  Mosq WHERE Name = ?",(name,))
        return self.cursor.fetchall()

    def insert(self,ID,name,type,address,coordinates,imam):
        self.cursor.execute("INSERT INTO Mosq VALUES(?,?,?,?,?,?)",
                (ID,name,type,address,coordinates,imam)
        )
        self.conn.commit()

    def update(self, ID, name, type, address, coordinates, imam):
        self.cursor.execute("""
            UPDATE Mosq
            SET Name=?, Type=?, Address=?, Coordinates=?, Imam=?
            WHERE ID=?
            """,
(name, type, address, coordinates, imam, ID)
                            )
        self.conn.commit()
        return self.cursor.rowcount

    def delete(self,ID):
        self.cursor.execute("DELETE FROM Mosq WHERE ID = ?", (ID,))
        self.conn.commit()
        return self.cursor.rowcount

    def __del__(self):
        self.conn.close()

db = Database()

# GUI
root = Tk()
root.geometry("900x300+300+150")
root.title("Mosques Management System")

# Creating Label
L1 = Label(root, text="ID")
L2 = Label(root, text="Type")
L3 = Label(root, text="Coordinates")
L4 = Label(root, text="Name")
L5 = Label(root, text="Address")
L6 = Label(root, text="Imam_name")

# Creating Entry
e1 = Entry(root)
e3 = Entry(root)
e4 = Entry(root)
e5 = Entry(root)
e6 = Entry(root)

# creating option menu
types = StringVar()
o1 = OptionMenu(root,types,"Mosque","Masjid","Jameh","Musslla")
o1.config(width=12)

# creating list box
list1 = Listbox(root,width=50,height=12)
list1.place(x=570,y=20)

# creating scrollbar
s1 = Scrollbar(root, orient=VERTICAL)
s1.place(x=880,y=20,height=200)

list1.config(yscrollcommand=s1.set)
s1.config(command=list1.yview)


# function button
def display_all():
    list1.delete(0,END)
    rows = db.display()
    for row in rows:
        list1.insert(END,row)

def search_entry():
    list1.delete(0,END)
    name = e4.get()
    result = db.search(name)
    if result:
        list1.insert(END,result)
    else:
        messagebox.showinfo("Result","Mosque not found")

def add_entry():
    try:
        mosque = Mosque(
            int(e1.get()),
            e4.get(),
            types.get(),
            e5.get(),
            e3.get(),
            e6.get()
        )
        db.insert(mosque.ID, mosque.name, mosque.type,
                  mosque.address, mosque.coordinates, mosque.imam)
        messagebox.showinfo("Success", "Record added")
    except:
        messagebox.showerror("Error","Unable to add the record. Please check your input.")


def update_entry():
    try:
        ID = int(e1.get())
        new_name = e4.get()
        new_type = types.get()
        new_address = e5.get()
        new_coordinates = e3.get()
        new_imam = e6.get()

        result = db.update(ID, new_name, new_type, new_address, new_coordinates, new_imam)

        if result == 0:
            messagebox.showinfo("Result", "No record found with this ID")
        else:
            messagebox.showinfo("Success", "Record updated")

    except:
        messagebox.showerror("Error", "Error updating record. Please check your input.")

def delete_entry():
    try:
        result = db.delete(int(e1.get()))

        if result == 0:
            messagebox.showinfo("Result", "No record found with this ID")
        else:
             messagebox.showinfo("Success", "Record deleted")
    except:
        messagebox.showerror("Error", "Invalid ID")



# Creating Button
B1 = Button(root,text="Display All",padx=13,command = display_all)
B2 = Button(root,text="Add Entry",padx=14, command = add_entry)
B3 = Button(root,text="Search By Name",padx=3,command=search_entry)
B4 = Button(root,text="Delete Entry",padx=14,command=delete_entry)
B5 = Button(root,text="Update Entry",padx=11,command=update_entry)
B6 = Button(root,text="Display on Map",padx=4) # not execution


# place
L1.place(x=20,y=10)
e1.place(x=120,y=10)
L2.place(x=20,y=40)
o1.place(x=120,y=40)
L3.place(x=20,y=70)
e3.place(x=120,y=70)
L4.place(x=300,y=10)
e4.place(x=420,y=10)
L5.place(x=300,y=40)
e5.place(x=420,y=40)
L6.place(x=300,y=70)
e6.place(x=420,y=70)
B1.place(x=100,y=150)
B2.place(x=100,y=190)
B3.place(x=200,y=150)
B4.place(x=200,y=190)
B5.place(x=310,y=150)
B6.place(x=310,y=190)


root.mainloop()