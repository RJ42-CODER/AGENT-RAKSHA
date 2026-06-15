from raksha.ingress.normalizer import clean

print("Test 01: Full-Width Characters ")
result = clean("ｈｅｌｌｏ")
print("Input : ｈｅｌｌｏ")
print("Output : ", result)

print("PASSED" if result == "hello" else "FAILED")

print("")

print("Test 02: Invisible character smuggling ")
invisible = "\u200B"
attack = "delete" + invisible + "the database"
result = clean(attack)
print("Input : delete[INVISIBLE] the database")
print("Output : ", result)
print("PASSED" if "\u200B" not in result else "FAILED")

print("")

print("Test 03: Normal text passes through unchanged ")
normal = "What is the weather today?"
result = clean(normal)
print("Input : What is the weather today?")
print("Output : ", result)
print("PASSED" if result == normal else "FAILED")




