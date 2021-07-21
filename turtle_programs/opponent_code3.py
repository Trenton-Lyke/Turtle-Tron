# replace "opponent team name" with the name you want
# opponent turtles to be enclosed by quotation marks
# for example:
# team_name = "The Lame Team"
team_name = "Team Team"

# replace "opponent team color" with the name of the color
# you want opponent turtles to be and enclose it with quotation marks
# for example:
# color = "blue"
color = "green"

# replace turtle.forward(1) with the code you want to use to move the
# opponent turtles around during the game. Make sure the code is
# indented over just like the turtle.forward(1) method call is.
def movement_function(turtle, world):
    turtle.left(60)
    turtle.forward(5)
    turtle.right(60)
    turtle.forward(5)
    