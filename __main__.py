import curses
scr=curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()
scr.keypad(True)
scrsize=scr.getmaxyx()
curses.start_color()
cloc='home'
home_opts=['PLAY','PLAY vs AI','EXIT']
curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_GREEN)
curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_RED)
curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
def cwrite(color,y,x,txt):
    scr.attron(color)
    scr.addstr(y,x,txt)
    scr.attroff(color)
def homescreen():
    scr.clear()
    for i in enumerate(home_opts):
        if i[0] in range(len(home_opts)//2+1):yadjust=-(len(home_opts)//2-(i[0]+1))
        else:yadjust=(i[0]+1)-(len(home_opts)//2)
        color=curses.color_pair(1)if copt==i[1]else curses.color_pair(3)
        cwrite(color,scrsize[0]//2+yadjust,scrsize[1]//2-(len(i[1])//2),i[1])
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
    sym='(X)'if cplayer=='1'else'(O)'
    if cplayer=='tie':scr.addstr(y+10,x+5,'Tie!')
    elif cplayer[:3]=='win':scr.addstr(y+10,x,f'Player {cplayer[-1]} has won!')
    else:scr.addstr(y+10,x,f'Player {cplayer}\'s Turn'+sym)
    scr.addstr(y+11,x-10,'Press \'q\' to return to Home Screen')
    scr.refresh()
copt='PLAY'    
homescreen()

import random
while 1:
    if __name__!='__main__':break
    if cloc=='home':
        key = scr.getch()
        if key == curses.KEY_UP:
            copt=home_opts[home_opts.index(copt)-1]
        elif key == curses.KEY_DOWN:
            copt=home_opts[(home_opts.index(copt)+1)%len(home_opts)]
        elif key == curses.KEY_ENTER or key == 10:
            if copt=='PLAY':
                cloc='play'
                cplayer='1'
                copt='a1'
                game=[[' 'for i in' '*3]for i in ' '*3]
                moves=0
                gamerender()
                continue
            if copt=='PLAY vs AI':
                cloc='playvsai'
                cplayer='1'
                copt='a1'
                game=[[' 'for i in' '*3]for i in' '*3]
                moves=0
                gamerender()
                continue
            if copt=='EXIT':
                scr.clear()
                break
        homescreen()
    if cloc=='play' or cloc=='playvsai':
        if cloc=='playvsai':aiplay=True if cplayer=='2'else False
        if (cloc=='playvsai'and not aiplay) or cloc=='play':
            key = scr.getch()
            if key == 113:
                copt=cloc=='play'and'PLAY'or'PLAY vs AI'
                cloc='home'
                del game
                del cplayer
                del moves
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
                moves+=1
                cplayer=cplayer.replace('1','a').replace('2','1').replace('a','2')
                aiplay=False
            del key
        if cloc=='playvsai'and aiplay:
            moves+=1
            pmc={}
            for i in enumerate([p1,p2,p3,p4,p5,p6,p7,p8]):
                if (i[1].count('X')==2 or i[1].count('O')==2) and i[1].count(' ')==1:pmc[i[0]]=(1,i[1])
                elif i[1].count('O')==2 and i[1].count(' ')==1:pmc[i[0]]=(2,i[1])
                elif i[1].count(' ')==2:pmc[i[0]]=(0,i[1])
                else:(-1,i[1])
            pmc=random.choice([(j,pmc[j][1])for j in list(filter(lambda i:pmc[i][0]==max(pmc.values(),key=lambda i:i[0])[0],pmc))])
            if pmc[0]in[0,1,2]:
                game[pmc[0]][pmc[1].index(' ')]='O'
            if pmc[0]in[3,4,5]:
                game[pmc[1].index(' ')][pmc[0]-3]='O'
            if pmc[0]==6:
                game[pmc[1].index(' ')][pmc[1].index(' ')]='O'
            if pmc[0]==7:
                game[pmc[1].index(' ')][2-pmc[1].index(' ')]='O'
            cplayer='1'
            del pmc
        p1,p2,p3=game
        p4,p5,p6=[[j[i] for j in game]for i in range(3)]
        p7=[game[0][0],game[1][1],game[2][2]]
        p8=[game[0][2],game[1][1],game[2][0]]
        if moves>8:cplayer='tie'
        if moves>4:
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
