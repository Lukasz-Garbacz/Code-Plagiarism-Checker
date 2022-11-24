from curses.ascii import isalpha
import tkinter as tk
from tkinter import ttk
from os.path import exists
import platform
import time
import sys
import copy
from multiprocessing import Process, Queue, Event
from screeninfo import get_monitors

#import other files
from Stack import Stack
from Git import Git
from Progress import Progress
from Report import Report
from Support_windows import Support_windows


# check if entered extention is known and fill other entry entities
def check_extension_label8(extention):

    global extension_git
    global extension_stack
    language_selected = False

    if extention == ".py" or extention == "py" or extention == "python" or extention == "Python":

        label1_entry.delete(0, tk.END)  # variable definitions
        label1_entry.insert(tk.END, "-")

        label2_entry.delete(0, tk.END)  # skipable syntaxes
        label2_entry.insert(
            tk.END, "print import from def [] try except else finally return")

        label3_entry.delete(0, tk.END)  # single line comment
        label3_entry.insert(tk.END, "#")

        label4_entry.delete(0, tk.END)  # multi line comment
        label4_entry.insert(tk.END, "-")

        label5_entry.delete(0, tk.END)  # module definitions
        label5_entry.insert(tk.END, "tab")

        label6_entry.delete(0, tk.END)  # saved addresses
        label6_entry.insert(tk.END, "1")

        label7_entry.delete(0, tk.END)  # checked addresses
        label7_entry.insert(tk.END, "10")

        label9_entry.delete(0, tk.END)  # programming language
        label9_entry.insert(tk.END, "Python")

        extension_git = "py"
        extension_stack = "python"
        language_selected = True

    elif extention == ".c" or extention == "c" or extention == "C" or extention == ".C":

        label1_entry.delete(0, tk.END)  # variable definitions
        label1_entry.insert(tk.END, "char int float double _Bool")

        label2_entry.delete(0, tk.END)  # skipable syntaxes
        label2_entry.insert(tk.END, "#include printf scanf return main() do")

        label3_entry.delete(0, tk.END)  # single line comment
        label3_entry.insert(tk.END, "//")

        label4_entry.delete(0, tk.END)  # multi line comment
        label4_entry.insert(tk.END, "/* */")

        label5_entry.delete(0, tk.END)  # module definitions
        label5_entry.insert(tk.END, "{ }")

        label6_entry.delete(0, tk.END)  # saved addresses
        label6_entry.insert(tk.END, "1")

        label7_entry.delete(0, tk.END)  # checked addresses
        label7_entry.insert(tk.END, "10")

        label9_entry.delete(0, tk.END)  # programming language
        label9_entry.insert(tk.END, "C")

        extension_git = "c"
        extension_stack = "c"
        language_selected = True

    elif extention == ".cpp" or extention == "cpp" or extention == "Cpp" or extention == "c++" or extention == "C++":

        label1_entry.delete(0, tk.END)  # variable definitions
        label1_entry.insert(tk.END, "char int float double string bool")

        label2_entry.delete(0, tk.END)  # skipable syntaxes
        label2_entry.insert(
            tk.END, "#include cout cin return main() do namespace")

        label3_entry.delete(0, tk.END)  # single line comment
        label3_entry.insert(tk.END, "//")

        label4_entry.delete(0, tk.END)  # multi line comment
        label4_entry.insert(tk.END, "/* */")

        label5_entry.delete(0, tk.END)  # module definitions
        label5_entry.insert(tk.END, "{ }")

        label6_entry.delete(0, tk.END)  # saved addresses
        label6_entry.insert(tk.END, "1")

        label7_entry.delete(0, tk.END)  # checked addresses
        label7_entry.insert(tk.END, "10")

        label9_entry.delete(0, tk.END)  # programming language
        label9_entry.insert(tk.END, "C++")

        extension_git = "cpp"
        extension_stack = "c++"
        language_selected = True
        
    elif extention != "":
        extension_git = extention
        extension_stack = extention
        language_selected = True

    if language_selected:
        label_log.config(
            text="Proszę wybrać folder zawierający pliki do sprawdzenia")
    return True


#~~~~~~~~~~~~~~~~~~~~~~~~PERFORM SEARCH~~~~~~~~~~~~~~~~~~~~~~~~~#
def perform_search(variable_definitions, skippable_syntax, single_line_comment, multi_line_comment,
                   module_definitions, saved_addresses_number, checked_addresses_number, extension_git,
                   extension_stack, search_type, treat_files_together):
    code_lines = []
    code_lines_unmodified = []
    code_lines = copy.deepcopy(support.code_lines)
    code_lines_unmodified = copy.deepcopy(support.code_lines)

    # check if entered data is correct
    if multi_line_comment.find(" ") == -1 and multi_line_comment != "-" and multi_line_comment != "":
        label_log.config(text="Błędnie wprowadzony\n komentarz wielolinijkowy")
        return
    if single_line_comment.find(" ") != -1:
        label_log.config(text="Błędnie wprowadzony\n komentarz jednolinijkowy")
        return
    if module_definitions.find(" ") == -1 and module_definitions != "" and module_definitions != "-" and module_definitions != "space" and module_definitions != "spacja" and module_definitions != "tab":
        label_log.config(text="Błędnie wprowadzona\n definicja modułu")
        return
    if saved_addresses_number.isdigit() == False or checked_addresses_number.isdigit() == False:
        label_log.config(text="Błędnie wprowadzona\n liczba adresów")
        return
    if extension_git.find(" ") != -1 or extension_stack.find(" ") != -1:
        label_log.config(text="Błędnie wprowadzone\n rozszerzenia git/stack")
        return

    label10.config(state=tk.DISABLED)
    label11.config(state=tk.DISABLED)
    label12.config(state=tk.DISABLED)
    root.update_idletasks()

    # get login credentials from file
    if exists("login_credentials.txt"):
        with open("login_credentials.txt", 'r') as login_file:
            login_info = login_file.read().splitlines()

            # insert info from file
            if len(login_info) >= 4:
                git_username = login_info[0]
                git_password = support.decode(login_info[1])
                stack_username = login_info[2]
                stack_password = support.decode(login_info[3])
            # if not found use default values
            else:
                label_log.config(
                    text="Brak lub niepoprawny format pliku 'login_credentials.txt'")
                time.sleep(2)
                git_username = git_def_login
                git_password = git_def_password
                stack_username = stack_def_login
                stack_password = stack_def_password

    # get login urls from file
    if exists("login_urls.txt"):
        with open("login_urls.txt", 'r') as login_file:
            login_info = login_file.read().splitlines()

            # insert info from file
            if len(login_info) >= 2:
                git_login_url = login_info[0]
                stack_login_url = login_info[1]
            # if not found use default values
            else:
                label_log.config(
                    text="Brak lub niepoprawny format pliku 'login_urls.txt'")
                time.sleep(2)
                git_login_url = git_def_login_url
                stack_login_url = stack_def_login_url

    # merge files if user selected that option
    if treat_files_together:
        for i in range(1, len(code_lines)):
            code_lines[0].extend(code_lines[i])
        del code_lines[1:]

    # process code lines according to user search specifications
    comment_active = False
    comment_starting_line = False
    skip_strings = []
    skip_variables = []
    defined_variables = []

    # extract data from entry entities input
    if skippable_syntax != "-" and skippable_syntax != "":
        skip_strings = skippable_syntax.split()
    if multi_line_comment != "-" and multi_line_comment != "":
        comment_start, comment_end = multi_line_comment.split(' ', 1)
    if variable_definitions != "-" and variable_definitions != "":
        skip_variables = variable_definitions.split()

    for file_number in range(len(code_lines)):
        for line in range(len(code_lines[file_number])):

            # remove endlines
            code_lines[file_number][line] = code_lines[file_number][line].replace(
                "\n", "")

            # remove single line comments
            if single_line_comment != "-" and single_line_comment != "":
                comment_position = code_lines[file_number][line].rfind(
                    single_line_comment)
                if code_lines[file_number][line].lstrip().find(single_line_comment) == 0 and comment_active == False:
                    code_lines[file_number][line] = ""
                elif comment_position > 0:
                    if code_lines[file_number][line].count("\"", 0, comment_position) % 2 == 0 and code_lines[file_number][line].count("'", 0, comment_position) % 2 == 0 and comment_active == False:
                        code_lines[file_number][line] = code_lines[file_number][line][0:comment_position]

            # remove multi line comments
            if multi_line_comment != "-" and multi_line_comment != "":
                comment_start_position = code_lines[file_number][line].find(
                    comment_start)
                comment_end_position = code_lines[file_number][line].find(
                    comment_end)
                current_line = code_lines[file_number][line]
                # comment beginnings
                if comment_start_position != -1:
                    if current_line.count("\"", 0, comment_start_position) % 2 == 0 and current_line.count("'", 0, comment_start_position) % 2 == 0:
                        comment_active = True
                        comment_starting_line = True
                        code_lines[file_number][line] = code_lines[file_number][line][0:comment_start_position]
                # comment ends
                if comment_end_position != -1:
                    if current_line.count("\"", 0, comment_end_position) % 2 == 0 and current_line.count("'", 0, comment_end_position) % 2 == 0:
                        comment_active = False
                        code_lines[file_number][line] = ""
                if comment_active == True and comment_starting_line == False:
                    code_lines[file_number][line] = ""
                comment_starting_line = False

            # find variable definitions and save variable names
            if variable_definitions != "-" and variable_definitions != "":
                for variable in range(len(skip_variables)):
                    variable_position = code_lines[file_number][line].find(
                        skip_variables[variable])
                    if variable_position != -1:
                        if code_lines[file_number][line][variable_position + len(skip_variables[variable])] == " ":
                            if variable_position == 0 or (variable_position > 0 and code_lines[file_number][line][variable_position - 1] == " "):
                                variable_position = code_lines[file_number][line].find(
                                    " ", variable_position) + 1
                                var_comma = code_lines[file_number][line].find(
                                    ",", variable_position)
                                var_space = code_lines[file_number][line].find(
                                    " ", variable_position)
                                var_semicolon = code_lines[file_number][line].find(
                                    ";", variable_position)
                                var_equal = code_lines[file_number][line].find(
                                    "=", variable_position)
                                if var_comma == -1:
                                    var_comma = sys.maxsize
                                if var_space == -1:
                                    var_space = sys.maxsize
                                if var_semicolon == -1:
                                    var_semicolon = sys.maxsize
                                if var_equal == -1:
                                    var_equal = sys.maxsize
                                var_end = min(var_comma, var_space, var_semicolon, var_equal, len(
                                    code_lines[file_number][line]))
                                if code_lines[file_number][line][variable_position:var_end] not in defined_variables:
                                    defined_variables.append(
                                        code_lines[file_number][line][variable_position:var_end])
            else:
                # find variables defined just by "="
                current_line = code_lines[file_number][line].lstrip()
                variable_name_end = current_line.find("=")
                if variable_name_end != -1:
                    if current_line[variable_name_end-1] == " ":
                        variable_name_end -= 1
                for character in range(0, variable_name_end):
                    if current_line[character].isalpha() == False and current_line[character] != "_":
                        variable_name_end = -1
                        break
                if variable_name_end != -1 and current_line[:variable_name_end] not in defined_variables:
                    defined_variables.append(current_line[:variable_name_end])

    #initialize progress window with event to cancel search
    update_queue = Queue()
    cancel_event = Event()
    s_progress = Progress(cancel_event, update_queue)
    progress_process = Process(target=s_progress.display, args=())
    progress_process.start()
    
    s_stack = Stack(copy.deepcopy(code_lines),copy.deepcopy(defined_variables), update_queue, debug_flag)
    s_git = Git(copy.deepcopy(code_lines), copy.deepcopy(defined_variables), update_queue, debug_flag)

    # perform search
    queue = Queue()
    if search_type:
        git_process = Process(target=s_git.fast_search, args=(git_username, git_password, git_login_url, extension_git, int(
            saved_addresses_number), defined_variables, module_definitions, int(checked_addresses_number), skip_strings, queue,))
        stack_process = Process(target=s_stack.fast_search, args=(stack_username, stack_password, stack_login_url, extension_stack, int(
            saved_addresses_number), defined_variables, module_definitions, int(checked_addresses_number), skip_strings, queue,))

        git_process.start()
        stack_process.start()
        # git_process.join()
        # stack_process.join()

    else:
        git_process = Process(target=s_git.slow_search, args=(git_username, git_password, git_login_url, extension_git, int(
            saved_addresses_number), defined_variables, int(checked_addresses_number), skip_strings, module_definitions, queue, s_progress,))
        stack_process = Process(target=s_stack.slow_search, args=(stack_username, stack_password, stack_login_url, extension_stack, int(
            saved_addresses_number), defined_variables, int(checked_addresses_number), skip_strings, module_definitions, queue,))

        git_process.start()
        stack_process.start()
        # git_process.join()
        # stack_process.join()

    # get results in order depending on which process finished first
    while queue.qsize() < 4:
        if cancel_event.is_set():
            git_process.terminate()
            stack_process.terminate()
            progress_process.terminate()
            
            # unlock buttons
            label10.config(state=tk.NORMAL)
            label11.config(state=tk.NORMAL)
            label12.config(state=tk.NORMAL)
            root.update_idletasks()
            return
    
    #close progress window after search is done
    progress_process.terminate()

    #read git and stack class search output
    for iter in range(0, 4):
        result = queue.get()
        if result[0] == "results_git":
            results_git = result[1]
        elif result[0] == "results_git_html":
            results_git_html = result[1]
        elif result[0] == "results_stack":
            results_stack = result[1]
        elif result[0] == "results_stack_html":
            results_stack_html = result[1]

    # unlock buttons
    label10.config(state=tk.NORMAL)
    label11.config(state=tk.NORMAL)
    label12.config(state=tk.NORMAL)
    label15.config(state=tk.NORMAL)
    root.update_idletasks()

    #place results into report object
    report.update(results_git, results_git_html, results_stack, results_stack_html, code_lines_unmodified)




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if __name__ == '__main__':

    #read settings
    if exists("settings.txt"):
            with open("settings.txt", 'r') as settings_file:
                settings = settings_file.read().splitlines()
    debug_flag = False
    if settings[0] == "DEBUG = True":
        debug_flag = True
    
    # initialize variables
    report = Report(debug_flag)

    # default login credentials
    git_def_login = "whydoineedthiscmon"
    git_def_password = "Defaultcredsantyplagiat123"
    stack_def_login = "defaultcredsantyplagiat@gmail.com"
    stack_def_password = "Defaultcredsantyplagiat123"
    git_def_login_url = "https://github.com/session"
    stack_def_login_url = "https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f"

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~GUI~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    support = Support_windows(git_def_login, git_def_password, stack_def_login, stack_def_password)
    # start tkinter
    root = tk.Tk()
    # setting default attributes
    root.attributes('-fullscreen', False)
    root.title("Antyplagiat")

    # display on primary screen in fullscreen windowed mode
    # monitors = get_monitors()
    # for monitor in range(len(monitors)):
    #     resolution = re.findall('\d+', str(monitors[monitor]))
    #     if resolution[6] == "1":
    #         root.geometry("%dx%d" % (int(resolution[2]), int(resolution[3])))

    root.geometry("%dx%d" % (1400, 800))
    # set program icon
    if platform.system() == "Linux":
        root.iconbitmap("@antip_icon.xbm")
    elif platform.system() == "Windows":
        root.iconbitmap("antip_icon.ico")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~FRAMES~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    root.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8], weight=1, minsize=40)
    root.columnconfigure([0, 1, 2, 3], weight=1, minsize=200)

    frame1 = tk.LabelFrame(master=root, text='Tryb pracy')
    frame1.rowconfigure(0, weight=1)
    frame1.columnconfigure([0, 1], weight=1)

    frame2 = tk.LabelFrame(master=root, text='Traktuj pliki jako jedną całość')
    frame2.rowconfigure(0, weight=1)
    frame2.columnconfigure([0, 1], weight=1)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~LABELS~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # entry labels
    label1 = tk.Label(text="Wyrażenia definiujące zmienne:", bg="white",
                      fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label2 = tk.Label(text="Lista pomijanych syntaxów:", bg="white",
                      fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label3 = tk.Label(text="Oznaczenia komentarzy jednolinijkowych:",
                      bg="white", fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label4 = tk.Label(text="Oznaczenia komentarzy wielolinijkowych:",
                      bg="white", fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label5 = tk.Label(text="Wyrażenia definiujące moduły:", bg="white",
                      fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label6 = tk.Label(text="Liczba zapisywanych stron:", bg="white",
                      fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label7 = tk.Label(text="Liczba sprawdzanych adresów:", bg="white",
                      fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label8 = tk.Label(text="Rozszerzenie sprawdzanych plików:", bg="beige",
                      fg="black", master=root, relief=tk.RAISED, borderwidth=3)
    label9 = tk.Label(text="Język programowania plików:", bg="white",
                      fg="black", master=root, relief=tk.RAISED, borderwidth=3)

    # entry label windows
    label1_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)
    label2_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)
    label3_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)
    label4_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)
    label5_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)
    label6_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)
    label7_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)
    label8_entry = tk.Entry(master=root, bg="beige", fg="black", borderwidth=3,
                            validate='key', validatecommand=(root.register(check_extension_label8), '%P'))
    label9_entry = tk.Entry(master=root, bg="white", fg="black", borderwidth=3)

    # selection button labels
    group_one = tk.IntVar()
    group_two = tk.IntVar()
    label1_select1 = tk.Radiobutton(
        text="Modułowy (szybki)", master=frame1, variable=group_one, value=1)
    label1_select2 = tk.Radiobutton(
        text="Linijkowy (wolny)", master=frame1, variable=group_one, value=0)
    label2_select1 = tk.Radiobutton(
        text="Tak", master=frame2, variable=group_two, value=1)
    label2_select2 = tk.Radiobutton(
        text="Nie", master=frame2, variable=group_two, value=0)

    # interactive buttons
    label10 = tk.Button(text="GitHub & Stackoverflow login", bg="beige", fg="black",
                        master=root, relief=tk.RAISED, borderwidth=4.5, command=lambda:[support.get_login_credentials(root)])
    label11 = tk.Button(text="Wybierz folder do sprawdzenia", bg="beige", fg="black",
                        master=root, relief=tk.RAISED, borderwidth=4.5, command=lambda:[support.select_folder(label_log, label12, extension_git)])

    code_positions_git = []
    code_positions_stack = []
    label12 = tk.Button(text="Wykonaj sprawdzanie", bg="green4", fg="black", master=root, relief=tk.RAISED, borderwidth=6, state=tk.DISABLED,
                        command=lambda: [perform_search(label1_entry.get(), label2_entry.get(), label3_entry.get(),
                                                        label4_entry.get(), label5_entry.get(), label6_entry.get(
                        ), label7_entry.get(), label8_entry.get(),
                            label9_entry.get(), group_one.get(), group_two.get())])

    label13 = tk.Button(text="Instrukcja użytkowania", bg="beige", fg="black",
                        master=root, relief=tk.RAISED, borderwidth=4.5, command=lambda:[support.display_manual(root)])

    label15 = tk.Button(text="Wyświetl raport", bg="goldenrod2", fg="black", master=root,
                        relief=tk.RAISED, borderwidth=4.5, command=lambda: [report.display_report(root)], state=tk.DISABLED)

    # progress bar
    progress_bar = ttk.Progressbar(
        root, orient='horizontal', mode='determinate', length=100, maximum=100)

    # log label
    label_log = tk.Label(text="Proszę najpierw wprowadzić rozszerzenie sprawdzanych plików",
                         fg="black", master=root, borderwidth=1, wraplength=270, justify="left")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~GRID~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    # labels grid
    label1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    label2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    label3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    label4.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
    label5.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
    label6.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
    label7.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
    label8.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
    label9.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
    label10.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")
    label11.grid(row=8, column=1, padx=5, pady=5, sticky="nsew")
    label12.grid(row=4, column=2, padx=5, pady=5,
                 columnspan=2, rowspan=2, sticky="nsew")
    label13.grid(row=6, column=2, padx=5, pady=5, columnspan=2, sticky="nsew")
    label15.grid(row=8, column=3, padx=5, pady=5, sticky="nsew")

    # entry labels grid
    label1_entry.grid(row=0, column=1, padx=5, pady=5,
                      columnspan=3, sticky="nsew")
    label2_entry.grid(row=1, column=1, padx=5, pady=5,
                      columnspan=3, sticky="nsew")
    label3_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    label4_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
    label5_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
    label6_entry.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")
    label7_entry.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")
    label8_entry.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")
    label9_entry.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")

    # selection labels grid
    label1_select1.grid(row=0, column=0, padx=5, pady=5, sticky="nse")
    label1_select2.grid(row=0, column=1, padx=5, pady=5, sticky="nsw")
    label2_select1.grid(row=0, column=0, padx=5, pady=5, sticky="nse")
    label2_select2.grid(row=0, column=1, padx=5, pady=5, sticky="nsw")

    # frames grid
    frame1.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
    frame2.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")

    # progress bar grid
    progress_bar.grid(row=7, column=2, padx=5, pady=5,
                      columnspan=2, sticky="nsew")

    # log label grid
    label_log.grid(row=8, column=2, padx=5, pady=5, sticky="nsew")

    root.mainloop()
