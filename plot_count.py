import matplotlib.pyplot as plt

# 한글은 제목에만 있으므로 제목에만 한글 글꼴(Malgun Gothic)을 쓴다.
# 전체를 한글 글꼴로 바꾸면 로그 눈금(10^-4)의 − 기호가 깨진다.
KOREAN_FONT = "Malgun Gothic"

# measure_count.py 결과 (n = 100만 고정, 찾는 개수 k만 증가)
K = [100, 1000, 10000, 100000]

# 랜덤 key k개를 하나씩 찾는 전체 시간(초). Linear는 k=1만부터 측정하지 않았다.
EQ = {
    "Linear": [1.61e+01, 1.75e+02, None, None],
    "Hash": [2.41e-04, 1.76e-03, 1.51e-02, 1.49e-01],
    "B tree": [2.81e-03, 4.93e-02, 1.77e-01, 1.93e+00],
    "B plus tree": [9.16e-04, 7.06e-03, 5.67e-02, 6.56e-01],
}

# 레코드 k개가 든 범위를 한 번 검색하는 시간(초). Hash는 버킷 전체를 훑는 scan 방식이다.
RANGE = {
    "Linear": [6.22e-01, 6.19e-01, 6.20e-01, 6.30e-01],
    "Hash": [4.26e-01, 4.40e-01, 4.30e-01, 4.40e-01],
    "B tree": [7.05e-05, 4.66e-04, 5.05e-03, 7.58e-02],
    "B plus tree": [2.84e-05, 1.55e-04, 4.24e-03, 2.55e-02],
}


# 자료구조마다 색을 고정한다. 일부만 그려도 색이 바뀌지 않는다.
COLORS = {"Linear": "C0", "Hash": "C1", "B tree": "C2", "B plus tree": "C3"}


def draw(data, title, filename, names=None):
    # names: 그릴 자료구조 목록. None이면 전부 그린다.
    plt.figure(figsize=(7, 5))
    for name, ys in data.items():
        if names is not None and name not in names:
            continue
        # None(측정 안 함)인 칸은 빼고 그린다
        xs = []
        vals = []
        for x, y in zip(K, ys):
            if y is not None:
                xs.append(x)
                vals.append(y)
        plt.plot(xs, vals, marker="o", label=name, color=COLORS[name])
    # 값이 1e-5 ~ 1e+2로 퍼져 있어서 로그 축을 쓴다. 기울기 = 복잡도
    plt.xscale("log")
    plt.yscale("log")
    plt.xticks(K, [f"{x:,}" for x in K])
    plt.xlabel("k (records to find)")
    plt.ylabel("time (s)")
    if title is not None:   # title=None이면 제목을 넣지 않는다
        plt.title(title, fontfamily=KOREAN_FONT)
    plt.grid(True, which="major", alpha=0.3)
    plt.legend()
    plt.savefig(filename, dpi=120, bbox_inches="tight")
    print(f"saved: {filename}")


draw(EQ, "select_eq, 등호 검색 (n=1,000,000)", "count_eq.png")
draw(RANGE, "select_range, 범위 검색 (n=1,000,000)", "count_range.png")
# 선형 탐색과 B+트리만 비교
ONLY = ["Linear", "B plus tree"]
draw(EQ, None, "count_eq_lb.png", ONLY)   # 이 그래프는 제목 없음
draw(RANGE, "select_range, 범위 검색 (n=1,000,000)", "count_range_lb.png", ONLY)
# 해시와 B+트리만 비교
HB = ["Hash", "B plus tree"]
draw(EQ, "select_eq, 등호 검색 (n=1,000,000)", "count_eq_hb.png", HB)
draw(RANGE, "select_range, 범위 검색 (n=1,000,000)", "count_range_hb.png", HB)
plt.show()
