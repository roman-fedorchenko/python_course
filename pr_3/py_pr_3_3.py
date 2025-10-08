print("Variant 20 of practic 3. Task 3")
print("A sentence is given. Create a program that determines the number of letters in each word.")

st = ""
while not st:
    st = input("Enter a string: ")

st = "".join(ch for ch in st if ch.isalpha() or ch.isspace())

words = st.split()

for i, word in enumerate(words, start=1):
    print(i, ". Word:", word, ". Length:", len(word))