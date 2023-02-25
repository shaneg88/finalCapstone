#=====importing libraries===========
from datetime import datetime
from datetime import date
import os.path

# define functions
# define reg_user
def reg_user():
    if username == "admin":
            new_user = input("Please input new username: ")
            new_pass = input("Please input new password: ")
            new_pass_check = input("Please re enter password: ")

            # check username not already in use
            while new_user in user_list:
                print("Username already taken, please retry\n")
                new_user = input("Please input new username: ")
                new_pass = input("Please input new password: ")
                new_pass_check = input("Please re enter password: ")

                # check passwords match and if not prompt for retry            
                if new_pass != new_pass_check:
                    print("Your passwords do not match please retry")
                    new_pass = input("Please input new password: ")
                    new_pass_check = input("Please re enter password: ")


                # if password check is completed store new user in user.txt file                
                if new_pass == new_pass_check:
                    new_info = ("\n" + new_user + ", " + new_pass)
                    with open("user.txt", "a") as f:
                        f.write(new_info)

    # if a non admin login used deny access to this section
    else:
        print("\nYou do not have access to this section\n")

# define add_task
def add_task():
    name = input("\nPlease input username to assign task to: ")
    task = input("Please input task title: ")
    task_desc = input("Please input task description: ")
    date_assigned = date.today
    due_date = input("Please input due date (yyyy-mm-dd format): ")
    new_task = f"\n{name}, {task}, {task_desc}, {date_assigned}, {due_date}, No"
    with open("tasks.txt", "a") as f:
        f.write(new_task)
    print("Task added\n")    

# define view_all
def view_all():
    with open("tasks.txt", "r") as f:
        # split and strip lines
        for pos, line in enumerate(f, 1):
            line = line.strip()
            line = line.split(", ")

            # print in easy to read block
            output = f"\n---------------[{pos}]---------------\n"
            output += f"Task: \t\t{line[1]}\n"
            output += f"Assigned to: \t{line[0]}\n"
            output += f"Date assigned: \t{line[3]}\n"
            output += f"Due date: \t{line[4]}\n"
            output += f"Task complete: \t{line[5]}\n"
            output += f"Task description:\n {line[2]}\n"
            output += f"------------------------------\n"

            print(output)

# define view_mine
def view_mine():
    with open("tasks.txt", "r") as f:
        tasks = f.readlines()
        # split lines
        for pos, line in enumerate(tasks, 1):
            line = line.split(", ")
            
            # check if username matches login and print associated tasks if so
            if username == line[0]:
                output = f"\n---------------[{pos}]---------------\n"
                output += f"Task: \t\t{line[1]}\n"
                output += f"Assigned to: \t{line[0]}\n"
                output += f"Date assigned: \t{line[3]}\n"
                output += f"Due date: \t{line[4]}\n"
                output += f"Task complete: \t{line[5]}\n"
                output += f"Task description:\n {line[2]}\n"
                output += f"------------------------------\n"

                print(output) 

        # ask which task number the user wants
        while True:
            to_edit = int(input("Which task number do you wish to edit(0 to exit): ")) - 1

            if to_edit < -1:
                print("Invalid choice, please retry")
                continue
            elif to_edit >= len(tasks):
                print("Invalid choice, please retry")
                continue
            elif to_edit == -1:
                return None
            else:
                task_edit = tasks[to_edit]
                break
            

        # ask what to do with task
        while True:
            output = "-------Please select an option------\n"
            output += "Option 1 - Mark as complete\n"
            output += "Option 2 - Edit task\n"
            output += "-1 to Exit\n"
            output += "-----------------------------------\n"
            print(output)
            
            option = int(input("Option: "))

            # mark as completed
            if option == 1:
                line_data = task_edit.split(", ")
                line_data[-1] = "Yes\n"
                new_line = ", ".join(line_data)
                tasks[to_edit] = new_line
            # write amended task to .txt file
                with open("tasks.txt", "w") as f:
                    for line in tasks:
                        f.write(line)
                print("You have marked this task complete.\n")
                break
            
            # edit task
            elif option == 2:
                line_data = task_edit.split(", ")
                # if completed dont allow editing
                if line_data[-1] == "Yes\n":
                    print("Task already completed can't be modified.\n")
                    break
                # if not completed ask what to change name or due date
                elif line_data[-1] != "Yes\n":
                    output = "\n What do you wish to change\n"
                    output += "N (for name)\n"
                    output += "D (for due date)\n"
                    choice = input("Please select N or D: ").upper()
                    # if N is chosen
                    if choice == "N":
                        new_name = input("Please enter new name: ")
                        line_data[0] = new_name
                        new_line = ", ".join(line_data)
                        tasks[to_edit] = new_line
                        # write amended name to .txt file
                        with open("tasks.txt", "w") as f:
                            for line in tasks:
                                f.write(line)
                        print("You have changed the name on this task.\n")
                        break
                    # if D is chosen
                    elif choice == "D":
                        new_date = input("Please input new due date (yyyy-mm-dd format): ")
                        line_data[-2] = new_date
                        new_line = ", ".join(line_data)
                        tasks[to_edit] = new_line
                        # write amended date to .txt file
                        with open("tasks.txt", "w") as f:
                            for line in tasks:
                                f.write(line)
                        print("You have changed the due date on this task.\n")
                        break
                    # if incorrect input chosen
                    else:
                        print("Incorrect option, please retry.") 
                        continue   

            elif option == -1:
                break

            else:
                print("Incorrect option, Please retry\n")
                continue

# create function to generate task overview
def generate_task_overview():
    # open files to get info from
    with open ("user.txt", "r") as userfile, open ("tasks.txt", "r") as taskfile:
        # work out amount of users and tasks
        taskfile = taskfile.readlines()
        userfile = userfile.readlines()
        tasks = len(taskfile)
        users = len(userfile)
        
        # create an empty dictionary and variables to work out totals
        task_dict = {}
        comp = 0
        uncomp = 0
        overdue = 0

        # create dictionary with user as key
        for line in taskfile:
            line = line.strip()
            line = line.split(", ")
            task_dict[line[0]] = [line[1:]]

        # use the last entry in the value to see whether task completed
        for key, value in task_dict.items():
            for i in value:
                if i[-1] == "Yes":
                    comp += 1
                elif i[-1] == "No":
                    uncomp += 1

                # compare due date with todays date to see whether overdue
                if datetime.strptime(i[-2], "%Y-%m-%d") < datetime.now() and i[-1] == "No":
                    overdue += 1

            # work out percentages of completed and overdue tasks
            percent_uncomp = round((uncomp * 100) / (len(task_dict)), 2)
            percent_overdue = round((overdue * 100) / (len(task_dict)), 2)

    # write the info to a .txt file + print out confirmation message
    with open("task_overview.txt", "w") as f:
        f.write(f"The number of tasks is: {tasks}\n") 
        f.write(f"The number of completed tasks is {comp}\n")
        f.write(f"The number of uncompleted tasks is {uncomp}\n")
        f.write(f"The number of overdue tasks is {overdue}\n")
        f.write(f"The percentage of tasks uncompleted is: {percent_uncomp}%\n")
        f.write(f"The percentage of tasks overdue is {percent_overdue}%\n")

    print("\ntask_overview file written\n")
        
# create function to generate user overview
def generate_user_overview():
    # open files to get info from
    with open ("user.txt", "r") as userfile, open ("tasks.txt", "r") as taskfile, open("user_overview.txt", "w") as f:
        # work out amount of users and tasks
        taskfile = taskfile.readlines()
        userfile = userfile.readlines()
        tasks = len(taskfile)
        users = len(userfile)

        # add first two lines of text to file so its not repeated while in loop for each user
        f.write(f"\nThe total number of users is: {users}\n")
        f.write(f"the total number of tasks is: {tasks}\n")
        
        
        # create dict to use 
        user_dict = {}
        
        # split line in user text and add usernames to dictionary
        for line in userfile:
            line = line.split(", ")
            user = line[0]
            user_dict[user] = ""

        for name in user_dict:
            # create empty variables for use
            user_tasks = 0
            user_completed = 0
            user_uncompleted = 0
            user_overdue = 0
            percent_tasks = 0
            percent_comp = 0
            percent_uncomp = 0
            percent_overdue = 0

            
            # figure out which tasks are assigned to each user and wether they are completed or overdue
            for lines in taskfile:
                lines = lines.strip().split(", ")
                if lines[0] == name:
                    user_tasks += 1
                    if lines[-1] == "Yes":
                        user_completed += 1
                    elif lines[-1] == "No":
                        user_uncompleted += 1
                    if datetime.strptime(lines[-2], "%Y-%m-%d") < datetime.now() and lines[-1] == "No":
                        user_overdue += 1
            
            
            # if tasks is over zero figure out percentage amounts for each field
            if user_tasks != 0:
                percent_tasks = round((user_tasks * 100) / tasks, 2)
                percent_comp = round((user_completed * 100) / user_tasks, 2)
                percent_uncomp = round((user_uncompleted * 100) / user_tasks, 2)
                percent_overdue = round((user_overdue * 100) / user_tasks, 2)    

            # copy info for each user to text file + print confirmation message
            f.write(f"""\nUsername: {name}
            percentage of tasks assigned: {percent_tasks}%
            percentage of tasks completed: {percent_comp}%
            percentage of tasks uncompleted: {percent_uncomp}%
            percentage of tasks overdue: {percent_overdue}%\n""")


        print("user overview text file written\n")    
            




#====Login Section====
# open user.txt file
with open("user.txt", "r") as f:
    users = f.readlines()
    user_list = []
    pass_list = []

# create lists of usernames and passwords
    for user in users:
        line = user.split(", ")
        user_list.append(line[0])
        pass_list.append(line[1].strip("\n"))

# ask for username and password
username = input("Please enter username: ")
password = input("Please enter password: ")

# check if username is in list and if password matches
while True:
    if username in user_list:
        if pass_list[user_list.index(username)] == password:
            print("You've been logged in\n")
            break
        else:
            print("Incorrect login details, please retry")
            username = input("Please enter username: ")
            password = input("Please enter password: ")
    else:
            print("Incorrect login details, please retry")
            username = input("Please enter username: ")
            password = input("Please enter password: ")




while True:
# offer two different menus one for admin containing statistics    
    if username == "admin":
        menu = input("""\nSelect one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
: """).lower()
# one menu for standard users
    else:
        menu = input("""Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: """).lower()

# if admin login used allow access to adding users
    if menu == 'r':
        reg_user()
     
# in add task section ask for relative info then store to tasks.txt file
    elif menu == 'a':
        add_task()            
            
# print all tasks in an easy to read format
    elif menu == 'va':
        view_all()

# check the username matches the task, then only print out matched tasks
    elif menu == 'vm':
        view_mine()

# create the generate reports section                   
    elif menu == 'gr':
        if username == "admin":
            generate_task_overview()
            generate_user_overview()
        else:
            print("You dont have access to this section")

    elif menu == "ds":
        if username == "admin":
            # if the files dont already exist create them
            if not os.path.exists('task_overview.txt') and not os.path.exists('user_overview.txt'):
                generate_task_overview()
                generate_user_overview()

                # print files to screen in readable way
                with open("task_overview.txt", "r") as tasks:
                    for line in tasks:
                        print(line.strip())

                with open("user_overview.txt", "r") as users:
                    for line in users:
                        print(line.strip())
            
            # if files exist just print the info to screen
            elif os.path.exists('task_overview.txt') and os.path.exists('user_overview.txt'):
                with open("task_overview.txt", "r") as tasks:
                    for line in tasks:
                        print(line.strip())

                with open("user_overview.txt", "r") as users:
                    for line in users:
                        print(line.strip())

        else:
           print("You dont have access to this section")         

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")