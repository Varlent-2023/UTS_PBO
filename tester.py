import datetime

# User
class User:
    def __init__(self, user_id, password, user_type):
        if not isinstance(user_id, str) or not isinstance(password, str) or not isinstance(user_type, str):
            raise ValueError("user_id, password, and user_type must be strings")
        self._user_id = user_id
        self._password = password
        self._user_type = user_type

    def login(self, user_id, password):
        return True

    def get_user_id(self):
        return self._user_id
    
    def logout(self):
        return False
    
    def get_user_type(self):
        return self._user_type
    
    def report_bug(self, operator, bug_description):
        if not isinstance(operator, Operator):
            raise ValueError("Invalid operator object")
        bug_report = operator.create_bug_report(self, bug_description)
        return bug_report


# Course
class Course:
    def __init__(self, course_name):
        self.course_name = course_name
        self.students = []

    def enroll_student(self, user):
        if not isinstance(user, User):
            raise ValueError("Invalid user object")
        if user not in self.students:
            self.students.append(user)
            return f"Student with user id {user.get_user_id()} has been enrolled in {self.course_name}."
        else:
            return f"Student with user id {user.get_user_id()} is already enrolled in {self.course_name}."

    def unenroll_student(self, user):
        if not isinstance(user, User):
            raise ValueError("Invalid user object")
        if user in self.students:
            self.students.remove(user)
            return f"Student with user id {user.get_user_id()} has been unenrolled from {self.course_name}."
        else:
            raise ValueError(f"Student with user id {user.get_user_id()} is not enrolled in {self.course_name}.")
    def __str__(self):
        return self.course_name

# Operator
class Operator(User):
    def __init__ (self, user_id, password) -> None:
        super().__init__(user_id, password, 'operator')
        self._operatorid = user_id

    def createBilling(self, *args):
        new_bill = Billing (*args)
        return new_bill

    def create_user_account(self, user_id, password, user_type):
        if user_type == "student":
            return Student(user_id, password)
        elif user_type == "Dosen":
            return Dosen(user_id, password)
        elif user_type == "operator":
            return Operator(user_id, password)
        else:
            return None
        
    def confirm_payment(self, student, payment):
        if not isinstance(student, Student):
            raise ValueError("Invalid student object")
        student.confirm_payment(payment)

    def create_bug_report(self, user, bug_description):
        if not isinstance(user, User):
            raise ValueError("Invalid user object")
        bug_report = BugReport(user, bug_description)
        return bug_report
    
    def upload_krs_schedule(self, schedule_file):
        krs_schedule = KRSSchedule(self, schedule_file)
        return f"Operator {self.get_user_id()} has uploaded KRS schedule: {krs_schedule.get_schedule_file()}."


# Payment
class Billing:
    def __init__(self, studentID, Amount, Desc) -> None:
        self.studentID = studentID
        self.Amount = Amount
        self.Decs = Desc

# Proffesor
class Dosen(User):
    def __init__ (self, user_id, password) -> None:
        super().__init__(user_id, password, 'Dosen')
        self._dosenid = user_id
        self._course = []

    def add_course(self, course):
        self._course.append(course)
        return self._course

    def input_attendance(self, course, student, attendance_status):
        attendance = Attendance(course, student, attendance_status)
        return attendance

    def input_grade(self, student, course,grade):
        if not isinstance(student, Student):
            raise ValueError("Invalid student object")
        student.add_grade(course, grade)

    def update_schedule(self, student, new_schedule):
        if not isinstance(student, Student):
            raise ValueError("Invalid student object")
        student.update_schedule(new_schedule)
    
    def get_user_id(self):
        return self._user_id

# Student
class Student(User):
    def __init__(self, user_id, password):
        super().__init__(user_id, password, 'student')
        self._StudentID = user_id
        self._grade = {}
        self._schedule = {}
        self._payment_bill = {}
        self._payment_status = False
        self._courses = [] 
        self._bill = 0

    def enroll_in_course(self, course):
        self._courses.append(course)

    def get_courses(self):
        return self._courses
    
    def add_grade(self, course, grade):
        self._grade[course] = grade

    def view_grades(self):
        return {str(course): grade for course, grade in self._grade.items()} 
    
    def view_schedule(self):
        return self._schedule
    
    def view_payment_bill(self):
        return self._payment_bill
    
    def confirm_payment(self, payment):
        if payment:
            self._payment_status = True
        
    def view_payment_status(self):
        return self._payment_status

    def set_bill(self, amount):
        self._bill = amount

    def get_bill(self):
        return self._bill
    
    def choose_krs(self, krs_type):
        if krs_type.lower() not in ["paket", "non paket"]:
            raise ValueError("Invalid KRS type. Choose either 'paket' or 'non paket'")
        self._krs_type = krs_type
        return f"Student {self.get_user_id()} has chosen {self._krs_type} KRS."
    
    def upload_certificate(self, certificate_file):
        certificate = Certificate(self, certificate_file)
        return f"Student {self.get_user_id()} has uploaded certificate: {certificate.get_certificate_file()}."

# Attendance
class Attendance:
    def __init__(self, user, date, is_present):
        self._user = user
        self._date = date
        self._is_present = is_present

    @staticmethod
    def get_current_date():
        return datetime.datetime.now()

    def mark_attendance(self, is_present):
        self._is_present = is_present
        self._date = self.get_current_date()
        return f"Attendance marked for user {self._user.get_user_id()} on {self._date}. Present: {self._is_present}"

# Bug report
class BugReport:
    def __init__(self, user, bug_description):
        self._user = user
        self._bug_description = bug_description
        self._ticket_id = self.generate_ticket_id()

    def generate_ticket_id(self):
        return f"{self._user.get_user_id()}-{hash(self._bug_description)}"

    def get_ticket_id(self):
        return self._ticket_id

    def get_bug_description(self):
        return self._bug_description


# Certificate
class Certificate:
    def __init__(self, user, certificate_file):
        self._user = user
        self._certificate_file = certificate_file

    def get_certificate_file(self):
        return self._certificate_file
    

# KRS
class KRSSchedule:
    def __init__(self, operator, schedule_file):
        self._operator = operator
        self._schedule_file = schedule_file

    def get_schedule_file(self):
        return self._schedule_file


# Tester
def main():
    admin = Operator("Admin", "adminpass")
    operator = Operator("Admin", "adminpass")
    student = admin.create_user_account("student1", "studentpass", "student")
    student = admin.create_user_account("studen1", "studentpass", "student")
    student1 = admin.create_user_account("studen2", "testtest", "student")
    professor = admin.create_user_account("Gunawan", "F5678", "Dosen")
    student1.set_bill(0)

    # Courses
    dsp_course = Course("Algorithma")
    pbo_course = Course("PBO")

    #Enroll student and assign professor
    if student:
        dsp_course.enroll_student(student)
    if student1:
        pbo_course.enroll_student(student1)
        student1.set_bill(0)
    if professor:
        professor.add_course(pbo_course)

    # Polymorphism
    for user in [student, student1, professor]:
        if user:
            if isinstance(user, Student):
                user.add_grade(dsp_course, '90')
                user.add_grade(pbo_course, '78')
                if user.get_user_id() != "studen2":
                    user.set_bill(5000000)  # Set bill for student
                print(f"Student {user.get_user_id()} memiliki nilai {user.view_grades()}")
                print(f"Student {user.get_user_id()} memiliki tagihan {user.get_bill()} yang belum dibayar")
                if dsp_course in user.get_courses():
                    print(f"Student {user.get_user_id()} berhasil enroll course {dsp_course.course_name}")
            elif isinstance(user, Dosen):
                print(f"Dosen {user.get_user_id()} berhasil login")
        operator = Operator("Admin", "adminpass")
        student = operator.create_user_account("student1", "studentpass", "student")
        bug_report = student.report_bug(operator, "App crashes when clicking on 'Save' button")
        print(f"Bug Report ID: {bug_report.get_ticket_id()} for bug: {bug_report.get_bug_description()}")
        operator = Operator("Admin", "adminpass")
        student = operator.create_user_account("student1", "studentpass", "student")
        print(operator.upload_krs_schedule("KRS_schedule.pdf"))
        print(student.choose_krs("paket"))
        print(student.upload_certificate("certificate.pdf"))

if __name__ == "__main__":
    main()