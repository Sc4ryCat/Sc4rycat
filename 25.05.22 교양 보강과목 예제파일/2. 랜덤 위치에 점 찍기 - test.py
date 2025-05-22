import turtle      # 거북이 그래픽을 위한 turtle 모듈 불러오기
import random      # 무작위 수 생성을 위한 random 모듈 불러오기

# turtle 객체 생성
t = turtle.Turtle()

# 거북이 커서를 숨김 (점만 찍히게 하기 위해)
t.hideturtle()

# 거북이 속도를 최대로 설정 (0은 가장 빠름)
t.speed(15)

# 100개의 무작위 점을 찍기 위한 반복문
for _ in range(100):
    # 무작위 좌표 (x, y) 생성 (화면 좌우/상하 -300~300 범위 내)
    x = random.randint(-300, 300)
    y = random.randint(-300, 300)
    
    # 선을 그리지 않도록 펜을 들고
    t.penup()
    
    # 무작위 위치로 이동
    t.goto(x, y)

        # 무작위 색상 설정 (RGB, 각각 0.0 ~ 1.0 사이 실수)
    r = random.random()
    g = random.random()
    b = random.random()
    t.color((r, g, b))  # 펜 색상 및 채우기 색상 모두 동일하게 설정
    
    # 해당 위치에 점을 찍음 (점 크기도 무작위: 3~10픽셀)
    t.dot(random.randint(3, 50))

# 거북이 그래픽 창을 닫지 않고 유지
turtle.done()
