import json

FILE = "todos.json"
LANG_PROMPT = "请选择语言 / Choose language (1.中文 2.English): "

MSG = {
    "zh": {
        "menu": "\n1.添加 2.完成 3.查看 0.退出 > ",
        "add_hint": "请输入待办（每行一条，空行结束）：",
        "complete": "完成序号：",
        "invalid": "无效序号。",
        "empty": "清单为空。",
        "added": "已添加 {n} 条待办。",
    },
    "en": {
        "menu": "\n1.Add 2.Done 3.View 0.Quit > ",
        "add_hint": "Enter todos (one per line, empty line to finish):",
        "complete": "Number to complete: ",
        "invalid": "Invalid number.",
        "empty": "List is empty.",
        "added": "Added {n} todo(s).",
    },
}


def load():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save(todos):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def show(todos, m):
    if not todos:
        print(m["empty"])
        return
    for i, t in enumerate(todos, 1):
        print(f"{i}. {'[x]' if t['done'] else '[ ]'} {t['content']}")


def main():
    m = MSG["en" if input(LANG_PROMPT).strip() == "2" else "zh"]
    todos = load()
    while True:
        choice = input(m["menu"]).strip()
        if choice == "0":
            break
        if choice == "1":
            print(m["add_hint"])
            new = []
            while line := input().strip():
                new.append({"content": line, "done": False})
            if new:
                todos.extend(new)
                save(todos)
                print(m["added"].format(n=len(new)))
        elif choice == "2":
            show(todos, m)
            try:
                todos[int(input(m["complete"])) - 1]["done"] = True
                save(todos)
            except (ValueError, IndexError):
                print(m["invalid"])
        elif choice == "3":
            show(todos, m)


if __name__ == "__main__":
    main()