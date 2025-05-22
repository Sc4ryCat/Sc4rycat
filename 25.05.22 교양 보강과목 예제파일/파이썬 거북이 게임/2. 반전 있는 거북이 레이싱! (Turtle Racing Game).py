import turtle            # turtle 그래픽 모듈 (거북이, 선, 도형 등을 그릴 수 있음)
import random            # 난수 생성을 위한 모듈 (무작위 이동, 전략 지정 등에 사용)

# --- 화면 설정 ---
screen = turtle.Screen()               # turtle 화면 생성
screen.setup(width=1000, height=600)   # 화면 크기 설정 (가로 1000, 세로 600)
screen.title("🐢 반전 있는 거북이 레이싱!")  # 창 제목 설정

# --- 트랙 구분선 그리기 ---
track_drawer = turtle.Turtle()         # 트랙 라인을 그릴 거북이 생성
track_drawer.hideturtle()              # 거북이 모양 숨기기 (선만 보이게)
track_drawer.speed("fastest")          # 최대 속도로 선 그리기
track_drawer.pensize(1)                # 선 두께 설정
track_drawer.color("black")            # 선 색상은 검정색

for y in list(range(-170, 171, 40)):   # y좌표 -170부터 170까지 40 간격으로 반복
    track_drawer.penup()               # 선을 그리지 않고 이동
    track_drawer.goto(-450, y)         # 각 라인의 시작점으로 이동 (왼쪽에서 시작)
    track_drawer.pendown()             # 선 그리기 시작
    track_drawer.forward(900)          # 오른쪽 방향으로 900픽셀 선 긋기 (전체 트랙 너비)

# --- 결승선 그리기 ---
finish_line = 380                      # 결승선 위치 (x 좌표 기준)

line = turtle.Turtle()                 # 결승선을 그릴 거북이 생성
line.hideturtle()                      # 거북이 모양 숨김
line.speed("fastest")                 # 결승선도 빠르게 그림
line.penup()                           # 선 없이 이동
line.goto(finish_line, -200)          # 결승선의 아래쪽 시작 지점으로 이동
line.setheading(90)                    # 위쪽 방향(90도)으로 방향 설정
line.pensize(3)                        # 선 굵게 설정
line.pendown()                         # 선 그리기 시작
line.forward(400)                      # 위쪽으로 400픽셀 결승선 그리기

# --- 참가자 설정 ---
colors = ["red", "blue", "green", "orange", "purple", "cyan", "pink", "yellow"]  
# 참가할 거북이들의 색상 목록

start_y = list(range(-150, 151, 40))   # 각 거북이의 y좌표 설정 (트랙에 맞춰 수직 정렬)

racers = []                            # 모든 거북이 객체를 담을 리스트
strategies = {}                        # 각 거북이의 전략을 저장할 딕셔너리 (색상 → 전략)

# 전략 정의 함수
def assign_strategy():
    return random.choice(["steady", "early_boost", "late_boost", "wavy", "surge"])
    # 전략은 무작위로 선택됨

# 각 거북이 생성 및 초기 설정
for i in range(len(colors)):
    t = turtle.Turtle()                # 새로운 거북이 생성
    t.shape("turtle")                  # 모양을 거북이로 설정
    t.color(colors[i])                 # 색상 지정
    t.penup()                          # 이동할 때 선 그리지 않음
    t.goto(-350, start_y[i])          # 출발선 좌표로 이동 (왼쪽 x=-350, y는 트랙에 맞춰 지정)
    racers.append(t)                  # 생성된 거북이를 리스트에 추가
    strategies[colors[i]] = assign_strategy()  
    # 각 거북이에 전략 할당 (색상을 키로 사용)

# --- 사용자 입력 ---
user_bet = screen.textinput("거북이 레이싱",
                            f"누가 이길까요? ({' / '.join(colors)}):")
# 사용자가 어떤 색상의 거북이가 우승할지 입력 (입력창 제공)

# --- 레이싱 루프 시작 ---
race_on = True                         # 게임이 실행 중인지 여부를 나타내는 변수

while race_on:
    for racer in racers:              # 각 거북이에 대해 반복
        color = racer.pencolor()      # 현재 거북이의 색상 (전략 판별용)
        strategy = strategies[color]  # 해당 거북이의 전략 가져오기
        x = racer.xcor()              # 현재 x좌표 가져오기
        race_progress = (x + 350) / (finish_line + 350)  
        # 경과율 계산 (0.0 ~ 1.0 사이): 현재 위치가 전체 코스 중 얼마나 왔는지

        # --- 전략별 속도 계산 ---
        if strategy == "steady":
            step = random.randint(4, 6)  # 꾸준한 속도

        elif strategy == "early_boost":
            # 초반엔 빠르고, 후반엔 느림
            step = random.randint(7, 10) if race_progress < 0.5 else random.randint(1, 4)

        elif strategy == "late_boost":
            # 초반엔 느리고, 후반엔 확 치고 나감
            step = random.randint(1, 4) if race_progress < 0.6 else random.randint(7, 12)

        elif strategy == "wavy":
            # 들쭉날쭉한 속도
            step = random.randint(1, 10)

        elif strategy == "surge":
            # 70% 전까지는 매우 느림, 이후 폭주
            if race_progress < 0.7:
                step = random.randint(1, 3)
            else:
                step = random.randint(10, 14)

        else:
            step = random.randint(3, 6)  # 기타 전략 (예외 처리)

        racer.forward(step)             # 계산된 거리만큼 앞으로 이동

        # --- 결승선 도착 여부 확인 ---
        if racer.xcor() >= finish_line:  # x좌표가 결승선보다 크거나 같으면
            winner = color               # 우승자 색상 저장
            race_on = False              # 게임 루프 종료
            break                        # 더 이상 거북이 이동하지 않음

# --- 결과 메시지 출력 ---
msg = turtle.Turtle()                    # 메시지를 출력할 turtle 객체 생성
msg.hideturtle()                         # 커서 숨기기
msg.penup()                              # 선 없이 이동
msg.goto(0, 200)                         # 중앙 상단 위치로 이동

if winner == user_bet:
    # 사용자의 예측이 맞았을 경우
    msg.write(f"🎉 {winner} 거북이 우승! 정답입니다!", align="center", font=("Arial", 20, "bold"))
else:
    # 틀렸을 경우
    msg.write(f"🏁 {winner} 거북이 우승! 아쉽지만 틀렸어요.", align="center", font=("Arial", 20, "bold"))

# --- 게임 종료 후 창 유지 ---
screen.mainloop()                        # 화면을 닫지 않고 유지 (사용자 종료 시까지)
