import timeit, chardet


# Алгоритм вимірювання часу виконання функції пошуку підрядка
def measure_time(search_function, text, pattern):
    start_time = timeit.default_timer()
    result = search_function(text, pattern)
    execution_time = timeit.default_timer() - start_time
    return result, execution_time

   
# Алгоритм пошуку підрядка Кнута-Морріса-Пратта (KMP)
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    M = len(pattern)
    N = len(text)

    lps = compute_lps(pattern)
    i = j = 0

    while i < N:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1 


# Алгоритм пошуку підрядка Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for char in pattern:
        table[char] = length
    
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0 

    while i <= len(text) - len(pattern):
        j = len(pattern) - 1 

        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1 

        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    return -1


# Алгоритм пошуку підрядка Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(text, pattern):
   
    substring_length = len(pattern)
    main_string_length = len(text)
    base = 256 
    modulus = 101  
    
    substring_hash = polynomial_hash(pattern, base, modulus)
    current_slice_hash = polynomial_hash(text[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if text[i:i+substring_length] == pattern:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(text[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(text[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1


search_function = {
    "Алгоритм Кнута-Морріса-Пратта": kmp_search,
    "Алгоритм Боєра-Мура": boyer_moore_search,
    "Алгоритм Рабіна-Карпа": rabin_karp_search,
}

text = {
    "ВИКОРИСТАННЯ АЛГОРИТМІВ У БІБЛІОТЕКАХ МОВ ПРОГРАМУВАННЯ": "goit-algo-hw-05-main/article1.txt",
    "МЕТОДИ ТА СТРУКТУРИ ДАНИХ ... ДЛЯ СОЦІАЛЬНОЇ МЕРЕЖІ": "goit-algo-hw-05-main/article2.txt"
}

pattern = [
    "правильно підібраний алгоритм пошуку",
    "колекція повинна бути відсортована",
    "діапазон",
    "кожна система містить набір обмежень і вимог",
    "імітаційна модель рекомендаційної системи для проведення експериментів",
    "дослідження та програмна реалізація",
    "Хеш-таблиця (hash map) – це структура даних, у якій пошук елементу здійснюється на основі його ключа"
]


if __name__ == "__main__":

    print("       ПОШУК ПІДРЯДКА В ТЕКСТІ ЗА ДОПОМОГОЮ РІЗНИХ АЛГОРИТМІВ\n")
    
    # Словники для збереження абсолютно найкращих/найгірших результатів
    all_results = []

    for title, t in text.items():
        # Автоматично визначаємо кодування, читаємо файл як сирі байти ('rb'), аналізуємо байти та отримуємо словник із результатом
        with open(t, 'rb') as raw_file:
            raw_data = raw_file.read()
            detection = chardet.detect(raw_data)
            detected_encoding = detection['encoding']
        
        text_content = raw_data.decode(detected_encoding, errors='ignore').lower()
        print(f'📄 РЕСУРС №{list(text.keys()).index(title) + 1} "{title}"')
        print(f'   ⚙️  Автовизначене кодування ресурса: \033[93m{detected_encoding}\033[0m')
        print(f'   📏 Довжина тексту: {len(text_content)} символів.\n')

        for p_original in pattern:
            p = p_original.lower()
            print(f'🔍 Пошук підрядка:  "\033[96m{p}\033[0m"')    

            print(f"┌{'─'*31}┬{'─'*15}┬{'─'*10}┬{'─'*15}┐")
            print(f"│ {'Алгоритм':<30}│ {'  Статус':<12}  │ {'Позиція':<8} │ {'Час (сек)':<8}     │")
            print(f"├{'─'*31}┼{'─'*15}┼{'─'*10}┼{'─'*15}┤")
            
            for name, func in search_function.items():
                result, execution_time = measure_time(func, text_content, p)
                
                # Форматуємо статус, позицію та додаємо кольори
                if result != -1:
                    status = "\033[32m Знайдено\033[0m"
                    # Додаємо пробіли для вирівнювання через те, що ANSI-коди ламають стандартну довжину рядка
                    status_padding = " " * 4  
                    pos_str = f"{result:<8}"
                else:
                    status = "\033[31m Не знайдено\033[0m"
                    status_padding = " " * 1
                    pos_str = f"{'-':<8}"
                
                # Виведення рядка таблиці з чітким вирівнюванням
                print(f"│ {name:<30}│ {status}{status_padding} │ {pos_str} │ {execution_time:<10.8f}    │")
                # --- Фіксація глобальної статистики для кожного алгоритму ---
                
                all_results.append({
                    'name': name,
                    'time': execution_time,
                    'pattern': p,
                    'resource': title
                })

            print(f"└{'─'*31}┴{'─'*15}┴{'─'*10}┴{'─'*15}┘")
            print("")


# --- ФІНАЛЬНИЙ ЗВІТ ---

    print("=" * 76)
    print("🏆 ФІНАЛЬНІ РЕЗУЛЬТАТИ ТЕСТУВАННЯ АЛГОРИТМІВ:")
    print("=" * 76)

    # Визначаємо абсолютного переможця за мінімальним часом серед усіх записів
    if all_results:
        # Шукаємо запис із мінімальним часом серед абсолютно всіх запусків
        best_data = min(all_results, key=lambda x: x['time'])
        print(f"⚡ Абсолютно \033[32m НАЙШВИДШИЙ\033[0m запуск:")
        print(f"   Алгоритм:  \033[1m{best_data['name']}\033[0m")
        print(f"   ⏱ Час:        {best_data['time']:.6f} sec.")
        print(f"   Патерн:    '{best_data['pattern']}'")
        print(f"   📄 Ресурс:    '{best_data['resource']}'\n")

        # Шукаємо запис із максимальним часом серед абсолютно всіх запусків
        worst_data = max(all_results, key=lambda x: x['time'])
        print(f"🐢 Абсолютно \033[31m НАЙПОВІЛЬНІШИЙ\033[0m запуск:")
        print(f"   Алгоритм:  \033[1m{worst_data['name']}\033[0m")
        print(f"   ⏱ Час:        {worst_data['time']:.6f} sec.")
        print(f"   Патерн:    '{worst_data['pattern']}'")
        print(f"   📄 Ресурс:    '{worst_data['resource']}'")
        print("=" * 76)
