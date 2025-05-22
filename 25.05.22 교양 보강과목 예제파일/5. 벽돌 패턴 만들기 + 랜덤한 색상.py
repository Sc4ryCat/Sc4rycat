import turtle       # 그래픽 그리기를 위한 turtle 모듈 불러오기
import random       # 무작위 색상 생성을 위한 random 모듈 불러오기

# 거북이 객체 생성 및 초기 설정
t = turtle.Turtle()     # turtle 객체 생성
t.shape("turtle")       # 커서 모양을 거북이로 설정 (기본 삼각형 아님)
t.speed(3)              # 속도를 1~10 중 중간 정도인 3으로 설정 (느림)
t.penup()               # 선을 그리지 않도록 초기에는 펜을 들고 있음

# 벽돌 배열 설정값
rows = 6               # 벽돌의 줄 수 (세로 방향 총 6줄)
cols = 8               # 각 줄당 벽돌의 개수 (가로 방향 총 8개)
brick_w = 60           # 각 벽돌의 가로 길이 (픽셀 단위)
brick_h = 30           # 각 벽돌의 세로 길이

# 이중 반복문을 통해 벽돌을 그리기
for row in range(rows):                      # 세로 방향으로 6줄 반복
    y = -row * brick_h                       # 줄이 내려갈수록 y 좌표 감소 (아래쪽으로 이동)
    start_x = -cols * brick_w / 2            # 전체 벽돌이 가운데 정렬되도록 왼쪽 x 시작점 계산

    if row % 2 == 1:                         # 홀수 번째 줄(1,3,5...)일 경우
        start_x += brick_w / 2               # 시작 위치를 반 칸 오른쪽으로 밀어 지그재그 배열 구현

    for col in range(cols):                  # 각 줄마다 가로 방향으로 8개 벽돌 반복
        x = start_x + col * brick_w          # 벽돌의 x 좌표 계산
        t.goto(x, y)                         # 거북이를 해당 벽돌 위치로 이동

        # 랜덤 색상 설정 (각각 R, G, B는 0.0~1.0 실수 범위)
        r = random.random()                  # 빨간색 성분
        g = random.random()                  # 초록색 성분
        b = random.random()                  # 파란색 성분
        t.fillcolor(r, g, b)                 # 벽돌의 채우기 색상 지정

        # 사각형 색 채우기 시작
        t.begin_fill()

        # 사각형(벽돌) 그리기: 가로 → 세로 → 가로 → 세로 (2번 반복)
        t.pendown()                          # 선을 그리기 시작
        for _ in range(2):
            t.forward(brick_w)               # 가로 방향 선
            t.left(90)
            t.forward(brick_h)               # 세로 방향 선
            t.left(90)

        # 색상 채우기 마무리
        t.end_fill()

        # 다음 위치로 이동을 위한 준비
        t.penup()                            # 다음 벽돌로 이동할 때 선이 그려지지 않게 함

# turtle 그래픽 창이 닫히지 않도록 유지
turtle.done()
