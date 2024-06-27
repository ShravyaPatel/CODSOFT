import tkinter as tk
from tkinter import messagebox
from quiz_data import quizzes  # Corrected import statement

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("400x300")  # Set the window size

        # Define styles
        self.title_font = ("Helvetica", 16, "bold")
        self.question_font = ("Helvetica", 14)
        self.option_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12)
        self.bg_color = "#f0f0f0"  # Background color
        self.button_color = "#4CAF50"  # Button color
        self.button_text_color = "#ffffff"  # Button text color

        self.quiz_data = quizzes
        self.current_quiz = None
        self.current_question = 0
        self.score = 0

        self.root.configure(bg=self.bg_color)
        self.create_home_screen()

    def create_home_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Welcome to the Quiz App", font=self.title_font, bg=self.bg_color).pack(pady=20)

        for quiz_name in self.quiz_data.keys():
            tk.Button(
                self.root, text=quiz_name, command=lambda q=quiz_name: self.start_quiz(q),
                font=self.button_font, bg=self.button_color, fg=self.button_text_color
            ).pack(pady=10)

    def start_quiz(self, quiz_name):
        self.current_quiz = quiz_name
        self.current_question = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        self.clear_screen()

        quiz = self.quiz_data[self.current_quiz]
        question_data = quiz[self.current_question]

        tk.Label(self.root, text=question_data["question"], font=self.question_font, bg=self.bg_color).pack(pady=20)

        self.selected_option = tk.StringVar()
        for option in question_data["options"]:
            tk.Radiobutton(
                self.root, text=option, variable=self.selected_option, value=option,
                font=self.option_font, bg=self.bg_color, anchor="w"
            ).pack(anchor="w")

        tk.Button(
            self.root, text="Submit", command=self.submit_answer,
            font=self.button_font, bg=self.button_color, fg=self.button_text_color
        ).pack(pady=20)

    def submit_answer(self):
        selected_answer = self.selected_option.get()
        if not selected_answer:
            messagebox.showwarning("Warning", "Please select an option")
            return

        correct_answer = self.quiz_data[self.current_quiz][self.current_question]["answer"]
        if selected_answer == correct_answer:
            self.score += 1

        self.current_question += 1
        if self.current_question < len(self.quiz_data[self.current_quiz]):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()

        tk.Label(
            self.root, text=f"Quiz Complete! Your Score: {self.score}/{len(self.quiz_data[self.current_quiz])}",
            font=self.question_font, bg=self.bg_color
        ).pack(pady=20)
        tk.Button(
            self.root, text="Return to Home", command=self.create_home_screen,
            font=self.button_font, bg=self.button_color, fg=self.button_text_color
        ).pack(pady=20)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
