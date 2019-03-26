#Project Members:
#William D. Wells
#Dan R. Vandiver
#Connor Myers


from tkinter import *
from tkinter.scrolledtext import ScrolledText

import re

class lexer:
    operators = r'\+|\>|\=|\*'  # working
    keywords = r'\bint\b|\bif\b|\belse\b|\bfloat\b'  # working
    seperators = r'\"|\:|\(|\)'  # working
    identifiers = r'(?<=\").+?(?=\")|\b(?!int\b)\b(?!if\b)\b(?!else\b)\b(?!float\b)[A-Za-z]+\d*'
    literals = r'\w+?(?=\")|[\d\.\d]+'

    def __init__(self):
        self.untokenized = []
        self.MyTokens = []

    def CutOneLineTokens(self, untokenized):
        tokenlist = []
        error = 0
        while not self.isEmpty(untokenized) and error < 50:
            keyCheck = re.search(self.keywords, untokenized)
            idCheck = re.search(self.identifiers, untokenized)
            sepCheck = re.search(self.seperators, untokenized)
            opCheck = re.search(self.operators, untokenized)
            litCheck = re.search(self.literals, untokenized)
            if keyCheck:
                tokenlist.append('<key,' + keyCheck.group(0) + '>')
                untokenized = untokenized[:keyCheck.start()] + untokenized[keyCheck.end():]
                keyCheck = None
            if idCheck:
                tokenlist.append('<id,' + idCheck.group(0) + '>')
                idCheck = re.search(self.identifiers, untokenized)
                tmp = ("id", idCheck.group(0))
                self.MyTokens.append(tmp)
                untokenized = untokenized[:idCheck.start()] + untokenized[idCheck.end():]
                idCheck = None
            if opCheck:
                tokenlist.append('<op,' + opCheck.group(0) + '>')
                opCheck = re.search(self.operators, untokenized)
                tmp = ("op", opCheck.group(0))
                self.MyTokens.append(tmp)
                untokenized = untokenized[:opCheck.start()] + untokenized[opCheck.end():]
                opCheck = None
            if sepCheck:
                #loop here is to maintain order for (" [string] ") combos
                for x in range(2):
                    if sepCheck:
                        tokenlist.append(r'<sep,' + sepCheck.group(0) + '>')
                        sepCheck = re.search(self.seperators, untokenized)
                        tmp = ("sep", sepCheck.group(0))
                        self.MyTokens.append(tmp)
                        untokenized = untokenized[:sepCheck.start()] + untokenized[sepCheck.end():]
                        sepCheck = re.match(self.seperators, untokenized)
                sepCheck = None
            if litCheck:
                tokenlist.append('<lit,' + litCheck.group(0) + '>')
                litCheck = re.search(self.literals, untokenized)
                stringCheck = litCheck.group(0)
                try:
                    floatCheck = float(stringCheck)
                    if (str(floatCheck) == stringCheck):
                        tmp = ("float", stringCheck)
                        self.MyTokens.append(tmp)
                    else:
                        tmp = ("int", stringCheck)
                        self.MyTokens.append(tmp)
                except:
                    tmp = ("str", stringCheck)
                    self.MyTokens.append(tmp)
                untokenized = untokenized[:litCheck.start()] + untokenized[litCheck.end():]
                litCheck = None

            error += 1
        return tokenlist

    def isEmpty(self, untokenized):
        isEmpty = False
        if len(untokenized) <= 1:
            return True
        for x in untokenized:
            if x != ' ' and x != '\t' and x != ';':
                return False
            else:
                isEmpty = True
        return isEmpty

    def clearTokens(self):
        self.MyTokens.clear()

    def getParseTokens(self):
        tmp = ("sep", ";")
        self.MyTokens.append(tmp)
        return self.MyTokens


class LEX_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Lexical Analyzer for TinyPie")
        self.count = 0.0
        self.var = StringVar()
        self.var.set('0')
        self.width = 40
        self.sourcecode = lexer()

        self.label_title = Label(master, text="Lexical Analyzer for TinyPie", bg="Cornflower Blue", fg = "white", padx = 60).grid(row = 0, column = 1)
        self.label_fill1 = Label(master, bg = "Cornflower Blue", width =(self.width + 15), padx = 20).grid(row = 0, column = 0)
        self.label_fill2 = Label(master, bg="Cornflower Blue", width=(self.width + 15), padx=60).grid(row=0, column=2)
        self.label_source = Label(master, text = "Source Code Input:", padx = 50).grid(row = 1, column = 0, sticky=W)
        self.label_lexical = Label(master, text="Lexical Analyzed Result: ", padx = 40).grid(row = 1, column = 1, sticky = W)
        self.label_parser = Label(master, text="Parsing Analyzed Result: ", padx=5).grid(row=1, column=2, sticky=W)
        self.text_source = ScrolledText(master, height=self.width / 2, width= self.width)
        self.text_source.grid(row = 2, column = 0)
        self.text_output = ScrolledText(master, height=self.width / 2, width= self.width - 20)
        self.text_output.grid(row = 2, column = 1)
        self.text_output.config(state="disabled")
        self.text_parse = ScrolledText(master, height=self.width / 2, width=self.width + 20)
        self.text_parse.grid(row=2, column=2)
        self.text_parse.config(state="disabled")

        self.label_lineCount = Label(master, text="Current Processing Line: ", padx = 40).grid(row = 3, column = 0, sticky = W)
        self.line_num = Label(master, textvariable = self.var, bg = "White", padx = 10, bd = 3).grid(row = 3, column = 0, sticky = E)
        self.nextline = Button(master, text="Next Line", width = 10, padx = 5, bg = "Dark Sea Green", fg = "white", command = self.nextLine).grid(row=4, column=0, sticky = E)
        self.quit = Button(master, text="Quit", width=10, padx=5, bg="Dark Sea Green", fg="white", command = self.quit).grid(row=4, column=2, sticky = E)

    def nextLine(self):
        self.count += 1
        text_length = float('.' + str(self.width))
        #This gets the string from left box
        send_string = self.text_source.get(str(self.count), str(self.count + text_length) + "0")
        if len(send_string) <= 0:
            self.var.set(str(int(self.count)))
            return
        else:
            self.var.set(str(int(self.count)))
            self.text_output.config(state="normal")
            token_list = self.sourcecode.CutOneLineTokens(send_string)
            token_list.append('<sep, ;>')
            for tokens in token_list:
                self.text_output.insert(INSERT, tokens + '\n\n')
            self.text_output.config(state="disabled")
            self.text_parse.config(state="normal")
            self.parser = parser(self.sourcecode.getParseTokens(), self.text_parse)
            self.text_parse.config(state="disabled")
            self.sourcecode.clearTokens()

    def quit(self):
        self.master.destroy()

class parser:
    def __init__(self, tokenList, parserBox):
        self.Mytokens = tokenList
        self.parseBox = parserBox
        self.inToken = ("empty", "empty")
        self.inToken = self.Mytokens.pop(0)
        self.exp()

    def accept_token(self):
        self.parseBox.insert(INSERT, "Accept token from the list: " + self.inToken[1] + "\n")
        self.inToken = self.Mytokens.pop(0)

    def string(self):
        self.parseBox.insert(INSERT, "\n----Parent node string, finding children nodes:\n")
        self.parseBox.insert(INSERT, "Child node (internal): sep\n")
        self.parseBox.insert(INSERT, "sep has child node (token): " + self.inToken[1] + "\n")
        self.accept_token()

        if (self.inToken[0] == "str"):
            self.parseBox.insert(INSERT, "Child node (internal): str\n")
            self.parseBox.insert(INSERT, "str has child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.parseBox.insert(INSERT, "Error: Expected str input after quotes\n")
            return

        if (self.inToken[1] == '"'):
            self.parseBox.insert(INSERT, "Child node (internal): sep\n")
            self.parseBox.insert(INSERT, "sep has child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.parseBox.insert(INSERT, "Error: Expected sep \"\n")
            return

        if (self.inToken[1] == ')'):
            self.parseBox.insert(INSERT, "Child node (internal): sep\n")
            self.parseBox.insert(INSERT, "sep has child node (token): " + self.inToken[1] + "\n")
            self.accept_token()

    def math(self):
        self.parseBox.insert(INSERT, "\n----Parent node math, finding children nodes:\n")
        if (self.inToken[0] == "float"):
            self.parseBox.insert(INSERT, "Child node (internal): float\n")
            self.parseBox.insert(INSERT, "float has child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
        elif (self.inToken[0] == "int"):
            self.parseBox.insert(INSERT, "Child node (internal): int\n")
            self.parseBox.insert(INSERT, "int has child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
        if (self.inToken[1] == "+"):
            self.parseBox.insert(INSERT, "Child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
            self.parseBox.insert(INSERT, "Child node (internal): math\n")
            self.math()
        elif (self.inToken[1] == "*"):
            self.parseBox.insert(INSERT, "Child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
            self.parseBox.insert(INSERT, "Child node (internal): math\n")
            self.math()
        else:
            self.parseBox.insert(INSERT, "Error, you need + or * after the datatype in the math\n")

    def exp(self):
        self.parseBox.insert(INSERT, "\n----Parent node exp, finding children nodes:\n")
        typeT, token = self.inToken;
        if (typeT == "id"):
            self.parseBox.insert(INSERT, "Child node (internal): identifier\n")
            self.parseBox.insert(INSERT, "Identifier has child node (token): " + token + "\n")
            self.accept_token()
        else:
            self.parseBox.insert(INSERT, "expect identifier as the first element of the expression!\n")
            return

        if (self.inToken[1] == "="):
            self.parseBox.insert(INSERT, "Child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
        elif self.inToken[1] == "(":
            self.parseBox.insert(INSERT, "Child node (token): " + self.inToken[1] + "\n")
            self.accept_token()
        else:
            self.parseBox.insert(INSERT, "expect = or ( as the second element of the expression!\n")
            return

        if (self.inToken[1] == '"'):
            self.string()
        else:
            self.math()

        if self.inToken[1] == ";":
            self.parseBox.insert(INSERT, "\nParse Tree building success!\n")
            return


if __name__ == '__main__':
    root = Tk()
    my_gui = LEX_GUI(root)
    root.mainloop()
