import curses
scr=curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()
scr.keypad(True)
scrsize=scr.getmaxyx()
curses.start_color()
cloc='home'
print=lambda a:[scr.addstr(0,0,a),scr.refresh()]
curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_GREEN)
curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_RED)
curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)

def cwrite(color,y,x,txt):
    scr.attron(color)
    scr.addstr(y,x,txt)
    scr.attroff(color)

def homescreen():
    scr.clear()
    select=curses.color_pair(1)
    if copt=='play':
        cwrite(select,scrsize[0]//2,scrsize[1]//2,'PLAY')
        scr.addstr(scrsize[0]//2+1,scrsize[1]//2,'EXIT')
    if copt=='exit':
        scr.addstr(scrsize[0]//2,scrsize[1]//2,'PLAY')
        cwrite(select,scrsize[0]//2+1,scrsize[1]//2,'EXIT')
    scr.refresh()

def gamerender():
    scr.clear()
    y,x=scrsize
    x=x//2-5
    y=y//2-4
    select=copt[0].replace('a','1').replace('b','2').replace('c','3')+copt[1]
    color=curses.color_pair(1)if game[int(select[0])-1][int(select[1])-1]==' ' else curses.color_pair(2)
    if cplayer not in['1','2']:color=curses.color_pair(3)
    f={1:1,2:1,4:2,5:2,7:3,8:3}
    for i in range(1,9):
        s='----+----+----'
        if (i==3 and copt in ['a1','a2','a3','b1','b2','b3']) or (i==6 and copt in ['b1','b2','b3','c1','c2','c3']):
            if select[1]=='1':
                cwrite(color,y+i,x-1,'-'+s[:5])
                scr.addstr(y+i,x+5,s[5:]+'-')
            if select[1]=='2':
                scr.addstr(y+i,x-1,'-'+s[:4])
                cwrite(color,y+i,x+4,s[4:10])
                scr.addstr(y+i,x+10,s[10:]+'-')
            if select[1]=='3':
                scr.addstr(y+i,x-1,'-'+s[:9])
                cwrite(color,y+i,x+9,s[9:]+'-')
            continue
        if i in [3,6]:
            scr.addstr(y+i,x-1,'-'+s+'-')
            continue
        a=[' \\/ ','+--+']if i in [1,4,7]else [' /\\ ','+--+']
        s=''
        d={1:0,4:1,7:2} if i in [1,4,7] else {2:0,5:1,8:2}
        for j in game[d[i]]:
            if j=='X':s+=a[0]
            elif j=='O':s+=a[1]
            else:s+='    '
            s+='|'
        s=s[:-1]
        if f[i]==int(select[0]):
            if int(select[1])==1:
                cwrite(color,y+i,x-1,' '+s[:5])
                scr.addstr(y+i,x+5,s[5:]+' ')
            if int(select[1])==2:
                scr.addstr(y+i,x,s[:4])
                cwrite(color,y+i,x+4,s[4:10])
                scr.addstr(y+i,x+10,s[10:])
            if int(select[1])==3:
                scr.addstr(y+i,x-1,' '+s[:9])
                cwrite(color,y+i,x+9,s[9:]+' ')
            continue
        scr.addstr(y+i,x,s)
    if cplayer=='tie':scr.addstr(y+10,x+5,'Tie!')
    elif cplayer[:3]=='win':scr.addstr(y+10,x,f'Player {cplayer[-1]} has won!')
    else:scr.addstr(y+10,x,f'Player {cplayer}\'s Turn')
    scr.refresh()

copt='play'    
homescreen()
while 1:
    if cloc=='home':
        key = scr.getch()
        if key == curses.KEY_DOWN and copt=='play':
            copt='exit'
            homescreen()
        elif key == curses.KEY_UP and copt=='exit':
            copt='play'
            homescreen()
        elif key == curses.KEY_ENTER or key == 10:
            if copt=='play':
                cloc='play'
                cplayer='1'
                copt='a1'
                game=[[' 'for i in' '*3]for i in ' '*3]
                moves=0
                gamerender()
            if copt=='exit':
                scr.clear()
                break
    if cloc=='play':
        key = scr.getch()
        if key == 113:
            cloc='home'
            copt='play'
            scr.clear()
            homescreen()
            continue
        if cplayer not in ['1','2']:continue
        if key == curses.KEY_UP:
            copt=copt.replace('b','a').replace('c','b')
        if key == curses.KEY_DOWN:
            copt=copt.replace('b','c').replace('a','b')
        if key == curses.KEY_RIGHT:
            copt=copt.replace('2','3').replace('1','2')
        if key == curses.KEY_LEFT:
            copt=copt.replace('2','1').replace('3','2')
        if (key == curses.KEY_ENTER or key == 10)and game[int(copt[0].replace('a','0').replace('b','1').replace('c','2'))][int(copt[1])-1]==' ' and cplayer in ['1','2']:
            game[int(copt[0].replace('a','0').replace('b','1').replace('c','2'))][int(copt[1])-1]=cplayer.replace('1','X').replace('2','O')
            cplayer=cplayer.replace('1','a').replace('2','1').replace('a','2')
            moves+=1
        if moves==9:
            cplayer='tie'
            copt='None'
        if moves>2:
            p1,p2,p3=game
            p4,p5,p6=[[j[i] for j in game]for i in range(3)]
            p7=[game[0][0],game[1][1],game[2][2]]
            p8=[game[0][2],game[1][1],game[2][0]]  
            for i in[p1,p2,p3,p4,p5,p6,p7,p8]:
                if i[0]=='X' and i.count('X')==3:
                    cplayer='win1'
                if i[0]=='O' and i.count('O')==3:
                    cplayer='win2'
        gamerender()
curses.echo()
curses.nocbreak()
scr.keypad(False)
curses.curs_set(1)
curses.endwin()
