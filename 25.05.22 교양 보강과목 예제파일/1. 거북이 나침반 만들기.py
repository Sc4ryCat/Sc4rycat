import turtle  # turtle 모듈 불러오기

# 거북이 객체 생성
t = turtle.Turtle()

# 거북이의 모양을 "turtle"로 설정 (삼각형 → 거북이 아이콘)
t.shape("turtle")

# ["N", "E", "S", "W"] 방향 리스트를 반복
for dir in ["N", "E", "S", "W"]:
    t.penup()  # 선을 그리지 않도록 펜 들기
    t.goto(0, 0)  # 중앙(0,0)으로 이동

    # 각 방향에 맞는 회전 각도를 설정
    # N: 90도(위쪽), E: 0도(오른쪽), S: 270도(아래), W: 180도(왼쪽)
    t.setheading({"N":90, "E":0, "S":270, "W":180}[dir])

    # 설정된 방향으로 100픽셀 앞으로 이동 (중심에서 바깥으로)
    t.forward(100)

    t.pendown()  # 선 그리기 시작
    t.forward(20)  # 방향선 추가로 20픽셀 더 그림

    t.penup()  # 다시 선 그리기 멈춤
    t.forward(10)  # 글자를 표시할 위치까지 조금 더 이동

    # 현재 위치에 방향 글자를 씀
    t.write(dir, align="center", font=("Arial", 12, "normal"))

# turtle 그래픽 창이 닫히지 않도록 유지
turtle.done()
