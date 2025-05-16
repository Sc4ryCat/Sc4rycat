from json_logic import jsonLogic
from statistics import mean
from enum import Enum, IntEnum
import random
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt


class Const(str, Enum):
    PASS = "Y"
    FAIL = "N"


class LearningConfig(IntEnum):
    RULE_CURRENT_SCORE = 70
    RULE_MEAN = 50
    RULE_FREE_PASS_SCORE = 90


# 룰을 이용해서 결과를 판단한다
# (현재 성적이 70 점 이상 and 전 시험과의 평균이 50 점 이상) or 현재 90점 이상
def check_exam_list(score_list):
    rule = {"or":
                [{"and":
                      [{">=": [{"var": "current_score"},
                               LearningConfig.RULE_CURRENT_SCORE]},
                       {">=": [{"var": "mean"},
                               LearningConfig.RULE_MEAN]}]},
                 {">=": [{"var": "current_score"},
                         LearningConfig.RULE_FREE_PASS_SCORE]}]
            }

    exam_dict = {}
    exam_dict["current_score"] = score_list[1]
    exam_dict["mean"] = score_list[2]

    rule_result = jsonLogic(rule, exam_dict)

    if rule_result:
        return Const.PASS.value
    else:
        return Const.FAIL.value


# 랜덤 데이터 만들어 줌.
def make_random_numbers(min, max, sample_number):
    my_set = set()

    # 겹치는 데이터가 없게 하기 위해서 set을 사용하여 중복 생성 데이터 제거
    while 1:
        previous_score = random.randint(min, max)
        current_score = random.randint(min, max)
        score_mean = mean([previous_score, current_score])
        my_set.add(tuple([previous_score, current_score, score_mean]))
        if len(my_set) == sample_number:
            break

    random_list = [list(x) for x in my_set]

    # 룰 엔진 정답 맨 앞에 추가
    for index, item in enumerate(random_list):
        result = check_exam_list(item)
        item.insert(0, result)

    return random_list


# 두 개의 영역으로 나뉜 랜덤 셋을 만든다.
random_set_normal = make_random_numbers(0, 100, 5000)
random_set_abnormal = make_random_numbers(150, 200, 10)
random_set_full = random_set_normal + random_set_abnormal

normal_df = pd.DataFrame.from_records(random_set_normal)
full_df = pd.DataFrame.from_records(random_set_full)

# 컬럼 이름을 달아준다.
normal_df.columns = ["result", "previous_score", "current_score", "mean"]
full_df.columns = ["result", "previous_score", "current_score", "mean"]

# 미사용 값 제거
normal_df.drop(["result", "mean"], axis=1, inplace=True)
full_df.drop(["result", "mean"], axis=1, inplace=True)
print(normal_df.head(3))
print(full_df.head(3))

# IsolationForest 모델 학습 시키기
model = IsolationForest(n_estimators=50, max_samples=100,
                        contamination=0.008, random_state=42)
model.fit(normal_df)

# 학습 시킨 모델로 abnormal 데이터 예측 하기
predict = pd.DataFrame(model.predict(full_df))
score = model.decision_function(full_df)
full_df['score'] = score
full_df['anomaly'] = predict
print(full_df.head(3))

anomaly_data = full_df.loc[full_df['anomaly']==-1]
print(anomaly_data.head(3))

axis1 = full_df.plot.scatter(x="previous_score",
                             y="current_score",
                             c="anomaly",
                             colormap='viridis')
axis1.set_title("Isolation Forest")

plt.show()
