"""
해시 연산을 수만번 반복 -> 연산 비용 증가
공격자가 무차별로 대입할 때 매우 느려짐
"""
import hashlib
import os # os모듈(무작위 바이트 생성용)

password = "admin"
salt = os.urandom(16)

# 초기 입력값: 비밀번호 + 솔트를 합쳐서 바이트로 변환
dk = password.encode() + salt

# 반복해싱 (예:100,000)
# 공격자가
# 0부터 99,999까지 총 100,000번 반복합니다
# _ => 변수를 쓰지 않겠다
for _ in range(100_000):
    dk = hashlib.sha256(dk).digest()

# 최종 해시값 출력
final_hash = dk.hex()

print("반복 해시 결과",final_hash)
print("사용된 솔트(hex)", salt.hex())


for _ in range(5):
    print("admin")