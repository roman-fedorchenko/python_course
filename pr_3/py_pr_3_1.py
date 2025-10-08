print("Variant 20 of practic 3. Task 1")
print("Get every 2nd character starting from the 5th character and up to the middle of the word.")
st=""
while not len(st)>0 or not st.isalpha():
   st=input("Enter a word: ")
n = len(st)
m = n // 2
result = st[4:m+1:2]
print("Result: ",result, end="\n")