print("일반 클래스 버전")

class User:
    def __init__(self, name, age): #__init__ 생성자 정의, name,age를 전달받습니다
        self.name = name # 전달받은 값을 인스턴스 변수로 저장
        self.age = age   # 전달받은 값을 인스턴스 변수로 저장

    def __repr__(self): # 객체를 보기좋게 포멧팅된 문자열 반환하는 함수
        return  f"User(name='{self.name}', age={self.age})"

# 객체 생성 User객체를 생성
user1 = User("tom",30)

# 출력 및 비교
print(user1) #__repr__ 으로 객체 내용을 보기좋게 출력
print(user1.name,user1.age) # 각각의 속성에 직접 접근하여 출력

user2 = User("tom",30)
# __eq__() 자동생성 안되기 때문에 False가 출력
print("두 객체가 같은가?", user1 == user2) # True,False





