count = 0
phrase = "hello, world"
for iteration in range(5):
    count += len(phrase)
    print("Iteration " + str(iteration) + "; count is: " + str(count))

import string

print(len(string.ascii_lowercase))
print(string.punctuation)
print(string.digits)
print(string.punctuation + " " + string.digits)