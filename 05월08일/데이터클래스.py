print("데이터 클래스")

from dataclasses import dataclass # @dataclass
# @dataclass 데코레이터를 사용하기 위한 표준 라이브러리

@dataclass
class UserData: # UserData 클래스를 데이터 클래스로 선언 생성자,출력,비교 기능이 자동으로 생성
    name: str # 필드타입 지정과 함께 선언
    age: int # 필드타입 지정과 함께 선언

# 객체 생성
user1 = UserData("tom",30) # name=tom,age=30을가진 객체를 생성
#출력
print(user1)
print(user1.name,user1.age)

user2 = UserData("tom",30) # name=tom,age=30을가진 객체를 생성
# __eq__() 자동생성 되기 때문에 True가 출력
print("두 객체가 같은가?", user1 == user2)



