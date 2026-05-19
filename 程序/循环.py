import time

#for-in
for i in range(5):
    print(i)
    time.sleep(0.1)

for _ in range(5):
    print("Hello")
    time.sleep(0.1)

#while
i = 0
while i < 5:
    print(i)
    i += 1
    time.sleep(0.1)

#break，continue
for i in range(5):
    if i == 2:
        continue
    elif i == 3:    
        break
    print(i)
    time.sleep(0.1)

#嵌套
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f'{i}×{j}={i * j}', end='\t')
    print()