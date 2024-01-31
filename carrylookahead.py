# @author James Shima, CSCI410
# python script to make hdl generation easy for 16 bit lookahead adder...
from sys import argv



def genPandG(bits):
    for i in range(bits):
        print(f"Xor(a=a[{i}],b=b[{i}],out=P{i});")
        print(f"And(a=a[{i}],b=b[{i}],out=G{i});")

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
    """ Less efficent recursive algorithm also works """
    # if len(args)%2==0:
    #     for i in range(0,len(args)-1,2):
    #         print(f"{gate}(a={args[i]},b={args[i+1]},out=C{C}-{c});")
    #         vars.append(f"C{C}-{c}")
    #         c+=1
    #     print()
    # else:   
    #     for i in range(0,len(args)-1,2):
    #         print(f"{gate}(a={args[i]},b={args[i+1]},out=C{C}-{c});")
    #         vars.append(f"C{C}-{c}")
    #         c+=1
    #     print(f"{gate}(a={args[-1]},b=C{C}-{c},out=C{C}-{c+1});")
    #     vars.append(f"C{C}-{c}")
    #     vars.append(f"C{C}-{c+1}")
    #     c+=2
    #     print()
    # makeNWayGate(gate, C, c, *vars)

def generateCarryEq(C_iplus1):
    # C_i+1 = (A_i and B_i) or (C_i and (A_i ^ B_i))
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
    # print(x)
    return x  

def generateCarryHdl(C):
    eq = generateCarryEq(C)
    # print(eq)
    print(f"//C{C}:")
    l = eq.split(" + ")
    for i in range(len(l)):
        l[i] = l[i].split('*')
    # print(l)
    c=0
    end_of_gate_blk =[]
    for i in range(len(l)):
        if i == 0:
            continue
        c,a = makeNWayGate("And",C,c,False,*l[i])
        print()
        end_of_gate_blk.append(a[-1].split("out=")[-1][:-2])
        # print(end_of_gate_blk)
    end_of_gate_blk.append(f"G{C-1}")
    c,_ = makeNWayGate("Or",C,c,True,*end_of_gate_blk)

    # print(end_of_gate_blk)

def genFullAdders(C):
    # cin is not defined :( assume its 0 ig...
    print(f"FullAdder(a=a[0], b=b[0], c=false, sum=out[0], carry=false);")

    for i in range(1,C-1):
        print(f"FullAdder(a=a[{i}], b=b[{i}], c=C{i}, sum=out[{i}], carry=false);")
    print(f"FullAdder(a=a[{C-1}], b=b[{C-1}], c=C{C-1}, sum=out[{C-1}], carry=C{C});")


if __name__ == "__main__":
    bits = 16
    genPandG(bits)
    for i in range(1,bits):
        generateCarryHdl(i)
    
    genFullAdders(16)








