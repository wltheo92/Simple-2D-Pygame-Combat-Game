import pygame as p,random,sys
p.init()
screen=p.display.set_mode((1200,700))
p.display.set_caption("Megaman X4")
clock=p.time.Clock()
fps=15
f=3 #factor for scaling up objects
font=p.font.Font("OpenSans-Bold.ttf",100)
font1=p.font.Font("OpenSans-BoldItalic.ttf",90)
font2=p.font.Font("OpenSans-BoldItalic.ttf",60)
p.mixer.music.load("battle_music.mp3")

def collideGround(x,y,R):return R.collidepoint(x,y)

#Zero Object
class Z:
    idle=[(292,103,44,49),(341,103,44,49),(389,103,44,49),(436,103,44,49),(485,103,44,49)]
    walk=[(208,323,51,45),(265,324,51,45),(320,323,49,46),(375,322,47,46),(429,320,45,49),(481,320,41,48),(111,385,47,48),(167,386,50,45),(223,387,47,46),(275,386,51,47),(332,385,48,48),(386,384,46,49),(437,384,44,50),(486,385,47,48)]
    jumpup=[(166,164,46,58),(219,166,45,56),(268,166,44,58),(319,166,44,58),(370,169,45,57)]
    jumpdown=[(424,169,41,53),(474,175,41,56),(132,234,39,65),(177,230,37,78),(221,230,36,80),(265,230,37,80),(310,249,42,60),(360,264,43,43)]
    dash=[(111,990,47,46),(162,993,56,42),(227,1001,58,35),(227,1001,58,35),(227,1001,58,35),(227,1001,58,35),(227,1001,58,35),(422,991,46,46),(522,990,42,46)]
    saber1=[(156,440,49,63),(214,440,78,63),(300,442,88,60),(390,455,92,48),(491,453,84,50),(25,514,71,45),(104,514,67,45),(176,514,60,45),(240,514,48,45),(296,514,47,45),(457,514,46,46),(508,513,42,46),(557,514,44,46)]
    oo1=[(-22,45),(-22,46),(-24,48),(-29,49),(-21,49),(-21,45),(-20,45),(-20,45),(-19,45),(-19,45),(-23,45),(-19,45),(-22,45)]
    wo1=[(-3,-63,27,23),(13,-63,43,47),(26,-59,37,58),(26,-39,37,38),(26,-15,36,14),(25,-15,26,13),(26,-18,20,15),(26,-15,14,11),None,None,None,None,None]
    saber2=[(151,567,53,45),(206,564,70,48),(278,566,85,46),(434,620,47,48)]
    oo2=[None,(-30,48),(-26,46),None]
    wo2=[None,(23,-29,16,10),(-10,-30,68,12),None]
    jumpsaber=[(59,837,54,62),(118,838,72,62),(193,839,91,66),(291,831,100,74),(524,829,42,79),(572,828,38,80)]
    oo3=[None,(-27,58),(-29,66),(-28,74),None,None]
    wo3=[None,(6,-62,40,32),(-10,-66,71,48),(28,-64,48,56),None,None]
    def collideG(x,y,dy,state,I,init,R,Z):
        K=["i","l","r"]
        if R.collidepoint(x,int(y+dy)):return (R.top,0,K[Z],0,1)
        return (y,dy,state,I,init)
    def transition_keydown(state,key,I):
        if key==p.K_RIGHT:
            if state=="i":return ["r",I]
            if state=="l":return ["r",I]
            if state=="ju":return ["jur",I]
            if state=="jul":return ["jur",I]
            if state=="jd":return ["jdr",I]
            if state=="jdl":return ["jdr",I]
        if key==p.K_LEFT:
            if state=="i":return ["l",I]
            if state=="r":return ["l",I]
            if state=="ju":return ["jul",I]
            if state=="jur":return ["jul",I]
            if state=="jd":return ["jdl",I]
            if state=="jdr":return ["jdl",I]
        if key==p.K_x:
            if state=="i":return ["ju",I]
            if state=="l":return ["jul",I]
            if state=="r":return ["jur",I]
        if key==p.K_z:
            if state=="i":return ["d",I]
            if state=="l":return ["dl",I]
            if state=="r":return ["dr",I]
        if key==p.K_c:
            if state=="i":return ["s1",0]
            if state in ["l","r"]:return ["s2",0]
            if state=="ju":return ["jus",0]
            if state=="jul":return ["jusl",0]
            if state=="jur":return ["jusr",0]
            if state=="jd":return ["jds",0]
            if state=="jdl":return ["jdsl",0]
            if state=="jdr":return ["jdsr",0]
        return [state,I]
    def transition_keyup(state,key):
        if state=="l":
            if key==p.K_LEFT:return "i"
        if state=="r":
            if key==p.K_RIGHT:return "i"
        return state
    def __init__(self,x,y,R,NPC):
        self.surf=p.image.load("zerox4sheet.jpg")
        self.M=Z.idle
        self.x=x
        self.y=y
        self.R=R
        self.I=0
        self.state="i"
        self.init=1
        self.HP=10000
        self.dx=0
        self.dy=0
        self.NPC=NPC
        self.xbool=1 if self.NPC else 0
        self.w=None
        self.h=None
        self.body_rect=None
        self.saber_rect=None
        self.blast=[]
        self.s=None
        self.Ox=None
        self.body_attack=False
        self.colorkey=None
    def transition(self,e):
        self.xbool=1 if e.x<self.x else 0
        if self.state=="i":
            if abs(self.x-e.x)<=40:
                if collideGround(e.x,e.y,self.R):self.state=random.choice(["s1","s2"])
                else:self.state="ju"
            else:self.state="l" if e.x<self.x else "r"
        if self.state in ["l","r"]:
            if abs(self.x-e.x)<=40:
                if collideGround(e.x,e.y,self.R):self.state=random.choice(["s1","s2"])
                else:self.state="jul" if self.state=="l" else "jur"
            else:self.state="l" if e.x<self.x else "r"
    def update(self):
        if self.state=="i":self.M,self.dx,self.dy,self.saber_s=Z.idle,0,0,None
        if self.state=="r":self.M,self.dx,self.dy,self.xbool=Z.walk,10,0,0
        if self.state=="l":self.M,self.dx,self.dy,self.xbool=Z.walk,-10,0,1
        if self.state=="ju":
            self.M=Z.jumpup
            if self.init:self.dy,self.init=-60,0
            else:
                self.dy=int(self.dy/2)
                if self.dy==0:self.state,self.I,self.init="jus" if self.NPC else "jd",0,1
        if self.state=="jd":
            self.M=Z.jumpdown
            if self.init:self.dy,self.init=10,0
            else:
                self.dy=self.dy*1.5;
                self.y,self.dy,self.state,self.I,self.init=Z.collideG(self.x,self.y,self.dy,self.state,self.I,self.init,self.R,0)
        if self.state=="jul":
            self.M,self.dx,self.xbool=Z.jumpup,-20,1
            if self.init:self.dy,self.init=-60,0
            else:
                self.dy=int(self.dy/2)
                if self.dy==0:self.state,self.I,self.init="jdsl" if self.NPC else "jdl",0,1
        if self.state=="jur":
            self.M,self.dx,self.xbool=Z.jumpup,20,0
            if self.init:self.dy,self.init=-60,0
            else:
                self.dy=int(self.dy/2)
                if self.dy==0:self.state,self.I,self.init="jdsr" if self.NPC else "jdr",0,1
        if self.state=="jdl":
            self.M,self.dx,self.xbool=Z.jumpdown,-20,1
            if self.init:self.dy,self.init=10,0
            else:
                self.dy=self.dy*1.5;
                self.y,self.dy,self.state,self.I,self.init=Z.collideG(self.x,self.y,self.dy,self.state,self.I,self.init,self.R,1)
        if self.state=="jdr":
            self.M,self.dx,self.xbool=Z.jumpdown,20,0
            if self.init:self.dy,self.init=10,0
            else:
                self.dy=self.dy*1.5;
                self.y,self.dy,self.state,self.I,self.init=Z.collideG(self.x,self.y,self.dy,self.state,self.I,self.init,self.R,2)
        if self.state=="d":
            self.M,self.dx,self.dy=Z.dash,-40 if self.xbool else 40,0
            if self.I==len(self.M)-1:self.state,self.I="i",0
        if self.state=="dl":
            self.M,self.dx,self.dy,self.xbool=Z.dash,-40,0,1
            if self.I==len(self.M)-1:self.state,self.I="l",0
        if self.state=="dr":
            self.M,self.dx,self.dy,self.xbool=Z.dash,40,0,0
            if self.I==len(self.M)-1:self.state,self.I="r",0
        if self.state=="s1":
            self.M,self.dx,self.dy=Z.saber1,0,0
            if self.I==len(self.M)-1:self.state,self.M,self.I="i",Z.idle,0
        if self.state=="s2":
            self.M,self.dx,self.dy=Z.saber2,0,0
            if self.I==len(self.M)-1:self.state,self.M,self.I="i",Z.idle,0
        if self.state=="jus":
            self.M,self.dy=Z.jumpsaber,int(self.dy/2)
            if self.dy==0:self.state,self.I,self.init="jds" if self.NPC else "jd",0,1
        if self.state=="jusl":
            self.M,self.xbool,self.dy=Z.jumpsaber,1,int(self.dy/2)
            if self.dy==0:self.state,self.I,self.init="jdsl" if self.NPC else "jdl",0,1
        if self.state=="jusr":
            self.M,self.xbool,self.dy=Z.jumpsaber,0,int(self.dy/2)
            if self.dy==0:self.state,self.I,self.init="jdsr" if self.NPC else "jdr",0,1
        if self.state=="jds":
            self.M=Z.jumpsaber
            if self.init:self.dy,self.init=10,0
            else:
                self.dy=1.5*self.dy
                self.y,self.dy,self.state,self.I,self.init=Z.collideG(self.x,self.y,self.dy,self.state,self.I,self.init,self.R,0)
        if self.state=="jdsl":
            self.M,self.dx,self.xbool=Z.jumpsaber,-20,1
            if self.init:self.dy,self.init=10,0
            else:
                self.dy=1.5*self.dy
                self.y,self.dy,self.state,self.I,self.init=Z.collideG(self.x,self.y,self.dy,self.state,self.I,self.init,self.R,1)
        if self.state=="jdsr":
            self.M,self.dx,self.xbool=Z.jumpsaber,20,0
            if self.init:self.dy,self.init=10,0
            else:
                self.dy=1.5*self.dy
                self.y,self.dy,self.state,self.I,self.init=Z.collideG(self.x,self.y,self.dy,self.state,self.I,self.init,self.R,2)
    def prepare(self):
        self.x+=self.dx
        self.y+=self.dy
        if self.x<0:self.x,self.xbool=int(self.w/2),0
        if self.x>2000:self.x,self.xbool=2000-int(self.w/2),1
        self.I=(self.I+1)%len(self.M)
        a,b,c,d=self.M[self.I]
        self.w,self.h=f*c,f*d
        self.s=self.surf.subsurface(p.Rect(a,b,c,d))
        self.s=p.transform.scale(self.s,(self.w,self.h))
        self.s=p.transform.flip(self.s,self.xbool,False)
        if self.state not in ["s1","s2","jus","jusl","jusr"]:
            self.body_rect=p.Rect(self.x-f*10,int(self.y-0.75*self.h),20*f,int(self.h/2))
            self.saber_rect=None
            self.Ox=None
        else:
            if self.state=="s1":OO,WO=Z.oo1,Z.wo1
            elif self.state=="s2":OO,WO=Z.oo2,Z.wo2
            else:OO,WO=Z.oo3,Z.wo3
            if WO[self.I]:
                sox,soy,sw,sh=WO[self.I]
                sox,soy,sw,sh=f*sox,f*soy,f*sw,f*sh
                if self.xbool:self.saber_rect=p.Rect(self.x-abs(sox)-sw,self.y+soy,sw,sh)
                else:self.saber_rect=p.Rect(self.x+sox,self.y+soy,sw,sh)
            if OO[self.I]:
                ox,oy=OO[self.I]
                self.Ox=f*ox
                oy=f*oy
                self.body_rect=p.Rect(self.x-f*10,int(self.y-0.75*oy),20*f,int(oy/2))
            else:
                self.body_rect=p.Rect(self.x-f*10,int(self.y-0.75*self.h),20*f,int(self.h/2))
                self.Ox=None

#X object
class X:
    i=[(244,7,36,48),(287,8,37,47),(330,9,37,46),(377,9,36,46),(422,9,36,46)]
    w=[(212,265,33,49),(249,266,41,46),(294,269,49,46),(348,267,50,47),(404,266,39,48),(448,268,31,47),\
       (137,321,29,51),(171,326,37,48),(214,325,40,48),(261,326,43,47),(308,324,44,47),(357,326,38,49),\
       (401,325,33,49),(440,323,27,50)]
    ju=[(108,71,27,52),(141,68,25,54),(172,66,25,57),(203,64,25,58),(237,64,28,56),(272,63,35,54)]
    jd=[(314,64,33,54),(352,63,29,57),(390,68,32,54),(428,73,31,51),(465,76,34,46)]
    d=[(107,383,36,43),(147,387,47,39),(201,392,54,34),(259,394,53,34),(259,394,53,34),(259,394,53,34),\
       (315,381,39,46),(360,379,32,47),(398,383,41,44),(444,380,34,45)]
    f=[(356,430,35,65),(400,435,35,62),(443,435,33,61)]
    ff=[(148,502,42,52),(200,503,41,52),(247,504,39,51),(293,500,43,53),(347,502,42,52),(397,504,40,52)]
    s1=[(92,132,48,47),(150,132,47,47),(205,131,49,47),(265,132,50,47),(323,132,52,47),(381,132,39,47),(429,132,37,47),(477,130,35,48)]
    o1=[(-19,47),(-19,47),(-19,47),(-20,47),(-19,47),None,None,None]
    s2=[(94,202,45,55),(148,195,46,62),(199,191,50,66),(258,189,55,69),(326,186,38,71),(377,206,38,50),(429,207,37,50),(480,207,33,50)]
    o2=[(-18,47),(-18,48),(-18,47),(-19,47),None,None,None,None]
    ns=[(59,1442,39,57),(103,1443,37,56),(147,1444,40,45),(191,1439,60,56),(258,1439,60,56),(322,1436,63,58),(388,1435,68,62),\
        (461,1433,124,66),(461,1433,124,66),(461,1433,124,66),(461,1433,124,66)]
    b=[[(958,282,29,20),(995,284,26,16),(1031,284,28,18),(1064,282,29,20)],[(916,313,57,30),(979,313,60,29),(1047,313,63,31)]]
    def transition_keydown(state,key,I):
        if key==p.K_x:
            if state=="i":return ["ju",I]
            elif state=="l":return ["jul",I]
            elif state=="r":return ["jur",I]
            elif state=="f":return ["jd",I]
        if key==p.K_UP:
            if state=="ju":return ["f",I]
        if key==p.K_LEFT:
            if state=="i":return ["l",I]
            if state=="r":return ["l",I]
            if state=="ju":return ["jul",I]
            if state=="jur":return ["jul",I]
            if state=="jd":return ["jdl",I]
            if state=="jdr":return ["jdl",I]
            if state=="f":return ["fl",I]
        if key==p.K_RIGHT:
            if state=="i":return ["r",I]
            if state=="l":return ["r",I]
            if state=="ju":return ["jur",I]
            if state=="jul":return ["jur",I]
            if state=="jd":return ["jdr",I]
            if state=="jdl":return ["jdr",I]
            if state=="f":return ["fr",I]
        if key==p.K_z:
            if state=="i":return ["d",I]
            elif state=="l":return ["dl",I]
            elif state=="r":return ["dr",I]
        if key==p.K_c:
            if state=="i":return ["s1",0]
            if state in ["ju","jul","jur","jd","jdl","jdr"]:return ["ns",0]
            if state=="s1":return ["s2",0]
        return [state,I]
    def transition_keyup(state,key):
        if key==p.K_LEFT:
            if state=="l":return "i"
            if state=="fl":return "f"
        if key==p.K_RIGHT:
            if state=="r":return "i"
            if state=="fr":return "f"
        return state
    def __init__(self,x,y,R,NPC):
        self.surf=p.image.load("X_ultimate.jpg")
        self.M=X.i
        self.x=x
        self.y=y
        self.R=R
        self.I=0
        self.state="i"
        self.init=1
        self.HP=10000
        self.dx=0
        self.dy=0
        self.NPC=NPC
        self.xbool=1 if self.NPC else 0
        self.w=39*f
        self.h=46*f
        self.body_rect=None
        self.saber_rect=None
        self.blast=[]
        self.s=None
        self.Ox=None
        self.body_attack=False
        self.colorkey=(0,0,0)
    def transition(self,e):
        if self.state=="i":self.state=random.choice(["jul" if e.x<self.x else "jur","s1","s2","l" if e.x<self.x else "r","dl" if e.x<self.x else "dr"])
        if self.state in ["l","r"]:self.state=random.choice(["jul" if e.x<self.x else "jur","s1","s2"])
        if self.state in ["s1","s2"]:self.xbool=1 if e.x<self.x else 0
    def update(self):
        if self.state=="i":self.M,self.dx,self.dy=X.i,0,0
        if self.state=="l":self.M,self.dx,self.dy,self.xbool=X.w,-20,0,1
        if self.state=="r":self.M,self.dx,self.dy,self.xbool=X.w,20,0,0
        if self.state=="ju":
            self.M=X.ju
            if self.init:self.dy,self.init=-60,0
            else:
                self.dy=int(self.dy/2)
                if self.dy==0:self.state,self.init,self.I="jd",1,0
        if self.state=="jd":
            self.M=X.jd
            if self.init:self.dy,self.init=40,0
            else:
                self.dy=1.5*self.dy
                if self.R.collidepoint(self.x,int(self.y+self.dy)):self.state,self.init,self.I,self.dy,self.y="i",1,0,0,self.R.top
        if self.state=="jul":
            self.dx,self.xbool,self.M=-40,1,X.ju
            if self.init:self.dy,self.init=-60,0
            else:
                self.dy=int(self.dy/2)
                if self.dy==0:self.state,self.init,self.I="ns" if self.NPC else "jdl",1,0
        if self.state=="jur":
            self.dx,self.xbool,self.M=40,0,X.ju
            if self.init:self.dy,self.init=-60,0
            else:
                self.dy=int(self.dy/2)
                if self.dy==0:self.state,self.init,self.I="ns" if self.NPC else "jdr",1,0
        if self.state=="jdl":
            self.dx,self.xbool,self.M=-40,1,X.jd
            if self.init:self.dy,self.init=40,0
            else:
                self.dy=1.5*self.dy
                if self.R.collidepoint(self.x,int(self.y+self.dy)):self.state,self.init,self.I,self.dy,self.y="l",1,0,0,self.R.top
        if self.state=="jdr":
            self.dx,self.xbool,self.M=40,0,X.jd
            if self.init:self.dy,self.init=40,0
            else:
                self.dy=1.5*self.dy
                if self.R.collidepoint(self.x,int(self.y+self.dy)):self.state,self.init,self.I,self.dy,self.y="r",1,0,0,self.R.top
        if self.state=="d":
            self.dx,self.dy,self.M=-40 if self.xbool else 40,0,X.d
            if self.I==len(self.M)-1:self.state,self.I="i",0
        if self.state=="dl":
            self.dx,self.dy,self.M=-40 if self.xbool else 40,0,X.d
            if self.I==len(self.M)-1:self.state,self.I="l",0
        if self.state=="dr":
            self.dx,self.dy,self.M=-40 if self.xbool else 40,0,X.d
            if self.I==len(self.M)-1:self.state,self.I="r",0
        if self.state=="s1":
            self.dx,self.dy,self.M=0,0,X.s1
            if self.I==3:self.blast.append([0,self.x-19*f if self.xbool else self.x+19*f,self.y-33*f,-40 if self.xbool else 40,0,"h"])
            if self.I==len(self.M)-1:
                if self.NPC:self.state,self.I=random.choice(["s1","s2"]),0
        if self.state=="s2":
            self.dx,self.dy,self.M=0,0,X.s2
            if self.I==3:self.blast.append([1,self.x-19*f if self.xbool else self.x+19*f,self.y-33*f,-40 if self.xbool else 40,0,"h"])
            if self.I==len(self.M)-1:self.state,self.I="i",0
        if self.state=="f":self.dy,self.dx,self.M,self.init=0,0,X.f,1
        if self.state=="fl":self.dy,self.dx,self.M,self.xbool=0,-40,X.ff,1
        if self.state=="fr":self.dy,self.dx,self.M,self.xbool=0,40,X.ff,0
        if self.state=="ns":
            self.dy,self.dx,self.M,self.body_attack=0,-40 if self.xbool else 40,X.ns,True
            if self.I==len(self.M)-1:self.state,self.I,self.body_attack,self.init="jdl" if self.xbool else "jdr",0,False,1
    def prepare(self):
        self.x+=self.dx
        if self.x<0:self.x,self.xbool=int(self.w/2),0
        if self.x>1200:self.x,self.xbool=1200-int(self.w/2),1
        self.y+=self.dy
        self.I=(self.I+1)%len(self.M)
        a,b,c,d=self.M[self.I]
        self.s=self.surf.subsurface(p.Rect(a,b,c,d))
        self.w=c*f
        self.h=d*f
        self.s=p.transform.scale(self.s,(self.w,self.h))
        self.s=p.transform.flip(self.s,self.xbool,False)
        self.s.set_colorkey((0,0,0))
        if self.state in ["s1","s2"]:
            if self.state=="s1":o=X.o1
            else:o=X.o2
            if o[self.I]:
                ox,oy=o[self.I]
                self.Ox=ox*f
                oy=oy*f
                self.body_rect=p.Rect(self.x-20*f,int(self.y-0.75*oy),40*f,int(oy/2))
            else:self.body_rect,self.Ox=p.Rect(self.x-20*f,int(self.y-0.75*self.h),40*f,int(self.h/2)),None
        else:self.body_rect,self.Ox=p.Rect(self.x-20*f,int(self.y-0.75*self.h),40*f,int(self.h/2)),None

def intro():
    I,mode,c=0,0,True
    while c:
        for e in p.event.get():
            if e.type==p.QUIT:
                p.quit()
                sys.exit()
            if e.type==p.KEYDOWN:
                if e.key==p.K_UP:
                    I-=1
                    if I<0:I=1
                if e.key==p.K_DOWN:
                    I+=1
                    if I>1:I=0
                if e.key==p.K_LEFT:
                    if I==1:
                        mode-=1
                        if mode<0:mode=1
                if e.key==p.K_RIGHT:
                    if I==1:
                        mode+=1
                        if mode>1:mode=0
                if e.key==p.K_SPACE:
                    if I==0:return mode
        screen.blit(p.transform.scale(p.image.load("intro.jpg"),(1200,700)),(0,0))
        t1=font1.render("MegamanX4 Combat",1,p.Color("white"))
        t2=font1.render("MegamanX4 Combat",1,p.Color("blue"))
        screen.blit(t2,(22,32))
        screen.blit(t1,(20,30))
        t3=font2.render("Start Game",1,p.Color("yellow" if I==0 else "blue"))
        t5=font2.render("Start Game",1,p.Color("white"))
        t4=font2.render("Game Mode: Story Mode" if mode==0 else "Game Mode: Combat Mode",1,p.Color("yellow" if I==1 else "blue"))
        t6=font2.render("Game Mode: Story Mode" if mode==0 else "Game Mode: Combat Mode",1,p.Color("white"))
        screen.blit(t5,(52,302))
        screen.blit(t3,(50,300))
        screen.blit(t6,(52,382))
        screen.blit(t4,(50,380))
        p.display.update()
        clock.tick(fps)

#Playable Character Selection Page
def select(Type):
    j=0
    Frames=[(250,200,264,276),(690,200,264,294)]
    while 1:
        for e in p.event.get():
            if e.type==p.QUIT:
                p.quit()
                sys.exit()
            if e.type==p.KEYDOWN:
                if e.key in [p.K_LEFT,p.K_UP]:
                    j-=1
                    if j<0:j=3
                if e.key in [p.K_RIGHT,p.K_DOWN]:
                    j+=1
                    if j>3:j=0
                if e.key==p.K_SPACE:return j
        screen.blit(p.transform.scale(p.image.load("character_selection.jpg"),(1200,700)),(0,0))
        a,b,c,d=Frames[j]
        p.draw.rect(screen,p.Color("yellow" if Type==0 else "red"),p.Rect(a,b,c,d),2)
        t1=font2.render("Select Your Avatar" if Type==0 else "Select Your Nemesis",1,p.Color("blue"))
        t2=font2.render("Select Your Avatar" if Type==0 else "Select Your Nemesis",1,p.Color("white"))
        screen.blit(t1,(332,32))
        screen.blit(t2,(330,30))
        A=p.image.load("X_ultimate.jpg").subsurface(p.Rect(150,9,44,46))
        A=p.transform.scale(A,(int(44*6),int(46*6)))
        A.set_colorkey((0,0,0))
        screen.blit(A,(250,200))
        B=p.image.load("zerox4sheet.jpg").subsurface(p.Rect(292,103,44,49))
        B=p.transform.scale(B,(int(44*6),int(49*6)))
        screen.blit(B,(690,200))
        p.display.update()
        clock.tick(fps)

def gameLoop(P1,P2):
    HI=0
    All=[X,Z]
    BG=["X_ultimate_bg.jpg","Z_bg.jpg"]
    GL=[570,650]
    R=p.Rect(0,GL[P2],1200,1200)
    z=All[P1](40,GL[P2],R,0)
    y=All[P2](800,GL[P2],R,1)
    bg=p.image.load(BG[P2])
    bg=p.transform.scale(bg,(1200,700))
    p.mixer.music.play()
    while 1:
        for e in p.event.get():
            if e.type==p.QUIT:
                p.quit()
                sys.exit()
            if e.type==p.KEYDOWN:z.state,z.I=All[P1].transition_keydown(z.state,e.key,z.I)
            if e.type==p.KEYUP:z.state=All[P1].transition_keyup(z.state,e.key)
        
        screen.blit(bg,(0,0))
        z.update()
        z.prepare()
    
        #Drawing playable character
        if z.HP>0:
            if z.Ox:
                if z.xbool:screen.blit(z.s,(z.x-z.w+abs(z.Ox),z.y-z.h))
                else:screen.blit(z.s,(z.x+z.Ox,z.y-z.h))
            else:screen.blit(z.s,(int(z.x-z.w/2),int(z.y-z.h)))
            p.draw.rect(screen,p.Color("white"),p.Rect(20,20,10,500))
            p.draw.rect(screen,p.Color("yellow"),p.Rect(20,20+int((1-z.HP/10000)*500),10,int(500*z.HP/10000)))
        else:
            text=font.render("GAME OVER",1,p.Color("white"),p.Color("blue"))
            screen.blit(text,(30,30))
            HI+=1
            if HI>20:return 0

        y.transition(z)
        y.update()
        y.prepare()
        
        if y.HP>0:
            if y.Ox:
                if y.xbool:screen.blit(y.s,(y.x-y.w+abs(y.Ox),y.y-y.h))
                else:screen.blit(y.s,(y.x+y.Ox,y.y-y.h))
            else:screen.blit(y.s,(int(y.x-y.w/2),int(y.y-y.h)))
            p.draw.rect(screen,p.Color("white"),p.Rect(1170,20,10,500))
            p.draw.rect(screen,p.Color("yellow"),p.Rect(1170,20+int((1-y.HP/10000)*500),10,int(500*y.HP/10000)))
        else:
            text=font.render("Victory",1,p.Color("white"),p.Color("blue"))
            screen.blit(text,(30,30))
            HI+=1
            if HI>20:return 1

        if len(z.blast)>0:
            NEW=[]
            for e in z.blast:
                A,B,C,D,E,F=e
                a,b,c,d=z.b[A][E]
                bs=z.surf.subsurface(p.Rect(a,b,c,d))
                bw,bh=c*f,d*f
                bs=p.transform.scale(bs,(bw,bh))
                bs=p.transform.flip(bs,False if F=="v" else (True if D<0 else False),False)
                if z.colorkey:bs.set_colorkey(z.colorkey)
                screen.blit(bs,(int(B-bw/2),int(C-bh/2)))
                if p.Rect(int(B-bw/2),int(C-bh/2),bw,bh).colliderect(y.body_rect):y.HP-=10
                if F=="h":
                    Y=B+D
                    if Y>0 and Y<1300:NEW.append([A,B+D,C,D,(E+1)%len(z.b[A]),F])
                else:
                    Y=C+D
                    if Y>0:NEW.append([A,B,C+D,D,(E+1)%len(z.b[A]),F])
            z.blast=NEW
       
        if len(y.blast)>0:
            NEW=[]
            for e in y.blast:
                A,B,C,D,E,F=e
                a,b,c,d=y.b[A][E]
                bs=y.surf.subsurface(p.Rect(a,b,c,d))
                bw,bh=c*f,d*f
                bs=p.transform.scale(bs,(bw,bh))
                bs=p.transform.flip(bs,False if F=="v" else (True if D<0 else False),False)
                if y.colorkey:bs.set_colorkey(y.colorkey)
                screen.blit(bs,(int(B-bw/2),int(C-bh/2)))
                if p.Rect(int(B-bw/2),int(C-bh/2),bw,bh).colliderect(z.body_rect):z.HP-=10
                if F=="h":
                    Y=B+D
                    if Y>0 and Y<1300:NEW.append([A,B+D,C,D,(E+1)%len(y.b[A]),F])
                else:
                    Y=C+D
                    if Y>0:NEW.append([A,B,C+D,D,(E+1)%len(y.b[A]),F])
            y.blast=NEW

        if z.saber_rect:
            if z.saber_rect.colliderect(y.body_rect):y.HP-=10

        if y.saber_rect:
            if y.saber_rect.colliderect(z.body_rect):z.HP-=10

        if z.body_attack:
            if z.body_rect.colliderect(y.body_rect):y.HP-=100

        if y.body_attack:
            if y.body_rect.colliderect(z.body_rect):z.HP-=10
        
        p.display.update()
        clock.tick(fps)

def restart():
    I=0
    while 1:
        for e in p.event.get():
            if e.type==p.QUIT:
                p.quit()
                sys.exit()
            if e.type==p.KEYDOWN:
                if e.key==p.K_UP:
                    I-=1
                    if I<0:I=1
                if e.key==p.K_DOWN:
                    I+=1
                    if I>1:I=0
                if e.key==p.K_SPACE:return I
        screen.blit(p.transform.scale(p.image.load("replay.jpg"),(1200,700)),(0,0))
        t1=font1.render("Play Again?",1,p.Color("white"))
        t2=font1.render("Play Again?",1,p.Color("blue"))
        screen.blit(t2,(105,155))
        screen.blit(t1,(100,150))
        t3=font2.render("YES",1,p.Color("yellow" if I==0 else "blue"))
        t4=font2.render("YES",1,p.Color("white"))
        screen.blit(t4,(205,305))
        screen.blit(t3,(200,300))
        t5=font2.render("No",1,p.Color("yellow" if I==1 else "blue"))
        t6=font2.render("No",1,p.Color("white"))
        screen.blit(t6,(905,305))
        screen.blit(t5,(900,300))
        p.display.update()
        clock.tick(fps)

def congratulate():
    I=0
    while 1:
        for e in p.event.get():
            if e.type==p.QUIT:
                p.quit()
                sys.exit()
        screen.blit(p.transform.scale(p.image.load("congratulate.jpg"),(1200,700)),(0,0))
        t1=font1.render("Congratulations!!",1,p.Color("white"))
        t2=font1.render("Congratulations!!",1,p.Color("blue"))
        screen.blit(t2,(105,305))
        screen.blit(t1,(100,300))
        p.display.update()
        clock.tick(fps)
        I+=1
        if I>20:p.quit()

mode=intro()
if mode==0:
    B=True
    P1=select(0)
    while 1:
        for I in range(2):
            J=gameLoop(P1,I)
            if J==0:
                B=False
                break
        if not B:
            if restart()==1:p.quit()
        else:congratulate()
else:
    c=True
    while c:
        gameLoop(select(0),select(1))
        if restart()==1:p.quit()
        else:congratulate()

