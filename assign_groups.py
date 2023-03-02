import canvasapi
import numpy

TOKEN = "DELETE THIS AND PASTE IN YOUR TOKEN"
INSTANCE = "https://canvas.ubc.ca"

def assign(assignment, student_ids):

    for array in student_ids:
        ids = list(array)

        try:
            assignment.create_override(assignment_override={"student_ids": ids})
            print("Successfully assigned group! Check Canvas to see if it worked. It might take some time for everything to load.")
        except canvasapi.exceptions.BadRequest as e:
            print(e)
            print(
                f"ERROR Unable to add students with ids: {ids} to assignment. Check that the assignment is currently assigned only to 'Everyone' and no student in specific"
            )
            exit()


def get_student_ids(course):
    users = course.get_users(enrollment_type=['student'])
    
    return [user.id for user in users]
        
def get_assignments(course):
    assignments = course.get_assignments()

    assignment_name = input(f"These are your available assignments. {[assignment.name for assignment in assignments]} \nPlease enter the name exactly of the assignment you would like to choose: ")
    try:
        assignment = next(a for a in assignments if a.name == assignment_name)
        return assignment
        
    except StopIteration:
        print("ERROR: Invalid assignment name, does not match any of the following: ", [assignment.name for assignment in assignments])
        exit()
        
def split_ids(ids):
    try:
        n = int(input(f"How many groups would you like to create? (You have {len(ids)} students in your course): "))
        if (n > len(ids)):
            print("ERROR: You can't create more groups than there are students")
            exit()
            
        l = numpy.array_split(numpy.array(ids), n)
        return l
    except ValueError:
        print("ERROR: Please enter a number")
        exit()
        
# Call override for each student

def main():
    course_id = input("Enter course ID: ")

    canvas = canvasapi.Canvas(INSTANCE, TOKEN)
    course = canvas.get_course(course_id)
    student_ids = get_student_ids(course)
    assignment = get_assignments(course)
    ids = split_ids(student_ids)
    assign(assignment, ids)

if __name__ == "__main__":
    main()
