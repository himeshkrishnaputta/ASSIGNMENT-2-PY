
"""
Author: himesh
Date: 2025-11-25
Title: Gradebook Analyzer - Main CLI
"""

def print_header():
    print("Gradebook Analyzer")
    print("Author: himesh  Date: 2025-11-25")
    print("-" * 50)

def print_menu():
    print("\nWelcome to Gradebook Analyzer\n")
    print("Choose input method:")
    print("  1) Manual input (enter student names and grades)")
    print("  2) CSV file (load grades from a CSV file)")
    print("  q) Quit\n")

def main():
    print_header()
    while True:
        print_menu()
        choice = input("Enter choice [1/2/q]: ").strip().lower()
        if choice == '1':
            print("\nYou selected: Manual input.")
            print("Note: manual input functionality will be implemented in later tasks.\n")
        elif choice == '2':
            print("\nYou selected: CSV file input.")
            print("Note: CSV loading functionality will be implemented in later tasks.\n")
        elif choice in ('q', 'quit', 'exit'):
            print("Exiting Gradebook Analyzer. Goodbye.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or q.\n")

if __name__ == "__main__":
    main()
    import csv
from pathlib import Path

def manual_entry():
        marks = {}
        order = []
        print("Manual entry. Enter students one by one. Leave name blank to finish.")
        while True:
                name = input("Student name: ").strip()
                if not name:
                        break

                while True:
                        mark_str = input(f"Mark for {name}: ").strip()
                        try:
                                mark = float(mark_str)
                                if mark.is_integer():
                                        mark = int(mark)
                                break
                        except Exception:
                                print("Invalid mark. Enter a number (e.g., 78 or 92.5).")
                if name in marks:
                        print(f"Warning: '{name}' already exists — overwriting previous mark.")
                marks[name] = mark
                order.append((name, mark))
        return marks, order


def load_csv():
        marks = {}
        order = []
        path_str = input("Path to CSV file: ").strip()
        path = Path(path_str)
        if not path.exists():
                print("File not found.")
                return marks, order

        with path.open(newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                first_row = None
                for row in reader:
                        if not row or all(cell.strip() == "" for cell in row):
                                continue
                        first_row = row
                        break
                if first_row is None:
                        print("CSV is empty.")
                        return marks, order

                def try_parse_mark(s):
                        s = s.strip()
                        if s == "":
                                raise ValueError
                        m = float(s)
                        return int(m) if m.is_integer() else m


                maybe_rows = reader
                if len(first_row) < 2:
                        print("CSV must have at least two columns: name, mark")
                        return marks, order

                second_cell = first_row[1].strip()
                header = False
                try:
                        _ = try_parse_mark(second_cell)
                except Exception:
                        header = True

                if not header:
                        name = first_row[0].strip()
                        try:
                                mark = try_parse_mark(first_row[1])
                                marks[name] = mark
                                order.append((name, mark))
                        except Exception:
                                print(f"Skipping row with invalid mark: {first_row}")

                for row in maybe_rows:
                        if not row or all(cell.strip() == "" for cell in row):
                                continue
                        if len(row) < 2:
                                print(f"Skipping malformed row (fewer than 2 columns): {row}")
                                continue
                        name = row[0].strip()
                        try:
                                mark = try_parse_mark(row[1])
                        except Exception:
                                print(f"Skipping row with invalid mark: {row}")
                                continue
                        if name in marks:
                                print(f"Warning: duplicate name '{name}' — overwriting previous mark.")
                        marks[name] = mark
                        order.append((name, mark))
        return marks, order


def main():
        print("Choose input method:")
        print("a) Manual entry")
        print("b) Load from CSV file")
        choice = input("Enter a or b: ").strip().lower()
        if choice == "a":
                marks_dict, marks_list = manual_entry()
        elif choice == "b":
                marks_dict, marks_list = load_csv()
        else:
                print("Invalid choice.")
                return

        if not marks_dict:
                print("No data loaded.")
                return

        print(f"\nLoaded {len(marks_dict)} students.")
        print("marks (dict):")
        for k in sorted(marks_dict.keys()):
                print(f"  {k}: {marks_dict[k]}")
        print("\nmarks (list, entry order):")
        for name, mark in marks_list:
                print(f"  {name}: {mark}")


if __name__ == "__main__":
        main()

from typing import Dict, Tuple, List

def calculate_average(marks_dict: Dict[str, float]) -> float:

    if not marks_dict:
        raise ValueError("marks_dict is empty")
    total = 0.0
    count = 0
    for v in marks_dict.values():
        total += v
        count += 1
    return total / count


def calculate_median(marks_dict: Dict[str, float]) -> float:

    if not marks_dict:
        raise ValueError("marks_dict is empty")
    values = sorted(marks_dict.values())
    n = len(values)
    mid = n // 2
    if n % 2 == 1:
        return float(values[mid])
    else:
        return (values[mid - 1] + values[mid]) / 2.0


def find_max_score(marks_dict: Dict[str, float]) -> Tuple[List[str], float]:

    if not marks_dict:
        raise ValueError("marks_dict is empty")
    max_score = None
    for v in marks_dict.values():
        if max_score is None or v > max_score:
            max_score = v
    names = [name for name, score in marks_dict.items() if score == max_score]
    return names, max_score


def find_min_score(marks_dict: Dict[str, float]) -> Tuple[List[str], float]:

    if not marks_dict:
        raise ValueError("marks_dict is empty")
    min_score = None
    for v in marks_dict.values():
        if min_score is None or v < min_score:
            min_score = v
    names = [name for name, score in marks_dict.items() if score == min_score]
    return names, min_score


def print_analysis_summary(marks_dict: Dict[str, float]) -> None:
    """Compute statistics using the custom functions and print a summary."""
    try:
        avg = calculate_average(marks_dict)
        med = calculate_median(marks_dict)
        max_names, max_score = find_max_score(marks_dict)
        min_names, min_score = find_min_score(marks_dict)
    except ValueError as e:
        print(f"Cannot compute analysis: {e}")
        return

    print("Analysis Summary")
    print("----------------")
    print(f"Number of students : {len(marks_dict)}")
    print(f"Average score      : {avg:.2f}")
    print(f"Median score       : {med:.2f}")
    print(f"Maximum score      : {max_score:.2f} (achieved by: {', '.join(max_names)})")
    print(f"Minimum score      : {min_score:.2f} (achieved by: {', '.join(min_names)})")


if __name__ == "__main__":
    # Example usage / simple test data
    sample_marks = {
        "Alice": 85,
        "Bob": 92,
        "Charlie": 78,
        "Diana": 92,
        "Evan": 69,
        "Fiona": 85,
    }
    print_analysis_summary(sample_marks)
    from collections import Counter


scores = {
    "Alice": 87,
    "Bob": 93,
    "Charlie": 68,
    "Diana": 74,
    "Eve": 58,
    "Frank": 100,
    "Grace": 82,
}

def assign_grade(score: float) -> str:
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


grades = {name: assign_grade(score) for name, score in scores.items()}

dist = Counter(grades.values())

for g in ["A", "B", "C", "D", "F"]:
    dist.setdefault(g, 0)


if __name__ == "__main__":
    print("Gradebook:", grades)
    print("Grade distribution:")
    for g in ["A", "B", "C", "D", "F"]:
        print(f"  {g}: {dist[g]}")


students = [
    ('Alice', 85),
    ('Bob', 30),
    ('Charlie', 45),
    ('David', 20),
    ('Eve', 60)
]
passed_students = [name for name, score in students if score >= 40]
failed_students = [name for name, score in students if score < 40]


print(f"Passed Students ({len(passed_students)}): {passed_students}")
print(f"Failed Students ({len(failed_students)}): {failed_students}")