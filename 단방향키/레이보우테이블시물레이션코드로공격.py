import hashlib

# 비밀번호 후보 목록(공격자가 미리 알고 있는 약한 패스워들)
password_list = ["1234","password","qwerty","admin"]

# 레이보우 테이블 생성( 평문 -> SHA256 해시값)
rainbow_table = {} # 딕셔너리{key:value}
for pw in password_list:
    hash_val = hashlib.sha256(pw.encode()).hexdigest()
    rainbow_table[hash_val] = pw

# 피해자의 유출된 해시값(예:admin)
target_hash = hashlib.sha256("password".encode()).hexdigest()
print("유출된 해시값:",target_hash)
#print(rainbow_table)

# 공격자가 레이보우 테이블로 역추적 시도
if target_hash in rainbow_table:
    print("비밀번호 추출됨", rainbow_table[target_hash])
else:
    print("테이블에 일치하는 해시없음(방어 성공)"),





