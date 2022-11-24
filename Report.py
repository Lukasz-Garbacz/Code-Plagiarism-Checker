import tkinter as tk
import copy
import webbrowser

class Report:
    #attributes
    results_git = None
    results_git_html = None
    results_stack = None
    results_stack_html = None
    code_lines_unmodified = None
    debug_flag = False

    displayed_file = None
    displayed_address = None
    report_box = None
    counter_table_git = None
    counter_table_stack = None
    #updated buttons and labels
    label1 = None
    label2 = None
    label3 = None
    label4 = None
    label5 = None
    label6 = None
    label_count = None
    label2_add = None
    label3_add = None
    label4_add = None
    label5_add = None
    label6_add = None

    #methods
    def update(self, results_git, results_git_html, results_stack, results_stack_html, code_lines_unmodified):
        self.results_git = results_git
        self.results_git_html = results_git_html
        self.results_stack = results_stack
        self.results_stack_html = results_stack_html
        self.code_lines_unmodified = code_lines_unmodified

    def __init__(self, debug_flag):
        self.debug_flag = debug_flag
        
    def display_report(self, root):
        #debug
        if self.debug_flag:
            print("report displayed")

        # initialize report window
        report = tk.Toplevel(root)
        report.attributes('-fullscreen', False)
        report.title("Raport z wyszukiwania")
        report.geometry("%dx%d" % (1200, 800))
        report.rowconfigure([1, 2, 3, 4, 5, 6, 7, 8], weight=1)
        report.columnconfigure([0, 1, 2, 3], weight=1)

        # main text box
        self.report_box = tk.Text(master=report)
        self.report_box.grid(row=0, column=0, padx=5, pady=5,
                        columnspan=4, rowspan=7, sticky="nsew")
        # color tags
        self.report_box.tag_configure("red", background="red")
        self.report_box.tag_configure("green", background="green")
        self.report_box.tag_configure("orange", background="orange")

        self.displayed_file = 0
        self.displayed_address = 0

        # right side button panel frame
        frame1 = tk.LabelFrame(master=report, text='Konfiguracja')
        frame1.rowconfigure([1, 2, 3, 4, 5, 6, 7, 8], minsize=60)
        frame1.columnconfigure(0, minsize=300)
        frame1.grid(row=0, column=4, padx=5, pady=10, rowspan=7, sticky="nsew")

        # statistics secendary frame
        stats_frame = tk.LabelFrame(master=frame1, text='Najpopularniejsze adresy')
        stats_frame.rowconfigure([0, 1, 2, 3, 4, 5], minsize=60)
        stats_frame.columnconfigure(0, minsize=300)
        stats_frame.grid(row=6, column=0, padx=5, pady=10,
                        rowspan=5, sticky="nsew")

        self.label_count = tk.Label(text="", bg="white", fg="black",
                            master=frame1, relief=tk.RAISED, borderwidth=3)
        self.label_count.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # statistics secendary labels
        self.label1 = tk.Label(text="", bg="white", fg="black",
                        master=stats_frame, relief=tk.RAISED, borderwidth=3, width=10)
        self.label2 = tk.Label(text="", bg="white", fg="black",
                        master=stats_frame, relief=tk.RAISED, borderwidth=3, width=10)
        self.label3 = tk.Label(text="", bg="white", fg="black",
                        master=stats_frame, relief=tk.RAISED, borderwidth=3, width=10)
        self.label4 = tk.Label(text="", bg="white", fg="black",
                        master=stats_frame, relief=tk.RAISED, borderwidth=3, width=10)
        self.label5 = tk.Label(text="", bg="white", fg="black",
                        master=stats_frame, relief=tk.RAISED, borderwidth=3, width=10)
        self.label6 = tk.Label(text="", bg="white", fg="black",
                        master=stats_frame, relief=tk.RAISED, borderwidth=3, width=10)

        self.label2_add = tk.Button(text="Otwórz w przeglądarce", bg="beige", fg="black",
                            master=stats_frame, relief=tk.RAISED, borderwidth=4.5, cursor="hand2")
        self.label3_add = tk.Button(text="Otwórz w przeglądarce", bg="beige", fg="black",
                            master=stats_frame, relief=tk.RAISED, borderwidth=4.5, cursor="hand2")
        self.label4_add = tk.Button(text="Otwórz w przeglądarce", bg="beige", fg="black",
                            master=stats_frame, relief=tk.RAISED, borderwidth=4.5, cursor="hand2")
        self.label5_add = tk.Button(text="Otwórz w przeglądarce", bg="beige", fg="black",
                            master=stats_frame, relief=tk.RAISED, borderwidth=4.5, cursor="hand2")
        self.label6_add = tk.Button(text="Otwórz w przeglądarce", bg="beige", fg="black",
                            master=stats_frame, relief=tk.RAISED, borderwidth=4.5, cursor="hand2")

        # statistics secendary labels grid
        self.label1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.label2.grid(row=1, column=0, padx=5, pady=5, sticky="nsw")
        self.label3.grid(row=2, column=0, padx=5, pady=5, sticky="nsw")
        self.label4.grid(row=3, column=0, padx=5, pady=5, sticky="nsw")
        self.label5.grid(row=4, column=0, padx=5, pady=5, sticky="nsw")
        self.label6.grid(row=5, column=0, padx=5, pady=5, sticky="nsw")

        self.label2_add.grid(row=1, column=0, padx=5, pady=5, sticky="nse")
        self.label3_add.grid(row=2, column=0, padx=5, pady=5, sticky="nse")
        self.label4_add.grid(row=3, column=0, padx=5, pady=5, sticky="nse")
        self.label5_add.grid(row=4, column=0, padx=5, pady=5, sticky="nse")
        self.label6_add.grid(row=5, column=0, padx=5, pady=5, sticky="nse")

        # buttons
        website_value = tk.IntVar()
        radio1 = tk.Radiobutton(text="GitHub", master=frame1, variable=website_value, value=0,
                                command=lambda: [self.reprint(0, self.displayed_file, self.displayed_address)])
        radio2 = tk.Radiobutton(text="Stackoverflow", master=frame1, variable=website_value, value=1,
                                command=lambda: [self.reprint(1, self.displayed_file, self.displayed_address)])
        button1 = tk.Button(text="Poprzedni plik", bg="beige", fg="black", master=frame1, relief=tk.RAISED, borderwidth=4.5,
                            command=lambda: [self.reprint(int(website_value.get()), self.displayed_file-1, self.displayed_address)])
        button2 = tk.Button(text="Następny plik", bg="beige", fg="black", master=frame1, relief=tk.RAISED, borderwidth=4.5,
                            command=lambda: [self.reprint(int(website_value.get()), self.displayed_file+1, self.displayed_address)])
        button3 = tk.Button(text="Bardziej popularny adres", bg="beige", fg="black", master=frame1, relief=tk.RAISED, borderwidth=4.5,
                            command=lambda: [self.reprint(int(website_value.get()), self.displayed_file, self.displayed_address-1)])
        button4 = tk.Button(text="Mniej popularny adres", bg="beige", fg="black", master=frame1, relief=tk.RAISED, borderwidth=4.5,
                            command=lambda: [self.reprint(int(website_value.get()), self.displayed_file, self.displayed_address+1)])

        # grid
        radio1.grid(row=1, column=0, padx=5, pady=5, sticky="nsw")
        radio2.grid(row=1, column=0, padx=5, pady=5, sticky="nse")
        button1.grid(row=3, column=0, padx=5, pady=5, sticky="nsw")
        button2.grid(row=3, column=0, padx=5, pady=5, sticky="nse")
        button3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        button4.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        # find addresses with higest plagiarism
        self.counter_table_git = []
        self.counter_table_stack = []

        # count how many lines appear under each address
        # count git addresses
        for file in range(len(self.results_git)):
            self.counter_table_git.append([])
            for address in range(len(self.results_git[file])):
                counter = 0
                for line in range(len(self.results_git[file][address])):
                    if str(self.results_git[file][address][line]) != "-" and str(self.results_git[file][address][line]) != "-1":
                        counter += 1
                self.counter_table_git[file].append(counter)

            # count stack addresses
            self.counter_table_stack.append([])
            for address in range(len(self.results_stack[file])):
                counter = 0
                for line in range(len(self.results_stack[file][address])):
                    if str(self.results_stack[file][address][line]) != "-" and str(self.results_stack[file][address][line]) != "-1":
                        counter += 1
                self.counter_table_stack[file].append(counter)

        # sort counts paired with their indexes to find the highest ones
        for file in range(len(self.results_git)):
            self.counter_table_git[file] = sorted(((value, index) for index, value in enumerate(
                self.counter_table_git[file])), reverse=True)
            self.counter_table_stack[file] = sorted(((value, index) for index, value in enumerate(
                self.counter_table_stack[file])), reverse=True)

        # sort results
        temp_results = copy.deepcopy(self.results_git)
        for file in range(len(self.results_git)):
            if self.results_git[file] != []:
                for line in range(len(self.results_git[file])):
                    self.results_git[file][line] = temp_results[file][self.counter_table_git[file][line][1]]

        temp_results = copy.deepcopy(self.results_stack)
        for file in range(len(self.results_stack)):
            if self.results_stack[file] != []:
                for line in range(len(self.results_stack[file])):
                    self.results_stack[file][line] = temp_results[file][self.counter_table_stack[file][line][1]]

        temp_results = copy.deepcopy(self.results_git_html)
        for file in range(len(self.results_git_html)):
            if self.results_git_html[file] != []:
                for line in range(len(self.results_git_html[file])):
                    self.results_git_html[file][line] = temp_results[file][self.counter_table_git[file][line][1]]

        temp_results = copy.deepcopy(self.results_stack_html)
        for file in range(len(self.results_stack_html)):
            if self.results_stack_html[file] != []:
                for line in range(len(self.results_stack_html[file])):
                    self.results_stack_html[file][line] = temp_results[file][self.counter_table_stack[file][line][1]]

        # display default info upon opening
        self.reprint(0, self.displayed_file,
                self.displayed_address)

    # refresh displayed code and statistics

    def reprint(self, website, file, address):
        #debug
        if self.debug_flag:
            print("reprint called")
        
        #create dictionary with buttons and labels
        stat_labels = [
            self.label1,
            self.label2,
            self.label3,
            self.label4,
            self.label5,
            self.label6,
            self.label_count
        ]
        #if no addresses were found to display, return
        if website == 0 and self.results_git[self.displayed_file] == [] or website == 1 and self.results_stack[self.displayed_file] == []:
            return
        # check if chosen file and address is correct and modify them
        if 0 <= file < len(self.code_lines_unmodified):
            self.displayed_file = file
        if (website == 0 and 0 <= address < len(self.results_git[self.displayed_file])) or (website == 1 and 0 <= address < len(self.results_stack[self.displayed_file])):
            self.displayed_address = address
        elif website == 0 and address >= len(self.results_git[self.displayed_file]):
            self.displayed_address = len(self.results_git[self.displayed_file]) - 1
        elif website == 1 and address >= len(self.results_stack[self.displayed_file]):
            self.displayed_address = len(self.results_stack[self.displayed_file]) - 1

        self.report_box.config(state=tk.NORMAL)
        self.report_box.delete(1.0, tk.END)
        stat_labels[6].config(text="Plik: " + str(self.displayed_file + 1) +
                            "   Adres: " + str(self.displayed_address + 1))

        # check if there is data to display
        if (website == 0 and len(self.results_git) == 0) or (website == 1 and len(self.results_stack) == 0):
            self.report_box.insert(tk.INSERT, "Nie znaleziono żadnych plików")
            return
        elif (website == 0 and len(self.results_git[self.displayed_file]) == 0) or (website == 1 and len(self.results_stack[self.displayed_file]) == 0):
            self.report_box.insert(
                tk.INSERT, "Nie znaleziono żadnych adresów - plagiat 0%, sprawdź ustawienia wyszukiwania")
            return
        # print code and color it
        for line in range(len(self.code_lines_unmodified[self.displayed_file])):
            # if github is selected
            if website == 0:
                if str(self.results_git[self.displayed_file][self.displayed_address][line]) == "-":
                    tag = "orange"
                elif self.results_git[self.displayed_file][self.displayed_address][line] == -1:
                    tag = "green"
                else:
                    tag = "red"
            # if stack is selected
            elif website == 1:
                if str(self.results_stack[self.displayed_file][self.displayed_address][line]) == "-":
                    tag = "orange"
                elif self.results_stack[self.displayed_file][self.displayed_address][line] == -1:
                    tag = "green"
                else:
                    tag = "red"
            self.report_box.insert(
                tk.INSERT, self.code_lines_unmodified[self.displayed_file][line], tag)
        self.report_box.config(state=tk.DISABLED)

        # calculate plagiarism percentage for top 5 addresses
        # count searchable lines
        searchable_lines = 0
        for line in range(len(self.results_git[self.displayed_file][0])):
            if str(self.results_git[self.displayed_file][0][line]) != "-":
                searchable_lines += 1

        percentage_table = []
        # for git
        if website == 0:
            # create empty table with spaces for each line
            for line in range(len(self.results_git[self.displayed_file][0])):
                percentage_table.append([])
            # check results line by line for up to 5 addresses
            for address in range(min(len(self.results_git[self.displayed_file]), 5)):
                for line in range(len(self.results_git[self.displayed_file][address])):
                    # lines skipped
                    if str(self.results_git[self.displayed_file][address][line]) == "-":
                        percentage_table[line] = 0
                    # lines not found
                    elif self.results_git[self.displayed_file][address][line] == -1 and percentage_table[line] != 1:
                        percentage_table[line] = -1
                # lines found
                    else:
                        percentage_table[line] = 1

        # for stack
        if website == 1:
            # create empty table with spaces for each line
            for line in range(len(self.results_stack[self.displayed_file][0])):
                percentage_table.append([])
            # check results line by line for up to 5 addresses
            for address in range(min(len(self.results_stack[self.displayed_file]), 5)):
                for line in range(len(self.results_stack[self.displayed_file][address])):
                    # lines skipped
                    if str(self.results_stack[self.displayed_file][address][line]) == "-":
                        percentage_table[line] = 0
                    # lines not found
                    elif self.results_stack[self.displayed_file][address][line] == -1 and percentage_table[line] != 1:
                        percentage_table[line] = -1
                # lines found
                    else:
                        percentage_table[line] = 1

        # display overall plagiarism percentage
        overall_percentage = percentage_table.count(
            1)/searchable_lines*100
        stat_labels[0].config(
            text="Procent plagiatowanych linijek: " + f"{overall_percentage:.2f}" + "% ")
        if overall_percentage < 25:
            stat_labels[0].config(bg="green")
        elif overall_percentage < 50:
            stat_labels[0].config(bg="orange")
        else:
            stat_labels[0].config(bg="red")

        # display up to top 5 addresses with proper background color
        for label in range(1, 6):
            if label <= len(self.counter_table_git[self.displayed_file]) and website == 0:
                percentage = self.counter_table_git[self.displayed_file][label -1][0]/searchable_lines*100
                if percentage < 25:
                    stat_labels[label].config(
                        text="   " + f"{percentage:.2f}" + "%   ", bg="green")
                elif percentage < 50:
                    stat_labels[label].config(
                        text="   " + f"{percentage:.2f}" + "%   ", bg="orange")
                else:
                    stat_labels[label].config(
                        text="   " + f"{percentage:.2f}" + "%   ", bg="red")
            elif website == 0:
                stat_labels[label].config(text="brak", bg="white")
            elif label <= len(self.counter_table_stack[self.displayed_file]) and website == 1:
                percentage = self.counter_table_stack[self.displayed_file][label -1][0]/searchable_lines*100
                if percentage < 25:
                    stat_labels[label].config(
                        text="   " + f"{percentage:.2f}" + "%   ", bg="green")
                elif percentage < 50:
                    stat_labels[label].config(
                        text="   " + f"{percentage:.2f}" + "%   ", bg="orange")
                else:
                    stat_labels[label].config(
                        text="   " + f"{percentage:.2f}" + "%   ", bg="red")
            elif website == 1:
                stat_labels[label].config(text="brak", bg="white")

        # bind addresses to buttons, manually for each button because command=lambda seems to
        #not work with enums, dictionaries, globals(), lists, etc, it doesn't update
        if website == 0:
            results = self.results_git_html
            address_prefix = "https://github.com/"
        else:
            results = self.results_stack_html
            address_prefix = "https://stackoverflow.com/questions/"

        if (0 < len(self.results_git_html[self.displayed_file]) and website == 0) or (0 < len(self.results_stack_html[self.displayed_file]) and website == 1):
            self.label2_add.config(command=lambda: [webbrowser.open_new(address_prefix + results[self.displayed_file][0])])
            if self.displayed_address == 0:
                self.label2_add.config(relief=tk.RIDGE)
                stat_labels[1].config(relief=tk.RIDGE)
            else:
                self.label2_add.config(relief=tk.RAISED)
                stat_labels[1].config(relief=tk.RAISED)
        else:
            self.label2_add.config(command=lambda: [])

        if (1 < len(self.results_git_html[self.displayed_file]) and website == 0) or (1 < len(self.results_stack_html[self.displayed_file]) and website == 1):
            self.label3_add.config(command=lambda: [webbrowser.open_new(address_prefix + results[self.displayed_file][1])])
            if self.displayed_address == 1:
                self.label3_add.config(relief=tk.RIDGE)
                stat_labels[2].config(relief=tk.RIDGE)
            else:
                self.label3_add.config(relief=tk.RAISED)
                stat_labels[2].config(relief=tk.RAISED)
        else:
            self.label3_add.config(command=lambda: [])

        if (2 < len(self.results_git_html[self.displayed_file]) and website == 0) or (2 < len(self.results_stack_html[self.displayed_file]) and website == 1):
            self.label4_add.config(command=lambda: [webbrowser.open_new(address_prefix + results[self.displayed_file][2])])
            if self.displayed_address == 2:
                self.label4_add.config(relief=tk.RIDGE)
                stat_labels[3].config(relief=tk.RIDGE)
            else:
                self.label4_add.config(relief=tk.RAISED)
                stat_labels[3].config(relief=tk.RAISED)
        else:
            self.label4_add.config(command=lambda: [])

        if (3 < len(self.results_git_html[self.displayed_file]) and website == 0) or (3 < len(self.results_stack_html[self.displayed_file]) and website == 1):
            self.label5_add.config(command=lambda: [webbrowser.open_new(address_prefix + results[self.displayed_file][3])])
            if self.displayed_address == 3:
                self.label5_add.config(relief=tk.RIDGE)
                stat_labels[4].config(relief=tk.RIDGE)
            else:
                self.label5_add.config(relief=tk.RAISED)
                stat_labels[4].config(relief=tk.RAISED)
        else:
            self.label5_add.config(command=lambda: [])

        if (4 < len(self.results_git_html[self.displayed_file]) and website == 0) or (4 < len(self.results_stack_html[self.displayed_file]) and website == 1):
            self.label6_add.config(command=lambda: [webbrowser.open_new(address_prefix + results[self.displayed_file][4])])
            if self.displayed_address == 4:
                self.label6_add.config(relief=tk.RIDGE)
                stat_labels[5].config(relief=tk.RIDGE)
            else:
                self.label6_add.config(relief=tk.RAISED)
                stat_labels[5].config(relief=tk.RAISED)
        else:
            self.label6_add.config(command=lambda: [])