#Sdev220 Final Proj Starter
#Cole Shane
#Cheyanne Madara

#In it's current state this will receive input for 1 student and their guardian. This is saved to an object
#and it will then print it out. Eventually this will be bound to a GUI


from datetime import date
class Person:
    def __init__(self, id, first_name, last_name, date_of_birth, contact_number, email, street, city):
        self.id = id
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
    def __init__(self, student_id, id, street, city, grade, parent_first_name, parent_last_name, **kwargs):
        super().__init__(id=id, street=street, city=city, **kwargs)
        self.student_id = student_id
        self.grade = grade
        self.parent_first_name = parent_first_name
        self.parent_last_name = parent_last_name
        self.parent_street = street
        self.parent_city = city

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
        return f"Parent ID: {self.parent_id}, Guardian: {self.is_guardian}, Name: {self.get_full_name()}"


class StudentApp:
    def __init__(self):
        self.students_list = []

    def create_parent(self):
        # Get parent info from user input
        parent_first_name = input("Enter Parent's First Name: ")
        parent_last_name = input("Enter Parent's Last Name: ")
        parent_street = input("Enter Street Address: ")
        parent_city = input("Enter City: ")

        # Create Parent instance
        parent = Parent(parent_first_name=parent_first_name, parent_last_name=parent_last_name,
                        parent_street=parent_street, parent_city=parent_city)

        # Add parent to list
        self.students_list.append(parent)

        # Display student details
        self.display_student_details()

    def create_student(self):
        try:
            # Get student details from user input
            student_id = int(input("Enter Student ID: "))
            student_first_name = input("Enter First Name: ")
            student_last_name = input("Enter Last Name: ")
            student_dob = date.fromisoformat(input("Enter Date of Birth (YYYY-MM-DD): "))
            student_contact = input("Enter Contact Number: ")
            student_email = input("Enter Email: ")
            student_grade = int(input("Enter Grade: "))
            parent_first_name = input("Enter Parent's First Name: ")
            parent_last_name = input("Enter Parent's Last Name: ")
            parent_street = input("Enter Parent's Street Address: ")
            parent_city = input("Enter Parent's City: ")

            # Create Student instance
            student = Student(student_id=student_id, grade=student_grade,
                              id=student_id, first_name=student_first_name, last_name=student_last_name,
                              date_of_birth=student_dob, contact_number=student_contact, email=student_email,
                              parent_first_name=parent_first_name, parent_last_name=parent_last_name,
                              street=parent_street, city=parent_city)

            # Add student to the list
            self.students_list.append(student)

            # Display student details
            self.display_student_details()

        except ValueError:
            print("Invalid input. Please enter correct values for Student ID, Date of Birth, and Grade.")

    def display_student_details(self):
        # Display all students with numbering
        details = ""
        for i, student in enumerate(self.students_list, start=1):
            details += f"{i}. {student.get_student_details()}\n"

        print(details)

if __name__ == "__main__":
    app = StudentApp()
    app.create_student()
    app.create_parent
