class Developer:
    def __init__(self, name, language, experience_years):
        self.name = name
        self.language = language
        self.experience_years = experience_years

    def introduce(self):
        return (
            f"안녕하세요. 저는 {self.name}입니다. "
            f"{self.language}를 주로 사용하며, "
            f"개발 경력은 {self.experience_years}년입니다."
        )

    def code(self):
        return f"{self.name}님이 {self.language}로 코딩하고 있습니다."


# 사용 예시
developer = Developer("홍길동", "Python", 3)

print(developer.introduce())
print(developer.code())