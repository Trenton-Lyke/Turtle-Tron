# replace "your team name" with the name you want 
# for your turtle. Make sure the text is enclosed 
# by quotation marks
# for example:
# team_name = "The Team"
team_name = "Team212"

# replace "your team color" with the name of the color 
# you want your turtle to be. Make sure the text is 
# enclosed by quotation marks
# for example:
# color = "green"
color = "purple"

# replace turtle.forward(1) with the code you want to use to move your
# turtle around during the game. Make sure your code is
# indented over just like the turtle.forward(1) method call is.
def movement_function(turtle, world):
  turtle.forward(15)
  turtle.setheading(270)
  turtle.forward(15)
  turtle.left(15)
  turtle.right(15)
  for i in range(360):
    turtle.forward(1)
    turtle.right(1)
  for i in range(4):
    turtle.right(90)
    turtle.forward(15)