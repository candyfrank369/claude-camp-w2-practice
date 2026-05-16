import re

MESSAGES = {
    "zh": {
        "choose_lang": "请选择语言 / Please choose language:\n  1. 中文\n  2. English\n请输入序号 (1/2): ",
        "invalid_choice": "无效的选择，默认使用中文。",
        "prompt_input": "请输入一段文字（输入完成后按回车）：",
        "no_words": "未检测到任何单词。",
        "result_title": "\n词频统计结果（按出现次数从高到低）：",
        "header_word": "单词",
        "header_count": "次数",
    },
    "en": {
        "choose_lang": "请选择语言 / Please choose language:\n  1. 中文\n  2. English\nEnter number (1/2): ",
        "invalid_choice": "Invalid choice, defaulting to English.",
        "prompt_input": "Please enter a paragraph of text (press Enter when done):",
        "no_words": "No words detected.",
        "result_title": "\nWord Frequency Results (sorted by count, high to low):",
        "header_word": "Word",
        "header_count": "Count",
    },
}


def count_word_frequency(text):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    sorted_frequency = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    return sorted_frequency


def choose_language():
    choice = input(MESSAGES["zh"]["choose_lang"]).strip()
    if choice == "1":
        return "zh"
    if choice == "2":
        return "en"
    print(MESSAGES["zh"]["invalid_choice"])
    return "zh"


def main():
    lang = choose_language()
    msg = MESSAGES[lang]

    print(msg["prompt_input"])
    text = input()
    result = count_word_frequency(text)

    if not result:
        print(msg["no_words"])
        return

    print(msg["result_title"])
    print("-" * 30)
    print(f"{msg['header_word']:<15} {msg['header_count']}")
    print("-" * 30)
    for word, count in result:
        print(f"{word:<15} {count}")


if __name__ == "__main__":
    main()
