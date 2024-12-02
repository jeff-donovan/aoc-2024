'''
--- Part Two ---
The engineers are surprised by the low number of safe reports until they realize they forgot to tell you about the Problem Dampener.

The Problem Dampener is a reactor-mounted module that lets the reactor safety systems tolerate a single bad level in what would otherwise be a safe report. It's like the bad level never happened!

Now, the same rules apply as before, except if removing a single level from an unsafe report would make it safe, the report instead counts as safe.

More of the above example's reports are now safe:

7 6 4 2 1: Safe without removing any level.
1 2 7 8 9: Unsafe regardless of which level is removed.
9 7 6 2 1: Unsafe regardless of which level is removed.
1 3 2 4 5: Safe by removing the second level, 3.
8 6 4 4 1: Safe by removing the third level, 4.
1 3 6 7 9: Safe without removing any level.
Thanks to the Problem Dampener, 4 reports are actually safe!

Update your analysis by handling situations where the Problem Dampener can remove a single level from unsafe reports. How many reports are now safe?
'''

def get_reports(contents):
    return [[int(n) for n in report.split(' ') if n != ''] for report in contents.split('\n') if report]

def num_safe_reports(reports):
    num = 0
    for report in reports:
        if report:
            if is_safe(report):
                num += 1
            else:
                for i in range(len(report)):
                    report_copy = report.copy()
                    report_copy.pop(i)
                    is_safe_without_level = is_safe(report_copy)
                    if is_safe_without_level:
                        num += 1
                        break
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
    with open('day_2_test.txt', 'r') as f:
        contents = f.read()

    reports = get_reports(contents)
    num = num_safe_reports(reports)
    print(num)
