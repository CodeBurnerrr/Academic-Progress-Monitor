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



user = APM()
user.login()
