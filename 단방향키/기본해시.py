"""
특징
단순 SHA-256 햇
보안 강화 요소 없음 -> 레이보우테이블(사전공격)에 취약
"""
import hashlib
# 사용자 비밀번호
password = "admin1234"

# 해시 생성
hashed_pw = hashlib.sha256(password.encode()).hexdigest()
print("해시값:",hashed_pw)
