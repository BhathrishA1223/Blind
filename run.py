import tkinter as tk
import subprocess

def run_main():
    subprocess.run(["python", "main.py"])

def run_picture():
    subprocess.run(["python", "picture.py"])

root = tk.Tk()
root.title("Select Script to Run")
root.geometry("300x150")

label = tk.Label(root, text="Click a button to run a script:", font=('Arial', 12))
label.pack(pady=10)

btn_main = tk.Button(root, text="Run main.py", command=run_main, bg="lightblue", font=('Arial', 10, 'bold'))
btn_main.pack(pady=5)

btn_picture = tk.Button(root, text="Run picture.py", command=run_picture, bg="lightgreen", font=('Arial', 10, 'bold'))
btn_picture.pack(pady=5)

root.mainloop()
