import turtle         # 그래픽 그리기를 위한 turtle 모듈 불러오기
import time           # 시간 지연(슬립)을 위한 time 모듈 불러오기
import random         # 무작위 색상을 만들기 위한 random 모듈 불러오기

# 배경 계단을 그릴 거북이 객체 생성
bg = turtle.Turtle()
bg.hideturtle()       # 배경 그리는 거북이는 화면에 표시하지 않음
bg.pensize(3)         # 선 굵기 3으로 설정 (좀 더 굵게 계단 표시)
bg.speed(0)           # 배경은 최대로 빠르게 그림 (애니메이션 없이)

# 계단을 따라 올라갈 거북이 객체 생성
walker = turtle.Turtle()
walker.shape("turtle")   # 거북이 모양 커서로 설정
walker.pensize(2)        # 선 굵기 2로 설정 (강조용 아님)
walker.penup()           # 선을 그리지 않도록 펜을 올림
walker.goto(0, 0)        # 계단 시작점 (화면의 왼쪽 아래 모서리)로 이동
walker.setheading(0)     # 오른쪽(0도) 방향을 바라보게 초기화
walker.pendown()         # 이동 시 선을 그리도록 설정
walker.speed(1)          # 느린 속도로 설정 (움직임이 보이도록)

# 계단 관련 설정
step_size = 30           # 계단 한 칸의 크기 (가로, 세로 동일)
num_steps = 10           # 계단 개수 (총 10번 반복)

# 1단계: 배경 계단 그리기
for _ in range(num_steps):      # 계단 개수만큼 반복
    bg.forward(step_size)       # 오른쪽으로 한 칸(30픽셀) 직선 그리기 (가로)
    bg.left(90)                 # 방향을 위쪽으로 90도 회전
    bg.forward(step_size)       # 위쪽으로 한 칸(30픽셀) 직선 그리기 (세로)
    bg.right(90)                # 다시 원래 방향(오른쪽)으로 회전

# 2단계: 거북이 계단 오르기
walker.penup()                 # 선은 그리지 않도록 펜 올림
walker.goto(0, 0)              # 계단 시작점으로 다시 이동
walker.setheading(0)           # 오른쪽(0도) 방향을 바라보도록 초기화

for _ in range(num_steps):     # 계단을 하나씩 올라갈 반복문
    r = random.random()        # 빨간색 성분 (0.0 ~ 1.0 사이 실수)
    g = random.random()        # 초록색 성분
    b = random.random()        # 파란색 성분
    walker.color((r, g, b))    # 거북이의 색상 설정 (펜 색 + 몸 색 동시에 적용)

    walker.forward(step_size)  # 오른쪽으로 계단 가로 한 칸 이동
    time.sleep(0.2)            # 애니메이션 효과를 위해 잠시 멈춤 (0.2초)

    walker.left(90)            # 위쪽 방향으로 회전
    walker.forward(step_size)  # 계단 세로 한 칸 위로 이동
    time.sleep(0.2)            # 애니메이션 효과를 위해 잠시 멈춤 (0.2초)

    walker.right(90)           # 다시 오른쪽으로 방향 회전 (다음 계단 준비)

# turtle 그래픽 창이 꺼지지 않도록 유지
turtle.done()
