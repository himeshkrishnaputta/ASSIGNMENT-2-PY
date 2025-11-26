import csv
import statistics
import os
import sys

#!/usr/bin/env python3
"""
Author: Krish
Date: 2025-11-26
Title: Gradebook Analyzer
"""


def print_welcome():
    print("Gradebook Analyzer")
    print("Options:")
    print("  1) Manual input of student names and marks")
    print("  2) Load from CSV file (name,score)")
    print("Enter the option number (or q to quit).")

def manual_entry():
    marks = {}
    print("Manual entry mode. Enter student name (blank to finish).")
    while True:
        name = input("Name: ").strip()
        if name == "" :
            break
        score_raw = input("Score (0-100): ").strip()
        try:
            score = float(score_raw)
        except ValueError:
            print("Invalid score. Try again.")
            continue
        marks[name] = score
    return marks

def load_csv(filepath):
    marks = {}
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return marks
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            # Accept rows with at least 2 columns; first is name, second is score
            name = row[0].strip()
            if len(row) < 2:
                print(f"Skipping row (no score): {row}")
                continue
            score_raw = row[1].strip()
            try:
                score = float(score_raw)
            except ValueError:
                # Try skipping header-like rows
                print(f"Skipping row (invalid score): {row}")
                continue
            if name == "":
                name = "<Unknown>"
            marks[name] = score
    return marks

# Task 3: Statistical functions
def calculate_average(marks_dict):
    if not marks_dict:
        return None
    return statistics.mean(marks_dict.values())

def calculate_median(marks_dict):
    if not marks_dict:
        return None
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict):
    if not marks_dict:
        return ([], None)
    max_score = max(marks_dict.values())
    names = [n for n, s in marks_dict.items() if s == max_score]
    return (names, max_score)

def find_min_score(marks_dict):
    if not marks_dict:
        return ([], None)
    min_score = min(marks_dict.values())
    names = [n for n, s in marks_dict.items() if s == min_score]
    return (names, min_score)

# Task 4: Grade assignment
def assign_grades(marks_dict):
    grades = {}
    distribution = {"A":0, "B":0, "C":0, "D":0, "F":0}
    for name, score in marks_dict.items():
        if score >= 90:
            g = "A"
        elif score >= 80:
            g = "B"
        elif score >= 70:
            g = "C"
        elif score >= 60:
            g = "D"
        else:
            g = "F"
        grades[name] = g
        if g in distribution:
            distribution[g] += 1
    return grades, distribution

# Task 5: Pass/Fail with list comprehension
def pass_fail_lists(marks_dict, threshold=40):
    passed = [n for n, s in marks_dict.items() if s >= threshold]
    failed = [n for n, s in marks_dict.items() if s < threshold]
    return passed, failed

def print_analysis(marks):
    if not marks:
        print("No data to analyze.")
        return

    avg = calculate_average(marks)
    med = calculate_median(marks)
    max_names, max_score = find_max_score(marks)
    min_names, min_score = find_min_score(marks)

    print("\n=== Analysis Summary ===")
    print(f"Total students: {len(marks)}")
    print(f"Average score: {avg:.2f}")
    print(f"Median score: {med:.2f}")
    print(f"Max score: {max_score} - {', '.join(max_names)}")
    print(f"Min score: {min_score} - {', '.join(min_names)}")

    grades, distribution = assign_grades(marks)
    print("\nGrades:")
    for name, g in grades.items():
        print(f"  {name}: {g}")

    print("\nGrade distribution:")
    for g in ["A","B","C","D","F"]:
        print(f"  {g}: {distribution.get(g,0)}")

    passed, failed = pass_fail_lists(marks, threshold=40)
    print(f"\nPassed (>=40): {len(passed)}")
    if passed:
        print("  " + ", ".join(passed))
    print(f"Failed (<40): {len(failed)}")
    if failed:
        print("  " + ", ".join(failed))
    print("========================\n")

def main():
    print_welcome()
    choice = input("Choice: ").strip().lower()
    if choice == 'q':
        print("Exiting.")
        sys.exit(0)

    marks = {}
    if choice == '1':
        marks = manual_entry()
    elif choice == '2':
        path = input("Enter path to CSV file: ").strip()
        marks = load_csv(path)
    else:
        print("Invalid option.")
        return

    print_analysis(marks)

if __name__ == "__main__":
    main()