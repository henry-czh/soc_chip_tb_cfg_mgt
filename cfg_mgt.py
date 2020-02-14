#!/usr/bin/env python3

from os import system
import curses

stdscr = curses.initscr()

#get win maxyx
maxy = stdscr.getmaxyx()

head_maxy = 4
state_miny = maxy[0]-3

def find_min_len(rfile):
    ml = 0
    for line in rfile:
        line = line.split('.')
        if line!='' and len(line) < ml or ml==0:
            ml = len(line)
    return ml

def file_read():
    dh = open('design_her.cfg','r+')
    min_len = find_min_len(dh)
    dh.close()

    dh = open('design_her.cfg','r+')
    gui_file = open('gui_file','w')
    first_line = 1
    for item in dh.readlines():
        items = item.split(' ')[0].split('.')
        if first_line:
            first_line = 0
            gui_file.write('+++Instance+++\n')
            for i in range(min_len-1):
                if i>1:
                    gui_file.write((i-1)*'|   '+'|---'+items[i].strip('\n')+' [D]'+'\n')
                else:
                    gui_file.write(i*'|---'+items[i].strip('\n')+'\n')
        if len(items)>1:
            gui_file.write((len(items)-2)*'|   '+'|---'+items[-1].strip('\n')+' [D]'+'\n')
        else:
            gui_file.write((len(items)-1)*'|---'+items[-1].strip('\n')+'\n')

    gui_file.close()
    dh.close()


def cfg_win():
    #cfg_win = curses.newwin(maxy[0]-head_maxy-3,int(maxy[1]/2-1),head_maxy+1,int(maxy[1]/2+1))
    cfg_win = stdscr.subwin(maxy[0]-head_maxy-4,int(maxy[1]/2-1),head_maxy+1,int(maxy[1]/2+1))
    cfg_win.border(0)
    cfg_win.keypad(True)
    cfg_win.leaveok(False)

    cfg_maxy = cfg_win.getmaxyx()

    curses.curs_set(0)
    cfg_win.bkgd(curses.color_pair(5))
    #title
    cfg_win.addstr(0,int(cfg_maxy[0]/2),'- Verfication Configuration ',curses.color_pair(6))

    cfg_win.refresh()

def desing_win():
    desing_win = curses.newwin(maxy[0]-head_maxy-4,int(maxy[1]/2),head_maxy+1,1)
    desing_win.border(0)
    desing_win.keypad(True)
    desing_win.leaveok(False)

    desing_win.bkgd(curses.color_pair(5))
    main_maxy = desing_win.getmaxyx()
    
    #title
    desing_win.addstr(0,int(main_maxy[0]/2),'- Design Configuration ',curses.color_pair(6))

    init_file = open("design_her.cfg",'r+')
    dh = open("gui_file",'r+')
    dh_list = dh.readlines()
    initf_list = init_file.readlines()
    
    len_sum = open('design_her.cfg','r+')
    min_len = find_min_len(len_sum)+1
    len_sum.close()

    for i in range(len(dh_list)):
        desing_win.addstr(i+1,2,dh_list[i].strip('\n'),curses.color_pair(1))
    
    desing_win.refresh()
    #user ctl
    while True:
        dim = desing_win.getyx()
        desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(3))
        desing_win.refresh()

        c = desing_win.getch()
        if c == ord('p'):
            break
        elif c == ord('\n'):
            if dh_list[dim[0]-1].find('[D]')>0:
                if initf_list[dim[0]-min_len].find('[V]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[D]','[V]')
                elif initf_list[dim[0]-min_len].find('[S]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[D]','[S]')
                elif initf_list[dim[0]-min_len].find('[N]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[D]','[N]')
            elif dh_list[dim[0]-1].find('[V]')>0:
                if initf_list[dim[0]-min_len].find('[S]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[V]','[S]')
                elif initf_list[dim[0]-min_len].find('[N]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[V]','[N]')
                elif initf_list[dim[0]-min_len].find('[D]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[V]','[D]')
            elif dh_list[dim[0]-1].find('[S]')>0:
                if initf_list[dim[0]-min_len].find('[N]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[S]','[N]')
                elif initf_list[dim[0]-min_len].find('[D]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[S]','[D]')
                elif initf_list[dim[0]-min_len].find('[V]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[S]','[V]')
            elif dh_list[dim[0]-1].find('[N]')>0:
                if initf_list[dim[0]-min_len].find('[D]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[N]','[D]')
                elif initf_list[dim[0]-min_len].find('[V]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[N]','[V]')
                elif initf_list[dim[0]-min_len].find('[S]')>0:
                    dh_list[dim[0]-1]=dh_list[dim[0]-1].replace('[N]','[S]')
            desing_win.refresh()
        elif (c == curses.KEY_UP or c == ord('k')) and dim[0] != 0 and dim[0] !=1:
            if dh_list[dim[0]-1].find('[D]')>0:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(1))
            elif dh_list[dim[0]-1].find('[V]')>0:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(4))
            elif dh_list[dim[0]-1].find('[S]')>0:
                desing_win.addstr(dim[0],1,dh_list[dim[0]-1].strip('\n'),curses.color_pair(5))
            elif dh_list[dim[0]-1].find('[N]')>0:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(6))
            else:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(1))
            desing_win.move(dim[0]-1,dim[1])
            desing_win.refresh()
        elif (c == curses.KEY_DOWN or c == ord('j')) and dim[0] != main_maxy[0]-1 and dim[0] != main_maxy[0]-2 and dim[0] < len(dh_list):
            if dh_list[dim[0]-1].find('[D]')>0:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(1))
            elif dh_list[dim[0]-1].find('[V]')>0:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(4))
            elif dh_list[dim[0]-1].find('[S]')>0:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(5))
            elif dh_list[dim[0]-1].find('[N]')>0:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(6))
            else:
                desing_win.addstr(dim[0],2,dh_list[dim[0]-1].strip('\n'),curses.color_pair(1))
            desing_win.move(dim[0]+1,dim[1])
            desing_win.refresh()
        elif (c == curses.KEY_LEFT or c == ord('h')) and dim[1] != 0:
            desing_win.move(dim[0],dim[1]-1)
        elif (c == curses.KEY_RIGHT or c == ord('l')) and dim[1] != main_maxy[1]-1:
            desing_win.move(dim[0],dim[1]+1)

    taget = open("taget_file",'w+')
    for i in range(len(dh_list)):
        taget.write(dh_list[i])
    taget.close()
    dh.close()
    init_file.close()
    

def main(stdscr):
    stdscr.clear()

    #enable key input and allow index move
    stdscr.keypad(True)
    stdscr.leaveok(False)
    
    #close input and dont display input 
    curses.noecho()
    curses.start_color()
    #design color
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
    ##verif color
    curses.init_pair(4,curses.COLOR_RED,curses.COLOR_WHITE)
    ##simu color
    curses.init_pair(5,curses.COLOR_CYAN,curses.COLOR_WHITE)
    ##null color
    curses.init_pair(6,curses.COLOR_MAGENTA,curses.COLOR_WHITE)

    #main front color
    curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_BLACK)

    #select line color
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)

    #back ground color
    curses.init_pair(7,curses.COLOR_WHITE,curses.COLOR_BLUE)
    curses.init_pair(8,curses.COLOR_BLACK,curses.COLOR_WHITE)
    stdscr.border(0)

    #head
    div_line=''
    for i in range(0,curses.COLS-2):
        div_line = div_line+'='
    
    stdscr.addstr(0,int(maxy[1]/2-15),'-System Testbench Config Manager-',curses.color_pair(2))
    
    #stdscr.addstr(1,1,div_line,curses.color_pair(2))
    stdscr.addch(2,1,curses.ACS_PLMINUS,curses.color_pair(2))
    stdscr.addstr(4,1,div_line,curses.color_pair(2))

    stdscr.bkgd(curses.color_pair(7))

    save_x = int(maxy[1]/4)
    load_x = save_x*2
    exit_x = save_x*3

    stdscr.addstr(maxy[0]-3,save_x,'<Save>',curses.color_pair(6))
    stdscr.addstr(maxy[0]-3,load_x,'<Load>',curses.color_pair(6))
    stdscr.addstr(maxy[0]-3,exit_x,'<Exit>',curses.color_pair(6))


    stdscr.refresh()

    file_read()
    cfg_win()
    desing_win()
    
    curses.endwin()
curses.wrapper(main)
