from tkinter import *
from tkinter import ttk
import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS items(
            id Integer Primary Key,
            question text,
            a text,
            b text,
            c text,
            d text,
            ans text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, question, a, b, c, d, ans):
        self.cur.execute("insert into items values (NULL,?,?,?,?,?,?)",
                         (question, a, b, c, d, ans))
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * from items")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("delete from items where id=?", (id,))
        self.con.commit()

    def update(self, id, question, a, b, c, d, ans):
        self.cur.execute(
            "update items set question=?, a=?, b=?, c=?, d=?, ans=? where id=?",
            (question, a, b, c, d, ans, id))
        self.con.commit()

db = Database("item.db")
root = Tk()
root.title("Item Editor")
root.geometry("900x700")
root.config(bg="#2c3e50")
# root.state("zoomed")

question = StringVar()
a = StringVar()
b = StringVar()
c = StringVar()
d = StringVar()
ans = StringVar()

entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Item Editor", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblTitle = Label(entries_frame, text="Question", font=("Calibri", 16), bg="#535c68", fg="white")
lblTitle.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtTitle = Entry(entries_frame, textvariable=question, font=("Calibri", 16), width=68)
txtTitle.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky="w")

lbla = Label(entries_frame, text="a", font=("Calibri", 16), bg="#535c68", fg="white")
lbla.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txta = Entry(entries_frame, textvariable=a, font=("Calibri", 16), width=30)
txta.grid(row=2, column=1, padx=10, pady=10, sticky="w")

lblb = Label(entries_frame, text="b", font=("Calibri", 16), bg="#535c68", fg="white")
lblb.grid(row=2, column=2, padx=10, pady=10, sticky="w")
txtb = Entry(entries_frame, textvariable=b, font=("Calibri", 16), width=30)
txtb.grid(row=2, column=3, padx=10, pady=10, sticky="w")

lblc = Label(entries_frame, text="c", font=("Calibri", 16), bg="#535c68", fg="white")
lblc.grid(row=3, column=0, padx=10, pady=10, sticky="w")
txtc = Entry(entries_frame, textvariable=c, font=("Calibri", 16), width=30)
txtc.grid(row=3, column=1, padx=10, sticky="w")

lbld = Label(entries_frame, text="d", font=("Calibri", 16), bg="#535c68", fg="white")
lbld.grid(row=3, column=2, padx=10, pady=10, sticky="w")
txtd = Entry(entries_frame, textvariable=d, font=("Calibri", 16), width=30)
txtd.grid(row=3, column=3, padx=10, sticky="w")

lblans = Label(entries_frame, text="ans", font=("Calibri", 16), bg="#535c68", fg="white")
lblans.grid(row=4, column=2, padx=10, pady=10, sticky="w")
txtans = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=ans, state="readonly")
txtans['values'] = ("a", "b", "c", "d")
txtans.grid(row=4, column=3, padx=10, sticky="w")

def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    question.set(row[1])
    a.set(row[2])
    b.set(row[3])
    c.set(row[4])
    d.set(row[5])
    ans.set(row[6])

def dispalyAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)

def add_item():
    if txtTitle.get() == "" or txta.get() == "" or txtb.get() == "" or txtc.get() == "" or txtd.get() == "" or txtans.get() == "" :
        print("Erorr", "Please Fill All the Fields")
        return
    db.insert(txtTitle.get(),txta.get(), txtb.get() , txtc.get() ,txtd.get(), txtans.get())
    print("Success", "Record Inserted")
    clearAll()
    dispalyAll()

def update_item():
    if txtTitle.get() == "" or txta.get() == "" or txtb.get() == "" or txtc.get() == "" or txtd.get() == "" or txtans.get() == "" :
        print("Erorr", "Please Fill All the Fields")
        return
    db.update(row[0],txtTitle.get(), txta.get(), txtb.get(), txtc.get(), txtd.get(), txtans.get())
    print("Success", "Record Updated")
    clearAll()
    dispalyAll()

def delete_item():
    db.remove(row[0])
    clearAll()
    dispalyAll()

def clearAll():
    question.set("")
    a.set("")
    b.set("")
    c.set("")
    d.set("")
    ans.set("")

btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="w")
btnAdd = Button(btn_frame, command=add_item, text="Add Record", width=15, font=("Calibri", 16, "bold"), bd=0).grid(row=0, column=0)
btnEdit = Button(btn_frame, command=update_item, text="Update Record", width=15, font=("Calibri", 16, "bold"), bd=0).grid(row=0, column=1, padx=10)
btnDelete = Button(btn_frame, command=delete_item, text="Delete Record", width=15, font=("Calibri", 16, "bold"), bd=0).grid(row=0, column=2, padx=10)
btnClear = Button(btn_frame, command=clearAll, text="Clear Input", width=15, font=("Calibri", 16, "bold"), bd=0).grid(row=0, column=3, padx=10)

tree_frame = Frame(root, bg="#ecf0f1")
tree_frame.place(x=0, y=480, width=1980, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 18), rowheight=50)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))
tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7), style="mystyle.Treeview")
tv.heading(1,text="id", anchor="center")
tv.heading(2,text="question", anchor="center")
tv.heading(3,text="a", anchor="center")
tv.heading(4,text="b", anchor="center")
tv.heading(5,text="c", anchor="center")
tv.heading(6,text="d", anchor="center")
tv.heading(7,text="ans", anchor="center")
tv.column("#1",anchor="w",width=100, stretch=False)
tv.column("#2",anchor="w", width=200, stretch=False)
tv.column("#3",anchor="w", width=100, stretch=False)
tv.column("#4",anchor="w", width=100, stretch=False)
tv.column("#5",anchor="w", width=100, stretch=False)
tv.column("#6",anchor="w", width=100, stretch=False)
tv.column("#7",anchor="w", width=100, stretch=False)
tv['show'] = 'headings'
tv.bind("<ButtonRelease>", getData)
tv.pack(fill=X)

dispalyAll()
root.mainloop()
