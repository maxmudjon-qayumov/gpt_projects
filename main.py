"""Pirate Pairs — pirate-themed memory game. Run: py main.py"""
from __future__ import annotations
import random
import time
import tkinter as tk

W, H = 920, 760
CW, CH, GAP, BX, BY = 142, 142, 18, 116, 158
CARDS = [
    ("TREASURE", "chest", "#f4b942"), ("BLACKBEARD", "skull", "#f1efe1"),
    ("CAPTAIN'S MAP", "map", "#e5bb78"), ("PARROT", "parrot", "#57c47c"),
    ("CUTLASS", "sword", "#cad5df"), ("PIRATE SHIP", "ship", "#62b6df"),
    ("COMPASS", "compass", "#f48e55"), ("BOTTLE", "bottle", "#65d8d0"),
]

class PiratePairs:
    def __init__(self, root: tk.Tk):
        self.root = root; root.title("Pirate Pairs — Memory Game"); root.resizable(False, False)
        self.c = tk.Canvas(root, width=W, height=H, bg="#08253a", highlightthickness=0); self.c.pack()
        self.c.bind("<Button-1>", self.click); root.bind("r", lambda _e:self.new()); root.bind("R", lambda _e:self.new())
        root.bind("<space>", lambda _e:self.new() if self.finished else None); self.new()

    def new(self):
        self.deck = list(range(8))*2; random.shuffle(self.deck); self.flipped=[]; self.matched=set()
        self.moves=self.pairs=0; self.finished=self.locked=False; self.started=time.monotonic(); self.elapsed=0
        self.draw(); self.clock()

    def clock(self):
        if not self.finished:
            self.elapsed=int(time.monotonic()-self.started); self.draw(); self.root.after(500,self.clock)

    def click(self,e):
        if self.finished: self.new(); return
        if self.locked: return
        col=(e.x-BX)//(CW+GAP); row=(e.y-BY)//(CH+GAP)
        if not(0<=row<4 and 0<=col<4): return
        i=int(row*4+col)
        if i in self.matched or i in self.flipped: return
        self.flipped.append(i); self.draw()
        if len(self.flipped)==2: self.moves+=1; self.locked=True; self.root.after(650,self.check)

    def check(self):
        a,b=self.flipped
        if self.deck[a]==self.deck[b]:
            self.matched.update((a,b)); self.pairs+=1
            if self.pairs==8: self.finished=True; self.elapsed=int(time.monotonic()-self.started)
        self.flipped=[]; self.locked=False; self.draw()

    def box(self,x,y,fill,outline="#d8b46a"):
        c=self.c; c.create_rectangle(x+4,y+6,x+CW+4,y+CH+6,fill="#021522",outline="",stipple="gray50")
        c.create_rectangle(x,y,x+CW,y+CH,fill=fill,outline=outline,width=3)

    def back(self,x,y):
        c=self.c; self.box(x,y,"#153f58","#d7b967"); c.create_rectangle(x+9,y+9,x+CW-9,y+CH-9,outline="#73b7cb",width=2)
        c.create_oval(x+35,y+27,x+107,y+99,fill="#0c2b42",outline="#d7b967",width=3)
        c.create_text(x+71,y+63,text="☠",fill="#e5c873",font=("Segoe UI Symbol",36,"bold")); c.create_text(x+71,y+116,text="PIRATE PAIRS",fill="#d7b967",font=("Arial",8,"bold"))

    def art(self,x,y,kind,color):
        c=self.c; cx,cy=x+71,y+62
        if kind=="chest":
            c.create_rectangle(cx-39,cy-8,cx+39,cy+31,fill="#8a4e24",outline="#573017",width=3); c.create_arc(cx-39,cy-28,cx+39,cy+15,start=0,extent=180,fill="#b96e2e",outline="#573017",width=3); c.create_rectangle(cx-5,cy+2,cx+5,cy+14,fill="#f6cf56",outline="")
            for xx in (-28,0,28): c.create_line(cx+xx,cy-8,cx+xx,cy+31,fill="#e3ae43",width=3)
        elif kind=="skull":
            c.create_oval(cx-31,cy-31,cx+31,cy+27,fill=color,outline="#907d67",width=2); c.create_rectangle(cx-18,cy+15,cx+18,cy+34,fill=color,outline="")
            for xx in (-11,0,11): c.create_line(cx+xx,cy+18,cx+xx,cy+32,fill="#6e6255",width=2)
            c.create_oval(cx-20,cy-9,cx-6,cy+5,fill="#283545",outline=""); c.create_oval(cx+6,cy-9,cx+20,cy+5,fill="#283545",outline=""); c.create_polygon(cx,cy+2,cx-5,cy+13,cx+5,cy+13,fill="#8c7c6c",outline="")
        elif kind=="map":
            c.create_polygon(cx-37,cy-34,cx+38,cy-29,cx+34,cy+35,cx-39,cy+30,fill=color,outline="#9e6d38",width=3); c.create_line(cx-23,cy-13,cx+5,cy-18,cx+20,cy+5,cx+2,cy+21,fill="#9e6d38",smooth=True,width=2); c.create_text(cx+18,cy+17,text="X",fill="#d34f41",font=("Arial",18,"bold"))
        elif kind=="parrot":
            c.create_oval(cx-26,cy-30,cx+23,cy+36,fill="#39a96b",outline="#176a50",width=3); c.create_oval(cx-8,cy-42,cx+29,cy-7,fill="#e84f53",outline="#9d313b",width=2); c.create_polygon(cx+25,cy-28,cx+48,cy-17,cx+25,cy-8,fill="#f0ba46",outline="#b87929"); c.create_oval(cx+9,cy-31,cx+15,cy-25,fill="white",outline=""); c.create_arc(cx-21,cy-5,cx+22,cy+30,start=200,extent=180,outline="#e9d665",width=5)
        elif kind=="sword":
            c.create_line(cx-28,cy+30,cx+27,cy-28,fill="#73889a",width=9); c.create_line(cx-28,cy+30,cx+27,cy-28,fill="#dde7ec",width=4); c.create_line(cx-36,cy+18,cx-13,cy+40,fill="#e0b746",width=7); c.create_line(cx-42,cy+12,cx-21,cy+33,fill="#663d2e",width=8)
        elif kind=="ship":
            c.create_polygon(cx-42,cy+17,cx+42,cy+17,cx+25,cy+37,cx-22,cy+37,fill="#663a28",outline="#3b241d",width=2); c.create_line(cx,cy+17,cx,cy-42,fill="#5b3828",width=5); c.create_polygon(cx+3,cy-38,cx+3,cy+7,cx+35,cy+7,fill="#f1ead6",outline="#ad9d81"); c.create_polygon(cx-2,cy-31,cx-2,cy+11,cx-31,cy+11,fill="#d7e5e7",outline="#91a6a9")
        elif kind=="compass":
            c.create_oval(cx-34,cy-34,cx+34,cy+34,fill="#d89043",outline="#7b4728",width=4); c.create_oval(cx-26,cy-26,cx+26,cy+26,fill="#f3e2b2",outline="#805c3d",width=2); c.create_polygon(cx,cy-23,cx+8,cy+7,cx,cy+23,cx-8,cy+7,fill="#d95145",outline="#6f3a34"); c.create_polygon(cx,cy-23,cx-8,cy+7,cx,cy+2,fill="#35556d",outline="")
        else:
            c.create_rectangle(cx-10,cy-36,cx+10,cy-20,fill="#d7c27d",outline="#746333"); c.create_polygon(cx-25,cy-20,cx+25,cy-20,cx+20,cy+36,cx-20,cy+36,fill="#52bdbb",outline="#267472",width=3); c.create_line(cx-17,cy+5,cx+17,cy+5,fill="#c7ecdf",width=3); c.create_text(cx,cy+18,text="⚓",fill="#e8d7a8",font=("Segoe UI Symbol",18,"bold"))

    def front(self,x,y,cid,found):
        name,kind,color=CARDS[cid]; self.box(x,y,"#d6efc7" if found else "#f3dfac","#7cc986" if found else "#e8c96e"); self.art(x,y,kind,color)
        self.c.create_text(x+71,y+116,text=name,fill="#24415a",font=("Arial",8,"bold"),width=124)
        if found: self.c.create_text(x+119,y+20,text="✓",fill="#2f9b58",font=("Arial",16,"bold"))

    def draw(self):
        c=self.c; c.delete("all"); c.create_rectangle(0,0,W,H,fill="#08253a",outline="")
        for y in range(100,H,32): c.create_line(0,y,W,y,fill="#0c3048")
        c.create_rectangle(0,0,W,110,fill="#061a2a",outline=""); c.create_text(46,37,text="☠",anchor="w",fill="#f5c952",font=("Segoe UI Symbol",30,"bold")); c.create_text(90,30,text="PIRATE PAIRS",anchor="w",fill="#f7e4ae",font=("Georgia",27,"bold")); c.create_text(92,59,text="Find every matching treasure before the tide turns.",anchor="w",fill="#8dc8d5",font=("Arial",11))
        c.create_text(W-54,31,text=f"MOVES  {self.moves:02}",anchor="e",fill="#f7e4ae",font=("Arial",14,"bold")); c.create_text(W-54,57,text=f"TIME  {self.elapsed//60:02}:{self.elapsed%60:02}",anchor="e",fill="#8dc8d5",font=("Arial",13,"bold")); c.create_text(W/2,132,text=f"TREASURES FOUND  {self.pairs} / 8",fill="#f5c952",font=("Arial",12,"bold"))
        for i,cid in enumerate(self.deck):
            row,col=divmod(i,4); x=BX+col*(CW+GAP); y=BY+row*(CH+GAP)
            self.front(x,y,cid,i in self.matched) if i in self.flipped or i in self.matched else self.back(x,y)
        if self.finished:
            c.create_rectangle(148,273,W-148,487,fill="#061a2a",outline="#f4c34e",width=3); c.create_text(W/2,323,text="THE TREASURE IS YOURS!",fill="#f4c34e",font=("Georgia",24,"bold")); c.create_text(W/2,367,text=f"You found all 8 pairs in {self.moves} moves.",fill="#f4ead2",font=("Arial",16,"bold")); c.create_text(W/2,408,text=f"Final time: {self.elapsed//60:02}:{self.elapsed%60:02}",fill="#8dc8d5",font=("Arial",13)); c.create_text(W/2,452,text="CLICK ANYWHERE OR PRESS SPACE TO PLAY AGAIN",fill="#f4c34e",font=("Arial",11,"bold"))

if __name__ == "__main__":
    root=tk.Tk(); PiratePairs(root); root.mainloop()
