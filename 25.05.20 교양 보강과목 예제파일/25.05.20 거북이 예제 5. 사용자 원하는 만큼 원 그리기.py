import turtle as t

t.shape("turtle")

n = int(input("원의 개수를 입력하시오:"))

for i in range(n):
    t.circle(100)
    t.left(360/n)

t.done()
