# base64 모듈을 가져옴
import base64
# 원본 문자열 정의
origin_text = "국제직업전문학교"

# 1번째 문자열을 utf-8로 인코딩->바이트로 변환
origin_byte = origin_text.encode('UTF-8')
print(origin_byte)
# 2번째 바이트를 base64로 인코딩
encode_bytes = base64.b64encode(origin_byte)
print(encode_bytes)
# 3번째 인코딩된 바이트를 사람이 읽을 수 있는 문자열로 디코딩
encoded_text = encode_bytes.decode('UTF-8')
print(encoded_text)
# 4번째 인코딩된 문자열을 다시 바이트로 변환
encoded_bytes_again = encoded_text.encode('UTF-8')
print(encoded_bytes_again )
# 5번째 base64로 디코딩 -> 원래 바이트
decoded_bytes = base64.b64decode(encoded_bytes_again)
print(decoded_bytes)
# 6번째 디코딩된 바이트를 utf-8로 문자열 변환
decode_text = decoded_bytes.decode('UTF-8')
# 결과 출력
print("\n 디코딩 결과:")
print(decode_text)


