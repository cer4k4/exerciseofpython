def testGenerator():
    for i in range(10):
        yield i


generator = testGenerator()

comlist = [g for g in generator]

print(comlist)


