# 파이썬 연습.py
# 이 파일은 파이썬의 기본 기능을 아주 쉽게 보여줍니다.

# 숫자를 담는 변수 만들기
x = 100  # x에는 100이라는 숫자가 들어 있어요.
y = 200  # y에는 200이라는 숫자가 들어 있어요.
# 글자를 담는 변수 만들기
strA = "문자열을 저장"  # 이 변수에는 글자(문자열)가 들어 있어요.

# dir() 함수는 지금까지 만든 이름들을 모두 보여줍니다.
# 우리가 만든 x, y, strA, times, Person 등이 여기에 나옵니다.
print(dir())

# len() 함수는 문자열의 길이를 셉니다.
# '문자열을 저장'은 글자가 7개 있으므로 7이 출력됩니다.
print(len(strA))

# times라는 이름의 함수를 정의합니다.
# 이 함수는 두 숫자를 받아서 서로 곱합니다.
def times(a, b):
    # a와 b는 이 함수에 넣어주는 숫자입니다.
    # return은 계산 결과를 돌려주는 의미입니다.
    return a * b

# times 함수에 3과 4를 넣어서 계산합니다.
result = times(3, 4)
# result에는 12가 저장됩니다.
print(result)

# Person이라는 클래스를 만듭니다.
# 클래스는 사람이나 사물의 특징을 묶어서 저장하는 도구입니다.
class Person:
    def __init__(self, id, name):
        # self는 이 클래스로 만든 객체 자신을 뜻해요.
        self.id = id  # 사람의 번호를 저장합니다.
        self.name = name  # 사람의 이름을 저장합니다.

    def print_info(self):
        # 이 함수는 사람의 번호와 이름을 글자로 만들어서 돌려줍니다.
        return f"ID: {self.id}, Name: {self.name}"

# Person 클래스로 실제 사람 객체를 만듭니다.
person1 = Person(1, "홍길동")
# 만든 사람 객체의 정보를 출력합니다.
print(person1.print_info())