import psycopg2
from matplotlib.lines import Line2D
from prettytable import PrettyTable
from errors import *
import numpy as np
import matplotlib.pyplot as plt
import re
from mail import EmailVerification

emails = EmailVerification()

class APM:
    def __init__(self):
        self.conn = psycopg2.connect(database="Student", host="localhost", user="postgres", password="root", port=5432)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def login(self):
        while True:
            print()
            print("###########################################################################################################################")
            print("                                           Welcome To Academic Progress Monitor                    ")
            print()
            print("###########################################################################################################################")
            print()
            print("Login: ")
            print(" o Student ( Press 1 )")
            print(" o Admin ( Press 2 )")
            print(" o Exit ( Press 3 )")
            print()
            print("--------------------------------------------------------------------------------------------------------------------------")
            print()
            print("Your Choice: ", end="")
            choice = (input())
            if choice == '1':
                self.user = Student(self.cursor)
            elif choice == '2':
                self.user = Admin(self.cursor)
            elif choice == '3':
                print("\033[91m{}\033[0m".format("Exiting............"))
                break
            else:
                print("\033[91m{}\033[0m".format("Please enter correct choice."))


class Student:
    def __init__(self, cursor):
        self.cursor = cursor
        self.login()

    def login(self):
        attempts = 0  # Initialize counter for login attempts

        while attempts < 3:  # Allow up to 3 attempts
            print()
            try:
                Enrollment_no = int(input("Enter Login id (Enrollment no.): "))
                password = input("Enter password: ")
                self.cursor.execute(
                    f"SELECT COUNT(*) FROM login_credentials WHERE enrollment_no = {Enrollment_no};")
                count = self.cursor.fetchone()[0]
                if count == 0:
                    raise EnrollmentError("\033[91m{}\033[0m".format("Invalid enrollment number!"))

                self.cursor.execute(
                    f"SELECT password FROM login_credentials WHERE enrollment_no = {Enrollment_no};")
                match = self.cursor.fetchone()
                if match is None or match[0] != password:
                    raise PasswordError("\033[91m{}\033[0m".format("Invalid password!"))

            except (EnrollmentError, PasswordError) as e:
                print(e.message)
                attempts += 1  # Increment the attempt counter
                continue
            else:
                print()
                print("\033[92m{}\033[0m".format("Login successful!..........."))
                self.details(Enrollment_no)
                self.menu(Enrollment_no)
                break  # Exiting the loop after successful login
        else:
            print()
            # print("Too many failed login attempts. Please try again later.")
            print('Forgot password?\n1. Yes\n2. No')
            pass_choice = int(input())
            if pass_choice == 1:
                self.cursor.execute(
                    f"SELECT email FROM student_details WHERE enrollment_no = {Enrollment_no};")
                email = self.cursor.fetchone()[0] 
                emails.send_verification_code(email)
                print("\033[92m{}\033[0m".format('Check the mail for the otp code and enter'))
                user_otp = int(input('Enter the otp: '))
                if user_otp ==  int(emails.verification_code):
                    print('Enter the new password: ')
                    self.change_password(Enrollment_no)
                else:
                    print("\033[91m{}\033[0m".format("Wrong Otp"))
                    
            else:
                exit()


    def menu(self, Enrollment_no):
        while True:
            print()
            print("--------------------------------------------------------------------------------------------------------------------------")
            print("Select what would you like to do: ")
            print()
            print("1. Change your Password")
            print("2. View your marks")
            print("3. View your progress report")
            print("Enter 4 to go back")
            print("--------------------------------------------------------------------------------------------------------------------------")
            print()

            print("Your choice: ", end="")
            choice = (input())

            if choice == '1':
                self.change_password(Enrollment_no)
            elif choice == '2':
                self.marks(Enrollment_no)
            elif choice == '3':
                self.progress(Enrollment_no)
            elif choice == '4':
                print("\033[91m{}\033[0m".format("Exiting Student Panel..."))
                break
            else:
                print("\033[91m{}\033[0m".format("Please enter valid choice (From 1 - 4)"))


    def change_password(self, enrollment_no):
        print()
        print("\033[93m{}\033[0m".format("Note: "))
        print("\033[93m{}\033[0m".format("Password must be at least 8 characters long."))
        print("\033[93m{}\033[0m".format("Password must contain at least one uppercase letter."))
        print("\033[93m{}\033[0m".format("Password must contain at least one lowercase letter."))
        print("\033[93m{}\033[0m".format("Password must contain at least one digit."))
        print("\033[93m{}\033[0m".format("Password must contain at least one special character. ( from @#$_ )"))
        print()

        while True:
            new_password = input("Enter new password: ")

            if len(new_password) < 8:
                print("\033[91m{}\033[0m".format("Password must be at least 8 characters long."))
                continue

            if not re.search(r"[A-Z]", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one uppercase letter."))
                continue

            if not re.search(r"[a-z]", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one lowercase letter."))
                continue

            if not re.search(r"\d", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one digit."))
                continue

            if not re.search(r"[@#$_]", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one special character."))
                continue

            break

        query = "UPDATE login_credentials SET password = %s WHERE enrollment_no = %s;"
      
        try:
            self.cursor.execute(query, (new_password, enrollment_no))
            self.cursor.connection.commit()
            print("\033[92m{}\033[0m".format("Password changed successfully!"))
        except Exception as e:
            print(f"Error occurred: {e}")
            
    def change_password_admin(self, email):
        print()
        print("\033[93m{}\033[0m".format("Note: "))
        print("\033[93m{}\033[0m".format("Password must be at least 8 characters long."))
        print("\033[93m{}\033[0m".format("Password must contain at least one uppercase letter."))
        print("\033[93m{}\033[0m".format("Password must contain at least one lowercase letter."))
        print("\033[93m{}\033[0m".format("Password must contain at least one digit."))
        print("\033[93m{}\033[0m".format("Password must contain at least one special character. ( from @#$_ )"))
        print()

        while True:
            new_password = input("Enter new password: ")

            if len(new_password) < 8:
                print("\033[91m{}\033[0m".format("Password must be at least 8 characters long."))
                continue

            if not re.search(r"[A-Z]", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one uppercase letter."))
                continue

            if not re.search(r"[a-z]", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one lowercase letter."))
                continue

            if not re.search(r"\d", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one digit."))
                continue

            if not re.search(r"[@#$_]", new_password):
                print("\033[91m{}\033[0m".format("Password must contain at least one special character.( from @#$_ )"))
                continue

            break

        query = "UPDATE admin_credentials SET password = %s WHERE email = %s;"
        try:
            self.cursor.execute(query, (new_password, email))
            self.cursor.connection.commit()
            print("Password changed successfully!")
        except Exception as e:
            print("\033[91m{}\033[0m".format(f"Error occurred: {"\033[91m{}\033[0m".format(e)}"))

    def details(self, Enrollment_no):
        self.cursor.execute(f"SELECT Name FROM student_details WHERE enrollment_no = {Enrollment_no};")
        name = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT Department FROM student_details WHERE enrollment_no = {Enrollment_no};")
        dept = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT Branch FROM student_details WHERE enrollment_no = {Enrollment_no};")
        branch = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT Batch FROM student_details WHERE enrollment_no = {Enrollment_no};")
        batch = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT Roll_no FROM student_details WHERE enrollment_no = {Enrollment_no};")
        roll_no = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT Rank FROM student_details WHERE enrollment_no = {Enrollment_no};")
        rank = self.cursor.fetchone()[0]

        self.cursor.execute(f"SELECT email FROM student_details WHERE enrollment_no = {Enrollment_no};")
        email = self.cursor.fetchone()[0]

        table = PrettyTable(["Your Details: ", ""])

        Name = ["Name "]
        Email = ["Email"]
        Enroll = ["Enrollment no "]
        Depart = ["Department "]
        Branch = ["Branch "]
        Batch = ["Batch "]
        Roll = ["Roll no "]
        Rank = ["Rank  "]

        Name += [name]
        Email += [email]
        Enroll += [Enrollment_no]
        Depart += [dept]
        Branch += [branch]
        Batch += [batch]
        Roll += [roll_no]
        Rank += [rank]

        # Add rows to the table
        table.add_row(Name)
        table.add_row(Email)
        table.add_row(Enroll)
        table.add_row(Depart)
        table.add_row(Branch)
        table.add_row(Batch)
        table.add_row(Roll)
        table.add_row(Rank)

        # Print the table
        print(table)

    def format_marks(self, mark):
        if mark and int(mark) < 9:
            return "\033[91m{}\033[0m".format(mark)  # ANSI escape code for red color
        return mark

    def format_total_marks(self, mark):
        if mark and int(mark) < 35:
            return "\033[91m{}\033[0m".format(mark)  # ANSI escape code for red color
        elif mark and int(mark) > 35:
            return "\033[92m{}\033[0m".format(mark)  # ANSI escape code for red color
        return mark

    def marks(self, Enrollment_no):

        t1_marks = ["T1"]
        t2_marks = ["T2"]
        t3_marks = ["T3"]
        t4_marks = ["T4"]

        t1_marks_temp = t1_marks.copy()
        t2_marks_temp = t2_marks.copy()
        t3_marks_temp = t3_marks.copy()
        t4_marks_temp = t4_marks.copy()

        #########################################################################################

        self.cursor.execute(f"SELECT * FROM t1_marks WHERE enrollment_no = {Enrollment_no};")
        mark = self.cursor.fetchone()

        for i in range(1, 7):
            t1_marks += [mark[i]]
            temp = mark[i]
            t1_marks_temp.append(self.format_marks(temp))

        ##########################################################################################

        #########################################################################################

        self.cursor.execute(f"SELECT * FROM t2_marks WHERE enrollment_no = {Enrollment_no};")
        mark = self.cursor.fetchone()

        for i in range(1, 7):
            t2_marks += [mark[i]]
            temp = mark[i]
            t2_marks_temp += [(self.format_marks(temp))]

        ##########################################################################################

        #########################################################################################

        self.cursor.execute(f"SELECT * FROM t3_marks WHERE enrollment_no = {Enrollment_no};")
        mark = self.cursor.fetchone()

        for i in range(1, 7):
            t3_marks += [mark[i]]
            temp = mark[i]
            temp = self.format_marks(temp)
            t3_marks_temp.append(temp)

        ##########################################################################################

        #########################################################################################

        self.cursor.execute(f"SELECT * FROM t4_marks WHERE enrollment_no = {Enrollment_no};")
        mark = self.cursor.fetchone()

        for i in range(1, 7):
            t4_marks += [mark[i]]
            temp = mark[i]
            temp = self.format_marks(temp)
            t4_marks_temp.append(temp)

        ##########################################################################################

        total_marks = ["Total"]
        total = 0
        for i in range(1, 7):
            total += t1_marks[i]
            total += t2_marks[i]
            total += t3_marks[i]
            total += t4_marks[i]
            total_marks += [self.format_total_marks(total)]
            total = 0

        print()
        print("--------------------------------------------------------------------------------------------------------------------------")
        print("Select the Subject to View marks")
        print("Enter 1 for PS")
        print("Enter 2 for DE")
        print("Enter 3 for FCSP-1")
        print("Enter 4 for FSD-1")
        print("Enter 5 for ETC")
        print("Enter 6 for CI")
        print("Enter 7 to view overall marks summary")
        print("Enter 8 to go back")
        print("--------------------------------------------------------------------------------------------------------------------------")
        print()
        print("Your Choice: ", end="")
        choice = (input())

        ps_marks = ["PS"]
        de_marks = ["DE"]
        fcsp1_marks = ["FCSP-1"]
        fsd1_marks = ["FSD-1"]
        etc_marks = ["ETC"]
        ci_marks = ["CI"]

        ps_average = ["Average"]
        de_average = ["Average"]
        fcsp1_average = ["Average"]
        fsd1_average =["Average"]
        etc_average = ["Average"]
        ci_average = ["Average"]


        if choice == '1':
            choice = int(choice)
            self.cursor.execute(f"SELECT ps FROM t1_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg/ len(mark)
            ps_average += [int(avg)]

            self.cursor.execute(f"SELECT ps FROM t2_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            ps_average += [int(avg)]

            self.cursor.execute(f"SELECT ps FROM t3_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            ps_average += [int(avg)]

            self.cursor.execute(f"SELECT ps FROM t4_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            ps_average += [int(avg)]


            table = PrettyTable(["", "T1", "T2", "T3", "T4"])
            ps_marks.append(t1_marks_temp[choice])
            ps_marks.append(t2_marks_temp[choice])
            ps_marks.append(t3_marks_temp[choice])
            ps_marks.append(t4_marks_temp[choice])
            table.add_row(ps_marks)
            table.add_row(ps_average)
            print(table)

        elif choice == '2':
            choice = int(choice)
            self.cursor.execute(f"SELECT de FROM t1_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            de_average += [int(avg)]

            self.cursor.execute(f"SELECT de FROM t2_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            de_average += [int(avg)]

            self.cursor.execute(f"SELECT de FROM t3_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            de_average += [int(avg)]

            self.cursor.execute(f"SELECT de FROM t4_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            de_average += [int(avg)]

            table = PrettyTable(["", "T1", "T2", "T3", "T4"])
            de_marks.append(t1_marks_temp[choice])
            de_marks.append(t2_marks_temp[choice])
            de_marks.append(t3_marks_temp[choice])
            de_marks.append(t4_marks_temp[choice])
            table.add_row(de_marks)
            table.add_row(de_average)
            print(table)

        elif choice == '3':
            choice = int(choice)
            self.cursor.execute(f"SELECT \"fcsp_1\" FROM t1_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fcsp1_average += [int(avg)]

            self.cursor.execute(f"SELECT \"fcsp_1\" FROM t2_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fcsp1_average += [int(avg)]

            self.cursor.execute(f"SELECT \"fcsp_1\" FROM t3_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fcsp1_average += [int(avg)]

            self.cursor.execute(f"SELECT \"fcsp_1\" FROM t4_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fcsp1_average += [int(avg)]


            table = PrettyTable(["", "T1", "T2", "T3", "T4"])
            fcsp1_marks.append(t1_marks_temp[choice])
            fcsp1_marks.append(t2_marks_temp[choice])
            fcsp1_marks.append(t3_marks_temp[choice])
            fcsp1_marks.append(t4_marks_temp[choice])
            table.add_row(fcsp1_marks)
            table.add_row(fcsp1_average)
            print(table)

        elif choice == '4':
            choice = int(choice)
            self.cursor.execute(f"SELECT \"fsd_1\" FROM t1_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fsd1_average += [int(avg)]

            self.cursor.execute(f"SELECT \"fsd_1\" FROM t2_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fsd1_average += [int(avg)]

            self.cursor.execute(f"SELECT \"fsd_1\" FROM t3_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fsd1_average += [int(avg)]

            self.cursor.execute(f"SELECT \"fsd_1\" FROM t4_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            fsd1_average += [int(avg)]

            table = PrettyTable(["", "T1", "T2", "T3", "T4"])
            fsd1_marks.append(t1_marks_temp[choice])
            fsd1_marks.append(t2_marks_temp[choice])
            fsd1_marks.append(t3_marks_temp[choice])
            fsd1_marks.append(t4_marks_temp[choice])
            table.add_row(fsd1_marks)
            table.add_row(fsd1_average)
            print(table)

        elif choice == '5':
            choice = int(choice)
            self.cursor.execute("SELECT etc FROM t1_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            etc_average += [int(avg)]

            self.cursor.execute("SELECT etc FROM t2_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            etc_average += [int(avg)]

            self.cursor.execute("SELECT etc FROM t3_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            etc_average += [int(avg)]

            self.cursor.execute("SELECT etc FROM t4_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            etc_average += [int(avg)]


            table = PrettyTable(["", "T1", "T2", "T3", "T4"])
            etc_marks.append(t1_marks_temp[choice])
            etc_marks.append(t2_marks_temp[choice])
            etc_marks.append(t3_marks_temp[choice])
            etc_marks.append(t4_marks_temp[choice])
            table.add_row(etc_marks)
            table.add_row(etc_average)
            print(table)

        elif choice == '6':
            choice = int(choice)
            self.cursor.execute(f"SELECT etc FROM t1_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            ci_average += [int(avg)]

            self.cursor.execute(f"SELECT etc FROM t2_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            ci_average += [int(avg)]

            self.cursor.execute(f"SELECT etc FROM t3_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            ci_average += [int(avg)]

            self.cursor.execute(f"SELECT etc FROM t4_marks;")
            mark = self.cursor.fetchall()
            avg = 0
            for i in range(len(mark)):
                avg += mark[i][0]

            avg = avg / len(mark)
            ci_average += [int(avg)]

            table = PrettyTable(["", "T1", "T2", "T3", "T4"])
            ci_marks.append(t1_marks_temp[choice])
            ci_marks.append(t2_marks_temp[choice])
            ci_marks.append(t3_marks_temp[choice])
            ci_marks.append(t4_marks_temp[choice])
            table.add_row(ci_marks)
            table.add_row(ci_average)
            print(table)

        elif choice == '7':
            choice = int(choice)
            table = PrettyTable(["", "PS", "DE", "FCSP-1", 'FSD-1', 'ETC', 'CI'])

            # Add rows to the table
            table.add_row(t1_marks_temp)
            table.add_row(t2_marks_temp)
            table.add_row(t3_marks_temp)
            table.add_row(t4_marks_temp)
            table.add_row(["", "", "", "", "", "", ""])
            table.add_row(total_marks)

            # Print the table
            print(table)

        elif choice == '8':
            return

        else:
            print("\033[91m{}\033[0m".format("Please enter correct choice."))

    def subject_wise_graph(self, Enrollment_no, subject):

        if subject == 'FCSP-1':
            sub_name = '\"fcsp_1\"'
        elif subject == 'FSD-1':
            sub_name = '\"fsd_1\"'
        else:
            sub_name = subject

        mark_list = []
        average_list = []


        tables = ["t1_marks", "t2_marks", "t3_marks", "t4_marks"]
        for table in tables:
            self.cursor.execute(f"SELECT {sub_name} FROM {table} WHERE enrollment_no = {Enrollment_no};")
            mark = self.cursor.fetchone()
            mark_list.append(mark[0])

        for table in tables:
            self.cursor.execute(f"SELECT {sub_name} FROM {table}")
            marks = self.cursor.fetchall()
            avg = sum(mark[0] for mark in marks) / len(marks)
            average_list.append(int(avg))

        x = tables
        y = mark_list
        avg_y = average_list

        plt.figure(figsize=(8, 6))

        plt.plot(x, y, linestyle='-', color='blue',
                 label='Individual Marks')

        for i, mark in enumerate(y):
            color = 'r' if mark < 9 else 'b'
            marker = '*' if mark < 9 else 'o'
            plt.plot(x[i], y[i], marker=marker, linestyle='None', color=color, markersize=12,
                     markeredgecolor='black', zorder=3)

        plt.plot(x, avg_y, linestyle='--', color='green', marker='s', markersize=8,
                 label='Average Marks')


        plt.title(f'Performance Score ( {subject} )')
        plt.xlabel('Test')
        plt.ylabel('Marks')


        plt.ylim(0, 30)


        plt.xticks(rotation=45)
        plt.grid(True)


        legend_handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Pass'),
            plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=8, label='Fail'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='green', markersize=8,
                       label='Average Marks')
        ]
        plt.legend(handles=legend_handles, loc='lower right')


        for i, txt in enumerate(y):
            plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(8, 0),
                         ha='left')

        # Show the average marks on the plot
        for i, txt in enumerate(avg_y):
            plt.annotate(f'{txt}', (x[i], avg_y[i]), textcoords="offset points", xytext=(-7, -15),
                         ha='left', color='green')

        plt.tight_layout()
        plt.show()


    def test_wise_graph(self, Enrollment_no, test):
        self.cursor.execute(f"SELECT * FROM {test} WHERE enrollment_no = {Enrollment_no};")
        mark = self.cursor.fetchone()

        test_scores = mark[1:7]
        subjects = ["PS", "DE", "FCSP-1", "FSD-1", "ETC", "CI"]

        total_score = sum(test_scores)


        max_score = max(test_scores)
        min_score = min(test_scores)
        max_score_indices = [i for i, score in enumerate(test_scores) if score == max_score]
        min_score_indices = [i for i, score in enumerate(test_scores) if score == min_score]


        explode = [0] * len(subjects)


        for i in max_score_indices + min_score_indices:
            explode[i] = 0.2


        colors = ['blue','yellow','pink','skyblue','orange', 'purple']
        for i in max_score_indices:
            colors[i] = 'green'
        for i in min_score_indices:
            colors[i] = 'red'


        plt.figure(figsize=(8, 8))
        patches, texts, autotexts = plt.pie(test_scores, labels=subjects, autopct='%1.1f%%',
                                            startangle=140, explode=explode, colors=colors)


        for i in max_score_indices + min_score_indices:
            patches[i].set_edgecolor('black')
            patches[i].set_linewidth(2)


        legend_handles = []
        if max_score_indices:
            legend_handles.append(
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10,
                           label='Max Contributor'))
        if min_score_indices:
            legend_handles.append(
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10,
                           label='Min Contributor'))


        legend_handles.append(plt.Line2D([0], [0], color='black', markerfacecolor='white', markersize=0,
                                         label=f'Total Score: {total_score}/150'))

        legend_handles.append(plt.Line2D([0], [0], color='black', markerfacecolor='white', markersize=0,
                                         label=f'Percentage: {round((total_score / 150) * 100, 2)}%'))

        plt.legend(handles=legend_handles, loc='upper right')

        plt.title(f'Test Scores Distribution ( {test} )', y=1.05)
        plt.axis('equal')
        plt.show()


    def progress(self, Enrollment_no):

        while True:
            print()
            print("--------------------------------------------------------------------------------------------------------------------------")
            print("How would you like to view progress graph: ")
            print()
            print("1. Subject wise report")
            print("2. Test wise report")
            print("3. Cumulative report")
            print("Enter 0 to go back")
            print("--------------------------------------------------------------------------------------------------------------------------")
            print()
            print("Your choice: ", end ="")

            choice = input()


            if choice == '1':
                while True:
                    print()
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print("Choose the subject: ")
                    print("1. PS")
                    print("2. DE")
                    print("3. FCSP-1")
                    print("4. FSD-1")
                    print("5. ETC")
                    print("6. CI")
                    print("Enter 7 to go back")
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print()

                    sub = int(input())

                    if sub == 1:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'PS')
                    elif sub == 2:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'DE')
                    elif sub == 3:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no, 'FCSP-1')
                    elif sub == 4:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'FSD-1')
                    elif sub == 5:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no, 'ETC')
                    elif sub == 6:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'CI')
                    elif sub == 7:
                        break
                    else:
                        print("\033[91m{}\033[0m".format('Please select correct option......'))

            elif choice == '2':
                while True:
                    print()
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print("Choose which test report you want to see: ")
                    print("1. T1")
                    print("2. T2")
                    print("3. T3")
                    print("4. T4")
                    print("Enter 0 to go back...")
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print()

                    test_choice = (input())

                    if test_choice == '1':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no,'t1_marks')
                    elif test_choice == '2':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no, 't2_marks')
                    elif test_choice == '3':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no, 't3_marks')
                    elif test_choice == '4':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no, 't4_marks')
                    elif test_choice == '0':
                        break
                    else:
                        print("\033[91m{}\033[0m".format("Please select correct option"))


            elif choice == '3':
                while True:
                    print()
                    print(
                        "--------------------------------------------------------------------------------------------------------------------------")
                    print("Choose how would you like to see: ")
                    print("1. Test-Wise Cumulative Analysis")
                    print("2. Individual vs Collective Average Analysis")
                    print("Enter 0 to go back...")
                    print(
                        "--------------------------------------------------------------------------------------------------------------------------")
                    print()

                    print("Your Choice: ", end="")
                    choice = input()
                    print()

                    x = ["PS", "DE", "FCSP-1", "FSD-1", "ETC", "CI"]
                    y1 = []
                    y2 = []
                    y3 = []
                    y4 = []

                    tables = ["t1_marks", "t2_marks", "t3_marks", "t4_marks"]

                    for table in tables:
                        self.cursor.execute(
                            f"SELECT * FROM {table} WHERE enrollment_no = {Enrollment_no};")
                        mark = self.cursor.fetchone()

                        if (table == 't1_marks'):
                            y1 = mark[1:7]
                        elif (table == 't2_marks'):
                            y2 = mark[1:7]
                        elif (table == 't3_marks'):
                            y3 = mark[1:7]
                        else:
                            y4 = mark[1:7]

                    if choice == '1':

                        fig = plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        ax.plot(x, y1, marker='o', color='blue', label='T1')
                        ax.plot(x, y2, marker='s', color='green', label='T2')
                        ax.plot(x, y3, marker='^', color='magenta', label='T3')
                        ax.plot(x, y4, marker='*', color='purple', label='T4')

                        # Annotate starting points with test names
                        ax.text(x[0], y1[0], 'T1', color='blue', fontsize=12, ha='right', va='bottom')
                        ax.text(x[0], y2[0], 'T2', color='green', fontsize=12, ha='right', va='bottom')
                        ax.text(x[0], y3[0], 'T3', color='magenta', fontsize=12, ha='right', va='bottom')
                        ax.text(x[0], y4[0], 'T4', color='purple', fontsize=12, ha='right', va='bottom')

                        ax.set_title('Test Report')
                        ax.set_xlabel('Subject')
                        ax.set_ylabel('Marks')

                        ax.set_xticks(np.arange(len(x)))
                        ax.set_xticklabels(x, rotation=45)
                        ax.grid(True)  # Show grid

                        ax.set_ylim(0, 30)

                        legend_handles = [
                            Line2D([0], [0], color='blue', lw=2, label='T1'),
                            Line2D([0], [0], color='green', lw=2, label='T2'),
                            Line2D([0], [0], color='magenta', lw=2, label='T3'),
                            Line2D([0], [0], color='purple', lw=2, label='T4'),
                        ]
                        ax.legend(handles=legend_handles, loc='lower right')

                        plt.tight_layout()
                        plt.show()

                    elif choice == '2':

                        # Calculate average marks subject-wise for current student
                        average_marks_student = [(np.mean([y1[i], y2[i], y3[i], y4[i]])) for i in range(len(x))]

                        z1 = []
                        z2 = []
                        z3 = []
                        z4 = []
                        sub_ = ['ps','de','fcsp_1','fsd_1','etc','ci']
                        for table in tables:
                            for sub in sub_:
                                mark_list = []
                                self.cursor.execute(
                                    f"SELECT \"{sub}\" FROM {table}")
                                mark = self.cursor.fetchall()
                                for i in range(len(mark)):
                                    mark_list += [mark[i][0]]

                                if(table == 't1_marks'):
                                    z1.append(np.mean(mark_list))
                                elif table == 't2_marks':
                                    z2.append(np.mean(mark_list))
                                elif table == 't3_marks':
                                    z3.append(np.mean(mark_list))
                                elif table == 't4_marks':
                                    z4.append(np.mean(mark_list))

                        overall_average_marks = [(np.mean([z1[i], z2[i], z3[i], z4[i]])) for i in range(len(x))]

                        # Plot double bar graph for average marks subject-wise
                        plt.figure(figsize=(12, 6))
                        bar_width = 0.35
                        index = np.arange(len(x))

                        bar1 = plt.bar(index, average_marks_student, bar_width, color='lightblue', label='Your average')
                        bar2 = plt.bar(index + bar_width, overall_average_marks, bar_width, color='orange',
                                       label='Overall Average')

                        plt.title('Average Marks Subject-wise')
                        plt.xlabel('Subject')
                        plt.ylabel('Average Marks')
                        plt.xticks(index + bar_width / 2, x, rotation=45)
                        plt.legend()
                        plt.grid(True)

                        # Annotate each bar with its corresponding average marks for the current student
                        for bar, mark in zip(bar1, average_marks_student):
                            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, round(mark, 2),
                                     ha='center', va='bottom')

                        # Annotate each bar with the overall average marks for all students
                        for bar, mark in zip(bar2, overall_average_marks):
                            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, round(mark, 2),
                                     ha='center', va='bottom')

                        plt.ylim(0, 30)  # Set y-axis limits
                        plt.tight_layout()
                        plt.show()

                    elif choice == '0':
                        break

                    else:
                        print("\033[91m{}\033[0m".format("Please choose correct option....."))

            elif choice == '0':
                break

            else:
                print("\033[91m{}\033[0m".format("Please choose right option....."))










'''

                                                        ADMIN PANEL

'''










class Admin(Student):
    def __init__(self, cursor):
        self.cursor = cursor
        self.admin_login()

    def subject_wise_graph(self, Enrollment_no, subject):

        if subject == 'FCSP-1':
            sub_name = '\"fcsp_1\"'
        elif subject == 'FSD-1':
            sub_name = '\"fsd_1\"'
        else:
            sub_name = subject

        mark_list = []
        average_list = []


        tables = ["t1_marks", "t2_marks", "t3_marks", "t4_marks"]
        for table in tables:
            self.cursor.execute(f"SELECT {sub_name} FROM {table} WHERE enrollment_no = {Enrollment_no};")
            mark = self.cursor.fetchone()
            mark_list.append(mark[0])

        for table in tables:
            self.cursor.execute(f"SELECT {sub_name} FROM {table}")
            marks = self.cursor.fetchall()
            avg = sum(mark[0] for mark in marks) / len(marks)
            average_list.append(int(avg))

        x = tables
        y = mark_list
        avg_y = average_list

        plt.figure(figsize=(8, 6))

        plt.plot(x, y, linestyle='-', color='blue',
                 label='Individual Marks')

        for i, mark in enumerate(y):
            color = 'r' if mark < 9 else 'b'
            marker = '*' if mark < 9 else 'o'
            plt.plot(x[i], y[i], marker=marker, linestyle='None', color=color, markersize=12,
                     markeredgecolor='black', zorder=3)

        plt.plot(x, avg_y, linestyle='--', color='green', marker='s', markersize=8,
                 label='Average Marks')


        plt.title(f'Performance Score ( {subject} )')
        plt.xlabel('Test')
        plt.ylabel('Marks')


        plt.ylim(0, 30)


        plt.xticks(rotation=45)
        plt.grid(True)


        legend_handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Pass'),
            plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markersize=8, label='Fail'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='green', markersize=8,
                       label='Average Marks')
        ]
        plt.legend(handles=legend_handles, loc='lower right')


        for i, txt in enumerate(y):
            plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(8, 0),
                         ha='left')

        # Show the average marks on the plot
        for i, txt in enumerate(avg_y):
            plt.annotate(f'{txt}', (x[i], avg_y[i]), textcoords="offset points", xytext=(-7, -15),
                         ha='left', color='green')

        plt.tight_layout()
        plt.show()

    def test_wise_graph(self, Enrollment_no, test):
        self.cursor.execute(f"SELECT * FROM {test} WHERE enrollment_no = {Enrollment_no};")
        mark = self.cursor.fetchone()

        test_scores = mark[1:7]
        subjects = ["PS", "DE", "FCSP-1", "FSD-1", "ETC", "CI"]

        total_score = sum(test_scores)


        max_score = max(test_scores)
        min_score = min(test_scores)
        max_score_indices = [i for i, score in enumerate(test_scores) if score == max_score]
        min_score_indices = [i for i, score in enumerate(test_scores) if score == min_score]


        explode = [0] * len(subjects)


        for i in max_score_indices + min_score_indices:
            explode[i] = 0.2


        colors = ['blue','yellow','pink','skyblue','orange', 'purple']
        for i in max_score_indices:
            colors[i] = 'green'
        for i in min_score_indices:
            colors[i] = 'red'


        plt.figure(figsize=(8, 8))
        patches, texts, autotexts = plt.pie(test_scores, labels=subjects, autopct='%1.1f%%',
                                            startangle=140, explode=explode, colors=colors)


        for i in max_score_indices + min_score_indices:
            patches[i].set_edgecolor('black')
            patches[i].set_linewidth(2)


        legend_handles = []
        if max_score_indices:
            legend_handles.append(
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10,
                           label='Max Contributor'))
        if min_score_indices:
            legend_handles.append(
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10,
                           label='Min Contributor'))


        legend_handles.append(plt.Line2D([0], [0], color='black', markerfacecolor='white', markersize=0,
                                         label=f'Total Score: {total_score}/150'))

        legend_handles.append(plt.Line2D([0], [0], color='black', markerfacecolor='white', markersize=0,
                                         label=f'Percentage: {round((total_score / 150) * 100, 2)}%'))

        plt.legend(handles=legend_handles, loc='upper right')

        plt.title(f'Test Scores Distribution ( {test} )', y=1.05)
        plt.axis('equal')
        plt.show()

    def stud_progress(self, Enrollment_no):

        while True:
            print()
            print("--------------------------------------------------------------------------------------------------------------------------")
            print("How would you like to view progress graph: ")
            print()
            print("1. Subject wise report")
            print("2. Test wise report")
            print("3. Cumulative report")
            print("Enter 0 to go back")
            print("--------------------------------------------------------------------------------------------------------------------------")
            print()
            print("Your choice: ", end ="")

            choice = input()


            if choice == '1':
                while True:
                    print()
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print("Choose the subject: ")
                    print("1. PS")
                    print("2. DE")
                    print("3. FCSP-1")
                    print("4. FSD-1")
                    print("5. ETC")
                    print("6. CI")
                    print("Enter 7 to go back")
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print()

                    sub = int(input())

                    if sub == 1:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'PS')
                    elif sub == 2:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'DE')
                    elif sub == 3:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no, 'FCSP-1')
                    elif sub == 4:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'FSD-1')
                    elif sub == 5:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no, 'ETC')
                    elif sub == 6:
                        print("Showing........................")
                        self.subject_wise_graph(Enrollment_no,'CI')
                    elif sub == 7:
                        break
                    else:
                        print("\033[91m{}\033[0m".format('Please select correct option......'))

            elif choice == '2':
                while True:
                    print()
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print("Choose which test report you want to see: ")
                    print("1. T1")
                    print("2. T2")
                    print("3. T3")
                    print("4. T4")
                    print("Enter 0 to go back...")
                    print("--------------------------------------------------------------------------------------------------------------------------")
                    print()

                    test_choice = (input())

                    if test_choice == '1':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no,'t1_marks')
                    elif test_choice == '2':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no, 't2_marks')
                    elif test_choice == '3':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no, 't3_marks')
                    elif test_choice == '4':
                        print("\033[92m{}\033[0m".format("Showing........................"))
                        self.test_wise_graph(Enrollment_no, 't4_marks')
                    elif test_choice == '0':
                        break
                    else:
                        print("\033[91m{}\033[0m".format("Please select correct option"))


            elif choice == '3':
                while True:
                    print()
                    print(
                        "--------------------------------------------------------------------------------------------------------------------------")
                    print("Choose how would you like to see: ")
                    print("1. Test-Wise Cumulative Analysis")
                    print("2. Individual vs Collective Average Analysis")
                    print("Enter 0 to go back...")
                    print(
                        "--------------------------------------------------------------------------------------------------------------------------")
                    print()

                    print("Your Choice: ", end="")
                    choice = input()
                    print()

                    x = ["PS", "DE", "FCSP-1", "FSD-1", "ETC", "CI"]
                    y1 = []
                    y2 = []
                    y3 = []
                    y4 = []

                    tables = ["t1_marks", "t2_marks", "t3_marks", "t4_marks"]

                    for table in tables:
                        self.cursor.execute(
                            f"SELECT * FROM {table} WHERE enrollment_no = {Enrollment_no};")
                        mark = self.cursor.fetchone()

                        if (table == 't1_marks'):
                            y1 = mark[1:7]
                        elif (table == 't2_marks'):
                            y2 = mark[1:7]
                        elif (table == 't3_marks'):
                            y3 = mark[1:7]
                        else:
                            y4 = mark[1:7]

                    if choice == '1':

                        fig = plt.figure(figsize=(10, 6))
                        ax = plt.gca()

                        ax.plot(x, y1, marker='o', color='blue', label='T1')
                        ax.plot(x, y2, marker='s', color='green', label='T2')
                        ax.plot(x, y3, marker='^', color='magenta', label='T3')
                        ax.plot(x, y4, marker='*', color='purple', label='T4')

                        # Annotate starting points with test names
                        ax.text(x[0], y1[0], 'T1', color='blue', fontsize=12, ha='right', va='bottom')
                        ax.text(x[0], y2[0], 'T2', color='green', fontsize=12, ha='right', va='bottom')
                        ax.text(x[0], y3[0], 'T3', color='magenta', fontsize=12, ha='right', va='bottom')
                        ax.text(x[0], y4[0], 'T4', color='purple', fontsize=12, ha='right', va='bottom')

                        ax.set_title('Test Report')
                        ax.set_xlabel('Subject')
                        ax.set_ylabel('Marks')

                        ax.set_xticks(np.arange(len(x)))
                        ax.set_xticklabels(x, rotation=45)
                        ax.grid(True)  # Show grid

                        ax.set_ylim(0, 30)

                        legend_handles = [
                            Line2D([0], [0], color='blue', lw=2, label='T1'),
                            Line2D([0], [0], color='green', lw=2, label='T2'),
                            Line2D([0], [0], color='magenta', lw=2, label='T3'),
                            Line2D([0], [0], color='purple', lw=2, label='T4'),
                        ]
                        ax.legend(handles=legend_handles, loc='lower right')

                        plt.tight_layout()
                        plt.show()

                    elif choice == '2':

                        # Calculate average marks subject-wise for current student
                        average_marks_student = [(np.mean([y1[i], y2[i], y3[i], y4[i]])) for i in range(len(x))]

                        z1 = []
                        z2 = []
                        z3 = []
                        z4 = []
                        sub_ = ['ps','de','fcsp_1','fsd_1','etc','ci']
                        for table in tables:
                            for sub in sub_:
                                mark_list = []
                                self.cursor.execute(
                                    f"SELECT \"{sub}\" FROM {table}")
                                mark = self.cursor.fetchall()
                                for i in range(len(mark)):
                                    mark_list += [mark[i][0]]

                                if(table == 't1_marks'):
                                    z1.append(np.mean(mark_list))
                                elif table == 't2_marks':
                                    z2.append(np.mean(mark_list))
                                elif table == 't3_marks':
                                    z3.append(np.mean(mark_list))
                                elif table == 't4_marks':
                                    z4.append(np.mean(mark_list))

                        overall_average_marks = [(np.mean([z1[i], z2[i], z3[i], z4[i]])) for i in range(len(x))]

                        # Plot double bar graph for average marks subject-wise
                        plt.figure(figsize=(12, 6))
                        bar_width = 0.35
                        index = np.arange(len(x))

                        bar1 = plt.bar(index, average_marks_student, bar_width, color='lightblue', label='Your average')
                        bar2 = plt.bar(index + bar_width, overall_average_marks, bar_width, color='orange',
                                       label='Overall Average')

                        plt.title('Average Marks Subject-wise')
                        plt.xlabel('Subject')
                        plt.ylabel('Average Marks')
                        plt.xticks(index + bar_width / 2, x, rotation=45)
                        plt.legend()
                        plt.grid(True)

                        # Annotate each bar with its corresponding average marks for the current student
                        for bar, mark in zip(bar1, average_marks_student):
                            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, round(mark, 2),
                                     ha='center', va='bottom')

                        # Annotate each bar with the overall average marks for all students
                        for bar, mark in zip(bar2, overall_average_marks):
                            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, round(mark, 2),
                                     ha='center', va='bottom')

                        plt.ylim(0, 30)  # Set y-axis limits
                        plt.tight_layout()
                        plt.show()

                    elif choice == '0':
                        break

                    else:
                        print("\033[91m{}\033[0m".format("Please choose correct option....."))

            elif choice == '0':
                break

            else:
                print("\033[91m{}\033[0m".format("Please choose right option....."))

    def admin_login(self):
        attempts = 0  # Counter for tracking login attempts

        while attempts < 3:  # Allow up to 3 attempts
            print()
            email = input("Enter Admin Email: ")
            password = input("Enter Password: ")
            print()
            try:
                # Query to find user by email
                self.cursor.execute("SELECT password FROM admin_credentials WHERE email = %s;", (email,))
                result = self.cursor.fetchone()

                if result is None:
                    raise EmailError("\033[91m{}\033[0m".format("Invalid Email!"))

                stored_password = result[0]

                if stored_password != password:
                    raise PasswordError("\033[91m{}\033[0m".format("Invalid Password!"))

            except (EmailError, PasswordError) as e:
                print()
                print(e.message)
                attempts += 1
                continue

            else:
                print()
                print("\033[92m{}\033[0m".format("Login successful! Logged in as : "))
                self.display_faculty_data(email)
                self.admin_menu()
                break

        else:
            print()
            # print("Too many failed login attempts. Please try again later.")
            print('Forgot password?\n1. Yes\n2. No')
            pass_choice = int(input())
            if pass_choice == 1:
                emails.send_verification_code(email)
                print("\033[92m{}\033[0m".format("Check the mail for the otp code and enter"))
                user_otp = int(input('Enter the otp: '))
                if user_otp == int(emails.verification_code):
                    print('Enter the new password: ')
                    self.change_password_admin(email)
                else:
                    print("\033[91m{}\033[0m".format("Wrong Otp"))

            else:
                exit()



    def admin_menu(self):
        while True:
            print()
            print("--------------------------------------------------------------------------------------------------------------------------")
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Update Student Details")
            print("4. Add/Update Student Marks")
            print("5. Display Student Information")
            print("6. To view student progess report")
            print("7. Go Back")
            print("--------------------------------------------------------------------------------------------------------------------------")
            print()
            choice = input("Your choice: ")
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.remove_student()
            elif choice == '3':
                self.update_student()
            elif choice == '4':
                self.student_marks()
            elif choice == '5':
                self.display_student()
            elif choice == '6':
                count = 0
                trial = 0
                while True:
                    try:
                        if trial == 3:
                            break
                        Enrollment_no = int(input("Enter Student Enrollment no: "))
                        self.cursor.execute(
                            f"SELECT COUNT(*) FROM login_credentials WHERE enrollment_no = {Enrollment_no};")
                        count = self.cursor.fetchone()[0]
                        if count == 0:
                            raise EnrollmentError("\033[91m{}\033[0m".format("Invalid enrollment number!"))
                        else:
                            break
                    except (EnrollmentError) as e:
                        print(e.message)
                        trial += 1  # Increment the attempt counter
                        continue

                if trial == 3:
                    break

                self.stud_progress(Enrollment_no)
            elif choice == '7':
                print("\033[91m{}\033[0m".format("Exiting Admin Panel..."))
                break
            else:
                print("\033[91m{}\033[0m".format("Please enter a valid choice."))


    def display_faculty_data(self, email):
        self.cursor.execute("SELECT email, name, shortname, department, subject FROM faculty_details WHERE email = %s;",
                            (email,))
        faculty_data = self.cursor.fetchone()

        if faculty_data:
            table = PrettyTable()
            table.field_names = ["Email", "Name", "Short Name", "Department", "Subject"]
            table.add_row(faculty_data)
            print(table)
        else:
            print("\033[91m{}\033[0m".format("Faculty data not found."))

    def generate_enrollment_no(self):
        self.cursor.execute("SELECT MAX(enrollment_no) FROM student_details;")
        last_record = self.cursor.fetchone()

        if last_record and last_record[0]:
            # If there is a record, increment the last enrollment number by 1
            new_enrollment_no = str(int(last_record[0]) + 1)
        else:
            # If there are no records, start from the initial 8-digit number
            new_enrollment_no = "10000001"  # Starting point

        return new_enrollment_no

    def generate_roll_no(self, batch):
        self.cursor.execute(f"SELECT MAX(roll_no) FROM student_details WHERE batch = %s;", (batch,))
        last_record = self.cursor.fetchone()

        if last_record and last_record[0]:
            try:
                roll_no = int(last_record[0]) + 1
            except ValueError:

                roll_no = 1
        else:
            roll_no = 1

        return roll_no

    def check_enrollment_no(self):
        attempt_count = 0

        while attempt_count < 3:
            enrollment_no = input("\nEnter the Enrollment Number of the student: ")

            # Check for the existence of the enrollment number in the database
            self.cursor.execute("SELECT * FROM student_details WHERE enrollment_no = %s;", (enrollment_no,))
            if self.cursor.fetchone() is not None:
                return enrollment_no  # Return the valid enrollment number
            else:
                print("\033[91m{}\033[0m".format("\nNo student found with the given enrollment number."))
                attempt_count += 1

        # If this point is reached, the user has failed all attempts
        print("\033[91m{}\033[0m".format("\nFailed to enter a valid enrollment number in 3 attempts."))
        return None


    def add_student(self):
        try:

            ############################################################################################################
            while True:
                try:
                    # Prompting for student details
                    print()
                    name = input("Enter Student Name: ")
                    # Checking if the name consists of alphabets and spaces only
                    if not all(x.isalpha() or x.isspace() for x in name):
                        raise InvalidInputError("\033[91m{}\033[0m".format("Name should consist of alphabets and spaces only."))
                    else:
                        break

                except InvalidInputError as e:
                    print()
                    print(f"Failed to add student: {e}")


            ############################################################################################################

            while True:
                try:
                    print()
                    print("Select Department:")
                    departments = ['SY1', 'SY2', 'SY3']
                    for idx, dept in enumerate(departments, 1):
                        print(f"{idx}. {dept}")
                    dept_choice = input("Enter your choice: ")
                    if dept_choice.isdigit() and 1 <= int(dept_choice) <= len(departments):
                        department = departments[int(dept_choice) - 1]
                        break
                    else:
                        raise InvalidInputError("\033[91m{}\033[0m".format("Invalid choice for department."))

                except InvalidInputError as e:
                    print()
                    print(f"Failed to add student: {e}")

            ############################################################################################################
            while True:
                try:
                    print()
                    # Map each department to its relevant batches
                    dept_to_batches = {
                        'SY1': ['A1', 'A2', 'A3'],
                        'SY2': ['B1', 'B2', 'B3'],
                        'SY3': ['C1', 'C2', 'C3']
                    }

                    print("Select Batch:")
                    # Fetch batches relevant to the selected department
                    batches = dept_to_batches.get(department, [])
                    for idx, batch in enumerate(batches, 1):
                        print(f"{idx}. {batch}")
                    batch_choice = input("Enter your choice: ")
                    if batch_choice.isdigit() and 1 <= int(batch_choice) <= len(batches):
                        batch = batches[int(batch_choice) - 1]
                        break
                    else:
                        raise InvalidInputError("\033[91m{}\033[0m".format("Invalid choice for batch."))

                except InvalidInputError as e:
                    print()
                    print(f"Failed to add student: {e}")

            ############################################################################################################
            while True:
                try:
                    print()
                    # Branch selection logic
                    print("Select Branch:")
                    dept_to_branch = {
                        'SY1': ['CE', 'IT', 'CSE'],
                        'SY2': ['CST', 'CEA', 'CS&IT'],
                        'SY3': ['AIML', 'AIDS', 'RAI']
                    }
                    branch = dept_to_branch.get(department, [])
                    for idx, branches in enumerate(branch, 1):
                        print(f"{idx}. {branches}")
                    branch_choice = input("Enter your choice: ")
                    if branch_choice.isdigit() and 1 <= int(branch_choice) <= len(branch):
                        selected_branch = branch[int(branch_choice) - 1]
                        print(selected_branch)
                        break
                    else:
                        raise InvalidInputError("\033[91m{}\033[0m".format("Invalid choice for branch."))

                except InvalidInputError as e:
                    print()
                    print(f"Failed to add student: {e}")


            ############################################################################################################

            roll_no = self.generate_roll_no(batch)

            ############################################################################################################

            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            while True:
                try:
                    print()
                    # Prompt the user to enter an email address
                    email = input("Enter student's email address: ")

                    if re.match(email_pattern, email):
                        print("Valid email address!")
                        break
                    else:
                        raise InvalidInputError("\033[91m{}\033[0m".format("Invalid email address. Please enter a valid email address."))

                except InvalidInputError as e:
                    print()
                    print(f"Failed to add student: {e}")

            ############################################################################################################

            # Generate Enrollment Number
            enrollment_no = self.generate_enrollment_no()

            ############################################################################################################

            # SQL Query to insert the student data into the database
            query = """INSERT INTO student_details (name, enrollment_no, department, branch, batch, roll_no, email)
                       VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            # Executing the query

            self.cursor.execute(query, (name, enrollment_no, department, selected_branch, batch, roll_no, email))

            # insert statement for login_credentials
            query_login_credentials = """INSERT INTO login_credentials (enrollment_no) VALUES (%s);"""
            self.cursor.execute(query_login_credentials, (enrollment_no,))

            # insert statements for marks tables
            tables = ['t1_marks', 't2_marks', 't3_marks', 't4_marks', 'total_marks']
            for table in tables:
                query = f"""INSERT INTO {table} (enrollment_no) VALUES (%s);"""
                self.cursor.execute(query, (enrollment_no,))


            # Committing the transaction to the database
            self.cursor.connection.commit()
            print()
            print("\033[92m{}\033[0m".format("Student added successfully."))
            print()
            print(f"Enrollment Number of {name}: {enrollment_no}")
            print()


        except Exception as e:
            # Rolling back in case of error
            self.cursor.connection.rollback()
            print()
            print(f"An error occurred: {e}")

    def remove_student(self):
            try:
                enrollment_no = self.check_enrollment_no()
                if enrollment_no is None:
                    print("Returning to admin menu...")  # Operation aborted
                    return

                # SQL Query to delete the student record from the database
                query = "DELETE FROM student_details WHERE enrollment_no = %s;"

                # Checking if the student exists before attempting to delete
                self.cursor.execute("SELECT * FROM student_details WHERE enrollment_no = %s;", (enrollment_no,))
                if self.cursor.fetchone() is None:
                    print()
                    print("\033[91m{}\033[0m".format("No student found with the given enrollment number."))
                    return

                # Executing the delete query
                self.cursor.execute(query, (enrollment_no,))

                for table_name in ['t1_marks', 't2_marks', 't3_marks', 't4_marks', 'total_marks', 'login_credentials']:
                    query_del = f"""
                            DELETE FROM {table_name} WHERE enrollment_no = %s;
                            """
                    self.cursor.execute(query_del, (enrollment_no,))

                # Committing the transaction to the database
                self.cursor.connection.commit()
                print()
                print("\033[91m{}\033[0m".format("Student removed successfully."))
            except Exception as e:
                # Rolling back in case of error
                self.cursor.connection.rollback()
                print()
                print(f"An error occurred: {e}")

    def update_student(self):
        while True:
            try:
                enrollment_no = self.check_enrollment_no()
                if enrollment_no is None:
                    print("\033[91m{}\033[0m".format("Returning to admin menu...") ) # Operation aborted
                    return

                self.cursor.execute("SELECT COUNT(*) FROM student_details WHERE enrollment_no = %s;", (enrollment_no,))
                if self.cursor.fetchone()[0] == 0:
                    raise EnrollmentError("\033[91m{}\033[0m".format("Invalid enrollment number!"))

                self.prompt_for_update(enrollment_no)
                break

            except Exception as e:
                self.cursor.connection.rollback()
                print()
                print(f"Failed to update student detail: {e}")


    def prompt_for_update(self, enrollment_no):
        while True:
            self.cursor.execute(f"SELECT batch from student_details WHERE enrollment_no = %s;", (enrollment_no,))
            old_batch = self.cursor.fetchone()[0]
            flag = False
            print()
            print(
                "--------------------------------------------------------------------------------------------------------------------------")
            print("Which detail would you like to update?")
            print()
            print("1. Name")
            print("2. Department (will also require updating the batch and branch)")
            print("3. Branch")
            print("4. Batch")
            print("5. Email")
            print("6. Go back")
            print(
                "--------------------------------------------------------------------------------------------------------------------------")
            print()
            choice = input("Enter your choice (1-6): ")


            if choice == '1':

                new_value = input("Enter the new Name: ")
                if not all(x.isalpha() or x.isspace() for x in new_value):
                    raise InvalidInputError("\033[91m{}\033[0m".format("Name should consist of alphabets and spaces only."))
                column = 'name'
                self.execute_update(column, new_value, enrollment_no, flag)
                print()
                print("\033[92m{}\033[0m".format("Update operation completed successfully."))

            elif choice == '2':
                new_department, new_batch , new_branch = self.prompt_for_department_and_batch_and_branch()
                if new_batch == old_batch:
                    flag = True
                self.execute_update('department', new_department, enrollment_no, flag)
                self.execute_update('batch', new_batch, enrollment_no, flag)
                self.execute_update('branch', new_branch, enrollment_no, flag)
                print()
                print("\033[92m{}\033[0m".format("Update operation completed successfully."))

            elif choice == '3':
                self.cursor.execute(f"SELECT department from student_details WHERE enrollment_no = %s;", (enrollment_no,))
                depart = self.cursor.fetchone()[0]

                new_value = self.prompt_for_branch(depart)
                self.execute_update('branch', new_value, enrollment_no, flag)
                print()
                print("\033[92m{}\033[0m".format("Update operation completed successfully."))

            elif choice == '4':
                new_value = self.prompt_for_batch(enrollment_no)
                if new_value == old_batch:
                    flag = True
                self.execute_update('batch', new_value, enrollment_no, flag)
                print()
                print("\033[92m{}\033[0m".format("Update operation completed successfully."))

            elif choice == '5':
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

                while True:
                    try:
                        # Prompt the user to enter an email address
                        email = input("Enter new email: ")

                        if re.match(email_pattern, email):
                            self.execute_update('email', email, enrollment_no, flag)
                            print("\033[92m{}\033[0m".format("Update operation completed successfully."))
                            break
                        else:
                            raise InvalidInputError("\033[91m{}\033[0m".format(
                                "Invalid email address. Please enter a valid email address."))

                    except InvalidInputError as e:
                        print()
                        print(f"{e}")

            elif choice == '6':
                break

            else:
                print()
                print("\033[91m{}\033[0m".format("Invalid choice. Operation cancelled."))



    def execute_update(self, column, new_value, enrollment_no, flag):
        if flag != True:
            if column == 'batch':
                roll_no = self.generate_roll_no(new_value)
                query = f"UPDATE student_details SET roll_no = %s WHERE enrollment_no = %s;"
                self.cursor.execute(query, (roll_no, enrollment_no))
                self.cursor.connection.commit()

        query = f"UPDATE student_details SET {column} = %s WHERE enrollment_no = %s;"
        self.cursor.execute(query, (new_value, enrollment_no))
        self.cursor.connection.commit()


    def prompt_for_department_and_batch_and_branch(self):
        print()
        print("Select the new Department:")
        departments = ['SY1', 'SY2', 'SY3']
        for idx, dept in enumerate(departments, 1):
            print(f"{idx}. {dept}")
        dept_choice = input("Enter your choice: ")
        if dept_choice.isdigit() and 1 <= int(dept_choice) <= len(departments):
            new_department = departments[int(dept_choice) - 1]
        else:
            raise InvalidInputError("\033[91m{}\033[0m".format("Invalid choice for department."))

        ################################################################################################################

        new_batch = self.prompt_for_batch_based_on_department(new_department)
        new_branch = self.prompt_for_branch_based_on_department(new_department)
        return new_department, new_batch, new_branch

    def prompt_for_branch(self, department):
        return self.prompt_for_branch_based_on_department(department)

    def prompt_for_batch_based_on_department(self, department):
        dept_to_batches = {
            'SY1': ['A1', 'A2', 'A3'],
            'SY2': ['B1', 'B2', 'B3'],
            'SY3': ['C1', 'C2', 'C3']
        }
        print()
        print("Select the new Batch:")
        batches = dept_to_batches[department]
        for idx, batch in enumerate(batches, 1):
            print(f"{idx}. {batch}")
        batch_choice = input("Enter your choice: ")
        if batch_choice.isdigit() and 1 <= int(batch_choice) <= len(batches):
            return batches[int(batch_choice) - 1]
        else:
            raise InvalidInputError("\033[91m{}\033[0m".format("Invalid choice for batch."))


    def prompt_for_branch_based_on_department(self, department):
        print()
        # Branch selection logic
        print("Select Branch:")
        dept_to_branch = {
            'SY1': ['CE', 'IT', 'CSE'],
            'SY2': ['CST', 'CEA', 'CS&IT'],
            'SY3': ['AIML', 'AIDS', 'RAI']
        }
        branch = dept_to_branch.get(department, [])
        for idx, branches in enumerate(branch, 1):
            print(f"{idx}. {branches}")
        branch_choice = input("Enter your choice: ")
        if branch_choice.isdigit() and 1 <= int(branch_choice) <= len(branch):
            return branch[int(branch_choice) - 1]
        else:
            raise InvalidInputError("\033[91m{}\033[0m".format("Invalid choice for branch."))



    def prompt_for_batch(self, enrollment_no):
        # Fetch the current department of the student
        self.cursor.execute("SELECT department FROM student_details WHERE enrollment_no = %s;", (enrollment_no,))
        current_dept = self.cursor.fetchone()[0]

        # Map departments to their respective batch options
        dept_to_batches = {
            'SY1': ['A1', 'A2', 'A3'],
            'SY2': ['B1', 'B2', 'B3'],
            'SY3': ['C1', 'C2', 'C3']
        }

        # Determine the correct batch options based on the current department
        available_batches = dept_to_batches.get(current_dept, [])
        print("Select the new Batch based on the current Department:")
        for idx, batch in enumerate(available_batches, 1):
            print(f"{idx}. {batch}")

        batch_choice = input("Enter your choice: ")
        if batch_choice.isdigit() and 1 <= int(batch_choice) <= len(available_batches):
            return available_batches[int(batch_choice) - 1]
        else:
            raise InvalidInputError("\033[91m{}\033[0m".format("Invalid choice for batch."))

    def student_marks(self):
        try:
            enrollment_no = self.check_enrollment_no()
            if enrollment_no is None:
                print("Returning to admin menu...")  # Operation aborted
                return

            self.cursor.execute("SELECT COUNT(*) FROM student_details WHERE enrollment_no = %s;", (enrollment_no,))
            if self.cursor.fetchone()[0] == 0:
                raise EnrollmentError("\033[91m{}\033[0m".format("Invalid enrollment number!"))

            while True:
                test_table = self.select_test()
                if not test_table:
                    return  # Go back to main menu

                subject_column = self.select_subject()
                if not subject_column:
                    continue  # Go back to test selection

                if self.update_marks(test_table, subject_column, enrollment_no):
                    continue  # Go back to test selection

        except Exception as e:
            self.cursor.connection.rollback()
            print("\033[91m{}\033[0m".format(f"\nFailed to update student marks: {e}"))


    def select_test(self):
        while True:
            print("\nSelect Test:")
            print("1. T1\n2. T2\n3. T3\n4. T4\n5. Go back")
            test_choice = input("Enter choice (1-5): ")

            if test_choice == '5':
                return None  # User chose to go back

            test_map = {
                '1': 't1_marks',
                '2': 't2_marks',
                '3': 't3_marks',
                '4': 't4_marks',
            }

            if test_choice in test_map:
                return test_map[test_choice]
            else:
                print("\033[91m{}\033[0m".format("\nInvalid choice."))

    def select_subject(self):
        subjects = ['ps', 'de', 'fcsp_1', 'fsd_1', 'etc', 'ci']
        while True:
            print("\nSelect Subject:")
            for index, subject in enumerate(subjects, start=1):
                print(f"{index}. {subject}")
            print(f"{len(subjects) + 1}. Go back")
            subject_choice = int(input("Enter choice: "))

            if subject_choice == len(subjects) + 1:
                return None  # User chose to go back

            if 1 <= subject_choice <= len(subjects):
                return subjects[subject_choice - 1]
            else:
                print("\033[91m{}\033[0m".format("\nInvalid choice."))

    def update_marks(self, test_table, subject_column, enrollment_no):
        while True:
            try:
                marks = int(input(f"\nEnter marks for {subject_column} (0-25): "))

                if 0 <= marks <= 25:
                    update_query = f"""
                                    UPDATE {test_table}
                                    SET {subject_column} = %s
                                    WHERE enrollment_no = %s;
                                    """
                    self.cursor.execute(update_query, (marks, enrollment_no))
                    self.cursor.connection.commit()
                    print("\033[92m{}\033[0m".format("\nMarks updated successfully."))
                    return True
                else:
                    raise InvalidMarksError("\033[91m{}\033[0m".format("Marks must be between 0 and 25!"))
            except InvalidMarksError as e:
                print(e)



    def display_student(self):
     try:
        enrollment_no = self.check_enrollment_no()
        if enrollment_no is None:
            print("Returning to admin menu...")  # Operation aborted
            return

        while True:
                print()
                print("What would you like to view?")
                print()
                print("Enter 1 to view student details")
                print("Enter 2 to view student marks")
                print("Enter 3 to go back")
                print()

                print("Your choice: ", end="")
                choice = int(input())

                if choice == 1:
                    self.details(enrollment_no)
                elif choice == 2:
                    self.marks(enrollment_no)
                elif choice == 3:
                    break
                else:
                    print("\033[91m{}\033[0m".format("Please enter valid choice (From 1 - 3)"))

     except Exception as e:
        print()
        print(f"Failed to display: {e}")


user = APM()
user.login()
