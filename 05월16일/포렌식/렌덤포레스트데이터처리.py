# 필수 라이브러리 임포트
from json_logic import jsonLogic  # 룰 기반 조건 판단용 라이브러리
from statistics import mean       # 평균 계산을 위한 내장 모듈
from enum import Enum, IntEnum    # 열거형(상수 집합)을 만들기 위한 클래스
import random                     # 랜덤 데이터 생성을 위한 모듈
import pandas as pd              # 데이터프레임 처리용 라이브러리
from sklearn.ensemble import RandomForestClassifier  # 랜덤 포레스트 모델
from sklearn import metrics       # 분류 성능 평가 지표
from sklearn.model_selection import train_test_split # 학습/테스트 분리
import matplotlib.pyplot as plt   # 시각화를 위한 그래프 도구

# 결과 및 학습 방법에 사용할 열거형 상수 정의
class Const(str, Enum):
    PASS = "Y"
    FAIL = "N"
    TRAINING_BY_ALL = "TA"
    TRAINING_BY_LOW_SAMPLE = "TL"
    TRAINING_BY_PREVIOUS_AND_MEAN = "TPM"
    TRAINING_BY_CURRENT = "TC"
    TRAINING_BY_PREVIOUS = "TP"
    TRAINING_BY_MISSING_DATA = "TM"

# 룰에서 사용할 기준 점수 정의
class LearningConfig(IntEnum):
    RULE_CURRENT_SCORE = 70
    RULE_MEAN = 50
    RULE_FREE_PASS_SCORE = 90
    LOW_SAMPLE = 10
    ENOUGH_SAMPLE = 5000


test_mode = Const.TRAINING_BY_ALL.value

def check_exam_list(score_list):
    # 조건: (현재 점수 ≥ 70 and 평균 ≥ 50) or 현재 점수 ≥ 90
    rule = {"or": [
        {"and": [
            {">=": [{"var": "current_score"}, LearningConfig.RULE_CURRENT_SCORE]},
            {">=": [{"var": "mean"}, LearningConfig.RULE_MEAN]}
        ]},
        {">=": [{"var": "current_score"}, LearningConfig.RULE_FREE_PASS_SCORE]}
    ]}

    # 룰에 넣을 변수 구성
    exam_dict = {
        "current_score": score_list[1],
        "mean": score_list[2]
    }


    rule_result = jsonLogic(rule, exam_dict)

    return Const.PASS.value if rule_result else Const.FAIL.value

def make_random_numbers(previous_min, previous_max, current_min,
                        current_max, sample_number):
    my_set = set()  # 중복 제거를 위해 set 사용

    while 1:
        previous_score = random.randint(previous_min, previous_max) # 0,100
        current_score = random.randint(current_min, current_max)    # 0,100
        score_mean = mean([previous_score, current_score]) # 평균점수
        my_set.add(tuple([previous_score, current_score, score_mean]))
        if len(my_set) == sample_number:
            break

    # set → list of list
    random_list = [list(x) for x in my_set]

    # 각 데이터에 룰 기반 PASS/FAIL 결과 추가
    for index, item in enumerate(random_list):
        result = check_exam_list(item)
        item.insert(0, result)  # 맨 앞에 판단 결과 삽입

    return random_list

# 선택된 테스트 모드에 따라 데이터 샘플 수 설정
if test_mode == Const.TRAINING_BY_LOW_SAMPLE:
    random_set = make_random_numbers(0, 100, 0, 100, LearningConfig.LOW_SAMPLE)
else:
    random_set = make_random_numbers(0, 100, 0, 100, LearningConfig.ENOUGH_SAMPLE)

# 판다스 데이터프레임으로 변환
ml_df = pd.DataFrame.from_records(random_set)

# 판단 결과값을 시각화 색상 코드로 변환
ml_df.loc[ml_df[0] == "N", 0] = "red"
ml_df.loc[ml_df[0] == "Y", 0] = "yellow"

# 컬럼명 설정
ml_df.columns = ["result", "previous_score", "current_score", "mean"]
print(ml_df.head(3))  # 상위 3개 출력

print(ml_df)
# 데이터/라벨 나누기
data = ml_df.iloc[:, 1:]  # 점수 데이터
label = ml_df.iloc[:, 0]  # 분류 라벨 (PASS/FAIL → 색상)

# 학습용과 테스트용 데이터 분할
data_train, data_test, label_train, label_test = train_test_split(data, label)
data_test_original = data_test.copy()  # 시각화를 위해 원본 백업

# 입력 피처 선택: 실험 모드에 따라 학습/테스트 컬럼을 선택적으로 축소
if test_mode == Const.TRAINING_BY_PREVIOUS_AND_MEAN:
    data_test = data_test.iloc[:, [0, 2]]
    data_train = data_train.iloc[:, [0, 2]]
elif test_mode == Const.TRAINING_BY_CURRENT:
    data_test = data_test.iloc[:, [1]]
    data_train = data_train.iloc[:, [1]]
elif test_mode == Const.TRAINING_BY_PREVIOUS:
    data_test = data_test.iloc[:, [0]]
    data_train = data_train.iloc[:, [0]]

# 머신러닝 모델 정의 (랜덤 포레스트 사용)
model = RandomForestClassifier()

# 특정 조건만 필터링하여 학습하는 테스트 모드
if test_mode == Const.TRAINING_BY_MISSING_DATA:
    ml_missing_df = ml_df.query('previous_score < 90 and current_score < 90')
    print(ml_missing_df.head(3))

    data_missing = ml_missing_df.iloc[:, 1:]
    label_missing = ml_missing_df.iloc[:, 0]

    data_missing_train, data_missing_test, label_missing_train, label_missing_test = \
        train_test_split(data_missing, label_missing)

    model.fit(data_missing_train, label_missing_train)
else:
    # 일반 데이터로 모델 학습
    model.fit(data_train, label_train)

# 학습된 모델로 예측 수행
predict = model.predict(data_test)
print("predict:" + str(predict))

# 예측 결과에 대한 정확도/통계 출력
accuracy_score = metrics.accuracy_score(label_test, predict)
classification_report = metrics.classification_report(label_test, predict)

print("Accuracy: ", accuracy_score)
print("Statistic: \n", classification_report)

# 시각화 1: 룰 기반 결과 분포 (과거 vs 현재 점수, 색상은 rule 결과)
axis1 = ml_df.plot.scatter(x="previous_score",
                           y="current_score",
                           c="result",
                           colormap="viridis")
axis1.set_title("Rule based")

# 시각화 2: 랜덤 포레스트 모델 결과 분포 (예측 결과에 따른 색상)
axis2 = data_test_original.plot.scatter(x="previous_score",
                                        y="current_score",
                                        c=predict,
                                        colormap="viridis")
axis2.set_title("Random Forest")

# 그래프 출력
plt.show()