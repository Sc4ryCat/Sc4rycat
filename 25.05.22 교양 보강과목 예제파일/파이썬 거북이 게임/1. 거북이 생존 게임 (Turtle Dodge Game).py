import turtle         # 거북이 그래픽 모듈 불러오기
import random         # 무작위 값 생성을 위한 모듈
import time           # 시간 지연(sleep)을 위한 모듈

# 화면 초기 설정
screen = turtle.Screen()                  # turtle 화면 객체 생성
screen.setup(width=600, height=600)       # 화면 크기 설정
screen.title("🐢 거북이 생존 게임")         # 제목 설정
screen.bgcolor("lightblue")              # 배경색 설정
screen.tracer(0)                         # 애니메이션을 수동으로 갱신 (더 부드러운 움직임 구현)

# 플레이어 거북이 생성
player = turtle.Turtle()                 # 플레이어용 turtle 객체 생성
player.shape("turtle")                   # 모양을 '거북이'로 설정
player.color("green")                    # 색상을 초록색으로 설정
player.penup()                           # 이동 시 선을 그리지 않도록 설정
player.goto(0, -250)                     # 화면 아래쪽 중앙에 위치
player.speed(0)                          # 최대 속도로 초기 위치 설정

# 플레이어 이동 함수 정의
def go_left():
    x = player.xcor() - 20               # 왼쪽으로 20픽셀 이동
    if x > -280:                         # 왼쪽 화면 경계 밖으로 나가지 않도록 제한
        player.setx(x)

def go_right():
    x = player.xcor() + 20               # 오른쪽으로 20픽셀 이동
    if x < 280:                          # 오른쪽 경계 제한
        player.setx(x)

def go_up():
    y = player.ycor() + 20               # 위로 20픽셀 이동
    if y < 280:                          # 위쪽 경계 제한
        player.sety(y)

def go_down():
    y = player.ycor() - 20               # 아래로 20픽셀 이동
    if y > -280:                         # 아래쪽 경계 제한
        player.sety(y)

# 키보드 이벤트 연결
screen.listen()                          # 키보드 입력을 받기 시작
screen.onkey(go_left, "Left")           # 왼쪽 화살표 키 입력시 go_left 함수 호출
screen.onkey(go_right, "Right")         # 오른쪽 화살표
screen.onkey(go_up, "Up")               # 위쪽 화살표
screen.onkey(go_down, "Down")           # 아래쪽 화살표

# 장애물(공) 생성
balls = []                               # 공 리스트 초기화
colors = ["red", "orange", "yellow", "green", "blue", "purple", "cyan", "pink"]  # 공에 사용할 색상 목록

for _ in range(20):                      # 공 20개 생성
    ball = turtle.Turtle()              # 공 객체 생성
    ball.shape("circle")                # 원 모양으로 설정
    ball.color(random.choice(colors))   # 무작위 색상 선택
    ball.penup()                        # 선을 그리지 않도록 설정
    ball.goto(random.randint(-280, 280), random.randint(100, 600))  # 무작위 위치에서 시작
    ball.speed(0)                       # 초기 속도 설정 (최대)
    balls.append(ball)                  # 공 리스트에 추가

# 점수 표시용 텍스트 거북이 설정
score = 0                               # 점수 초기값
score_writer = turtle.Turtle()          # 텍스트용 turtle 객체 생성
score_writer.hideturtle()               # 텍스트만 보이게 거북이 숨김
score_writer.penup()                    # 선 없이 위치 이동
score_writer.goto(-280, 260)            # 왼쪽 위에 점수 위치 표시
score_writer.write(f"Score: {score}", font=("Arial", 16, "bold"))  # 초기 점수 텍스트 출력

# 게임 실행 루프
game_running = True                     # 게임 실행 여부 변수
while game_running:
    screen.update()                     # 화면 갱신 (tracer(0) 설정 때문에 직접 호출 필요)

    # 각 공에 대해 처리
    for ball in balls:
        y = ball.ycor()                 # 현재 y 좌표 가져오기
        y -= random.randint(1, 15)     # 무작위 속도로 낙하 (빠르게)
        ball.sety(y)                    # 새로운 y 좌표로 설정

        if y < -300:                    # 공이 바닥에 닿았을 때
            ball.goto(random.randint(-280, 280), random.randint(300, 600))  # 다시 위쪽에서 떨어지게 위치 재설정
            ball.color(random.choice(colors))  # 색상도 새롭게 랜덤 지정
            score += 1                          # 점수 1점 증가
            score_writer.clear()                # 기존 점수 텍스트 지우기
            score_writer.write(f"Score: {score}", font=("Arial", 16, "bold"))  # 새 점수 출력

        if player.distance(ball) < 20:   # 플레이어와 공 간 거리가 20픽셀 이내이면 충돌로 판단
            game_running = False         # 게임 루프 종료
            score_writer.goto(0, 0)      # 중앙에 메시지 출력
            score_writer.write("💥 Game Over 💥", align="center", font=("Arial", 24, "bold"))  # 게임오버 메시지 출력

    # 점수 100점 도달 시 승리 처리
    if score >= 100:
        game_running = False             # 루프 종료
        score_writer.goto(0, 0)          # 중앙으로 이동
        score_writer.write("🎉 You Win! 🎉", align="center", font=("Arial", 24, "bold"))  # 승리 메시지 출력

    time.sleep(0.02)                     # 루프 속도 조절 (낙하 및 움직임 속도 제어)
