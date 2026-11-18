import random
import time

import hash
from measure_sparse import STRUCTURES, make_sparse_data, next_prime


def hash_scan_ops(n):
    # 해시와 같지만 범위 검색만 "버킷 전체 훑기"로 한다
    return (hash.make_table(next_prime(n)),
            hash.insert,
            hash.select_eq,
            hash.select_range_scan)

# 해시 바로 다음에 "Hash (scan)"을 끼워 넣는다
STRUCTURES = STRUCTURES[:2] + [("Hash (scan)", hash_scan_ops)] + STRUCTURES[2:]

# 실험 설정: 저장된 데이터 수 n과 gap은 고정하고,
# "찾아야 하는 레코드 수"(k)만 10배씩 늘린다
#   select_eq    : 랜덤 key k개를 등호 검색으로 하나씩 찾는 전체 시간
#   select_range : 레코드가 k개 들어 있는 범위를 한 번 검색하는 시간
N = 10**6
GAP = 1
COUNTS = [100, 1000, 10000, 100000]
REPEAT = 10          # 범위 검색은 10번 재서 평균을 낸다
# 선형 등호 검색은 1번에 약 0.06초(n=100만)라서 k=1만이면 10분이 넘는다.
# 그래서 이 k보다 크면 건너뛴다(표에 None).
LINEAR_EQ_MAX_K = 1000


def measure_count(name, make_ops):
    # 구조는 한 번만 만들고, k만 바꿔 가며 잰다
    table, insert, select_eq, select_range = make_ops(N)
    for rec in make_sparse_data(N, GAP):
        insert(table, rec)

    eq_results = []
    range_results = []
    for count in COUNTS:
        # 등호 검색: 실제로 있는 랜덤 key k개를 하나씩 찾는 전체 시간
        # (k번 검색 자체가 평균 역할을 하므로 반복하지 않는다)
        if name == "Linear" and count > LINEAR_EQ_MAX_K:
            eq_results.append(None)
        else:
            keys = []
            for _ in range(count):
                keys.append(random.randint(0, N - 1) * GAP)
            start = time.perf_counter()
            for key in keys:
                select_eq(table, key)
            eq_results.append(time.perf_counter() - start)

        # 범위 검색: 이 폭 안에 레코드가 정확히 k개 있다 (REPEAT번 평균)
        width = count * GAP
        los = []
        for _ in range(REPEAT):
            los.append(random.randint(0, (N - count) * GAP))
        start = time.perf_counter()
        for lo in los:
            select_range(table, lo, lo + width)
        range_results.append((time.perf_counter() - start) / REPEAT)
    return eq_results, range_results


def run(name, make_ops):
    eq_results, range_results = measure_count(name, make_ops)
    print()
    print(f"===== {name} (n={N:,}, gap={GAP}) =====")
    header = f"{'op':<22}" + "".join(f"{'k=' + format(c, ','):>14}" for c in COUNTS)
    print(header)
    print("-" * 78)
    for label, results in [("select_eq k keys", eq_results),
                           ("select_range k rec", range_results)]:
        row = f"{label:<22}"
        for t in results:
            if t is None:
                row += f"{'None':>14}"
            else:
                row += f"{t:>14.2e}"
        print(row, flush=True)


for name, make_ops in STRUCTURES:
    run(name, make_ops)
