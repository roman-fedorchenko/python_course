import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import string
# Завантаження необхідних ресурсів NLTK (виконується один раз)
nltk.download('gutenberg', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
# Вибір тексту для аналізу
text_name = 'milton-paradise.txt'
try:
# Отримання слів з тексту
    words = gutenberg.words(text_name)
    print(f"Text analysis: {text_name}") 
# Загальна кількість слів
    total_words = len(words)
    print(f"Total number of words in the text: {total_words}")
# До очищення
    fdist_raw = FreqDist(words)
    print("\nTop 10 words (before cleaning)")
    top_10_raw = fdist_raw.most_common(10)
    print(top_10_raw)
# Графік 1
# Розділяємо слова і кількість для графіка
    words_raw, counts_raw = zip(*top_10_raw)
    plt.figure(figsize=(10, 5))
# Використовуємо plt.bar замість fdist.plot
    plt.bar(words_raw, counts_raw, color='skyblue') 
    plt.title(f"Top 10 words in {text_name} (untreated)")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.show()
# Очищення
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
# Додаємо специфічні символи
    custom_filters = stop_words.union(punctuation).union({'--', '."', ',"', "''", "``"})
# Фільтрація
    filtered_words = [w.lower() for w in words if w.lower() not in custom_filters and w.isalpha()]
    print(f"\nNumber of words after cleaning: {len(filtered_words)}")
# Після очищення
    fdist_clean = FreqDist(filtered_words)
    print("\nTop 10 words (after cleaning)")
    top_10_clean = fdist_clean.most_common(10)
    print(top_10_clean)
# Графік 2
    words_plot, counts_plot = zip(*top_10_clean)
    plt.figure(figsize=(10, 5))
    plt.bar(words_plot, counts_plot, color='purple')
    plt.title(f"Top 10 words in {text_name} (after removing debris)")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.show()
except Exception as e:
    print(f"Error when working with NLTK: {e}")