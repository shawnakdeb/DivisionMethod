import math

count = 0
DIGITS = 3
ONES = (((10 ** DIGITS) - 1) / 9)
POWER = (10 ** (DIGITS - 1))
MAX_RUNS = 3
run_total = 0
run_count = 0
run_max = 0
min_dividend = 0

def estimate(dsor, dend):
    floor_estimate = min((dend // POWER) // math.floor(dsor / POWER), 9)
    if math.floor(dsor / POWER) == 1 and dsor >= ONES:
        floor_estimate = min(dend // ONES, 9)
    ceil_estimate = (dend // POWER) // math.ceil(dsor / POWER)
    if dsor != POWER and dsor <= ONES:
        ceil_estimate = dend // ONES
    correct_answer = dend // dsor
    return floor_estimate, ceil_estimate, correct_answer

def divide(dsor, cutoff):
    global run_total, run_count, run_max
    max_dend = 10 * dsor
    overran = 0
    for dend in range(10 * dsor):
        runs = 0
        orig_dend = dend
        final_answer = 0
        floor_est, ceil_est, correct_answer = estimate(dsor, dend)
        if abs(floor_est - correct_answer) > 1:
            max_dend = min(max_dend, dend)
        while dend < 0 or dend >= divisor:
            if runs >= MAX_RUNS:
                overran += 1
                runs += 1
                #raise Exception(f"Overran: {dsor}, {orig_dend}, {final_answer}, {correct_answer}")
                #print(dsor, orig_dend, floor_est, ceil_est, answer)
                break
            floor_est, ceil_est, answer = estimate(dsor, dend)
            if dend < -dsor:
                raise Exception(f"Overestimated: {dsor}, {orig_dend}, {final_answer}, {correct_answer}")
            elif dend < 0:
                dend += dsor
                final_answer -= 1
            elif dend < cutoff:
                # For divisor = 13, dividend up to < 77 at least < 52 (60 might be best choice ie if ceil estimate is < 3)
                dend -= floor_est * dsor
                final_answer += floor_est
            elif ceil_est == 0:
                dend -= dsor
                final_answer += 1
            else:
                dend -= ceil_est * dsor
                final_answer += ceil_est
            runs += 1
        if runs <= MAX_RUNS and final_answer != correct_answer:
            raise Exception(f"Incorrect Answer: {dsor}, {orig_dend}, {final_answer}, {correct_answer}")
        run_total += runs
        run_count += 1
        run_max = max(run_max, runs)
    return max_dend, overran

def search_min(dsor, max_dend):
    """left = 0
    right = max_dend
    min_dividend, overran = divide(dsor, max_dend)
    if overran > 0:
        return -1
    while left < right - 1:
        mid = (left + right) // 2
        min_dividend, overran = divide(dsor, mid)
        if overran == 0:
            right = mid
        else:
            left = mid"""
    min_dividend, overran = divide(dsor, max_dend)
    if overran > 0:
        return -1
    min_dividend, overran = divide(dsor, 6 * POWER)
    if overran == 0:
        return 6 * POWER
    return -2

run_total2 = 0
run_count2 = 0
for divisor in range(10 ** (DIGITS - 1), 10 ** DIGITS):
    run_total = 0
    run_count = 0
    cutoff = 0
    #if ONES < divisor < POWER * 4 / 3:
    #    cutoff = 6 * POWER
    max_dividend, overran = divide(divisor, cutoff)
    original_total = run_total
    min_dividend = 0
    print("-------------")
    if overran > 0:
        min_dividend = search_min(divisor, max_dividend)
        if min_dividend == -1:
            print(f"{divisor}: Not possible")
        else:
            print(f"{divisor}: {min_dividend} - {max_dividend}")
    min_latency = 4
    optimal_cutoff_low = None
    optimal_cutoff_high = None
    min_total = 0
    min_count = 0
    for cutoff in range(min_dividend, max_dividend + 1):
        run_total = 0
        run_count = 0
        divide(divisor, cutoff)
        latency = run_total / run_count
        if latency < min_latency:
            min_latency = latency
            min_total = run_total
            min_count = run_count
            optimal_cutoff_low = cutoff
            optimal_cutoff_high = cutoff
        elif latency == min_latency:
            optimal_cutoff_high = cutoff
    run_total2 += min_total
    run_count2 += min_count
    print(divisor, optimal_cutoff_low, optimal_cutoff_high, min_latency, original_total - min_total)
    #print(divisor)

print(count)
print(run_total2 / run_count2)
print(run_max)