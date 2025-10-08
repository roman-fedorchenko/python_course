print("Variant 20 of practic 3. Task 2")
print("A word has been given. Write the letters of the word in a column, first the vowels, and then the consonants.")
st=""
while not len(st)>0 or not st.isalpha():
   st=input("Enter a string: ")
mass="aAiIoOuUeEyY"
mass_a=[ch for ch in st if ch in mass]
mass_b=[ch for ch in st if ch not in mass]
st=mass_a+mass_b
print("Result string:")
for i in st:
   print(i, end="\n")