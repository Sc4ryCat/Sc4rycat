from Crypto.PublicKey import RSA
# RSA 암호화를 위한 OAEP 패닝 모듈 import
from Crypto.Cipher import PKCS1_OAEP
import base64 # base64로 화면에서 보기좋게 변환하기 위해

from 비대칭키_RSA.전자서명해킹 import public_key

key_pair = RSA.generate(2048)
public_key = key_pair.public_key() # 공개키를 추출
private_key = key_pair # 개인키는 생성된 key_pair 자체

plaintext = "비밀메시지 입니다".encode("utf-8") # 한글문자열을 바이트로 인코딩
# plaintext = b"secret message" # 영어는

# 공개키로 암호화
# 공개키를 사용해서 암호화 도구를 생성
cipher_encrypt = PKCS1_OAEP.new(public_key)
# 평문을 공개키로 암호화 -> 암호문이 생성이 됨
ciphertext = cipher_encrypt.encrypt(plaintext)

print("암호문(base64):",base64.b64encode(ciphertext).decode())

# 상황
# 해커가 개인키 없이 복호화를 시도하는 상황을 시물레이션
fake_key = RSA.generate(2048) # 해커가 가진 가짜키 쌍을 생성(정상적인 키와 무관)
fake_cipher = PKCS1_OAEP.new(fake_key) # 가짜 개인키로 복화화 시도할 객체 생성

# 복호화 시도
try:
    hacked = fake_cipher.decrypt(ciphertext) # 복호화 시도(실패해야 정상)
    print("해커가 복호화 성공",hacked)
except Exception as e:
    print("복호화 실패 - 해커는 개인키가 없어 실패", str(e))






