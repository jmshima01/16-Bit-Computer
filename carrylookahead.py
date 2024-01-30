# By James Shima
# python script to make hdl generation easy for lookahead adder...
from sys import argv


def makeNWayGate(gate, C, *args):
    c = 0
    print(f"//{args}")
    
    if c==0:
        print(f"{gate}(a={args[c]},b={args[c+1]},out=C{C}-{c});")
        
    for i in range(2,len(args)):
        print(f"{gate}(a={args[i]},b=C{C}-{c},out=C{C}-{c+1});")
        c+=1

    """ Less efficent recursive algorithm I made """
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

    print(" + ".join(res.split(" + ")[::-1]))  


    


    



if __name__ == "__main__":
    # C_i+1 = (A_i and B_i) or (C_i and (A_i ^ B_i))

    # if len(argv)<=4:
    #     print("useage: python3 (A-Z)+.py gate carry_id input1 input2 ... inputN")

    # makeNWayGate(argv[1],argv[2],*argv[3:])
    generateCarryEq(16)






