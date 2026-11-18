import matplotlib.pyplot as plt

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
    "Hash (scan)": [4.26e-01, 4.40e-01, 4.30e-01, 4.40e-01],
    "B tree": [7.05e-05, 4.66e-04, 5.05e-03, 7.58e-02],
    "B plus tree": [2.84e-05, 1.55e-04, 4.24e-03, 2.55e-02],
}


def draw(data, title, filename):
    plt.figure(figsize=(7, 5))
    for name, ys in data.items():
        # None(측정 안 함)인 칸은 빼고 그린다
        xs = []
        vals = []
        for x, y in zip(K, ys):
            if y is not None:
                xs.append(x)
                vals.append(y)
        plt.plot(xs, vals, marker="o", label=name)
    # 값이 1e-5 ~ 1e+2로 퍼져 있어서 로그 축을 쓴다. 기울기 = 복잡도
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("k (records to find)")
    plt.ylabel("time (s)")
    plt.title(title)
    plt.grid(True, which="major", alpha=0.3)
    plt.legend()
    plt.savefig(filename, dpi=120, bbox_inches="tight")
    print(f"saved: {filename}")


draw(EQ, "select_eq: k random keys, total time (n=1,000,000)", "count_eq.png")
draw(RANGE, "select_range: one range with k records (n=1,000,000)", "count_range.png")
plt.show()
