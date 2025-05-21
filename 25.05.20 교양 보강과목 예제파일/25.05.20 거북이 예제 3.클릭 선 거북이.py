import turtle
import random

## 함수 선언 부분 ##


def  screenLeftClick(x,y):
    
    tSize = random.randrange(2,10)
    turtle.shapesize(tSize)
    
    r = random.random()
    g = random.random()
    b = random.random()
    turtle.color((r, g, b))
    
    tAngle = random.randrange(0, 360)

    turtle.pendown()
    turtle.goto(x,y)
    turtle.left(tAngle)
    turtle.stamp()



## 변수 선언 부분 ##
tSize, tAngle = 0, 0
r, g, b = 0.0, 0.0, 0.0



## 메인 코드 부분 ##
turtle.title('거북이 도장 찍기')
turtle.shape('turtle')

turtle.onscreenclick(screenLeftClick,1)

turtle.done()
