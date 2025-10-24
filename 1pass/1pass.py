import random
nums = ["0","1","2","3","4","5","6","7","8","9"]
lowerLetters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
upperLetters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
symbols = ["~","!","@","#","$","%","^","&","*","(",")","_","-","+","=","}","{",":",";",">","<",".",",","/","?"]
password = ""
i = 0
while i < 36:
    rand = random.randint(0,3)
    if rand == 0:
        char = nums[random.randint(0,len(nums)-1)]
    elif rand == 1:
        char = lowerLetters[random.randint(0,len(lowerLetters)-1)]
    elif rand == 2:
        char = upperLetters[random.randint(0,len(upperLetters)-1)]
    else:
        char = symbols[random.randint(0,len(symbols)-1)]
    password += char
    i += 1
print(password)