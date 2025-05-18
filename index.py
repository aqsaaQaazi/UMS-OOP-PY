# ---------------CLASSES-----------------------

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        print(f"{self.__class__.__name__} created: {self.name}, Age: {self.age}")

    def get_name(self):
        return self.name

class Student(Person):
    def __init__(self, name: str, age: int, rollnumber: int):
        super().__init__(name, age)
        self.rollnumber = rollnumber
        self.courses = []

    def register_for_course(self, course):
        if course.title not in [c.title for c in self.courses]:
            self.courses.append(course)
            course.add_student(self)
            print(f"{self.name} registered for course: {course.title}")
        else:
            print(f"{self.name} is already registered in {course.title}")

class Instructor(Person):
    def __init__(self, name: str, age: int, salary: int):
        super().__init__(name, age)
        self.salary = salary
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)
        course.set_instructor(self)
        print(f"{self.name} is assigned to course: {course.title}")

class Course:
    def __init__(self, title: str):
        self.title = title
        self.instructor = None
        self.students = []
        print(f"Course created: {self.title}")

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)
            print(f"{student.name} added to {self.title}")

    def set_instructor(self, instructor: Instructor):
        self.instructor = instructor
        print(f"Instructor {instructor.name} set for {self.title}")

    def list_students(self):
        print(f"Students in {self.title}:")
        for s in self.students:
            print(f" - {s.name}")


# variables 

# Create Instructor
inst1 = Instructor("Noshaba", 45, 25000)

# Create Students
st1 = Student("Aqsaa", 20, 101)
st2 = Student("Murad", 21, 102)

# Create Courses
course1 = Course("English")
course2 = Course("Computer Science")

# Assign Instructor to Courses
inst1.assign_course(course1)
inst1.assign_course(course2)

# Register Students to Courses
st1.register_for_course(course1)
st2.register_for_course(course1)
st1.register_for_course(course2)

# Print enrolled students in a course
course1.list_students()
course2.list_students()