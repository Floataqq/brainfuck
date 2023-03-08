import sys


# noinspection DuplicatedCode
class Interpreter:
    """
    A basic brainfuck interpreter
    """
    def __init__(self, arr_size: int = 10000):
        """
        :param arr_size: size of the internal array that brainfuck uses
        """
        self.arr_size = arr_size
        self.array = [0 for _ in range(arr_size)]

    def exec(self, text: str, end: str = '\n'):
        """
        :param text: brainfuck code to execute
        :param end: a string to automatically print at the end
        """
        if type(text) != str:
            raise "Provided script is not text"

        opn = []
        pts = {}
        for i in range(len(text)):
            if text[i] == '[':
                opn.append(i)
            elif text[i] == ']':
                pts[i] = opn[-1]
                pts[opn.pop()] = i
        p = 0
        char = 0

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
            elif text[char] == ',':
                num = ord(sys.stdin.read(1))
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
            char += 1
        sys.stdout.write(end)


bf = Interpreter()
bf.exec('++[>+++++<-]>+[>++++++<-]>+[>++++<-]>[>++++<-]>+.>++[>+++++<-]>[<<+>>-]<<.>++++[>+++++<-]>[<<+>>-]<<.>++[' +
        '>+++++<-]>[<<->>-]<<---.>++[>+++++<-]>[<<+>>-]<<.')
