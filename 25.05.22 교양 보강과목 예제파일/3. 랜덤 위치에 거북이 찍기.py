import turtle      # turtle 모듈 불러오기
import random      # 무작위 숫자를 생성하는 random 모듈 불러오기

# 그래픽 창 설정 (배경색은 흰색)
screen = turtle.Screen()
screen.bgcolor("white")

# 메인 거북이 객체 생성 (화면에 표시하지 않음)
t = turtle.Turtle()
t.hideturtle()
t.speed(0)  # 최대 속도로 설정

# 100마리 거북이 찍기
for _ in range(100):
    # 각 거북이마다 별도의 turtle 객체 생성
    tur = turtle.Turtle()
    tur.shape("turtle")  # 거북이 모양으로 설정
    tur.penup()          # 이동 시 선을 그리지 않도록 펜 들기

    # 무작위 위치 설정 (-300 ~ +300 범위 내)
    x = random.randint(-300, 300)
    y = random.randint(-300, 300)
    tur.goto(x, y)

    # 무작위 방향 설정 (0 ~ 360도 사이)
    tur.setheading(random.randint(0, 360))

    # 무작위 색상 설정 (RGB, 각각 0.0 ~ 1.0 사이 실수)
    r = random.random()
    g = random.random()
    b = random.random()
    tur.color((r, g, b))  # 펜 색상 및 채우기 색상 모두 동일하게 설정

    # 무작위 크기 설정 (1.0배 ~ 3.0배 크기)
    size = random.uniform(1.0, 3.0)
    tur.turtlesize(size)  # 크기 조절

    # 현재 위치에 거북이 모양을 도장처럼 찍음 (움직이지 않음)
    tur.stamp()

    # 실제 turtle 객체는 화면에서 숨김 (모양만 유지)
    tur.hideturtle()

# turtle 그래픽 창이 닫히지 않도록 유지
turtle.done()
