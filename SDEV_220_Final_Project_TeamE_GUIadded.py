import tkinter as tk
from datetime import date
from tkinter import messagebox
import csv
import json

class Person:
    def __init__(self, person_id, first_name, last_name, date_of_birth, contact_number, email, street, city):
        self.id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.contact_number = contact_number
        self.email = email
        self.street = street
        self.city = city

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Student(Person):
    def __init__(self, student_id, person_id, grade, parent_first_name, parent_last_name, **kwargs):
        super().__init__(person_id=person_id, street="", city="", email="", **kwargs)
        self.student_id = student_id
        self.grade = grade
        self.parent_first_name = parent_first_name
        self.parent_last_name = parent_last_name

    def get_student_details(self):
        return f"Student ID: {self.student_id}, Grade: {self.grade}, " \
               f"Name: {self.first_name} {self.last_name}, " \
               f"Parent: {self.parent_first_name} {self.parent_last_name}"

class Parent(Person):
    def __init__(self, student_id, is_primary_guardian, **kwargs):
        super().__init__(**kwargs)
        self.parent_id = student_id
        self.is_primary_guardian = is_primary_guardian

    def get_parent_details(self):
        return f"Parent ID: {self.parent_id}, Guardian: {self.is_primary_guardian}, Name: {self.get_full_name()}"

class StudentApp:
    def __init__(self):
        self.students_list = []


    def create_parent(self, parent_first_name, parent_last_name, parent_street, parent_city, student_id, email):
        # Create Parent instance
        parent = Parent(
            student_id=student_id,
            person_id=student_id,
            is_primary_guardian=True,
            first_name=parent_first_name,
            last_name=parent_last_name,
            date_of_birth=date.today(),
            contact_number="",
            email=email,
            street=parent_street,
            city=parent_city
        )

        # Add parent to list
        self.students_list.append(parent)

        # Display student details
        self.display_details()

    def create_student(self, student_id, grade, first_name, last_name, date_of_birth, contact_number,
                        parent_first_name, parent_last_name):
        # Create Student instance
        student = Student(
            student_id=student_id,
            grade=grade,
            person_id=student_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            contact_number=contact_number,
            parent_first_name=parent_first_name,
            parent_last_name=parent_last_name
        )

        # Add student to the list
        self.students_list.append(student)

        # Display student details
        print("Student created. Please create parent.")

    def display_details(self):
        # Display all details with numbering
        details = ""
        for i, person in enumerate(self.students_list, start=1):
            if isinstance(person, Student):
                details += f"{i}. {person.get_student_details()}\n"
            elif isinstance(person, Parent):
                details += f"{i}. {person.get_parent_details()}\n"

        print(details)

class StudentAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student App")
        self.app = StudentApp()

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Labels
        tk.Label(self.root, text="Student Information").grid(row=0, column=0, columnspan=2)

        # Gather student Information
        self.create_entry_widgets(1, "Student ID:", "student_id_entry")
        self.create_entry_widgets(2, "Student Grade:", "student_grade_entry")
        self.create_entry_widgets(3, "Student First Name:", "student_first_name_entry")
        self.create_entry_widgets(4, "Student Last Name:", "student_last_name_entry")
        self.create_entry_widgets(5, "Student Date of Birth:", "student_date_of_birth_entry")
        self.create_entry_widgets(6, "Student Contact Number:", "student_contact_number_entry")
        

        # Label
        tk.Label(self.root, text="Parent Information").grid(row=8, column=0, columnspan=2)

        # Gather parent information
        self.create_entry_widgets(9, "Parent First Name:", "parent_first_name_entry")
        self.create_entry_widgets(10, "Parent Last Name:", "parent_last_name_entry")
        self.create_entry_widgets(11, "Parent Email Address:", "parent_email_entry")
        self.create_entry_widgets(12, "Parent Street Address:", "parent_street_entry")
        self.create_entry_widgets(13, "Parent City:", "parent_city_entry")

        # Buttons
        tk.Button(self.root, text="Create Student", command=self.create_student).grid(row=14, column=0, columnspan=2)
        tk.Button(self.root, text="Create Parent", command=self.create_parent).grid(row=15, column=0, columnspan=2)
        tk.Button(self.root, text="Export to CSV/JSON", command=self.export_to_csv).grid(row=16, column=0, columnspan=2)

    def create_entry_widgets(self, row, label_text, entry_name):
        tk.Label(self.root, text=label_text).grid(row=row, column=0)
        entry_widget = tk.Entry(self.root)
        entry_widget.grid(row=row, column=1)
        setattr(self, entry_name, entry_widget)

    def create_student(self):
        if not self.validate_student_entries():
            messagebox.showerror("Error", "Please fill out all student information fields.")
            return

        try:
            student_id = int(self.student_id_entry.get())
            grade = int(self.student_grade_entry.get())
            first_name = self.student_first_name_entry.get()
            last_name = self.student_last_name_entry.get()
            date_of_birth = date.fromisoformat(self.student_date_of_birth_entry.get())
            contact_number = self.student_contact_number_entry.get()
            parent_first_name = self.parent_first_name_entry.get()
            parent_last_name = self.parent_last_name_entry.get()

            # Call create_student method in StudentApp
            self.app.create_student(
                student_id, grade, first_name, last_name, date_of_birth, contact_number,
                 parent_first_name, parent_last_name
            )

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter correct values for Student ID, Date of Birth, and Grade.")

    def create_parent(self):
        # Get data from entry fields
        if not self.validate_parent_entries():
            messagebox.showerror("Error", "Please fill out all parent information fields.")
            return
        try:
            parent_first_name = self.parent_first_name_entry.get()
            parent_last_name = self.parent_last_name_entry.get()
            email = self.parent_email_entry.get()
            parent_street = self.parent_street_entry.get()
            parent_city = self.parent_city_entry.get()
            person_id = int(self.student_id_entry.get())  # Assuming student_id is the person_id for the parent

            # Create parent
            self.app.create_parent(parent_first_name, parent_last_name, parent_street, parent_city, person_id,email)

        except ValueError:
            messagebox.showerror("Error", "Invalid input for Parent ID.")

    def validate_student_entries(self):
        # Check if all student entry fields are filled
        return all([
            self.student_id_entry.get(),
            self.student_grade_entry.get(),
            self.student_first_name_entry.get(),
            self.student_last_name_entry.get(),
            self.student_date_of_birth_entry.get(),
            self.student_contact_number_entry.get(),
            self.parent_first_name_entry.get(),
            self.parent_last_name_entry.get(),
    ])
    
    def validate_parent_entries(self):
        # Check if all parent entry fields are filled
        return all([
            self.parent_first_name_entry.get(),
            self.parent_last_name_entry.get(),
            self.parent_email_entry.get(),
            self.parent_street_entry.get(),
            self.parent_city_entry.get(),
            self.student_id_entry.get(),  # Assuming student_id is the person_id for the parent
    ])

    def export_to_csv(self):
        # Get all items in the students_list
        items = self.app.students_list

        # Prepare data for student_info.csv
        student_info_csv_data = []
        parent_info_csv_data = []

        # Prepare data for student_info.json
        student_info_json_data = []
        parent_info_json_data = []

        for person in items:
            if isinstance(person, Student):
                student_info_csv_data.append([
                    person.student_id,
                    person.get_full_name(),
                    person.grade,
                    person.parent_first_name,
                    person.parent_last_name
                ])
                student_info_json_data.append({
                    "student_id": person.student_id,
                    "name": person.get_full_name(),
                    "grade": person.grade,
                    "parent_first_name": person.parent_first_name,
                    "parent_last_name": person.parent_last_name
                })
            elif isinstance(person, Parent):
                parent_info_csv_data.append([
                    person.parent_id,
                    person.get_full_name(),
                    person.is_primary_guardian,
                    person.email,
                    person.street,
                    person.city
                ])
                parent_info_json_data.append({
                    "parent_id": person.parent_id,
                    "name": person.get_full_name(),
                    "is_primary_guardian": person.is_primary_guardian,
                    "email":person.email,
                    "street": person.street,
                    "city": person.city
                })

        # Write to CSV files
        self.write_to_csv("student_info.csv", ["Student ID", "Name", "Grade", "Parent First Name", "Parent Last Name"], student_info_csv_data)
        self.write_to_csv("parent_info.csv", ["Parent ID", "Name", "Email", "Primary Guardian", "Street", "City"], parent_info_csv_data)

        # Write to JSON files
        self.write_to_json("student_info.json", student_info_json_data)
        self.write_to_json("parent_info.json", parent_info_json_data)


        # Clear the entry widgets
        self.clear_entry_widgets()

        messagebox.showinfo("Export Successful", "Data exported to CSV files successfully.")

    def write_to_csv(self, filename, header, data):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(data)

    def write_to_json(self, filename, data):
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=2)

    def clear_entry_widgets(self):
        self.student_id_entry.delete(0, 'end')
        self.student_grade_entry.delete(0, 'end')
        self.student_first_name_entry.delete(0, 'end')
        self.student_last_name_entry.delete(0, 'end')
        self.student_date_of_birth_entry.delete(0, 'end')
        self.student_contact_number_entry.delete(0, 'end')
        self.parent_first_name_entry.delete(0, 'end')
        self.parent_last_name_entry.delete(0, 'end')
        self.parent_email_entry.delete(0, 'end')
        self.parent_street_entry.delete(0, 'end')
        self.parent_city_entry.delete(0, 'end')

        
if __name__ == "__main__":
    root = tk.Tk()
    app_gui = StudentAppGUI(root)
    root.mainloop()
