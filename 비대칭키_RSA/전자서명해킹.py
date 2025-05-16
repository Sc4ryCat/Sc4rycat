# 필요한 모듈 import

from Crypto.PublicKey import RSA # RSA 키 생성 모듈
from Crypto.Signature import pkcs1_15 # 전자서명(v1.5방식) 모듈
from Crypto.Hash import SHA256 # 해시 알고리즘

# RSA 키 생성(개인키/공개키)
key = RSA.generate(2048) # 2048비트 rsa키쌍 생성
private_key = key # 개인키 추출
public_key = key.public_key() # 공개키 추출
# 서명 대상 평문 메시지 정의
message = '전자서명 테스트' # 평문
message_byte = message.encode('utf-8') # 평문을 바이트 형태로 변환(해시처리때문에)
# 서명 생성(개인키 사용)
hash_value = SHA256.new(message_byte) # sha-256 해시 객체 생성
# 개인키로 해시값을 서명
signature = pkcs1_15.new(private_key).sign(hash_value)

# 생성된 전자서명 출력(hex로 보기좋게 잘라서 출력)
print("전자서명 생성 완료",signature.hex()[:50]+"...")

# 서명 검증(공개키 사용)
try:
    pkcs1_15.new(public_key).verify(hash_value,signature) # 공개키로 서명을 검증
    print("전자서명 인증 성공! 메시지가 위조되지 않음!!")
except(ValueError,TypeError): # 검증 실패시 발생 가능한 예외 처리
    print("전자서명 검증 실패! 메시지가 변조되었거나 서명이 위조됨")






