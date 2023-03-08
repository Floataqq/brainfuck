from brainfuck import Interpreter
import sys

args = sys.argv
bf = Interpreter()
end = '\n'
if len(args) == 1:
    print('Usage:\nbfcli <path|-c|-h> <code> <advanced options>')
    exit(0)
try:
    for i in range(len(args) - 1, 0, -1):
        if args[i] == '--arr-size':
            arr_size = int(args[i + 1])
            bf = Interpreter(arr_size=arr_size)
        if args[i] == '--end':
            end = args[i + 1]
    if args[1] == '-c':
        bf.exec(args[2], end=end)
    elif args[1] == '-h':
        print("""
        A brainfuck interpreter
        Usage:

        bfcli <path|-c|-h> <code> <advanced options>

        bfcli <path/to/file> - execute a brainfuck script from file
        bfcli -c <code> - execute brainfuck script from string
        bfcli -h - display this help message

        Advanced options:
        --arr-size - internal array length, if not provided is set to 10000
        --end - a string the interpreter will automatically print after the code finished executing,
        default is a newline
        """)
        exit(0)
    else:
        filename = args[2]
        f = open(filename, 'r')
        bf.exec(f.read(), end=end)
        f.close()
except IndexError as e:
    print('Usage:\nbfcli <path|-c|-h> <code> <advanced options>')
    exit(0)
