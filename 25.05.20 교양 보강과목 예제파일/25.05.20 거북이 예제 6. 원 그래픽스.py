import turtle as t


t.speed(10)
t.shape('turtle')

size = 1

t.pendown()


for  i  in  range(-500,100,10)  :
     t.penup()
     t.goto(i,i)
     t.pendown()
     t.circle(size)
     
     size +=  3


