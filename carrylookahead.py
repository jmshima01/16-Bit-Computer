# By James Shima
# python script to make hdl for lookahead adder...
if __name__ == "__main__":
    # C_i+1 = (A_i and B_i) or (C_i and (A_i ^ B_i))
    
    

    def genCarry(C):
        r = f"G{C-1} + "
        for i in range(C-1):
            r += 

        return r 
            
            


    for i in range(4):
        # print(f"Xor(a=a[{i}],b=b[{i}],out=P{i})")
        # print(f"And(a=a[{i}],b=b[{i}],out=G{i})")

        print(f"FullAdder(a=a[{i}], b=b[{i}], c=C{i+1}, sum=out[{i}], carry=False)")





