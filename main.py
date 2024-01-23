# importing modules
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql


# defining the function to add tasks to the list
def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

# defining the function to update the list
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

# defining the function to delete a task from the list
def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

# function to clear the list
def clear_list():
    task_listbox.delete(0, 'end')


# function to close the application
def close():
    print(tasks)
    guiWindow.destroy()


# function to retrieve data from the database
def retrieve_database():
    while (len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

# main function

if __name__ == "__main__":
    guiWindow = tk.Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("500x450+750+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#e3b21e")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

    header_frame = tk.Frame(guiWindow, bg="#2795f8")
    functions_frame = tk.Frame(guiWindow, bg="#2795f8")
    listbox_frame = tk.Frame(guiWindow, bg="#2795f8")

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(
        header_frame,
        text="The To-Do List",
        font=("Consolas", "35", "bold"),
        background="#2795f8",
        foreground="#110f11"
    )
    header_label.pack(padx=20, pady=20)

    task_label = ttk.Label(
        functions_frame,
        text="Enter your Task:",
        font=("Consolas", "12"),
        background="#cfc2ef",
        foreground="#000000"
    )
    task_label.place(x=30, y=50)

    task_field = ttk.Entry(
        functions_frame,
        font=("Straight", "12"),
        width=18,
        background="#cfc2ef",
        foreground="#A52A2A"
    )
    task_field.place(x=30, y=80)

    add_button = ttk.Button(
        functions_frame,
        text="Add Task",
        width=24,
        command=add_task
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete Task",
        width=24,
        command=delete_task
    )
    exit_button = ttk.Button(
        functions_frame,
        text="Exit",
        width=24,
        command=close
    )
    add_button.place(x=30, y=140)
    del_button.place(x=30, y=180)
    exit_button.place(x=30, y=220)

    task_listbox = tk.Listbox(
        listbox_frame,
        width=32,
        height=15,
        selectmode='SINGLE',
        background="#FFFFFF",
        foreground="#000000",
        selectbackground="#CD853F",
        selectforeground="#FFFFFF"
    )
    task_listbox.place(x=10, y=20)
    retrieve_database()
    list_update()
    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()