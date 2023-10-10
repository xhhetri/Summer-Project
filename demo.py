import mysql.connector
import smtplib
import tkinter as tk
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import ttk, messagebox, filedialog

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


class StudentInfoWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Information")

        # Create a frame for the entire content
        self.content_frame = tk.Frame(master, bg='#2d3032')
        self.content_frame.pack(padx=20, pady=20)

        # Create a frame for the header
        self.header_frame = tk.Frame(self.content_frame, bg='#2d3032')
        self.header_frame.pack()

        self.LoginLabel = tk.Label(self.header_frame, text='Student Information', bg='#2d3032',
                                   font=('Helvetica', 20), fg='white')
        self.LoginLabel.pack(pady=(0, 10))

        # Create a frame for input fields
        self.input_frame = tk.Frame(self.content_frame, bg='#2d3032')
        self.input_frame.pack()

        self.nameLabel = tk.Label(self.input_frame, text='Student Name:', bg='#2d3032',
                                  font=('Helvetica', 12), fg='white')
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.nameTextbox = tk.Entry(self.input_frame, font=('Helvetica', 12), width=25,
                                    borderwidth='2', relief='ridge')
        self.nameTextbox.grid(row=0, column=1, padx=10, pady=10)

        self.classLabel = tk.Label(self.input_frame, text='Class:', bg='#2d3032',
                                   font=('Helvetica', 12), fg='white')
        self.classLabel.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.classTextbox = tk.Entry(self.input_frame, font=('Helvetica', 12), width=25,
                                     borderwidth='2', relief='ridge')
        self.classTextbox.grid(row=1, column=1, padx=10, pady=10)

        self.rollLabel = tk.Label(self.input_frame, text='Roll Number:', bg='#2d3032',
                                  font=('Helvetica', 12), fg='white')
        self.rollLabel.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.rollTextbox = tk.Entry(self.input_frame, font=('Helvetica', 12), width=25,
                                    borderwidth='2', relief='ridge')
        self.rollTextbox.grid(row=2, column=1, padx=10, pady=10)

        self.termLabel = tk.Label(self.input_frame, text='Term:', bg='#2d3032',
                                  font=('Helvetica', 12), fg='white')
        self.termLabel.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.termTextbox = tk.Entry(self.input_frame, font=('Helvetica', 12), width=25,
                                    borderwidth='2', relief='ridge')
        self.termTextbox.grid(row=3, column=1, padx=10, pady=10)

        self.emailLabel = tk.Label(self.input_frame, text='Receiver Email:', bg='#2d3032',
                                   font=('Helvetica', 12), fg='white')
        self.emailLabel.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.emailTextbox = tk.Entry(self.input_frame, font=('Helvetica', 12), width=25,
                                     borderwidth='2', relief='ridge')
        self.emailTextbox.grid(row=4, column=1, padx=10, pady=10)

        # Create a frame for buttons
        self.btns_frame = tk.Frame(self.content_frame, bg='#2d3032')
        self.btns_frame.pack()

        self.btnSubmit = tk.Button(self.btns_frame, text='Submit', bg='light grey',
                                   font=('Helvetica', 12), fg='black', padx=25,
                                   pady=5, command=self.show_data)
        self.btnSubmit.grid(row=0, column=0, padx=20, pady=20)

        self.btnCancel = tk.Button(self.btns_frame, text='Send mail', bg='light grey',
                                   font=('Helvetica', 12), fg='black', padx=25,
                                   pady=5, command=self.send_email)
        self.btnCancel.grid(row=0, column=1, padx=20, pady=20)



    def generate_table_labels(self, class_no):
        # Dictionary to map class numbers to table names and subjects
        class_info = {
            '1': {
                'table_name': 'class_one',
                'subjects': ['Social', 'Science', 'Maths', 'Nepali', 'English']
            },
            '2': {
                'table_name': 'class_two',
                'subjects': ['Social', 'Science', 'Maths', 'Nepali', 'English', 'Moral/Communication']
            },
            '3': {
                'table_name': 'class_three',
                'subjects': ['Social', 'Science', 'Maths', 'Nepali', 'English', 'Communication']
            },
            '4': {
                'table_name': 'class_four',
                'subjects': ['social/moral', 'Science', 'maths', 'Nepali', 'English', 'Communication']
            },
            '5': {
                'table_name': 'class_five',
                'subjects': ['social/moral', 'Science', 'maths', 'Nepali', 'English', 'Communication']
            }
        }

        if class_no in class_info:
            class_data = class_info[class_no]
            table_name = class_data['table_name']
            subjects = class_data['subjects']
            student_name = self.nameTextbox.get()
            roll_no = self.rollTextbox.get()
            term = self.termTextbox.get()  # Get the term input

            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    port='3307',
                    user='root',
                    password='root',
                    database='resultsystem',
                )
                cursor = conn.cursor()
                # Include the term in the SQL query
                query = f"SELECT {', '.join(subjects)} FROM {table_name} WHERE student_name = %s AND roll_no = %s AND term = %s"
                cursor.execute(query, (student_name, roll_no, term))
                data = cursor.fetchone()

                query = f"SELECT room_number FROM seat_placement WHERE {roll_no} >= roll_from AND {roll_no} <= roll_to;"
                cursor.execute(query)
                seat = cursor.fetchone()

                conn.close()

                return subjects, data, seat
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Database error: {err}")
                return [], [], []


    def show_data(self):
        # Generate the table data
        class_no = self.classTextbox.get()
        subjects, data, seat = self.generate_table_labels(class_no)
        roll_no = self.rollTextbox.get()
        term = self.termTextbox.get()

        if subjects and data:
            # Create a new window to display the data
            result_window = tk.Toplevel(self.master,bg="#2d3032")
            result_window.title("Student Result")

            result_label = tk.Label(result_window,fg= "white", bg="#2d3032",
                                    text=f"Result for {self.nameTextbox.get()} in grade {class_no} of {term} term",
                                    font=('Helvetica', 14))
            result_label.grid(row=1, column=0, columnspan=8, padx=10, pady=10)

            # Create and populate the Treeview
            tree = ttk.Treeview(result_window,
                                columns=(
                                "SNo", "Subject", "Full Marks", "Pass Marks", "Marks Obtained", "Percentage", "Grade"))
            tree.grid(row=2, column=0, padx=10, pady=10)

            tree.column("#0", width=40)  # This is for the treeview itself
            tree.column("#1", width=50)  # SNo
            tree.column("#2", width=150)  # Subject
            tree.column("#3", width=80)  # Full Marks
            tree.column("#4", width=80)  # Pass Marks
            tree.column("#5", width=120)  # Marks Obtained
            tree.column("#6", width=80)  # Percentage
            tree.column("#7", width=80)  # Grade

            # Add column headings
            tree.heading("#1", text="SNo")
            tree.heading("#2", text="Subject")
            tree.heading("#3", text="Full Marks")
            tree.heading("#4", text="Pass Marks")
            tree.heading("#5", text="Marks Obtained")
            tree.heading("#6", text="Percentage")
            tree.heading("#7", text="Grade")

            # Populate the Treeview with data and calculate percentage
            for i, (subject, marks_obtained) in enumerate(zip(subjects, data)):
                full_marks = 100  # Assuming full marks are 100 for all subjects
                pass_marks = 40  # Assuming pass marks are 40 for all subjects
                percentage = (marks_obtained / full_marks) * 100
                grade = "Pass" if marks_obtained >= pass_marks else "Fail"
                tree.insert("", "end", values=(
                i + 1, subject, full_marks, pass_marks, marks_obtained, f'{percentage:.2f}%', grade))

        else:
            messagebox.showerror("Error", "Student record not found")

        btnPrint = tk.Button(result_window, text='Print', bg='light grey',
                                  font=('Helvetica', 12), fg='black', padx=25,
                                  pady=5, command=self.print_data)
        btnPrint.grid(row=1, column=2, padx=20, pady=20)

    def print_data(self):
        # Generate the table data
        class_no = self.classTextbox.get()
        subjects, data, seat = self.generate_table_labels(class_no)
        student_name = self.nameTextbox.get()
        roll_no = self.rollTextbox.get()
        term = self.termTextbox.get()

        if subjects and data:
            # Create a PDF document
            pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if pdf_filename:
                try:
                    # Create a PDF document
                    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
                    elements = []

                    # Add a title to the PDF
                    title = f"Result for {student_name} in grade {class_no} of {term} term"
                    elements.append(Table([[title]], colWidths=[500], style=[('ALIGN', (0, 0), (-1, -1), 'CENTER')]))

                    # Create a PDF table from the HTML table
                    table_data = [[
                        "SNo", "Subject", "Full Marks", "Pass Marks", "Marks Obtained", "Percentage", "Grade"
                    ]]

                    for index, subj in enumerate(subjects, start=1):
                        marks_obtained = data[index - 1]
                        full_marks = 100
                        pass_marks = 40
                        percentage = (marks_obtained / full_marks) * 100
                        grade = "Pass" if marks_obtained >= pass_marks else "Fail"

                        table_data.append([
                            index, subj, full_marks, pass_marks, marks_obtained, f'{percentage:.2f}%', grade
                        ])

                    pdf_table = Table(table_data, colWidths=[30, 100, 60, 60, 70, 80, 60])
                    pdf_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))

                    elements.append(pdf_table)

                    # Build the PDF document
                    doc.build(elements)
                    messagebox.showinfo("PDF Created", "PDF file has been created successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while creating the PDF: {str(e)}")
        else:
            messagebox.showerror("Data Not Found", "No data found for the given input.")


    def generate_html_table(self):
        # Generate the table data
        class_no = self.classTextbox.get()
        subjects, data, seat = self.generate_table_labels(class_no)
        student_name = self.nameTextbox.get()
        roll_no = self.rollTextbox.get()
        term = self.termTextbox.get()

        if subjects and data:
            # Fetch data from the appropriate class table based on class_no and term
            if class_no.lower() in ['1', 'one']:
                class_table = 'class_one'
                subject = ['Social', 'Science', 'Maths', 'Nepali', 'English']
                query = f"SELECT social, science, maths, nepali, english FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['2', 'two']:
                class_table = 'class_two'
                subject = ['Social', 'Science', 'Maths', 'Nepali', 'English', 'Moral/Communication']
                query = f"SELECT social, science, maths, nepali, english, moral FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['3', 'three']:
                class_table = 'class_three'
                subject = ['Social', 'Science', 'Maths', 'Nepali', 'English', 'Communication']
                query = f"SELECT social, science, maths, nepali, english, moral_comm FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['4', 'four']:
                class_table = 'class_four'
                subject = ['social/moral', 'Science', 'maths', 'Nepali', 'English', 'Communication']
                query = f"SELECT social_moral, science, maths, nepali, english, comm FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['5', 'five']:
                class_table = 'class_five'
                subject = ['social/moral', 'Science', 'maths', 'Nepali', 'English', 'Communication']
                query = f"SELECT social_moral, science, maths, nepali, english, comm FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            else:
                messagebox.showerror("Error", "Invalid class number")
                return
            # Create an HTML table string
            table_html = (
                "<table border='1'><tr><th>SNo</th><th>Subject</th><th>Full Marks</th><th>Pass Marks</th><th>Marks Obtained</th><th>Grade</th></tr>")
            for index, subj in enumerate(subject, start=1):
                marks_obtained = data[index - 1]
                if marks_obtained >= 40:
                    grade = "Pass"
                else:
                    grade = "Fail"
                table_html += f"<tr><td>{index}</td><td>{subj}</td><td>100</td><td>40</td><td>{marks_obtained}</td><td>{grade}</td></tr>"
            table_html += "</table>"
            return table_html

    def send_email(self):
        # Generate the table data
        class_no = self.classTextbox.get()
        subjects, data, seat = self.generate_table_labels(class_no)
        student_name = self.nameTextbox.get()
        receiver_email = self.emailTextbox.get()
        roll_no = self.rollTextbox.get()
        term = self.termTextbox.get()

        if subjects and data:
            # Fetch data from the appropriate class table based on class_no and term
            if class_no.lower() in ['1', 'one']:
                class_table = 'class_one'
                subject = ['Social', 'Science', 'Maths', 'Nepali', 'English']
                query = f"SELECT social, science, maths, nepali, english FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['2', 'two']:
                class_table = 'class_two'
                subject = ['Social', 'Science', 'Maths', 'Nepali', 'English', 'Moral/Communication']
                query = f"SELECT social, science, maths, nepali, english, moral FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['3', 'three']:
                class_table = 'class_three'
                subject = ['Social', 'Science', 'Maths', 'Nepali', 'English', 'Communication']
                query = f"SELECT social, science, maths, nepali, english, moral_comm FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['4', 'four']:
                class_table = 'class_four'
                subject = ['social/moral', 'Science', 'maths', 'Nepali', 'English', 'Communication']
                query = f"SELECT social_moral, science, maths, nepali, english, comm FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

            elif class_no.lower() in ['5', 'five']:
                class_table = 'class_five'
                subject = ['social/moral', 'Science', 'maths', 'Nepali', 'English', 'Communication']
                query = f"SELECT social_moral, science, maths, nepali, english, comm FROM {class_table} WHERE student_name = %s AND roll_no = %s AND term = %s"

        if subjects and data:
            # Compose email
            sender_email = "oshan9814158662@gmail.com"
            sender_password = "avhrfskligqymaof"  # Replace with your password

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"Student Information for Roll Number {roll_no} (Term {term})"

            body = f"Dear {student_name},\n\nHere is your student information for Roll Number {roll_no} (Term {term}):\n"
            table_html = (
                "<table style='border-collapse: collapse;'>"
                "<tr><th style='border: 1px solid black;'>SNo</th><th style='border: 1px solid black;'>Subject</th>"
                "<th style='border: 1px solid black;'>Full Marks</th><th style='border: 1px solid black;'>Pass Marks</th>"
                "<th style='border: 1px solid black;'>Marks Obtained</th><th style='border: 1px solid black;'>Percentage</th><th style='border: 1px solid black;'>Grade</th></tr>"
            )
            for index, subj in enumerate(subjects, start=1):
                marks_obtained = data[index - 1]
                full_marks = 100
                pass_marks = 40
                percentage = (marks_obtained / full_marks) * 100
                grade = "Pass" if marks_obtained >= pass_marks else "Fail"

                table_html += (
                    f"<tr>"
                    f"<td style='border: 1px solid black;'>{index}</td>"
                    f"<td style='border: 1px solid black;'>{subj}</td>"
                    f"<td style='border: 1px solid black;'>{full_marks}</td>"
                    f"<td style='border: 1px solid black;'>{pass_marks}</td>"
                    f"<td style='border: 1px solid black;'>{marks_obtained}</td>"
                    f"<td style='border: 1px solid black;'>{percentage:.2f}%</td>"
                    f"<td style='border: 1px solid black;'>{grade}</td>"
                    f"</tr>"
                )
            table_html += "</table>"
            # Now you have added the Percentage column to the HTML table

            msg.attach(MIMEText(body, 'plain'))
            msg.attach(MIMEText(table_html, 'html'))


            try:
                # Send email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, receiver_email, text)
                server.quit()

                messagebox.showinfo("Email Sent", "Email sent successfully.")
            except Exception as e:
                messagebox.showerror("Email Error", f"An error occurred while sending the email: {str(e)}")
        else:
            messagebox.showerror("Data Not Found", "No data found for the given input.")

    def close_window(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = StudentInfoWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
