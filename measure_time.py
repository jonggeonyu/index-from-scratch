import linear
import hash
import btree
import bplustree

SIZES = [10**3, 10**4, 10**5, 10**6]
WIDTH = 100  # 범위 탐색 폭

# 측정할 자료구조 (이름, 모듈). 오래 걸리는 건 주석 처리해서 건너뛴다.
STRUCTURES = [
    ("Linear", linear),
    ("Hash", hash),
    ("B tree", btree),
    ("B plus tree", bplustree),
]


def fmt(t):
    # 숫자면 지수 표기, 아니면(None 등) 그대로 보여 준다
    if isinstance(t, (int, float)):
        return f"{t:.2e}"
    return str(t)


def measure(module, op, n):
    if op == "insert":
        return module.measure_insert(n)
    if op == "select_eq":
        return module.measure_select_eq(n)
    if op == "select_range":
        if module is linear:
            # linear.py는 폭 100이 함수 안에 고정되어 있어 n만 받는다
            return module.measure_select_range(n)
        return module.measure_select_range(n, WIDTH)


def run(name, module):
    ops = [
        # 한글은 터미널에서 폭이 2칸이라 줄이 어긋나므로 라벨은 영어로 쓴다
        ("insert", "insert (total)"),
        ("select_eq", "select_eq (avg)"),
        ("select_range", f"select_range w={WIDTH}"),
    ]
    print()
    print(f"===== {name} =====")
    header = f"{'op':<22}" + "".join(f"{'n=' + format(n, ','):>14}" for n in SIZES)
    print(header)
    print("-" * 78)
    for op, label in ops:
        row = f"{label:<22}"
        for n in SIZES:
            row += f"{fmt(measure(module, op, n)):>14}"
        print(row, flush=True)


for name, module in STRUCTURES:
    run(name, module)
