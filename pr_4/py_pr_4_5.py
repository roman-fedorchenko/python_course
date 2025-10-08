def process_text(text):
    vowels = {"a", "e", "i", "o", "u", "y"}
    text_set = set(text.lower())

    try:
        result = text_set & vowels
        return result, sum(1 for ch in text if ch.lower() in vowels)
    except Exception:
        text_list = list(text.lower())
        result = set([ch for ch in text_list if ch in vowels])
        return result, sum(1 for ch in text if ch.lower() in vowels)
    
print("Variant 20 of practic 4. Task 4")
st = input("Enter a text with letters and digits: ")
res_set, count = process_text(st)

print("Vowels found in text (set):", res_set)
print("Total number of vowels:", count)
