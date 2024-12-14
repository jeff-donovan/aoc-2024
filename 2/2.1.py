def get_reports(contents):
    return [[int(n) for n in report.split(' ') if n != ''] for report in contents.split('\n') if report]

def num_safe_reports(reports):
    num = 0
    for report in reports:
        if report and is_safe(report):
            num += 1
    return num

def is_safe(report):
    return is_diff_in_range(report) and (is_increasing(report) or is_decreasing(report))

def is_increasing(report):
    for i, level in enumerate(report):
        if i != 0:
            if level <= report[i - 1]:
                return False
    return True

def is_decreasing(report):
    for i, level in enumerate(report):
        if i != 0:
            if level >= report[i - 1]:
                return False
    return True

def is_diff_in_range(report):
    for i, level in enumerate(report):
        if i != 0:
            diff = abs(level - report[i - 1])
            if not (1 <= diff <= 3):
                return False
    return True


if __name__ == '__main__':
    with open('2/day_2_input.txt', 'r') as f:
        contents = f.read()

    reports = get_reports(contents)
    num = num_safe_reports(reports)
    print(num)
