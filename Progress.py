import tkinter as tk
from tkinter import ttk

class Progress:
    #attributes
    cancel_event = None
    progress_bar_git = None
    progress_bar_stack = None
    git_label = None
    stack_label = None
    update_queue = None

    def __init__(self, cancel_event, update_queue):
        self.cancel_event = cancel_event
        self.update_queue = update_queue

    #update git progress bar and label
    def update_git(self, git_text, bar_value):
        self.git_label.config(text = git_text)
        self.progress_bar_git['value'] = bar_value
    
    #update stack progress bar and label
    def update_stack(self, stack_text, bar_value):
        self.stack_label.config(text = stack_text)
        self.progress_bar_stack['value'] = bar_value

    def display(self):
        print("display called")
        window = tk.Tk()
        window.attributes('-fullscreen', False)
        window.title("Postęp")
        window.geometry("%dx%d" % (600, 210))
        window.rowconfigure([0, 1, 2], weight=1, minsize=70)
        window.columnconfigure([0, 1, 2], weight=1, minsize=200)

        self.progress_bar_git = ttk.Progressbar(
            window, orient='horizontal', mode='determinate', length=100, maximum=100)
        self.progress_bar_stack = ttk.Progressbar(
            window, orient='horizontal', mode='determinate', length=100, maximum=100)

        button1 = tk.Button(text="Anuluj przeszukiwanie", bg="red", fg="black",
                    master=window, relief=tk.RAISED, borderwidth=4.5, command=lambda: [self.cancel_event.set()])
        self.git_label = tk.Label(text="github.com", bg="beige", fg="black",
                    master=window, relief=tk.RAISED, borderwidth=4.5)
        self.stack_label = tk.Label(text="stackoverflow.com", bg="beige", fg="black",
                    master=window, relief=tk.RAISED, borderwidth=4.5)

        button1.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        self.git_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.stack_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.progress_bar_git.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky="nsew")
        self.progress_bar_stack.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="nsew")

        #mainloop
        while True:
            #update progress bar if new update is in queue
            update_string = ""
            update_value = 0
            if self.update_queue.qsize() > 0:
                (update_string, update_value) = self.update_queue.get()
            if update_string[:3] == "git":
                self.update_git(update_string, update_value)
            elif update_string[:3] == "sta":
                self.update_stack(update_string, update_value)

            #update progress window
            window.update_idletasks()
            window.update()