import json, re
from datetime import datetime

FILE = "roster.json"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

T = {
    "zh": {"name":"姓名","email":"邮箱","join":"加入日期(DD-MM-YYYY，回车=今天)","bday":"生日(DD-MM-YYYY，可留空)",
           "topic":"学习内容(可留空)","empty_name":"姓名不能为空","bad_email":"邮箱格式不正确","dup":"邮箱已存在",
           "bad_date":"日期格式不正确","added":"已添加","kw":"关键词(回车=全部)","none":"未找到",
           "del_kw":"要删除的姓名/邮箱","del_idx":"输入编号确认删除(回车取消)","not_int":"请输入数字",
           "deleted":"已删除","menu":"1.添加 2.查询 3.删除 0.退出 > ","invalid":"无效选项","bye":"再见"},
    "en": {"name":"Name","email":"Email","join":"Join date (DD-MM-YYYY, enter=today)","bday":"Birthday (DD-MM-YYYY, optional)",
           "topic":"Learning topic (optional)","empty_name":"Name required","bad_email":"Invalid email","dup":"Email exists",
           "bad_date":"Invalid date","added":"Added","kw":"Keyword (enter=all)","none":"None found",
           "del_kw":"Name/email to delete","del_idx":"Enter index to delete (enter=cancel)","not_int":"Number required",
           "deleted":"Deleted","menu":"1.Add 2.Query 3.Delete 0.Quit > ","invalid":"Invalid option","bye":"Bye"},
}
LANG = "zh"
def t(k): return T[LANG][k]

def load():
    try: return json.load(open(FILE, "r", encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError): return []

def save(r): json.dump(r, open(FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def valid_date(s):
    try: datetime.strptime(s, "%d-%m-%Y"); return True
    except ValueError: return False

def add(r):
    name = input(t("name")+": ").strip()
    bday = input(t("bday")+": ").strip()
    email = input(t("email")+": ").strip()
    date = input(t("join")+": ").strip() or datetime.today().strftime("%d-%m-%Y")
    topic = input(t("topic")+": ").strip()
    if not name: return print(t("empty_name"))
    if not EMAIL_RE.match(email): return print(t("bad_email"))
    if any(s["email"].lower() == email.lower() for s in r): return print(t("dup"))
    if not valid_date(date) or (bday and not valid_date(bday)): return print(t("bad_date"))
    r.append({"name":name,"birthday":bday,"email":email,"join_date":date,"topic":topic})
    save(r); print(f"{t('added')}: {name}")

def query(r):
    kw = input(t("kw")+": ").strip().lower()
    hits = [s for s in r if not kw or kw in s["name"].lower() or kw in s["email"].lower()]
    if not hits: return print(t("none"))
    for i, s in enumerate(hits, 1):
        print(f"{i}. {s['name']:<12}{s.get('birthday',''):<12}{s['email']:<26}{s.get('join_date',''):<12}{s.get('topic','')}")

def delete(r):
    kw = input(t("del_kw")+": ").strip().lower()
    hits = [(i, s) for i, s in enumerate(r) if kw and (kw in s["name"].lower() or kw in s["email"].lower())]
    if not hits: return print(t("none"))
    for n, (_, s) in enumerate(hits, 1): print(f"{n}. {s['name']}（{s['email']}）")
    try: idx = int(input(t("del_idx")+": ") or 0) - 1
    except ValueError: return print(t("not_int"))
    if 0 <= idx < len(hits):
        s = r.pop(hits[idx][0]); save(r); print(f"{t('deleted')}: {s['name']}")

ACTIONS = {"1": add, "2": query, "3": delete}
LANG = (input("Language / 语言 (zh/en, default=zh): ").strip().lower() or "zh")
if LANG not in T: LANG = "zh"
roster = load()
try:
    while (c := input("\n"+t("menu")).strip()) != "0":
        (ACTIONS.get(c) or (lambda _: print(t("invalid"))))(roster)
    print(t("bye"))
except (KeyboardInterrupt, EOFError): print("\n"+t("bye"))