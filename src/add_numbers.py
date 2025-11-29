import os
import sys

def add_numbers(lines, start_num=1):
    numbered_lines = []
    i = start_num
    for line in lines:
        numbered_lines.append(str(i)+". "+line)
        i += 1
    return numbered_lines

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"Usage: python {os.path.basename(__file__)}  <file> <start+_num>")
        sys.exit(-1)
    
    qs_filename = sys.argv[1]
    start_num = int(sys.argv[2])
    numbered_lines = []
    with open(qs_filename, 'r') as qs_file:
        lines = qs_file.readlines()
        numbered_lines = add_numbers(lines, start_num)

    assert(len(lines)==len(numbered_lines))

    with open(qs_filename, 'w') as qs_out_file:
        qs_out_file.writelines(numbered_lines)