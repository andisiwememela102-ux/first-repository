class Course:
    # Class attribute for the course name
    name = "Fundamentals of Computer Science"
    contact_website = "www.hyperiondev.com"

    # Method to display contact details
    def contact_details(self):
        print("Please contact us by visiting", self.contact_website)

    def head_office_Location(self):
        """
        New method added to the Course class as requested
        Print the head office location. 
        """
        print("Head Office Location: Cape Town")

class OOPCourse(Course):
    def __init__(self):
        self.description = "OOP Fundamentals"
        self.trainer = "Mr Anon A. Mouse"
        self.course_id = "#12345" #Defined here to be used by show_course_id() 

    def trainer_details(self):
        print(f"Course Description: {self.description}")
        print(f"Trainer Name:    {self.trainer}")   

    def show_course_id(self):
        print(f"Course ID:    {self.course_id}")

print("--- Running Required Method ---")

# Create an instance of the Course class
course_1 = OOPCourse()

# Call the contact_details method to display contact information
course_1.contact_details() 
course_1.trainer_details()  
course_1.show_course_id()   
course_1.head_office_Location()
