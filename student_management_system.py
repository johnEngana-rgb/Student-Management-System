import csv
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox

# access csv file

filepath = 'C:/Users/Acer/Desktop/student.csv'


class Stdudent_Management_System(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.style = ttk.Style()
        self.root = root
        self.setup()
        self.frame = Frame(root)
        # initialize self.id and iid for data insert
        self.id = 0
        self.iid = 0
        self.array = []
        self.tree_frame = self.root

    def setup(self):  # sets up the environment in the application
        self.root.title('Student Management System')
        self.root.geometry('800x550')
        self.root.resizable(0, 0)
        # setup table for csv file...

        # setup theme for ttk
        self.style.theme_use('clam')

        # define columns and headings
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Name', 'Year', 'gender', 'course'))

        self.tree.heading('ID', text='ID', anchor=W, )
        self.tree.heading('Name', text='Student Name', anchor=W)
        self.tree.heading('Year', text='Year', anchor=W)
        self.tree.heading('gender', text='Gender', anchor=W)
        self.tree.heading('course', text='Course', anchor=W)
        self.tree.place(x=400, y=200, anchor=CENTER)
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('ID', stretch=NO, minwidth=0, width=100)
        self.tree.column('Name', stretch=NO, minwidth=0, width=200)
        self.tree.column('Year', stretch=NO, minwidth=0, width=100)
        self.tree.column('gender', stretch=NO, minwidth=0, width=100)
        self.tree.column('course', stretch=NO, minwidth=0, width=100)
        self.tree.bind('<ButtonRelease-1>', self.select)

        # add widgets name

        self.frame_addstud = LabelFrame(self.root, text='Input Student Data', padx=10, pady=20)
        self.frame_addstud.pack(padx=5, pady=5)
        self.frame_addstud.place(x=25, y=340)

        # add widget ID
        self.ID_label = tk.Label(self.frame_addstud, text="ID Number")
        self.ID_entry = tk.Entry(self.frame_addstud, width=70)
        self.ID_label.grid(row=0, column=0, sticky=tk.W)
        self.ID_entry.grid(row=0, column=1)

        self.name_label = tk.Label(self.frame_addstud, text="Student Name")
        self.name_entry = tk.Entry(self.frame_addstud, width=70)
        self.name_label.grid(row=1, column=0, sticky=tk.W)
        self.name_entry.grid(row=1, column=1)

        # add widget year
        self.year_label = tk.Label(self.frame_addstud, text="Year level")
        self.year_entry = tk.Entry(self.frame_addstud, width=70)
        self.year_label.grid(row=2, column=0, sticky=tk.W)
        self.year_entry.grid(row=2, column=1)

        # add widget gender
        self.gender_label = tk.Label(self.frame_addstud, text="Gender")
        self.gender_entry = tk.Entry(self.frame_addstud, width=70)
        self.gender_label.grid(row=3, column=0, sticky=tk.W)
        self.gender_entry.grid(row=3, column=1)

        # add widget course
        self.course_label = tk.Label(self.frame_addstud, text="Course")
        self.course_entry = tk.Entry(self.frame_addstud, width=70)

        self.course_label.grid(row=4, column=0, sticky=tk.W)
        self.course_entry.grid(row=4, column=1)
        self.view_file()

        # BUTTONS.....
        # Submit button
        self.submit_btn = tk.Button(self.frame_addstud, text='insert', command=self.insert_data, width=20)
        self.submit_btn.grid(row=5, column=0)
        self.del_button = tk.Button(self.frame_addstud, text='delete', command=self.del_row, width=20)
        self.del_button.grid(row=5, column=1)
        self.edit_btn = tk.Button(self.frame_addstud, text='edit', command=self.edit_info, width=20)
        self.edit_btn.grid(row=5, column=2)
        self.chech_btn = tk.Button(self.frame_addstud, text='check', command=self.check_if_exists, width=20)
        self.chech_btn.grid(row=6, column=0)

        self.modify = StringVar()

        self.search = tk.Label(self.root, text="Input ID number")
        self.search.place(x=175, y=20)
        self.search_box = tk.Entry(self.root, textvariable=self.modify, width=50)
        self.search_box.place(x=270, y=20)
        self.modify.trace('w',
                          lambda name, index, mode, modify=self.modify: self.search_stud(str(self.search_box.get())))

        # search

    def edit_info(self):
        dlt = self.tree.selection()[0]
        print(dlt)
        self.tree.delete(dlt)
        self.infile()

        self.tree.insert('', 'end', iid=self.iid, text="Item_" + str(self.id),
                         values=(self.ID_entry.get(),
                                 self.name_entry.get(),
                                 self.year_entry.get(),
                                 self.gender_entry.get(),
                                 self.course_entry.get()))
        self.iid = self.iid + 1
        self.id = self.id + 1

        with open(filepath, 'a', newline='') as file:
            reader = csv.DictWriter(file,
                                    fieldnames=('ID number', 'Name', 'year', 'Gender', 'course'),
                                    lineterminator='\n'
                                    )
            reader.writerow({
                'Name': self.name_entry.get(),
                'ID number': self.ID_entry.get(),
                'year': self.year_entry.get(),
                'Gender': self.gender_entry.get(),
                'course': self.course_entry.get()
            })

    def search_stud(self, searching=''):
        self.tree.delete(*self.tree.get_children())

        with open(filepath, 'r') as file:
            read = csv.reader(file)
            self.iid = 1
            for student in read:
                if searching == '':
                    self.tree.insert(parent='', index='end', iid=self.iid, text='',
                                     values=(student[0], student[1], student[2], student[3], student[4]))
                else:
                    if searching in str(student[0]):
                        self.tree.insert(parent='', index='end', iid=self.iid, text='',
                                         values=(student[0], student[1], student[2], student[3], student[4]))

                self.iid += 1

    def check_if_exists(self):
        self.ID_num = self.sel['values'][0]
        list = []
        values = self.tree.item(self.var, 'values')
        print(values[0])
        print("hope this works")
        with open(filepath, 'r') as file:
            tups = tuple(file)
            for row in tups:
                print(row)


    def del_row(self):
        dlt = self.tree.selection()[0]
        print(dlt)
        self.tree.delete(dlt)
        self.infile()

        self.ID_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.gender_entry.delete(0, END)
        self.course_entry.delete(0, END)

    # def (del_csv):

    def select(self, a):
        self.ID_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.gender_entry.delete(0, END)
        self.course_entry.delete(0, END)
        self.var = self.tree.focus()
        self.sel = self.tree.item(self.var)
        self.ID_num = self.sel['values'][0]
        values = self.tree.item(self.var, 'values')

        self.ID_entry.insert(0, values[0])
        self.name_entry.insert(0, values[1])
        self.year_entry.insert(0, values[2])
        self.gender_entry.insert(0, values[3])
        self.course_entry.insert(0, values[4])

    def infile(self):
        self.array = []
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != self.ID_num:
                    self.array.append(row)

        with open(filepath, 'w', newline='') as newfile:
            writer = csv.writer(newfile)
            for i in self.array:
                writer.writerow(i)

    def view_file(self):
        with open(filepath) as access:
            reader = csv.DictReader(access, delimiter=",")
            for row in reader:
                ID = row["ID"]
                Student = row['STUDENT']
                year = row['YEAR LEVEL']
                gender = row['GENDER']
                course = row['COURSE']
                self.tree.insert("", 0, values=(ID, Student, year, gender, course))

        # set up Student management system table

    # FUNCTIONS....
    # write function for the csv and tkinter
    def insert_data(self):
        self.check_if_exists()
        self.tree.insert('', 'end', iid=self.iid, text="Item_" + str(self.id),
                         values=(self.ID_entry.get(),
                                 self.name_entry.get(),
                                 self.year_entry.get(),
                                 self.gender_entry.get(),
                                 self.course_entry.get()))
        self.iid = self.iid + 1
        self.id = self.id + 1

        with open(filepath, 'a', newline='') as file:
            reader = csv.DictWriter(file,
                                    fieldnames=('ID number', 'Name', 'year', 'Gender', 'course'),
                                    lineterminator='\n'
                                    )
            reader.writerow({
                'Name': self.name_entry.get(),
                'ID number': self.ID_entry.get(),
                'year': self.year_entry.get(),
                'Gender': self.gender_entry.get(),
                'course': self.course_entry.get()
            })
            self.name_entry.delete(0, END)
            self.course_entry.delete(0, END)
            self.ID_entry.delete(0, END)
            self.year_entry.delete(0, END)
            self.gender_entry.delete(0, END)


app = Stdudent_Management_System(Tk())
app.root.mainloop()
