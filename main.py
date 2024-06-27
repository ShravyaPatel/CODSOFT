import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")

        # Set up the user interface
        self.setup_ui()

        # Load tasks from the database
        self.load_tasks()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=15)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.edit_task_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack(pady=5)

        self.complete_task_button = tk.Button(self.root, text="Complete Task", command=self.complete_task)
        self.complete_task_button.pack(pady=5)

        self.delete_task_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=5)

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT id, title, completed FROM tasks")
        for row in c.fetchall():
            task = f"{row[1]} {'[Completed]' if row[2] else ''}"
            self.task_listbox.insert(tk.END, task)
        conn.close()

    def add_task(self):
        title = simpledialog.askstring("Task Title", "Enter task title:")
        if title:
            description = simpledialog.askstring("Task Description", "Enter task description:")
            priority = simpledialog.askinteger("Task Priority", "Enter task priority (1-5):", minvalue=1, maxvalue=5)
            due_date = simpledialog.askstring("Task Due Date", "Enter task due date (YYYY-MM-DD):")
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute("INSERT INTO tasks (title, description, priority, due_date, completed) VALUES (?, ?, ?, ?, ?)",
                      (title, description, priority, due_date, 0))
            conn.commit()
            conn.close()
            self.load_tasks()

    def edit_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_title = self.task_listbox.get(selected_task_index[0])
            task_id = self.get_task_id(task_title)
            if task_id:
                title = simpledialog.askstring("Edit Task Title", "Edit task title:", initialvalue=task_title)
                if title:
                    description = simpledialog.askstring("Edit Task Description", "Edit task description:")
                    priority = simpledialog.askinteger("Edit Task Priority", "Edit task priority (1-5):", minvalue=1,
                                                       maxvalue=5)
                    due_date = simpledialog.askstring("Edit Task Due Date", "Edit task due date (YYYY-MM-DD):")
                    conn = sqlite3.connect('todo.db')
                    c = conn.cursor()
                    c.execute("UPDATE tasks SET title=?, description=?, priority=?, due_date=? WHERE id=?",
                              (title, description, priority, due_date, task_id))
                    conn.commit()
                    conn.close()
                    self.load_tasks()
            else:
                messagebox.showerror("Error", "Task not found.")

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_title = self.task_listbox.get(selected_task_index[0])
            task_id = self.get_task_id(task_title)
            if task_id:
                conn = sqlite3.connect('todo.db')
                c = conn.cursor()
                c.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
                conn.commit()
                conn.close()
                self.load_tasks()
            else:
                messagebox.showerror("Error", "Task not found.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_title = self.task_listbox.get(selected_task_index[0])
            task_id = self.get_task_id(task_title)
            if task_id:
                conn = sqlite3.connect('todo.db')
                c = conn.cursor()
                c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
                conn.commit()
                conn.close()
                self.load_tasks()
            else:
                messagebox.showerror("Error", "Task not found.")

    def get_task_id(self, task_title):
        # Remove the '[Completed]' part of the task title if it exists
        if " [Completed]" in task_title:
            task_title = task_title.replace(" [Completed]", "")
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT id FROM tasks WHERE title=?", (task_title,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
