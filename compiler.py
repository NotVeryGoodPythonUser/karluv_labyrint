import re

def get_intent(line):
    spaces=0
    while line[0]==" ":                            #getting size of intent
        spaces+=1
        line = line[1:]
    return(spaces)

class Compiler():
    """gets code and robot and moves the robot according to the code"""
    def __init__(self, robot, main):
        self.karel = robot
        self.default_funcs = [
                {"name":r"left\(\)", "command":self.karel.left}, 
                {"name":r"move\(\)", "command":self.karel.move}
        ]
        self.main = main
        self.running = False

    def run(self, code):
        self.func_defs, self.code=self.precompile(code)
        self.running = True
        self.run_line(self.code)
    
    def stop(self):
        self.running = False
    def precompile(self, code):
        '''takes multiline string and separates it into lists and
           dictionaries'''
        print("full code:\n", code)
        basic_funcs = [r"left", r"move"]
        func_pattern = r" *def.+\):\n( +).+\n(\1.+\n)*"      #extracts custom function definitions
        func_defs=[]
        while re.search(func_pattern, code):
            match = re.search(func_pattern, code)
            code = code[:match.start()]+code[match.end():]
            func_defs.append(match.group(0))
        for i in range(len(func_defs)):
            func = func_defs[i]
            func = func.split("\n")
            name, args = re.search(r"(?<=def)(.+)\((.*)\)", func[0]).groups()
            print(name, args)
            name = name.strip()
            args = args.split(",")
            args = [item.strip() for item in args]
            body = func[1:]
            intent = get_intent(body[0])
            new_body=[]
            for line in body:
                new_body.append(line[intent:])
            body = self.structurise(new_body)["block"]
            func_defs[i] = {"name":name, "body":body, "args":args}

        code = code.split("\n")                              #splits code into peaces to structurise it
        code = self.structurise(code)
        code["type"] = "main"
        print("structurised code:\n", func_defs,"\n",code)
        return((func_defs, code))

    def structurise(self, code):
        print(code)
        '''takes list of lines and returns complex structure
            of nested lists and dictionaries'''
        block = {"block":[], "higher":None}
        intent=[]
        new_intent=False
        for line in code:
            print(line)
            if line == "": continue                             #skip empty lines
            while not (re.match(" {"+str(sum(intent))+"}", line)) and (len(intent)>0):                   #check if there are enough spaces to make intent
                intent.pop(-1)                                 #decreasing intent
                new_block = block["higher"]
                block.pop("higher")
                block = new_block
            line = line[sum(intent):]                          #substract intent
            if new_intent:                                     #intent expected
                spaces=get_intent(line)
                line = line[spaces:]
                if spaces == 0: print("invalid intent")
                intent.append(spaces)
                new_intent = False

            if re.match(r" ", line):                          #bad intent
                print("intent error")
            elif re.match(r"(if|while)", line):
                print("condition")                   #conditional statement
                new_block = {"higher":block, "block":[]}        #new block
                block["block"].append(new_block)
                block = new_block
                new_intent = True                               #expecting new intent
                if re.match(r"while", line):
                    block["type"] = "while"
                    block["cond"] = re.search(r"(?<=while).+(?=:)", line).group(0)
                elif re.match(r"if", line):
                    block["type"] = "while"
                    block["cond"] = re.search(r"(?<=if).+(?=:)", line).group(0)
            else:                                           #normal line
                block["block"].append(line)
        while len(intent)>0:
            intent.pop(-1)                                 #decreasing intent
            new_block = block["higher"]
            block = new_block
        block["line"]=0
        return(block)

    def run_line(self, code):
        if self.running == False:
            return(0)
        print(code["line"])
        line = code["block"][code["line"]]
        if type(line) == type(""):
            for func in self.func_defs:
                if re.match(func["name"], line):
                    code["block"]=code["block"][:code["line"]]+func["body"]+code["block"][code["line"]+1:]
            for func in self.default_funcs:
                print("found func", func)
                if re.match(func["name"], line):
                    code["line"] += 1
                    func["command"]()

            if len(code["block"])>code["line"]:
                print("continuing with line ", code["line"])
                self.main.after(500, lambda code=code : self.run_line(code))
            elif code["type"]=="if" or code["type"]=="while" or code["type"]=="func":
                new_block = code["higher"]
                print("returning to previous block")
                self.main.after(500, lambda code=line : self.run_line(new_block))

        elif type(line) == type({}):
            if (line["type"] == "if") or (line["type"] == "while"):
                if (eval(line["cond"])):
                    print("new block", line)
                    if line["type"] == "if":
                        code["line"] += 1
                    line["line"]=0
                    self.main.after(500, lambda code=line : self.run_line(code))
                else:
                    print("skiping block", line)
                    code["line"] += 1


     #   self.main.after(1000, run_piece(code))

                    






#list=["bagr = 1", "if bagr==3:", "    print(\"ajajaj\")", "    bagr=2","bagr += 3", "while bagr <= 6:", "    bagr+=1", "print(bagr)"]
#print("structurised: ",structurise(list))