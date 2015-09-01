from swampy.TurtleWorld import TurtleWorld, Turtle
from swampy.TurtleWorld import wait_for_user, fd, lt


def draw_square(turtle_name, length):
    for i in range(4):
        fd(turtle_name, length)
        lt(turtle_name)


def draw_polygon(turtle_name, length, num_sides):
    degree = 360 / num_sides

    for i in range(num_sides):
        fd(turtle_name, length)
        lt(turtle_name, degree)


print "\n\n*******************************************************************"
print "\t\t\tExercise 4.2"
print "*******************************************************************\n"

world = TurtleWorld()
bob = Turtle()

draw_square(bob, 100)
wait_for_user()


print "\n\n*******************************************************************"
print "\t\t\tExercise 4.3"
print "*******************************************************************\n"

world = TurtleWorld()
bob = Turtle()

draw_polygon(bob, 50, 8)
wait_for_user()
