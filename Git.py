import requests as r
from bs4 import BeautifulSoup as bs
import urllib.parse
import math
import collections
import fnmatch as fn
import time

class Git:

    # attributes
    code_lines = []
    defined_variables = []
    addresses_git = []
    var_positions = []
    update_queue = None
    debug_flag = False

    # default login credentials
    git_def_login = "whydoineedthiscmon"
    git_def_password = "Defaultcredsantyplagiat123"
    git_def_login_url = "https://github.com/session"

    # methods
    def __init__(self, code_lines, defined_variables, update_queue, debug_flag):
        self.code_lines = code_lines
        self.defined_variables = defined_variables
        self.update_queue = update_queue
        self.debug_flag = debug_flag

    def slow_search(self, git_username, git_password, git_login_url, extension_git, number_of_results, defined_variables, checked_addresses_number, skip_strings, module_definitions, queue, progress):
        # get module definition from string
        space_location = module_definitions.find(" ")
        if space_location > 0:
            module_begin = module_definitions[:space_location]
            module_end = module_definitions[space_location+1:]
        else:
            module_begin = module_definitions
            module_end = ""
        if module_begin == "tab":
            module_begin = "    "
        elif module_begin == "space" or module_begin == "spacja":
            module_begin = " "

        #get code size for progress bar
        code_size = 0
        current_line = 1
        for file in range(len(self.code_lines)):
            code_size += len(self.code_lines[file])
        
        with r.session() as git_search:

            #debug
            if self.debug_flag:
                print("Started:    slow search [GIT]")
                search_time_start = time.time()
            # log in into github
            login_page = git_search.get(git_login_url).text
            login_page_html = bs(login_page, features="html.parser")
            token = login_page_html.find(
                "input", {"name": "authenticity_token"}).attrs['value']
            commit_value = login_page_html.find(
                "input", {"name": "commit"}).attrs['value']
            login_data = {"login": git_username,
                          "password": git_password,
                          "commit": commit_value,
                          "authenticity_token": token}
            git_search.post(git_login_url, data=login_data)

            # git search all files line by line
            for file_number in range(len(self.code_lines)):

                #debug
                if self.debug_flag:
                    print("Started:    line searching, file number: " +
                        str(file_number) + " [GIT]")
                self.addresses_git.append([])
                self.var_positions.append([])
                
                for line in range(len(self.code_lines[file_number])):

                    self.addresses_git[file_number].append([])
                    self.var_positions[file_number].append([])

                    code_url = ""
                    previous_var = 0

                    #update progress window
                    update_string = "github.com (1/3)\n" + str(current_line) + "/" + str(code_size)
                    update_value = math.ceil(current_line/code_size*100)
                    self.update_queue.put((update_string, update_value))

                    # skip lines including skippable syntax
                    for word in range(len(skip_strings)):
                        if self.code_lines[file_number][line].find(skip_strings[word]) != -1:
                            self.code_lines[file_number][line] = ""
                    if self.code_lines[file_number][line] == module_begin or self.code_lines[file_number][line] == module_end:
                        self.code_lines[file_number][line] = ""

                    if self.code_lines[file_number][line] != "":
                        var_position = 0

                        # find variables that arent part of larger sentence and replace them with '+' in url
                        for variable in defined_variables:
                            while self.code_lines[file_number][line].find(variable, var_position) != -1:
                                var_position = self.code_lines[file_number][line].find(
                                    variable, var_position) + 1
                                # make sure it doesnt go out of bounds
                                if var_position-2 >= 0 and var_position + len(variable) <= len(self.code_lines[file_number][line]):
                                    if (self.code_lines[file_number][line][var_position-2].isalpha() == False and self.code_lines[file_number][line][var_position-2] != '_'):
                                        if (self.code_lines[file_number][line][var_position + len(variable)-1].isalpha() == False):
                                            self.code_lines[file_number][line] = self.code_lines[file_number][line][:var_position -1] + self.code_lines[file_number][line][var_position + len(variable) - 1:]
                                            self.var_positions[file_number][line].append(var_position-1)

                        for var_insert in self.var_positions[file_number][line]:
                            code_url += urllib.parse.quote(
                                self.code_lines[file_number][line][previous_var:var_insert].encode('utf8')) + "+"
                            previous_var = var_insert
                        code_url += urllib.parse.quote(
                            self.code_lines[file_number][line][previous_var:].encode('utf8'))

                        # get rid of multiple spaces next to each other
                        while code_url.find("%20%20") != -1:
                            space_pos = code_url.find("%20%20")
                            code_url = code_url[:space_pos] + \
                                code_url[space_pos+3:]
                        for result_page in range(1, math.ceil(number_of_results) + 1):
                            # create URL, replace white spaces with '+' and convert special characters to utf8
                            git_search_url = "https://github.com/search?p=" + \
                                str(result_page) + "&q=\"" + code_url + \
                                "\"+extension%3A" + extension_git + "&type=Code"

                            # get URLs data from html (OPTIMIZE LATER)
                            data = git_search.get(git_search_url).text

                            #limit search speed to not exceed limits
                            time.sleep(2)
                            sleep_timer = 5
                            
                            while data.find("You have exceeded a secondary rate limit") != -1 or data.find("Human verification") != -1:
                                time.sleep(sleep_timer)
                                sleep_timer += 5
                                data = git_search.get(git_search_url).text

                            for adres_begin in self.find_urls(";https://github.com/", data):
                                adres_end = data.find("&", adres_begin)

                                # dont save utility addresses
                                if data[adres_begin+20:adres_begin+27] != "search?":
                                    self.addresses_git[file_number][line].append(
                                        data[adres_begin+20:adres_end])
                        # else:
                        #     self.addresses_git[file_number][line].append("-")
                    
                    current_line += 1
            results_git = []
            merged_list_git = []

            # put all addresses into one list to count
            for file_number in range(len(self.addresses_git)):
                for line in range(len(self.addresses_git[file_number])):
                    merged_list_git.extend(
                        self.addresses_git[file_number][line])

            # find most common addresses in each file
                results_git.append([])
                counter_list = collections.Counter(
                    merged_list_git).most_common(checked_addresses_number)
                for line in range(len(counter_list)):
                    results_git[file_number].append(counter_list[line][0])

            result_html = []
            result_code = []

            #debug
            if self.debug_flag:
                print("Started:    getting resulted websites [GIT]")
                search_time_mid = time.time()

            #reset progress parameters
            code_size = 0
            current_line = 1
            for file in range(len(results_git)):
                code_size += len(results_git[file])

            # search all files line by line
            for file in range(len(results_git)):
                result_html.append([])
                for address in results_git[file]:
                    # create URL
                    if address != "" and address != "-":
                        #create address to raw github code
                        git_search_url = "https://github.com/" + address.replace("blob", "raw")
                        git_code = git_search.get(git_search_url).text
                        
                        #limit search speed to not exceed limits
                        time.sleep(2)

                        #update progress window
                        update_string = "github.com (2/3)\n" + str(current_line) + "/" + str(code_size)
                        update_value = math.ceil(current_line/code_size*100)
                        self.update_queue.put((update_string, update_value))

                        sleep_timer = 5
                        while git_code.find("You have exceeded a secondary rate limit") != -1 or git_code.find("Human verification") != -1:
                            time.sleep(sleep_timer)
                            sleep_timer += 5
                            git_code = git_search.get(git_search_url).text

                        result_html[file].append(git_code)

                    current_line += 1
        #debug
        if self.debug_flag:
            search_time_end = time.time()
        result_code = self.search_html(result_html)
        
        #put results into queue
        queue.put(("results_git", result_code))
        queue.put(("results_git_html", results_git))

        #debug
        if self.debug_flag:
            search_time_finished = time.time()
            print("Finished:   slow search [GIT]")
            print("Time of line searching [GIT]: " + str(search_time_mid - search_time_start))
            print("Time of getting addresses [GIT]: " + str(search_time_end - search_time_mid))
            print("Time of searching addresses [GIT]: " + str(search_time_finished - search_time_end))
            print("Time elapsed in total [GIT]: " + str(search_time_finished - search_time_start))

        return

    def fast_search(self, git_username, git_password, git_login_url, extension_git, number_of_results, defined_variables, module_definitions, checked_addresses_number, skip_strings, queue):

        with r.session() as git_search:
            #debug
            if self.debug_flag:
                print("Started:    fast search [GIT]")
                search_time_start = time.time()

            # log in into github
            login_page = git_search.get(git_login_url).text
            login_page_html = bs(login_page, features="html.parser")
            token = login_page_html.find(
                "input", {"name": "authenticity_token"}).attrs['value']
            commit_value = login_page_html.find(
                "input", {"name": "commit"}).attrs['value']
            login_data = {"login": git_username,
                          "password": git_password,
                          "commit": commit_value,
                          "authenticity_token": token}
            git_search.post(git_login_url, data=login_data)

            # get module definition from string
            space_location = module_definitions.find(" ")
            if space_location > 0:
                module_begin = module_definitions[:space_location]
                module_end = module_definitions[space_location+1:]
            else:
                module_begin = module_definitions
                module_end = ""
            if module_begin == "tab":
                module_begin = "    "
            elif module_begin == "space" or module_begin == "spacja":
                module_begin = " "

            temp_variable_pos = []
            # go through the file and replace variables
            for file_number in range(len(self.code_lines)):

                #debug
                if self.debug_flag:
                    print("Started:    module searching, file number: " +
                        str(file_number) + " [GIT]")

                temp_variable_pos.append([])
                self.addresses_git.append([])
                # module searching
                module_count = 1
                module_begin_pos = []
                module_end_pos = []
                # search line by line for module beginnings
                for line in range(len(self.code_lines[file_number])):
                    # stop if max module number has been reached
                    if len(module_end_pos) >= number_of_results*50:
                        break
                    # module beginning found
                    if self.code_lines[file_number][line].find(module_begin) != -1:
                        if module_begin[0] == " ":
                            if self.code_lines[file_number][line].startswith(module_begin*module_count):
                                module_begin_pos.append(line)
                                module_end_pos.append([])
                                module_count += 1
                        else:
                            module_begin_pos.append(line)
                            module_end_pos.append([])
                            module_count += 1

                    # module ending found
                    if module_begin[0] == " " and len(module_end_pos) > 0 and line > 0:
                        spaces_in_current_line = len(
                            self.code_lines[file_number][line]) - len(self.code_lines[file_number][line].lstrip())
                        spaces_in_previous_line = len(
                            self.code_lines[file_number][line-1]) - len(self.code_lines[file_number][line-1].lstrip())
                        if spaces_in_current_line < spaces_in_previous_line:
                            number_of_endings = math.floor(
                                (spaces_in_previous_line - spaces_in_current_line)/len(module_begin))
                            for ending in range(0, number_of_endings):
                                # end fits the last beginning (last empty element of module_end_pos)
                                pos = 0
                                for empty in range(len(module_end_pos)):
                                    if module_end_pos[empty] == []:
                                        pos = empty
                                #pos = len(module_end_pos) - 1 - module_end_pos[::-1].index([])
                                module_end_pos[pos] = line
                                module_count -= 1
                    elif self.code_lines[file_number][line].find(module_end) != -1 and len(module_end_pos) > 0:
                        # end fits the last beginning (last empty element of module_end_pos)
                        pos = 0
                        for empty in range(len(module_end_pos)):
                            if module_end_pos[empty] == []:
                                pos = empty
                        module_end_pos[pos] = line
                        module_count -= 1

                # get max length lines from each module to search
                lines_to_search = []

                for module in range(len(module_end_pos)):
                    # if module end not found set it to the last line
                    if module_end_pos[module] == []:
                        module_end_pos[module] = len(
                            self.code_lines[file_number]) - 1
                    code_line = ""
                    for line in range(module_begin_pos[module], module_end_pos[module]):
                        code_line += self.code_lines[file_number][line]
                    # truncate line to max length
                    code_line = code_line[:255]
                    code_line = code_line.rstrip()
                    code_line = code_line.lstrip()
                    code_line = code_line.replace("\n", "")
                    if module_begin != " ":
                        code_line = code_line.replace(module_begin, "")
                        code_line = code_line.replace(module_end, "")
                    lines_to_search.append(code_line)

                for line in range(len(lines_to_search)):

                    self.addresses_git[file_number].append([])
                    temp_variable_pos[file_number].append([])
                    code_url = ""
                    previous_var = 0

                    #update progress window
                    update_string = "github.com (1/3)\n" + str(line+1) + "/" + str(len(lines_to_search)) + " file: " + str(file_number+1) + "/" +str(len(self.code_lines))
                    update_value = math.ceil((line+1)/len(lines_to_search)*100)
                    self.update_queue.put((update_string, update_value))

                    if lines_to_search[line] != "":
                        var_position = 0

                        # find variables that arent part of larger sentence and replace them with '+' in url
                        for variable in defined_variables:
                            while lines_to_search[line].find(variable, var_position) != -1:
                                var_position = lines_to_search[line].find(
                                    variable, var_position) + 1
                                # make sure it doesnt go out of bounds
                                if var_position-2 >= 0 and var_position + len(variable) <= len(lines_to_search[line]):
                                    if (lines_to_search[line][var_position-2].isalpha() == False and lines_to_search[line][var_position-2] != '_'):
                                        if (lines_to_search[line][var_position + len(variable)-1].isalpha() == False):
                                            lines_to_search[line] = lines_to_search[line][:var_position -1] + lines_to_search[line][var_position + len(variable) - 1:]
                                            temp_variable_pos[file_number][line].append(var_position-1)
                        for var_insert in temp_variable_pos[file_number][line]:
                            code_url += urllib.parse.quote(
                                lines_to_search[line][previous_var:var_insert].encode('utf8')) + "+"
                            previous_var = var_insert
                        code_url += urllib.parse.quote(
                            lines_to_search[line][previous_var:].encode('utf8'))

                        # get rid of multiple spaces next to each other
                        while code_url.find("%20%20") != -1:
                            space_pos = code_url.find("%20%20")
                            code_url = code_url[:space_pos] + \
                                code_url[space_pos+3:]
                        for result_page in range(1, math.ceil(number_of_results) + 1):
                            # create URL, replace white spaces with '+' and convert special characters to utf8
                            git_search_url = "https://github.com/search?p=" + \
                                str(result_page) + "&q=\"" + code_url + \
                                "\"+extension%3A" + extension_git + "&type=Code"
                            # get URLs data from html (OPTIMIZE LATER)
                            data = git_search.get(git_search_url).text

                            #limit search speed to not exceed limits
                            time.sleep(2)
                            sleep_timer = 5
                            while data.find("You have exceeded a secondary rate limit") != -1 or data.find("Human verification") != -1:
                                time.sleep(sleep_timer)
                                sleep_timer += 5
                                data = git_search.get(git_search_url).text

                            for adres_begin in self.find_urls(";https://github.com/", data):
                                adres_end = data.find("&", adres_begin)

                                # dont save utility addresses
                                if data[adres_begin+20:adres_begin+27] != "search?":
                                    self.addresses_git[file_number][line].append(
                                        data[adres_begin+20:adres_end])

            # find variables that arent part of larger sentence and replace them with '"+"' in code_lines
            for file_number in range(len(self.code_lines)):
                self.var_positions.append([])
                for line in range(len(self.code_lines[file_number])):
                    self.var_positions[file_number].append([])

                    previous_var = 0
                    if self.code_lines[file_number][line] != "":
                        var_position = 0

                        for variable in defined_variables:
                            while self.code_lines[file_number][line].find(variable, var_position) != -1:
                                var_position = self.code_lines[file_number][line].find(
                                    variable, var_position) + 1
                                # make sure it doesnt go out of bounds
                                if var_position-2 >= 0 and var_position + len(variable) <= len(self.code_lines[file_number][line]):
                                    if (self.code_lines[file_number][line][var_position-2].isalpha() == False and self.code_lines[file_number][line][var_position-2] != '_'):
                                        if (self.code_lines[file_number][line][var_position + len(variable)-1].isalpha() == False):
                                            self.code_lines[file_number][line] = self.code_lines[file_number][line][:var_position -1] + self.code_lines[file_number][line][var_position + len(variable) - 1:]
                                            self.var_positions[file_number][line].append(var_position-1)

            results_git = []
            merged_list_git = []

            # put all addresses into one list to count
            for file_number in range(len(self.addresses_git)):
                for line in range(len(self.addresses_git[file_number])):
                    merged_list_git.extend(
                        self.addresses_git[file_number][line])

            
            # find most common addresses in each file
                results_git.append([])
                counter_list = collections.Counter(
                    merged_list_git).most_common(checked_addresses_number)
                for line in range(len(counter_list)):
                    results_git[file_number].append(counter_list[line][0])

            result_html = []
            result_code = []

            #debug
            if self.debug_flag:
                print("Started:    getting resulted websites [GIT]")
                search_time_mid = time.time()

            #reset progress parameters
            code_size = 0
            current_line = 1
            for file in range(len(results_git)):
                code_size += len(results_git[file])

            # get most commonly repeating websites
            for file in range(len(results_git)):
                result_html.append([])
                for address in results_git[file]:
                    # create URL
                    if address != "" and address != "-":
                        #create address to raw github code
                        git_search_url = "https://github.com/" + address.replace("blob", "raw")
                        git_code = git_search.get(git_search_url).text

                        #limit search speed to not exceed limits
                        time.sleep(2)

                        #update progress window
                        update_string = "github.com (2/3)\n" + str(current_line) + "/" + str(code_size)
                        update_value = math.ceil(current_line/code_size*100)
                        self.update_queue.put((update_string, update_value))

                        sleep_timer = 5
                        while git_code.find("You have exceeded a secondary rate limit") != -1 or git_code.find("Human verification") != -1:
                            time.sleep(sleep_timer)
                            sleep_timer += 5
                            git_code = git_search.get(git_search_url).text

                        result_html[file].append(git_code)

            # skip lines including skippable syntax
            for file_number in range(len(self.code_lines)):
                for line in range(len(self.code_lines[file_number])):
                    for word in range(len(skip_strings)):
                        if self.code_lines[file_number][line].find(skip_strings[word]) != -1:
                            self.code_lines[file_number][line] = ""
                    if self.code_lines[file_number][line] == module_begin or self.code_lines[file_number][line] == module_end:
                        self.code_lines[file_number][line] = ""
        
        #debug
        if self.debug_flag:
            search_time_end = time.time()

        result_code = self.search_html(result_html)

        #put results into queue
        queue.put(("results_git", result_code))
        queue.put(("results_git_html", results_git))

        #debug
        if self.debug_flag:
            search_time_finished = time.time()
            print("Finished:   fast search [GIT]")
            print("Time of line searching [GIT]: " + str(search_time_mid - search_time_start))
            print("Time of getting addresses [GIT]: " + str(search_time_end - search_time_mid))
            print("Time of searching addresses [GIT]: " + str(search_time_finished - search_time_end))
            print("Time elapsed in total [GIT]: " + str(search_time_finished - search_time_start))
        return

    # search html file for each line of code of given file

    def search_html(self, result_html):
        #debug
        if self.debug_flag:
            print("Started:    searching resulted websites [GIT]")
        
        result_code = []

        #reset progress parameters
        code_size = 0
        current_line = 1
        for file in range(len(result_html)):
            code_size += len(result_html[file])

        for file in range(len(result_html)):
            result_code.append([])

            for webpage in range(len(result_html[file])):
                result_code[file].append([])

                #update progress window
                update_string = "github.com (3/3)\n" + str(current_line) + "/" + str(code_size)
                update_value = math.ceil(current_line/code_size*100)
                self.update_queue.put((update_string, update_value))

                #search webpage for each line of code from given file
                for line in range(len(self.code_lines[file])):
                    if self.code_lines[file][line] != "" and self.code_lines[file][line] != "-":
                        
                        #include skipping varible names in webpage
                        if len(self.var_positions[file][line]) > 0:
                            search_string = ""
                            previous_var = 0
                            #insert * instead of variable names
                            for var_insert in self.var_positions[file][line]:
                                search_string += self.code_lines[file][line][previous_var:var_insert] + "*"
                                previous_var = var_insert
                            search_string += self.code_lines[file][line][previous_var:]
                            search_string = search_string.lstrip()
                            search_string = "*" + search_string + "*"

                            string_pos = fn.fnmatch(
                                result_html[file][webpage], search_string)

                            if string_pos == True:
                                result_code[file][webpage].append(1)
                            else:
                                result_code[file][webpage].append(-1)
                        else:
                            result_code[file][webpage].append(
                                result_html[file][webpage].find(self.code_lines[file][line].lstrip()))
                    else:
                        result_code[file][webpage].append("-")
                current_line += 1

        return (result_code)

    # find urls in html text

    def find_urls(self, search_substring, searched_string):
        i = searched_string.find(search_substring)
        while i != -1:
            yield i
            i = searched_string.find(search_substring, i+1)
