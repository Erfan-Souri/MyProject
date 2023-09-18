from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os.path
import requests
import json

# API KEY not implemented for security purposes
MY_API_KEY = ""

root = Tk()


# definition of root window
root.title("Personal Project of Erfan Souri")
root.geometry("480x350")
root.resizable(False,False)


# creating tables
if os.path.isfile('descriptive.db'):
    pass
else:
    # creating databases
    conn_descriptive = sqlite3.connect('descriptive.db')

    # creating cursors
    cursor_descriptive = conn_descriptive.cursor()
    cursor_descriptive.execute("""CREATE TABLE descriptive(
                                d_question text,
                                d_answer text,
                                d_level text)""")
    # commit changes
    conn_descriptive.commit()

    # close connection
    conn_descriptive.close()


frame_descriptive = LabelFrame(root, text="Descriptive" ,padx=0, pady=15)
frame_descriptive.grid(row=0, column=0,ipadx=20)

# definitions for descriptive
clicked_dmld = StringVar()
clicked_dmld.set("1")

label_question_descriptive = Label(frame_descriptive, text="Question :")
label_answer_descriptive = Label(frame_descriptive, text="Answer :")
label_level_descriptive = Label(frame_descriptive, text="Level :")
label_info_main_menu = Label(root,text="NOTE : Please write a question and an answer"+"\n"  " then hit the Add button to add it to database.")
drop_menu_level_descriptive = OptionMenu(frame_descriptive, clicked_dmld, "1", "2", "3", "4")
entry_question_descriptive = Entry(frame_descriptive, width=50)
entry_answer_descriptive = Entry(frame_descriptive, width=50)

# calls on main page for descriptive
label_question_descriptive.grid(row=1, column=1, padx=5, pady=5)
label_answer_descriptive.grid(row=2, column=1, padx=5, pady=5)
label_level_descriptive.grid(row=3, column=1, padx=5, pady=5)
entry_question_descriptive.grid(row=1, column=2, ipadx=10, padx=5, pady=5)
entry_answer_descriptive.grid(row=2, column=2, ipadx=10, padx=5, pady=5)
drop_menu_level_descriptive.grid(row=3, column=2, padx=5, pady=5)

label_info_main_menu.grid(row=4)
entry_question_descriptive.focus_set()

frame_menu_buttons = LabelFrame(root,text="Buttons")
frame_menu_buttons.grid(row=1, column=0,sticky=W+E, padx=13, pady=5)


def open_database():
    database_window=Toplevel()
    database_window.title('Database')
    database_window.geometry("1000x495")
    database_window.resizable(False,False)

    database_window.grab_set()

    # creating databases
    conn_descriptive = sqlite3.connect('descriptive.db')

    # creating cursors
    cursor_descriptive = conn_descriptive.cursor()

    cursor_descriptive.execute("SELECT *,oid FROM descriptive")
    records=cursor_descriptive.fetchall()

    # create a main frame
    database_frame = Frame(database_window)
    database_frame.pack(fill=BOTH, expand=1)

    # create a canvas
    database_canvas = Canvas(database_frame)
    database_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # add scrollbar to canvas
    database_scrollbar = ttk.Scrollbar(database_frame, orient=VERTICAL, command=database_canvas.yview)
    database_scrollbar.pack(side=RIGHT, fill=Y)

    # configure canvas
    database_canvas.configure(yscrollcommand=database_scrollbar.set)
    database_canvas.bind('<Configure>',
                         lambda e: database_canvas.configure(scrollregion=database_canvas.bbox("all")))

    # adding another frame
    second_frame = Frame(database_canvas)

    # add that new frame to window in canvas
    database_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    if not records:
        database_window.destroy()
        messagebox.showerror("Empty Database", "Please enter a record first.")

    else:
        entry_show_id=Entry(second_frame,width=3 )
        entry_show_question=Entry(second_frame,width=75)
        entry_show_answer=Entry(second_frame,width=75)
        entry_show_level=Entry(second_frame,width=8)

        entry_show_id.insert(0,"ID")
        entry_show_question.insert(0,"Question")
        entry_show_answer.insert(0,"Answer")
        entry_show_level.insert(0,"Level")

        entry_show_id.configure(state='readonly')
        entry_show_question.configure(state='readonly')
        entry_show_answer.configure(state='readonly')
        entry_show_level.configure(state='readonly')

        entry_show_id.grid(row=0,column=0, padx=2 , pady=2)
        entry_show_question.grid(row=0,column=1, padx=2 , pady=2)
        entry_show_answer.grid(row=0,column=2, padx=2 , pady=2)
        entry_show_level.grid(row=0,column=3, padx=2 , pady=2)

        r = int
        c = int
        r = 0
        c = 0

        # print_records=''
        for record in records:
            c = 0
            r = r+1
            id_e=Entry(second_frame,width=3)
            id_e.insert(0,str(record[3]))
            id_e.configure(state='readonly')
            id_e.grid(row=r,column=c)
            c = c+1

            question_e = Entry(second_frame, width=75)
            question_e.insert(0, str(record[0]))
            question_e.configure(state='readonly')
            question_e.grid(row=r,column=c)
            c = c+1

            answer_e = Entry(second_frame, width=75)
            answer_e.insert(0,str(record[1]))
            answer_e.configure(state='readonly')
            answer_e.grid(row=r,column=c)
            c = c+1

            level_e = Entry(second_frame,width=8)
            level_e.insert(0,str(record[2]))
            level_e.configure(state='readonly')
            level_e.grid(row=r,column=c)

    # commit changes
    conn_descriptive.commit()

    # close connection
    conn_descriptive.close()


def open_edit():
    edit_window=Toplevel()
    edit_window.title('Edit window')
    edit_window.geometry("1000x495")
    edit_window.resizable(False,False)

    edit_window.grab_set()

    main_frame = LabelFrame(edit_window, text="Question")
    main_frame.grid(row=1, column=0, padx=50)

    secondary_frame = LabelFrame(edit_window, text="Operators")
    secondary_frame.grid(row=1, column=2, rowspan=3, padx=60)

    # the call of invisable frame
    invisable_frame = Frame(edit_window)
    invisable_frame.grid(row=1, column=1, ipadx=80)

    # call on note label
    label_info_edit_window=Label(edit_window,text="NOTE : Please enter an ID number then hit the SELECT button to edit the record by SAVE CHANGES button."+"\n"+"For deleting a record,select its ID then hit DELETE button.")
    label_info_edit_window.grid(row=4 , columnspan=3, pady=40)

    # definition on main frame for edit
    label_question_descriptive = Label(main_frame, text="Question :")
    label_answer_descriptive = Label(main_frame, text="Answer :")
    label_level_descriptive = Label(main_frame, text="Level :")
    drop_menu_level_descriptive = OptionMenu(main_frame, clicked_dmld, "1", "2", "3", "4")
    entry_question_descriptive = Entry(main_frame, width=50, state='disable')
    entry_answer_descriptive = Entry(main_frame, width=50, state='disable')

    # calls on main frame for edit
    label_question_descriptive.grid(row=1, column=1, padx=5, pady=5)
    label_answer_descriptive.grid(row=2, column=1, padx=5, pady=5)
    label_level_descriptive.grid(row=3, column=1, padx=5, pady=5)
    entry_question_descriptive.grid(row=1, column=2, ipadx=10, padx=5, pady=5)
    entry_answer_descriptive.grid(row=2, column=2, ipadx=10, padx=5, pady=5)
    drop_menu_level_descriptive.grid(row=3, column=2, padx=5, pady=5)
    drop_menu_level_descriptive.config(state='disable')

    # definition on secondary frame for descriptive
    id_label = Label(secondary_frame, text="ID : ")
    id_entry = Entry(secondary_frame, width=8)
    id_entry.focus()

    def exit():
        msg=messagebox.askyesno("Exit", "Are you sure you want to exit edit window?")
        if msg==True:
            edit_window.destroy()

    def delete():

        entry_question_descriptive.delete(0, END)
        entry_answer_descriptive.delete(0, END)
        clicked_dmld.set("1")

        entry_question_descriptive.config(state='disable')
        entry_answer_descriptive.config(state='disable')
        drop_menu_level_descriptive.config(state='disable')

        if id_entry.get()=="":
            messagebox.showerror("Error", "Please enter ID number first")

        else:

            result = messagebox.askyesno("Delete a record", "Are you sure you want to delete the selected record?")

            if result == 1:

                # creating databases
                conn_descriptive = sqlite3.connect('descriptive.db')

                # creating cursors
                cursor_descriptive = conn_descriptive.cursor()
                try:
                    #delete query to delete from table
                    cursor_descriptive.execute("DELETE from descriptive WHERE oid = " +id_entry.get())
                    messagebox.showinfo("Done", "Selected record has been deleted!")
                except:
                    messagebox.showerror("Error", "Invalid ID number")


                # select query to update the database box
                cursor_descriptive.execute("SELECT *,oid FROM descriptive")
                records = cursor_descriptive.fetchall()

                if not records:
                    edit_window.focus()
                    messagebox.showerror("Empty Database", "Please enter a record first.")

                else:
                    entry_show_id = Entry(second_frame, width=3)
                    entry_show_question = Entry(second_frame, width=75)
                    entry_show_answer = Entry(second_frame, width=75)
                    entry_show_level = Entry(second_frame, width=8)

                    entry_show_id.insert(0, "ID")
                    entry_show_question.insert(0, "Question")
                    entry_show_answer.insert(0, "Answer")
                    entry_show_level.insert(0, "Level")

                    entry_show_id.configure(state='readonly')
                    entry_show_question.configure(state='readonly')
                    entry_show_answer.configure(state='readonly')
                    entry_show_level.configure(state='readonly')

                    entry_show_id.grid(row=0, column=0, padx=2, pady=2)
                    entry_show_question.grid(row=0, column=1, padx=2, pady=2)
                    entry_show_answer.grid(row=0, column=2, padx=2, pady=2)
                    entry_show_level.grid(row=0, column=3, padx=2, pady=2)

                    r = int
                    c = int
                    r = 0
                    c = 0

                    # print_records=''
                    for record in records:
                        c = 0
                        r = r + 1
                        id_e = Entry(second_frame, width=3)
                        id_e.insert(0, str(record[3]))
                        id_e.configure(state='readonly')
                        id_e.grid(row=r, column=c)
                        c = c + 1

                        question_e = Entry(second_frame, width=75)
                        question_e.insert(0, str(record[0]))
                        question_e.configure(state='readonly')
                        question_e.grid(row=r, column=c)
                        c = c + 1

                        answer_e = Entry(second_frame, width=75)
                        answer_e.insert(0, str(record[1]))
                        answer_e.configure(state='readonly')
                        answer_e.grid(row=r, column=c)
                        c = c + 1

                        level_e = Entry(second_frame, width=8)
                        level_e.insert(0, str(record[2]))
                        level_e.configure(state='readonly')
                        level_e.grid(row=r, column=c)

                # commit changes
                conn_descriptive.commit()

                # close connection
                conn_descriptive.close()

                id_entry.delete(0,END)

    def select():

        if id_entry.get()=="":
            messagebox.showerror("Error", "Please enter ID number first")
            btn_edit_savechanges.config(state='disable')
            btn_edit_remove.config(state='disable')
            entry_question_descriptive.config(state='disable')
            entry_answer_descriptive.config(state='disable')
            drop_menu_level_descriptive.config(state='disable')

        else:
            btn_edit_remove.config(state='normal')
            btn_edit_savechanges.config(state='normal')
            entry_question_descriptive.config(state='normal')
            entry_answer_descriptive.config(state='normal')
            drop_menu_level_descriptive.config(state='normal')


            entry_question_descriptive.delete(0, END)
            entry_answer_descriptive.delete(0,END)
            clicked_dmld.set("1")

            # creating databases
            conn_descriptive = sqlite3.connect('descriptive.db')

            # creating cursors
            cursor_descriptive = conn_descriptive.cursor()




            record_id = id_entry.get()
            cursor_descriptive.execute("SELECT * FROM descriptive WHERE oid = " + record_id)
            records = cursor_descriptive.fetchall()

            for record in records:
                entry_question_descriptive.insert(0, record[0])
                entry_answer_descriptive.insert(0, record[1])
                clicked_dmld.set(record[2])

            del record_id

            # commit changes
            conn_descriptive.commit()

            # close connection
            conn_descriptive.close()

    def update():

        if id_entry.get()=="":
            messagebox.showerror("Error", "Please enter ID number first")

        else:

            # creating databases
            conn_descriptive = sqlite3.connect('descriptive.db')

            # creating cursors
            cursor_descriptive = conn_descriptive.cursor()

            record_id=id_entry.get()

            cursor_descriptive.execute("""UPDATE descriptive SET
                    d_question = :one,
                    d_answer = :two,
                    d_level = :three
                    
                    WHERE oid = :oid""",
                                   {
                                       'one':entry_question_descriptive.get(),
                                       'two':entry_answer_descriptive.get(),
                                       'three':clicked_dmld.get(),
                                       'oid':record_id})

            cursor_descriptive.execute("SELECT *,oid FROM descriptive")
            records = cursor_descriptive.fetchall()

            if not records:
                edit_window.destroy()
                messagebox.showerror("Empty Database", "Please enter a record first.")

            else:
                entry_show_id = Entry(second_frame, width=3)
                entry_show_question = Entry(second_frame, width=75)
                entry_show_answer = Entry(second_frame, width=75)
                entry_show_level = Entry(second_frame, width=8)

                entry_show_id.insert(0, "ID")
                entry_show_question.insert(0, "Question")
                entry_show_answer.insert(0, "Answer")
                entry_show_level.insert(0, "Level")

                entry_show_id.configure(state='readonly')
                entry_show_question.configure(state='readonly')
                entry_show_answer.configure(state='readonly')
                entry_show_level.configure(state='readonly')

                entry_show_id.grid(row=0, column=0, padx=2, pady=2)
                entry_show_question.grid(row=0, column=1, padx=2, pady=2)
                entry_show_answer.grid(row=0, column=2, padx=2, pady=2)
                entry_show_level.grid(row=0, column=3, padx=2, pady=2)

                r = int
                c = int
                r = 0
                c = 0

                # print_records=''
                for record in records:
                    c = 0
                    r = r + 1
                    id_e = Entry(second_frame, width=3)
                    id_e.insert(0, str(record[3]))
                    id_e.configure(state='readonly')
                    id_e.grid(row=r, column=c)
                    c = c + 1

                    question_e = Entry(second_frame, width=75)
                    question_e.insert(0, str(record[0]))
                    question_e.configure(state='readonly')
                    question_e.grid(row=r, column=c)
                    c = c + 1

                    answer_e = Entry(second_frame, width=75)
                    answer_e.insert(0, str(record[1]))
                    answer_e.configure(state='readonly')
                    answer_e.grid(row=r, column=c)
                    c = c + 1

                    level_e = Entry(second_frame, width=8)
                    level_e.insert(0, str(record[2]))
                    level_e.configure(state='readonly')
                    level_e.grid(row=r, column=c)

            # commit changes
            conn_descriptive.commit()

            # close connection
            conn_descriptive.close()

            messagebox.showinfo("Done", "Updated the selected record succesfully!")
            edit_window.grab_set()
            entry_question_descriptive.delete(0,END)
            entry_answer_descriptive.delete(0,END)
            clicked_dmld.set("1")

            btn_edit_savechanges.config(state='disable')
            btn_edit_remove.config(state='disable')
            entry_question_descriptive.config(state='disable')
            entry_answer_descriptive.config(state='disable')
            drop_menu_level_descriptive.config(state='disable')

    # buttons on secondary frame
    btn_edit_select = Button(secondary_frame, text="Select", command=select)
    btn_edit_remove = Button(secondary_frame, text="Delete", command=delete ,state='disable')
    btn_edit_savechanges = Button(secondary_frame, text="Save changes", command=update, state='disable')
    btn_edit_exit = Button(secondary_frame, text="Exit", command=exit)

    # calls on secondary frame for edit
    id_label.grid(row=0, column=1)
    id_entry.grid(row=0, column=2)
    btn_edit_select.grid(row=1, column=0,pady=30)
    btn_edit_remove.grid(row=1, column=1,pady=30)
    btn_edit_savechanges.grid(row=1, column=2,pady=30)
    btn_edit_exit.grid(row=1, column=3,pady=30)

    # create a main frame
    edit_frame = Frame(edit_window)
    edit_frame.grid(row=0,column=0,columnspan=3,sticky=W+E)

    # create a canvas
    edit_canvas = Canvas(edit_frame)
    edit_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    # add scrollbar to canvas
    edit_scrollbar = ttk.Scrollbar(edit_frame, orient=VERTICAL, command=edit_canvas.yview)
    edit_scrollbar.pack(side=RIGHT, fill=Y)

    # configure canvas
    edit_canvas.configure(yscrollcommand=edit_scrollbar.set)
    edit_canvas.bind('<Configure>',
                         lambda e: edit_canvas.configure(scrollregion=edit_canvas.bbox("all")))

    # adding another frame
    second_frame = Frame(edit_canvas)

    # add that new frame to window in canvas
    edit_canvas.create_window((0, 0), window=second_frame, anchor="nw")

    # creating databases
    conn_descriptive = sqlite3.connect('descriptive.db')

    # creating cursors
    cursor_descriptive = conn_descriptive.cursor()

    cursor_descriptive.execute("SELECT *,oid FROM descriptive")
    records = cursor_descriptive.fetchall()

    if not records:
        edit_window.destroy()
        messagebox.showerror("Empty Database", "Please enter a record first.")

    else:
        entry_show_id=Entry(second_frame,width=3 )
        entry_show_question=Entry(second_frame,width=75)
        entry_show_answer=Entry(second_frame,width=75)
        entry_show_level=Entry(second_frame,width=8)

        entry_show_id.insert(0,"ID")
        entry_show_question.insert(0,"Question")
        entry_show_answer.insert(0,"Answer")
        entry_show_level.insert(0,"Level")

        entry_show_id.configure(state='readonly')
        entry_show_question.configure(state='readonly')
        entry_show_answer.configure(state='readonly')
        entry_show_level.configure(state='readonly')

        entry_show_id.grid(row=0,column=0, padx=2 , pady=2)
        entry_show_question.grid(row=0,column=1, padx=2 , pady=2)
        entry_show_answer.grid(row=0,column=2, padx=2 , pady=2)
        entry_show_level.grid(row=0,column=3, padx=2 , pady=2)

        r = int
        c = int
        r = 0
        c = 0

        # print_records=''
        for record in records:
            c = 0
            r = r+1
            id_e=Entry(second_frame,width=3)
            id_e.insert(0,str(record[3]))
            id_e.configure(state='readonly')
            id_e.grid(row=r,column=c)
            c = c+1

            question_e = Entry(second_frame, width=75)
            question_e.insert(0, str(record[0]))
            question_e.configure(state='readonly')
            question_e.grid(row=r,column=c)
            c = c+1

            answer_e = Entry(second_frame, width=75)
            answer_e.insert(0,str(record[1]))
            answer_e.configure(state='readonly')
            answer_e.grid(row=r,column=c)
            c = c+1

            level_e = Entry(second_frame,width=8)
            level_e.insert(0,str(record[2]))
            level_e.configure(state='readonly')
            level_e.grid(row=r,column=c)

    # commit changes
    conn_descriptive.commit()

    # close connection
    conn_descriptive.close()


def add():
    entry_question_descriptive.focus_set()
    if entry_question_descriptive.get()=="" or entry_answer_descriptive.get()=="":
        messagebox.showinfo("Empty boxes!","Please fill question and answer box before hitting the add buutton!")
    else:
        # creating databases
        conn_descriptive = sqlite3.connect('descriptive.db')

        # creating cursors
        cursor_descriptive = conn_descriptive.cursor()

        # insert into Table
        cursor_descriptive.execute("INSERT INTO descriptive VALUES (:a, :b, :c )",
                             {
                                 'a': entry_question_descriptive.get(),
                                 'b': entry_answer_descriptive.get(),
                                 'c': clicked_dmld.get()
                             }
                             )

        # commit changes
        conn_descriptive.commit()

        # close connection
        conn_descriptive.close()

        # Clearing entries
        entry_question_descriptive.delete(0,END)
        entry_answer_descriptive.delete(0,END)
        clicked_dmld.set("1")

        messagebox.showinfo("Add","Question has been added to database succesfully!")


# definition of clearing screen
def clear_btn_click():
    cal_entry.delete(0, END)


# definition of clicking on numbers
def number_click(number):
    current = cal_entry.get()
    cal_entry.delete(0, END)
    cal_entry.insert(0, str(current) + str(number))


# definition of clicking on multiplication operator
def operator_click_mul():
    global first_number
    global operator
    operator="multiplication"
    first_number = str(cal_entry.get())
    cal_entry.delete(0, END)


#definition of clicking on devision operator
def operator_click_dev():
    global first_number
    global operator
    operator="devision"
    first_number = str(cal_entry.get())
    cal_entry.delete(0, END)


# definition of clicking on addition operator
def operator_click_add():
    global first_number
    global operator
    operator="add"
    first_number = str(cal_entry.get())
    cal_entry.delete(0, END)


# definition of clicking on subtraction operator
def operator_click_sub():
    global first_number
    global operator
    operator="sub"
    first_number = str(cal_entry.get())
    cal_entry.delete(0, END)


# definition of error box
def show_error_box():
    messagebox.showerror("Error!", "Invalid Operator\nPlease only enter one operator at a time.")


# definition of button equal
def equal_click():
    global second_number
    second_number = int(cal_entry.get())
    cal_entry.delete(0, END)
    try:
        if operator == "multiplication":
            cal_entry.insert(0, float(first_number) * float(second_number))
        elif operator == "devision":
            cal_entry.insert(0, float(first_number) / float(second_number))
        elif operator == "sub":
            cal_entry.insert(0, float(first_number) - float(second_number))
        elif operator == "add":
            cal_entry.insert(0, float(first_number) + float(second_number))
    except:
        show_error_box()


# definition for open calculator function
def open_calculator():
    # definition of calculator window
    calculator_window=Toplevel()
    calculator_window.title('Calculator')
    calculator_window.geometry("308x315")
    calculator_window.resizable(False,False)
    calculator_window.configure(bg='#BDB1AE')

    # definition and call code for Entry box on calculator
    global cal_entry
    cal_entry = Entry(calculator_window, width=45, borderwidth=10)
    cal_entry.grid(row=0, column=0, columnspan=4, padx=8, pady=10)

    # button definition 0-3
    global btn_0
    global btn_1
    global btn_2
    global btn_3
    btn_0 = Button(calculator_window, text="0" , padx= 30 , pady= 20 , command=lambda :number_click(0))
    btn_1 = Button(calculator_window, text="1" , padx= 30 , pady= 20 , command=lambda :number_click(1))
    btn_2 = Button(calculator_window, text="2" , padx= 30 , pady= 20 , command=lambda :number_click(2))
    btn_3 = Button(calculator_window, text="3" , padx= 30 , pady= 20 , command=lambda :number_click(3))

    # button definition 4-6
    global btn_4
    global btn_5
    global btn_6
    btn_4 = Button(calculator_window, text="4" , padx= 30 , pady= 20, command=lambda :number_click(4))
    btn_5 = Button(calculator_window, text="5" , padx= 30 , pady= 20, command=lambda :number_click(5))
    btn_6 = Button(calculator_window, text="6" , padx= 30 , pady= 20, command=lambda :number_click(6))

    # button definition 7-9
    global btn_7
    global btn_8
    global btn_9
    btn_7 = Button(calculator_window, text="7", padx= 30 , pady= 20, command=lambda :number_click(7))
    btn_8 = Button(calculator_window, text="8" , padx= 30 , pady= 20, command=lambda :number_click(8))
    btn_9 = Button(calculator_window, text="9", padx= 30 , pady= 20, command=lambda :number_click(9))

    # button definition operators
    global btn_clear
    global btn_equal
    global btn_multiplicatiopn
    global btn_devision
    global btn_add
    global btn_sub
    btn_clear = Button(calculator_window, text="Clear", padx=19, pady=20, command=clear_btn_click)
    btn_equal = Button(calculator_window, text="=" , padx= 29 , pady= 20, command=equal_click)
    btn_multiplicatiopn = Button(calculator_window, text="*",padx= 30 , pady= 20, command=operator_click_mul)
    btn_devision= Button(calculator_window, text="/",padx= 30 , pady= 20, command=operator_click_dev)
    btn_add = Button(calculator_window, text="+",padx= 28 , pady= 20, command=operator_click_add)
    btn_sub = Button(calculator_window, text="-",padx= 30 , pady= 20, command=operator_click_sub)

    # button call on calculator window 0-3
    btn_0.grid(row=4, column=1)
    btn_1.grid(row=3, column=0)
    btn_2.grid(row=3, column=1)
    btn_3.grid(row=3, column=2)

    # button call on calculator window 4-6
    btn_4.grid(row=2, column=0)
    btn_5.grid(row=2, column=1)
    btn_6.grid(row=2, column=2)

    # button call on calculator window 7-9
    btn_7.grid(row=1, column=0)
    btn_8.grid(row=1, column=1)
    btn_9.grid(row=1, column=2)

    # button call on calculator operators
    btn_clear.grid(row=4, column=0)
    btn_equal.grid(row=4, column=2)
    btn_multiplicatiopn.grid(row=1, column=3)
    btn_devision.grid(row=2,column=3)
    btn_add.grid(row=3,column=3)
    btn_sub.grid(row=4,column=3)


# for weather API use ###############################################################

global city_name
try:
    city_name = ""
    api_request = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + f"&appid{MY_API_KEY}=&units=metric")
    api = json.loads(api_request.content)
    api_city_name=api['name']
    api_city_condition=api['weather'][0]['main']
    api_city_description=api['weather'][0]['description']
    api_city_temp=api['main']['temp']
    label_buttom = Label(root, text= "City : " + api_city_name + " is " +  api_city_condition +" with "+ api_city_description +"\t" + "Tempature is " +str(api_city_temp) + " C")
except Exception as e:
    label_buttom=Label(root,text="Error... try to load the city again\n make sure intrenet is connected!")


label_buttom.grid(row=6,column=0,pady=5,sticky=W+E)


def open_city():
    city_window = Toplevel()
    city_window.title('Change city')
    city_window.geometry("280x105")
    city_window.resizable(False, False)

    city_window.grab_set()

    def city_save():

        if city_entry.get()=="" :
            messagebox.showinfo("Change city", "Please Enter a city name first")

        else:
            try:
                global city_name
                city_name = ""
                city_name = city_entry.get()
                api_request = requests.get(
                "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + f"&appid={MY_API_KEY}&units=metric")
                api = json.loads(api_request.content)
                api_city_name = api['name']
                api_city_condition = api['weather'][0]['main']
                api_city_description = api['weather'][0]['description']
                api_city_temp = api['main']['temp']

                label_buttom = Label(root,
                                 text="City : " + api_city_name + " is " + api_city_condition + " with " + api_city_description + "\t" + "Tempature is " + str(
                                     api_city_temp) + " C")
                label_buttom.grid(row=6, column=0, pady=5, sticky=W + E)

            except Exception as e:
                label_buttom = Label(root,
                                     text="Error... try to load the city again\n make sure intrenet is connected!")

            city_window.destroy()

    city_label = Label(city_window, text="Enter city name :")
    city_entry = Entry(city_window, width=25)
    city_button = Button(city_window, text="Save", command=city_save)

    city_label.grid(row=0,column=0, pady=20, padx=5 )
    city_entry.grid(row=0,column=1, pady=20)
    city_button.grid(row=1,column=1, padx=(0,100), ipadx=20)

    city_entry.focus()
#######################################################################################


# calculator button on root window

btn_calculator= Button(root, text="Open calculator", command=open_calculator)
btn_calculator.grid(row=5,column=0,padx=(0,300), pady=5)

# city button on root window
btn_city = Button(root,text="Change City", command=open_city)
btn_city.grid(row=5,column=0,padx=(300,0), pady=5)


# add button on main page
btn_menu_add = Button(frame_menu_buttons, text="Add", padx=50, anchor=W, command=add)
btn_menu_add.grid(row=0, column=0)

# show database button on main page
btn_menu_showdatabase = Button(frame_menu_buttons, text="Show database",padx=50, command=open_database)
btn_menu_showdatabase.grid(row=0,column=1)

# edit button on main page
btn_menu_edit = Button(frame_menu_buttons, text="Edit",padx=50,anchor=E, command=open_edit)
btn_menu_edit.grid(row=0,column=2)


root.mainloop()