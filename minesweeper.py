import tkinter as tk
import random
#from functools import partial

#functions:

lst = []

def count_neighbours(index):
    count = 0
    if index > 10 and index/10 != 0 and index < 90 and index % 10 != 9:
        # is not on any edge
        for x in [index-11,index-10,index-9, index-1,index+1, index+9,index+10,index+11]:
            count += int(lst[x][1])
    elif index == 0:
        for x in [1,10,11]:
            count += int(lst[x][1])
    elif index == 9:
        for x in [8,18,19]:
            count += int(lst[x][1])    
    elif index == 90:
        for x in [80,81,91]:
            count += int(lst[x][1])
    elif index == 99:
        for x in [88,89,98]:
            count += int(lst[x][1])        
    elif index < 10: # top
        for x in [index-1,index+1, index+9,index+10,index+11]:
            count += int(lst[x][1])
    elif index % 10 == 0: # left
        for x in [index-10,index-9, index+1, index+10,index+11]:
            count += int(lst[x][1])
    elif index > 90: # bottom
        for x in [index-11,index-10,index-9, index-1,index+1]:
            count += int(lst[x][1])
    elif index % 10 == 9: # right
        for x in [index-11,index-10, index-1, index+9,index+10]:
            count += int(lst[x][1])
    return count 


def unhide_all():
    print("you lose")

def unhide(num):
    print("test",num,lst[num][1])
    if lst[num][1]:
        print("boom")
        lst[num][0].config(text="B")
        unhide_all()
    else:
        lst[num][0].config(text=str(count_neighbours(num)))


#-------------------------------------------------------------------------------


window = tk.Tk()
window.title("Moves left: 100")

for i in range(10):
    window.rowconfigure(i,minsize=1,weight=1)
for i in range(10):
    window.columnconfigure(i,minsize=1,weight=1)



lst = [[tk.Button(window,height=1,width=2,text="",command=lambda i=i: unhide(i),bg='white'),False] for i in range(100)]

for i, x in enumerate(lst):
    x[0].grid(row=int(i/10), column=int(i%10), sticky="ew", padx=0, pady=0)

for i in range(15):
    while True:
        if not lst[random.randint(0,99)][1]:
            lst[random.randint(0,99)][1] = True
            break
#-------------------------------------------------------------------------------


window.mainloop()