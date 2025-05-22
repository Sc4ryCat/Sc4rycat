import turtle  # turtle 그래픽 모듈 불러오기

# 거북이 객체 생성
t = turtle.Turtle()

# 거북이 모양으로 커서 변경 (기본은 삼각형 모양)
t.shape("turtle")

# 거북이 이동 속도 설정 (0: 최고속, 1~10은 점점 빨라짐 / 여기선 약간 천천히)
t.speed(3)

# 벽돌 그리기 설정 값
rows = 6         # 총 줄 수 (세로 방향)
cols = 8         # 각 줄마다 사각형 개수 (가로 방향)
brick_w = 60     # 벽돌 가로 길이 (픽셀)
brick_h = 30     # 벽돌 세로 길이 (픽셀)

# 벽돌을 행(row) 단위로 반복
for row in range(rows):
    y = -row * brick_h  # y 좌표 계산 (아래로 내려가기 위해 음수 곱)

    # 줄의 시작 x 좌표 계산
    start_x = -cols * brick_w / 2  # 전체 벽돌이 가운데 정렬되도록 시작점 설정

    # 홀수 줄(1, 3, 5...)은 반 칸 오른쪽으로 이동
    if row % 2 == 1:
        start_x += brick_w / 2

    # 현재 줄(row)에서 각 열(col)마다 사각형 그리기
    for col in range(cols):
        x = start_x + col * brick_w  # 현재 열의 x 좌표 계산
        t.penup()        # 선을 그리지 않도록 펜 올림
        t.goto(x, y)     # 지정된 좌표로 이동
        t.pendown()      # 선을 그리기 시작

        # 사각형 그리기 (두 번 반복으로 가로, 세로 그리기)
        for _ in range(2):
            t.forward(brick_w)  # 가로 선
            t.left(90)
            t.forward(brick_h)  # 세로 선
            t.left(90)

# 그래픽 창이 자동으로 닫히지 않도록 유지
turtle.done()
