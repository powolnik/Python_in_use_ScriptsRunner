import re

def select_lines(file_path, regex_pattern):
    selected_lines = []
    other_lines = []

    with open(file_path, "r") as f:
        lines = f.readlines()

    # Use an iterator to easily access the next line
    line_iterator = iter(lines)

    for line in line_iterator:
        if re.match(regex_pattern, line):
            if line not in selected_lines:
                selected_lines.append(line)
            try:
                next_line = next(line_iterator)
                if next_line not in selected_lines:
                    selected_lines.append(next_line)
            except StopIteration:
                pass
        else:
            other_lines.append(line)

    # Create a new file with the "selected" suffix and write selected lines to it
    file_name_without_ext = file_path.split(".")[0]
    output_file_path = f"{file_name_without_ext}_selected.txt"
    with open(output_file_path, "w") as f:
        f.writelines(selected_lines)

if __name__ == "__main__":
    # Accept user input for file path and regex pattern
    file_path = input("Enter file path: ")
    pattern = input("Enter regex pattern: ")

    select_lines(file_path, pattern)
