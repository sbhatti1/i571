import sys
import json
import re



VARIABLE_TYPE = re.compile(r"[a-zA-Z0-9_]*")
IDENTIFIERS = ['var', 'number', 'string', 'record']
TYPES_TOKENS = ["record", "string", "number"]
TOKEN_LIST = ["record", "string", "number", ";", ":", "var", "end"]

INDEX = 0


class parser():

    def parse_record_check(self):
        tok = parser()
        global INDEX
        tkn = ""
        if INDEX + 1 < len(lst):
            if lst[INDEX + 1] == ":" and INDEX + 2 < len(lst):
                INDEX += 2
                tkn = lst[INDEX]
                return tok.Type_Checker(tkn)

    def Parser_record_Declarations(self):
        tobj1 = parser()
        global INDEX
        variables = []
        if lst[INDEX] == "record" and INDEX + 1 < len(lst):
            INDEX += 1
            while INDEX < len(lst) and lst[INDEX] != "end":
                var_decl = parser.parse_record_check(self)
                if var_decl:
                    if [] in var_decl:
                        sys.exit("Empty-Record error")
                    variables.append(var_decl)
                    INDEX += 2
                else:
                    sys.exit("Invalid-Input-error")
            try:
                if INDEX < len(lst) and lst[INDEX] == "end" and lst[INDEX + 1] == ";":
                    if INDEX + 2 < len(lst) and lst[INDEX] != "end":
                        INDEX += 2
                        variables.append(tobj1.Type_Checker(lst[INDEX]))
                    return variables
            except:
                sys.exit("Invalid Input Error")
        return variables


    def literal_check(self, l: list):
        for i in l:
            if i not in TOKEN_LIST:
                if re.fullmatch(VARIABLE_TYPE, i):
                    continue
                else:
                    sys.exit("bad-char error")

    def record_Parser_check(self):
        global INDEX
        return [lst[INDEX - 2], parser.Parser_record_Declarations(self)]

    def semicolon_parser_check(self):
        global INDEX
        try:
            if lst[INDEX + 1] == ';':
                return 1
        except:
            sys.exit('Missing-Semicolon error')


    def number_parser_check(self):
        global INDEX
        if parser.semicolon_parser_check(self):
            if lst[INDEX - 1] == ":":
                if lst[INDEX + 1] == ";":
                    return [lst[INDEX - 2], lst[INDEX]]
                else:
                    sys.exit("Missing Semicolon error")
            else:
                sys.exit("Missing Colon error")
        else:
            return []

    def string_parser_check(self):
        if parser.semicolon_parser_check(self):
            return [lst[INDEX - 2], lst[INDEX]]
        else:
            return []

    def Type_Checker(self, tok: str):
        if tok not in TYPES_TOKENS:
            sys.exit("no-type error")
        if tok == 'record':
            return parser.record_Parser_check(self)
        if tok == 'number':
            return parser.number_parser_check(self)
        if tok == 'string':
            return parser.string_parser_check(self)

    def is_record_empty(self, list_item: list) -> bool:
        if [] in list_item:
            return True
        else:
            return False

    def parser_declarartions(self, st_lst: list):
        p = parser()
        global INDEX
        global lst
        lst = st_lst
        result = []
        tok_check = parser()
        while INDEX < len(lst):
            identifier = ""
            tok = ""
            if lst[INDEX] != "var":
                sys.exit("Invalid input error")
            if lst[INDEX] == "var" and INDEX + 1 < len(lst):
                INDEX += 1
                identifier = lst[INDEX]
                if lst[INDEX + 1] == ":" and INDEX + 2 < len(lst):
                    INDEX += 2
                    tok = lst[INDEX]
                    res = tok_check.Type_Checker(tok)
                    if res != []:
                        result.append(res)
                        INDEX += 2
                    else:
                        break
        for k in result:
            if p.is_record_empty(k):
                sys.exit("empty-record error")

        jsonStr = json.dumps(result)
        parsed = json.loads(jsonStr)
        print(json.dumps(parsed, indent=4))



class InputString():

    def Seperators(self, s: str):
        result_list = []
        literal = ''
        for i in s:
            if i == " ":
                if literal != '':
                    result_list.append(literal)
                    literal = ''
                continue
            elif i == ".":
                sys.exit("Invalid Input .")
            elif i == ';' or i == ':':
                if literal != '':
                    result_list.append(literal)
                    literal = ''
                result_list.append(i)
            elif i == "\t":
                continue
            else:
                literal += i
        return result_list


if __name__ == "__main__":
    is_tr = InputString()
    parse = parser()
    t = str(sys.stdin.read())
    s_list = [re.sub(r"#.*", "", line) for line in t.strip().split('\n')]
    s = ' '.join(s_list)
    result_list = is_tr.Seperators(s)
    try_list=s.split()
    parse.literal_check(result_list)
    parse.parser_declarartions(result_list)