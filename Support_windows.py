import tkinter as tk
from tkinter import filedialog
import glob
from os.path import exists
import base64

class Support_windows:

    #attributes
    code_lines = None

    # default login credentials
    git_def_login = None
    git_def_password = None
    stack_def_login = None
    stack_def_password = None

    #methods
    def __init__(self, git_def_login, git_def_password, stack_def_login, stack_def_password):
        self.git_def_login = git_def_login
        self.git_def_password = git_def_password
        self.stack_def_login = stack_def_login
        self.stack_def_password = stack_def_password
        
        
    # vigenere encoding with constant key
    def encode(self, clear):
        key = "/A?D(G+KbPeShVkYp3s6v9y$B&E)H@McQfTjWnZq4t7w!z%C*F-JaNdRgUkXp2s5"
        enc = []
        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode()).decode()


    # vigenere decoding with constant key
    def decode(self, enc):
        key = "/A?D(G+KbPeShVkYp3s6v9y$B&E)H@McQfTjWnZq4t7w!z%C*F-JaNdRgUkXp2s5"
        dec = []
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = key[i % len(key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)


    # select folder with files to check
    def select_folder(self, label_log, label12, extension_git):
        # select directory
        files_path = filedialog.askdirectory(mustexist=True)
        self.code_lines = []

        print(files_path)
        if files_path != ():
            if files_path != "":
                # read all files in directory
                files_to_read = glob.glob(files_path + "/*." + extension_git)
                for i in range(len(files_to_read)):
                    with open(files_to_read[i], 'r') as file_i:
                        self.code_lines.append(file_i.readlines())

        if len(self.code_lines) > 0:
            label_log.config(text="Znalezione pliki: " + str(len(self.code_lines)
                                                            ) + "\nprogram gotowy do wykonania sprawdzania")
            label12.config(state=tk.NORMAL)
        else:
            label_log.config(
                text="Nie znaleziono plików o wybranym rozszerzeniu, zmień rozszerzenie lub wybierz inny folder")
            label12.config(state=tk.DISABLED)
        print("Files read")


    # enter git and stack login credentials or check existing ones
    def get_login_credentials(self, root):

        # initialize login window
        login = tk.Toplevel(root)
        login.attributes('-fullscreen', False)
        login.title("Parametry Logowania")
        login.geometry("%dx%d" % (600, 300))
        login.rowconfigure([0, 1, 2, 3, 4], weight=1, minsize=40)
        login.columnconfigure([0, 1], weight=1, minsize=200)

        # entry labels
        label1_login = tk.Label(text="GitHub login:", bg="white",
                                fg="black", master=login, relief=tk.RAISED, borderwidth=3)
        label2_login = tk.Label(text="GitHub hasło:", bg="white",
                                fg="black", master=login, relief=tk.RAISED, borderwidth=3)
        label3_login = tk.Label(text="Stackoverflow login:", bg="white",
                                fg="black", master=login, relief=tk.RAISED, borderwidth=3)
        label4_login = tk.Label(text="Stackoverflow hasło:", bg="white",
                                fg="black", master=login, relief=tk.RAISED, borderwidth=3)

        label5_insert = tk.Button(text="Wstaw dane domyślne", bg="orange", fg="black", master=login, relief=tk.RAISED, borderwidth=5,
                                command=lambda: [label1_login_entry.delete(0, tk.END), label1_login_entry.insert(tk.END, self.git_def_login),
                                                label2_login_entry.delete(0, tk.END), label2_login_entry.insert(
                                    tk.END, self.git_def_password),
                                    label3_login_entry.delete(0, tk.END), label3_login_entry.insert(
                                    tk.END, self.stack_def_login),
                                    label4_login_entry.delete(0, tk.END), label4_login_entry.insert(tk.END, self.stack_def_password)])

        label6_accept = tk.Button(text="Zapisz", bg="green", fg="black", master=login, relief=tk.RAISED, borderwidth=5,
                                command=lambda: [self.save_login_credentials(label1_login_entry.get(), label2_login_entry.get(),
                                                                        label3_login_entry.get(), label4_login_entry.get()), login.destroy()])

        # entry label windows
        label1_login_entry = tk.Entry(
            master=login, bg="white", fg="black", borderwidth=3)
        label2_login_entry = tk.Entry(
            master=login, bg="white", fg="black", borderwidth=3, show="\u2022")
        label3_login_entry = tk.Entry(
            master=login, bg="white", fg="black", borderwidth=3)
        label4_login_entry = tk.Entry(
            master=login, bg="white", fg="black", borderwidth=3, show="\u2022")

        # read login info from file
        if exists("login_credentials.txt"):
            with open("login_credentials.txt", 'r') as login_file:
                login_info = login_file.read().splitlines()

                # insert info from file
                if len(login_info) >= 4:
                    label1_login_entry.insert(tk.END, login_info[0])
                    label2_login_entry.insert(tk.END, self.decode(login_info[1]))
                    label3_login_entry.insert(tk.END, login_info[2])
                    label4_login_entry.insert(tk.END, self.decode(login_info[3]))

        # labels grid
        label1_login.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        label2_login.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        label3_login.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        label4_login.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        label5_insert.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        label6_accept.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        # entry labels grid
        label1_login_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        label2_login_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        label3_login_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        label4_login_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")


    def save_login_credentials(self, git_login, git_password, stack_login, stack_password):
        with open('login_credentials.txt', 'w') as the_file:
            the_file.write(git_login + "\n" + self.encode(git_password) +
                        "\n" + stack_login + "\n" + self.encode(stack_password))
        print("login credentials saved")

    # open new window with program manual
    def display_manual(self, root):
        if exists("manual.txt"):

            # initialize manual window
            manual = tk.Toplevel(root)
            manual.attributes('-fullscreen', False)
            manual.title("Instrukcja użytkowania")
            manual.geometry("%dx%d" % (1200, 800))

            # read manual from file and display it
            with open("manual.txt", 'r') as manual_file:
                manual_text = manual_file.read()
                manual_box = tk.Text(manual, wrap=tk.WORD, width=1200, height=800)
                manual_box.insert(tk.INSERT, manual_text)
                manual_box.config(state=tk.DISABLED)
                manual_box.pack()
        else:
            tk.messagebox.showerror(
                title="Brak instrukcji", message="Nie znaleziono pliku 'manual.txt' zawierającego instrukcję użytkowania")