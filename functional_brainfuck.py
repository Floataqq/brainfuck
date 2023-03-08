import sys


# noinspection DuplicatedCode
class Interpreter:
    def __init__(self, arr_size: int = 10000):
        self.arr_size = arr_size
        self.array = [0 for _ in range(arr_size)]

    def exec(self, text: str, end: str = '\n'):
        if type(text) != str:
            raise "Provided script is not text!"
        opn = []
        pts = {}
        i = 0
        while i < len(text):
            if text[i] == '{':
                i += 1
                fname = ''
                while text[i] != '}':
                    fname += text[i]
                    i += 1
                f = open(fname, 'r')
                text = ''.join(i for i in text.replace('{' + fname + '}', f.read()) if i not in '\t\r \n')
                f.close()
            i += 1
        for i in range(len(text)):
            if text[i] == '[':
                opn.append(i)
            elif text[i] == ']':
                pts[i] = opn[-1]
                pts[opn.pop()] = i
        labels = dict()
        jumpback = dict()
        i = 0
        while i < len(text):
            if text[i] == ':' or text[i] == '#':
                while text[i] != ')':
                    i += 1
            if text[i] == '(':
                i += 1
                if text[i] == '!':
                    i += 1
                    name = ''
                    while text[i] != ')':
                        name += text[i]
                        i += 1
                    addr = i + 1
                    while text[i] != '/':
                        i += 1
                    i += 1
                    jumpback[name] = i
                else:
                    name = ''
                    while text[i] != ')':
                        name += text[i]
                        i += 1
                    addr = i + 1
                if name not in labels:
                    labels[name] = addr
                else:
                    raise f"Duplicated label {name}"
            i += 1
        p = 0
        char = 0
        lastlabel = ''
        stack = []
        while char < len(text):
            if text[char] == '<':
                try:
                    p -= 1
                except IndexError:
                    raise "Pointer tried to reach an element with index less than 0"
            elif text[char] == '>':
                try:
                    p += 1
                except IndexError:
                    raise "Pointer tried to reach an element with index more or equal arr_size"
            elif text[char] == '+':
                self.array[p] += 1
            elif text[char] == '-':
                self.array[p] -= 1
            elif text[char] == '.':
                sys.stdout.write(chr(self.array[p]))
            elif text[char] == '`':
                sys.stdout.write(str(self.array[p]))
            elif text[char] == ',':
                num = ord(sys.stdin.read(1))
                if num < 0 or num > 255:
                    raise "Not a byte!"
                else:
                    self.array[p] = num
            elif text[char] == '~':
                num = int(sys.stdin.read(1))
                if num < 0 or num > 255:
                    raise "Not a byte!"
                else:
                    self.array[p] = num
            elif text[char] == '[':
                if not self.array[p]:
                    char = pts[char]
            elif text[char] == ']':
                if self.array[p]:
                    char = pts[char]
            elif text[char] == ':':
                char += 2
                lbl = ''
                while text[char] != ')':
                    lbl += text[char]
                    char += 1
                char = labels[lbl] - 1
            elif text[char] == '#':
                char += 2
                lbl = ''
                while text[char] != ')':
                    lbl += text[char]
                    char += 1
                    jumpback[lbl] = char
                char = labels[lbl] - 1
                lastlabel = lbl
            elif text[char] == '!':
                while text[char] != '/':
                    char += 1
                char += 1
            elif text[char] == '/':
                if jumpback != -1:
                    char = jumpback[lastlabel]
            elif text[char] == '^':
                stack.append(self.array[p])
            elif text[char] == '_':
                self.array[p] = stack.pop()
            elif text[char] == '{':
                while text[char] != '}':
                    char += 1
            char += 1
        sys.stdout.write(end)


code = '''

'''

fbf = Interpreter(arr_size=256)
fbf.exec(code)
# {<filename>} - include                                            V
# (<label name>) - label                                            V
# (!<label_name>) - function label(does not                         V
# execute unless called directly and must have retn at the end)     V
# /@ - retn                                                         V
# :(<label name>) - goto                                            V
# #(<label name>) - call                                            V
# ^ - push value at the pointer on the stack                        V
# _ - pop value at the stack to the [pointer]                       V
# args are taken from the stack                                     V
# ` - integer output                                                V
# ~ - integer input                                                 V

