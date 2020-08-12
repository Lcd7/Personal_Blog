class Person:
    # 类属性
    home = "earth"
    def __init__(self, name, age):
        # 实例属性
        self.name = name
        self.age = age

a = Person('lcd', 22)
a.home = 'qwe'
print(a.home)

import random
for _ in range(100):
    print(random.randint(1, 50))