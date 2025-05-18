import streamlit as st
from streamlit_option_menu import option_menu

# ----------Classes-----------

class Person:
    def __init__(self, 
                name: str, 
                age : int
                ):
        self.name = name
        self.age = age

    def getName(self):
        return self.name

class Student(Person):
    def __init__(self, name: str, age: int, rollnumber: str):
        super().__init__(name, age)
        self.rollnumber = rollnumber
        self.courses = []

    def register_for_course(self, course):
        if course.title not in [c.title for c in self.courses]:
            self.courses.append(course)
            course.add_student(self)

class Instructor(Person):
    def __init__(self, 
                name: str,
                age: int,
                salary: int):
        super().__init__(name, age)
        self.salary = salary
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)
        course.set_instructor(self)

class Course:
    def __init__(self, title: str):
        self.title = title
        self.instructor = None
        self.students = []

    def add_student(self, student: Student):
        if student not in self.students:
            self.students.append(student)

    def set_instructor(self, instructor: Instructor):
        self.instructor = instructor

# Storage States
if "students" not in st.session_state:
    st.session_state.students = []

if "instructors" not in st.session_state:
    st.session_state.instructors = []

if "courses" not in st.session_state:
    st.session_state.courses = []

if "roll_counter" not in st.session_state:
    st.session_state.roll_counter = 1

def roll_num_func():
    roll_num = f"SAQM-{st.session_state.roll_counter:04d}"
    st.session_state.roll_counter += 1 
    return roll_num


# -------------UI-------------

st.set_page_config(
    page_title= "UMS - Aqsaa Qaazi",
    layout= "centered",
    page_icon="🎓"
)
st.title("A basic University Management System (UMS)")


# old sidebar styles
# pages = ["Home", 
#         "Add Course",
#         "Add Instructor", 
#         "Add Student", 
#         "View Data"]

# choice = st.sidebar.selectbox("Navigate", pages)

# new header
menu_options = ["Home", 
                "Add Student", 
                "Add Instructor", 
                "Add Course", 
                "View Data"]

menu_icons = ["house", "book", "person-plus", "person", "bar-chart"]

with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        
        options=["Home", 
                "Add Student", 
                "Add Instructor", 
                "Add Course", 
                "View Data"],
        
        icons=["house", 
            "person-plus", 
            "person", 
            "book", 
            "bar-chart"],
        
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "grey"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "brown",
            },
            "nav-link-selected": {"background-color": "brown"},
        }
    )

if selected == "Home":
    st.markdown("# 🎓 Welcome to University Management System (UMS)")
    st.markdown("###### Built by Aqsaa Qaazi")
    st.write("---")

    st.markdown("""
    ###  What is UMS?
    The **University Management System (UMS)** is a simple yet powerful tool for managing academic entities like:
    - Courses  
    - Students  
    - Instructors  
    - Enrollments

    It simulates how a real university or department might handle student registrations and instructor assignments.
    """)

    st.markdown("""
    ### Features:
    🗸  Add new students and register them in courses  
    🗸  Add instructors and assign them to courses  
    🗸  Create and view courses  
    🗸  View enrolled students and assigned instructors per course  
    """)

    st.write("---")
    st.markdown("""
    ### Built With:
    - Python 
    - Streamlit 
    - Object-Oriented Programming Principles  
    - Modern UI patterns (multiselect, dynamic dropdowns)  
    """)

    st.write("---")
    st.markdown("""
    ### Why Use This?
    If you're learning:
    - Python OOP  
    - Streamlit UI development  
    - Backend simulation with in-memory data

    This app gives you a **perfect start** to build bigger platforms.
    """)


elif selected == "Add Course":
    st.header("Create Course")
    title = st.text_input("Course Title")
    if st.button("Create Course"):
        if title:
            st.session_state.courses.append(Course(title))
            st.success(f"{title} successfully added to course.")
        else:
            st.error("Course title is required.")

elif selected == "Add Instructor":
    st.header("Hire an Instructor")
    name = st.text_input("Instructor's Name")
    age = st.number_input("Instructor Age", min_value=35, max_value=50, step=1)
    salary = st.number_input("Salary", min_value=35000, step=1150)

    course_titles = [course.title for course in st.session_state.courses]

    course_selection = st.multiselect("Assign Course(s)", course_titles)

    if st.button("Add Instructor"):
        if name:
            new_instructor = Instructor(name, age, salary)
            st.session_state.instructors.append(new_instructor)
            for title in course_selection:
                course_obj = next((c for c in st.session_state.courses if c.title == title), None)
                if course_obj:
                    new_instructor.assign_course(course_obj)
            st.success(f"Instructor {name} added and assigned to selected courses!")
        else:
            st.error("Please provide a name.")

elif selected == "Add Student":
    st.header("Register Student")
    name = st.text_input("Student's Name")
    age = st.number_input("Age", min_value=18, max_value=38)
    roll = roll_num_func()
    st.markdown(f"**Generated Roll Number:** `{roll}`")

    course_titles = [course.title for course in st.session_state.courses]

    course_selection = st.multiselect("Register for Course(s)", course_titles)

    if st.button("Add Student"):
        if name and roll:
            new_student = Student(name, age, roll)
            st.session_state.students.append(new_student)
            for title in course_selection:
                course_obj = next((c for c in st.session_state.courses if c.title == title), None)
                if course_obj:
                    new_student.register_for_course(course_obj)
            st.success(f"Student {name} added and registered to selected courses!")
        else:
            st.error("Please fill all fields.")

elif selected == "View Data":
    st.header("View Course Enrollments & Data")
    if not st.session_state.courses:
        st.warning("No courses available.")
    else:
        course = st.selectbox("Select Course", st.session_state.courses, format_func=lambda x: x.title)

        st.subheader(f"{course.title}")
        if course.instructor:
            st.markdown(f"**Instructor:** {course.instructor.name}")
        else:
            st.warning("No instructor assigned.")

        if course.students:
            st.markdown("**Enrolled Students:**")
            for student in course.students:
                st.write(f"- {student.name} (Roll: {student.rollnumber})")
        else:
            st.info("No students enrolled yet.")
