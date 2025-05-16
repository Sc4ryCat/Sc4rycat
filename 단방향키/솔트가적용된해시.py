"""
솔트를 추가해서 동일한 비밀번호라도 결과가 달라짐
솔트는 보통 해시값과 함께 DB에 저장함
"""
import hashlib
import os
# 사용자 비밀번호
password = "admin"
# 솔트 생성(16바이트로 랜덤하게 생성)
salt = os.urandom(16)

# 솔트 + 패스워드 결합 후 해시
hashed_pw = hashlib.sha256(salt + password.encode()).hexdigest()

print("해시값:", hashed_pw)
print("사용된 솔트(hex)", salt.hex())




