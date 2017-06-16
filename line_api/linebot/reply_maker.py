def make_reply(text):
    return naft_exec(text)

def bf_exec(code,input="",n_step=1024,n_size = 1024):
    memory = [0] * n_size
    index = 0
    exec_addr = 0
    ret = ""
    bracket_addr = []
    
    for i in range(n_step):
        if exec_addr >= len(code):
            break
        
        #print(code)
        #print(" " * exec_addr + "^")
        
        
        if code[exec_addr] == '+':
            # increment data
            memory[index] = (memory[index] + 1 + 256 ) % 256
        elif code[exec_addr] == '-':
            # decrement data
            memory[index] = (memory[index] - 1 + 256 ) % 256
        elif code[exec_addr] == '>':
            # increment data pointer
            index = (index+1+n_size)%n_size
        elif code[exec_addr] == '<':
            # decrement data pointer
            index = (index-1+n_size)%n_size
        elif code[exec_addr] == ',':
            # input one character
            if input == "":
                memory[index]=0
            else:
                memory[index]=ord(input[0])
                input = input[1:]
        elif code[exec_addr] == '.':
            # output one character
            ret = ret + chr(memory[index])
        elif code[exec_addr] == '[':
            # loop start
            if memory[index] == 0:
                # skip to ]
                n = 1
                for j in range(exec_addr+1,len(code)):
                    if code[j] == ']':
                        n-=1
                    elif code[j] == '[':
                        n+=1
                    
                    if n == 0:
                        exec_addr = j
                        break
            else:
                # push "[" address into stack
                bracket_addr.append(exec_addr)
        elif code[exec_addr] == ']':
            # end of loop
            if len(bracket_addr) == 0:
                pass
            else:
                # pop address
                exec_addr = bracket_addr.pop()-1
        
        exec_addr += 1
    
    return ret

def naft_exec(naft_code,input="",n_step=1024,n_size = 1024):
    return bf_exec(to_bf(naft_code),input,n_step,n_size)

def to_naftlang(bf_code):
    naft_code=[]
    dict = {
        "+":"NAFT",
        "-":"Nagoya",
        ">":"University",
        "<":"Aerospace",
        ".":"and",
        ",":"Flight",
        "[":"Technologies",
        "]":"linkspace"
    }
    for c in bf_code:
        if c in dict:
            naft_code.append(dict[c])
    return " ".join(naft_code)

def to_bf(naft_code):
    splited_code = naft_code.split(' ')
    bf_code = ""
    # NAFT: Nagoya University Aerospace and Flight Technologies
    dict = {
        "NAFT":"+",
        "Nagoya":"-",
        "University":">",
        "Aerospace":"<",
        "and":".",
        "Flight":",",
        "Technologies":"[",
        "linkspace":"]"
    }
    
    for cmd in splited_code:
        if cmd in dict:
            bf_code += dict[cmd]
            
    return bf_code

if __name__=="__main__":
    hw = "+++++++++[>++++++++>+++++++++++>+++++<<<-]>.>++.+++++++..+++.>-.------------.<++++++++.--------.+++.------.--------.>+."
    echos = "+[>,.<]"
    print( to_naftlang(hw) )
    print( to_bf(to_naftlang(hw)) == hw )
    print( to_bf(to_naftlang(echos)) == echos )
    print( naft_exec(to_naftlang(hw)))
    print( naft_exec(to_naftlang(echos),input="abcdefg"))