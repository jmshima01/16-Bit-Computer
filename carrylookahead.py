""" 
@author James Shima, CSCI410 - Dr. Romig III
python script to make hdl generation easy 
for 16 bit lookahead adder as it's alot of gates... 
(over 1000 without n-way ands and ors)
"""
# Xors and Ands of A_i B_i
def genPandG(bits):
    for i in range(bits):
        print(f"Xor(a=a[{i}],b=b[{i}],out=P{i});")
        print(f"And(a=a[{i}],b=b[{i}],out=G{i});")

# prints out an N way gate using only single gates
def makeNWayGate(gate, C, c, isEnd, *args):
    if len(args) < 2:
        return None

    l = []
    print(f"//{args}")
    if isEnd and C==1 and gate=="Or":
        print(f"{gate}(a={args[0]},b={args[1]},out=C{C});")
    else:
        print(f"{gate}(a={args[0]},b={args[1]},out=C{C}-{c});")
    l.append(f"{gate}(a={args[0]},b={args[1]},out=C{C}-{c});")    
    for i in range(2,len(args)):
        if isEnd and i == len(args)-1:
            print(f"{gate}(a={args[i]},b=C{C}-{c},out=C{C});")
        else:
            print(f"{gate}(a={args[i]},b=C{C}-{c},out=C{C}-{c+1});") 
        l.append(f"{gate}(a={args[i]},b=C{C}-{c},out=C{C}-{c+1});")
        c+=1
    return c+1,l

# prints the carry equation for a given carry bit number
# C_i+1 = (A_i and B_i) or (C_i and (A_i ^ B_i))
def generateCarryEq(C_iplus1):
    if C_iplus1 < 1:
        return None
    
    res = "Cin*"
    l = []
    for i in list(range(C_iplus1))[::-1]:
        if i == 0:
            res+=f"P{i}"
        else:
            res+=f"P{i}*"
        l.append(f"P{i}")
    res+=" + "
    l.pop(-1)
    G = C_iplus1-1
    for i in range(C_iplus1):
        if i == G:
            res+=f"G{i}"
            continue
        res+=f"G{i}"+ "*"+"*".join(l)
        res+=" + "
        l.pop(-1)

    x = " + ".join(res.split(" + ")[::-1])
    return x  

# puts it all tother and prints out the carry equation in hack hdl form
def generateCarryHdl(C):
    eq = generateCarryEq(C)

    print(f"//C{C}:")
    l = eq.split(" + ")
    for i in range(len(l)):
        l[i] = l[i].split('*')

    c=0
    end_of_gate_blk =[]
    for i in range(len(l)):
        if i == 0:
            continue
        c,a = makeNWayGate("And",C,c,False,*l[i])
        print()
        end_of_gate_blk.append(a[-1].split("out=")[-1][:-2])

    end_of_gate_blk.append(f"G{C-1}")
    c,_ = makeNWayGate("Or",C,c,True,*end_of_gate_blk)

# prints the full adders the carrys go into
def genFullAdders(C):
    # cin is not defined :( assume its 0 ig...
    print(f"FullAdder(a=a[0], b=b[0], c=false, sum=out[0], carry=false);")

    for i in range(1,C-1):
        print(f"FullAdder(a=a[{i}], b=b[{i}], c=C{i}, sum=out[{i}], carry=false);")
    print(f"FullAdder(a=a[{C-1}], b=b[{C-1}], c=C{C-1}, sum=out[{C-1}], carry=C{C});")

# USAGE python3 carrylookahead.py >> Add16.hdl
# or pipe result to a file of choice using > or >> or just stdout
if __name__ == "__main__":
    # bits = 16 # could make 32 or 64!
    # genPandG(bits)
    # for i in range(1,bits):
    #     generateCarryHdl(i)    
    # genFullAdders(16)
    f = [f"outt[{i}]" for i in range(16)]
    makeNWayGate("Or",1,0,False,*f)


    