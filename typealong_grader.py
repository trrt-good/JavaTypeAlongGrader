import os
import re
import csv
import argparse
import pandas
from typing import List, Tuple

# add eol notes to readme
# fix header comments

def myers_diff(a, b):
    """Compute the Myers diff between two sequences."""
    n, m = len(a), len(b)
    max_d = n + m

    v = {1: 0}
    trace = []

    for d in range(max_d + 1):
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v.get(k - 1, 0) < v.get(k + 1, 0)):
                x = v.get(k + 1, 0)
            else:
                x = v.get(k - 1, 0) + 1
            y = x - k

            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1

            v[k] = x

            if x >= n and y >= m:
                trace.append(v.copy())
                return build_diff(a, b, trace)

        trace.append(v.copy())

    return []  # No solution found

def build_diff(a, b, trace):
    """Build the diff from the trace."""
    n, m = len(a), len(b)
    x, y = n, m
    diff = []

    for d in range(len(trace) - 1, -1, -1):
        v = trace[d]
        k = x - y

        if k == -d or (k != d and v.get(k - 1, 0) < v.get(k + 1, 0)):
            prev_k = k + 1
        else:
            prev_k = k - 1

        prev_x = v.get(prev_k, 0)
        prev_y = prev_x - prev_k

        while x > prev_x and y > prev_y:
            x -= 1
            y -= 1
            diff.append(('same', a[x]))

        if d > 0:
            if x == prev_x:
                diff.append(('insert', b[y-1]))
            else:
                diff.append(('delete', a[x-1]))

        x, y = prev_x, prev_y

    return list(reversed(diff))

def preprocess_java_code(code: str, ignore_comments: str = 'none') -> str:
    """Preprocess Java code by removing headers and optionally comments."""
    # Remove header (text before 'import' or 'public class')
    code = re.sub(r'^.*?^(import|public\s+class)', r'\1', code, flags=re.DOTALL | re.MULTILINE).strip()

    # Remove comments based on the ignore_comments level
    if ignore_comments == 'all':
        code = re.sub(r'//.*?$|/\*.*?\*/', '', code, flags=re.MULTILINE | re.DOTALL)
    elif ignore_comments == 'eol':
        code = re.sub(r'^(.*\S)[ \t]*//.*$', r'\1', code, flags=re.MULTILINE)
        
    # Normalize line endings and replace tabs with spaces
    return '\n'.join(line.rstrip().replace('\t', '    ') 
                     for line in code.replace('\r\n', '\n').replace('\r', '\n').split('\n'))
    

def process_diff_results(diff_results: List[Tuple[str, str]]) -> dict:
    """Process the results of the Myers diff algorithm with more detailed mistake tracking."""
    total_mistakes = 0
    
    # Detailed tracking for different types of changes
    space_groups = 0
    newline_groups = 0
    text_insertions = 0
    text_deletions = 0
    
    # States to track consecutive changes
    in_space_group = False
    in_newline_group = False
    
    comment_count = 0
    in_comment = False

    mistake_tags = []

    for op, char in diff_results:
        if op == 'insert':
            if char == ' ':
                # Tracking space insertion groups
                if not in_space_group:
                    space_groups += 1
                    in_space_group = True
                    total_mistakes += 1
            elif char == '\n':
                # Tracking newline insertion groups
                if not in_newline_group:
                    newline_groups += 1
                    in_newline_group = True
                    total_mistakes += 1
            else:
                # Tracking text insertions
                text_insertions += 1
                total_mistakes += 1
                in_space_group = False
                in_newline_group = False
        
        elif op == 'delete':
            if char == ' ':
                # Tracking space deletion groups
                if not in_space_group:
                    space_groups += 1
                    in_space_group = True
                    total_mistakes += 1
            elif char == '\n':
                # Tracking newline deletion groups
                if not in_newline_group:
                    newline_groups += 1
                    in_newline_group = True
                    total_mistakes += 1
            else:
                # Tracking text deletions
                text_deletions += 1
                total_mistakes += 1
                in_space_group = False
                in_newline_group = False
        else:
            # Reset group tracking for non-insert/delete operations
            in_space_group = False
            in_newline_group = False
        
        # Count comments
        if char == '/' or (in_comment and char == '*'):
            if in_comment:
                comment_count += 1
            in_comment = True
        else:
            in_comment = False

    # Construct detailed mistake tags
    if space_groups > 0:
        mistake_tags.append(f"SpacingErrors:{space_groups}")
    if newline_groups > 0:
        mistake_tags.append(f"NewLineErrors:{newline_groups}")
    if text_insertions > 0:
        mistake_tags.append(f"ExtraCharacters:{text_insertions}")
    if text_deletions > 0:
        mistake_tags.append(f"MissingCharacters:{text_deletions}")
    if comment_count > 0:
        mistake_tags.append(f"Comments:{comment_count}")

    return total_mistakes, mistake_tags

def remove_comments_and_strings(code):
    # Pattern to match comments and strings
    pattern = r'''
        //.*?$              |   # Line comments
        /\*[\s\S]*?\*/      |   # Block comments
        "(?:\\.|[^"\\])*"   |   # Double-quoted strings
        '(?:\\.|[^'\\])*'       # Single-quoted chars
    '''
    regex = re.compile(pattern, re.MULTILINE | re.VERBOSE)
    # Replace matched patterns with spaces to keep line numbers consistent
    return regex.sub(lambda m: ' ' * (m.end() - m.start()), code)

def check_brackets(code: str):
    # Remove comments and strings to avoid false positives
    code_no_comments = remove_comments_and_strings(code)
    lines = code_no_comments.split('\n')
    errors = 0
    for line_num, line in enumerate(lines):
        stripped_line = line.strip()
        if not stripped_line:
            continue  # Skip empty lines
        if '{' in stripped_line or '}' in stripped_line:
            # If the line is exactly '{' or '}', it's acceptable
            if stripped_line == '{' or stripped_line == '}':
                continue
            else:
                # If '{' or '}' is not alone on the line, it's not Allman style
                errors += 1
    # All braces are correctly placed in Allman style
    return errors

def grade_java_code(source: str, student: str, ignore_comments: str = 'none') -> tuple:
    """Compare two Java code snippets and return the difference count."""
    processed_source = preprocess_java_code(source, ignore_comments)
    processed_student = preprocess_java_code(student, ignore_comments)
    
    diff_results = myers_diff(processed_source, processed_student)
    num_mistakes, mistake_tags = process_diff_results(diff_results)

    if check_brackets(student) > 0:
        mistake_tags.append(f"Brackets:{check_brackets(student)}")
    
    return (num_mistakes, mistake_tags)

def get_student_name(file_path: str) -> str:
    """Extract student name from the first line of the file."""
    with open(file_path, 'r') as file:
        return ''.join(c for c in file.readline().strip() if c.isalnum())

def find_java_files(directory: str) -> List[Tuple[str, str]]:
    """Find all Java files in the given directory with student names."""
    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                student_name = get_student_name(file_path)
                java_files.append((student_name, file_path))
    return java_files

def grade_typealong(source_code: str, student_files: List[Tuple[str, str]], 
                    total_points: float, points_per_mistake: float = 0.1, ignore_comments: str = 'eol') -> List[Tuple[str, float]]:
    """Grade type-along assignments."""
    grades = []
    for student_name, student_file in student_files:
        with open(source_code, 'r') as src, open(student_file, 'r') as student:
            num_mistakes, mistake_tags = grade_java_code(src.read(), student.read(), ignore_comments=ignore_comments)
        if "conlin" in student_name.lower():
            num_mistakes = num_mistakes+1
            mistake_tags.append("CopiedConlinName")
        score = max(0, total_points - (num_mistakes * points_per_mistake))
        grades.append((student_name, round(score, 2), mistake_tags))
    return grades

def main():
    """Main function to parse arguments and grade type-along assignments."""
    parser = argparse.ArgumentParser(description="Grade student type-along assignments")
    parser.add_argument("source_code", help="Path to the source code (teacher's code)")
    parser.add_argument("student_directory", help="Path to the directory containing student code")
    parser.add_argument("total_points", type=float, help="Total points for the type-along")
    parser.add_argument("--points_per_mistake", type=float, default=0.1, 
                        help="Points deducted per mistake (default: 0.1)")
    parser.add_argument("--ignore_comments", type=str, default="eol")
    parser.add_argument("--output", default="typealong-graded.csv", 
                        help="Path to the output CSV file (default: typealong-graded.csv)")

    args = parser.parse_args()

    student_files = find_java_files(args.student_directory)
    grades = grade_typealong(args.source_code, student_files, 
                             args.total_points, args.points_per_mistake, args.ignore_comments)

    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["StudentName", "Score", "Mistakes"])
        writer.writerows(grades)

    print(f"Grading complete. Results saved to {args.output}")

if __name__ == "__main__":
    main()

# if header name matches, penalty
# output the problem, like missing tabs
# check for allman style
# raw code difference
# tells you if theres extra or missing comments
