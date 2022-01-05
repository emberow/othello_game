# login.py
from os import truncate
from tkinter import *
from tkinter import messagebox
#import dashboard

import socket

import errno
import sys
import time

import pygame
from pygame.locals import QUIT
import math
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 12345

class record_window:
    def __init__(self, player1_name, player2_name, player1_score, player2_score):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player_score = []
        for i in range(len(player1_score)):
            self.player_score.append(str(player1_score[i]) + " : " + str(player2_score[i]))
    def create_window(self):
        window = Tk()
        # 使得視窗在螢幕正中間
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        x = int(width / 2 - 100 / 2)
        y = int(height / 2 - 50 / 2)
        # 多少筆記錄
        record_QTY = len(self.player1_name) 
        # 根據多少筆記錄調整視窗大小
        window.geometry('200x'+ str(25*record_QTY) + "+" +str(x) + "+" + str(y))
        r = 0
        for i in range(record_QTY):
            record = f"{self.player1_name[i]:>{10}}" + " vs " + f"{self.player2_name[i]:<{10}}" + f"{self.player_score[i]:<{10}}"
            temp_label = Label(window, text=record, bg='white', fg='#000000', font=('Arial', 12), justify = "center")
            temp_label.grid(column=0, row=r)
            r += 1

class result_window:
    def __init__(self, player1_name, player2_name, player1_score, player2_score):
        self.player = player1_name + " vs " + player2_name
        self.message = str(player1_score) + " : " + str(player2_score)
        self.player1_score = player1_score
        self.player2_score = player2_score
    def create_window(self):
        window = Tk()
        # 使得視窗在螢幕正中間
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        x = int(width / 2 - 100 / 2)
        y = int(height / 2 - 50 / 2)
        window.title('遊戲結束')
        window.geometry('100x75'+ "+" +str(x) + "+" + str(y))
        if self.player1_score > self.player2_score:
            result = "玩家1勝利"
        else:
            result = "玩家2勝利"
        lbl_1 = Label(window, text=result, bg='white', fg='#000000', font=('Arial', 12), justify = "center")
        lbl_1.grid(column=0, row=0)
        lbl_1 = Label(window, text=self.player, bg='white', fg='#000000', font=('Arial', 12), justify = "center")
        lbl_1.grid(column=0, row=1)
        lbl_2 = Label(window, text=self.message, bg='white', fg='#000000', font=('Arial', 12), justify = "center")
        lbl_2.grid(column=0, row=2)
        window.mainloop()
        


# 登入頁面視窗
class LoginWindow:
    def __init__(self):
        self.win = Tk()
        # reset the window and background color
        self.canvas = Canvas(self.win,
                             width=600, height=500,
                             bg='white')
        self.canvas.pack(expand=YES, fill=BOTH)
 
        # show window in center of the screen
        width = self.win.winfo_screenwidth()
        height = self.win.winfo_screenheight()
        x = int(width / 2 - 600 / 2)
        y = int(height / 2 - 500 / 2)
        str1 = "600x500+" + str(x) + "+" + str(y)
        self.win.geometry(str1)
 
        # disable resize of the window
        self.win.resizable(width=False, height=False)
 
        # change the title of the window
        self.win.title("Welcome | Login Window | Administrator")
 
    def add_frame(self):
        self.frame = Frame(self.win, height=400, width=450)
        self.frame.place(x=80, y=50)
 
        x, y = 70, 20
 
        self.img = PhotoImage(file='images/登入畫面.png')
        self.label = Label(self.frame, image=self.img)
        self.label.place(x=x+60, y=y+0)
 

 
        self.uidlabel = Label(self.frame, text="User ID:")
        self.uidlabel.config(font=("Courier", 12, 'bold'))
        self.uidlabel.place(x=50, y=y+250)
 
        self.userid = Entry(self.frame, font='Courier 12')
        self.userid.place(x=170, y=y+250)
 
        self.button = Button(self.frame, text="對戰紀錄",
                             font='Courier 15 bold',
                             command=self.get_record)
        self.button.place(x=230, y=y+290)
 
        self.button = Button(self.frame, text="登入",
                             font='Courier 15 bold',
                             command=self.login)
        self.button.place(x=150, y=y+290)
 
        self.win.mainloop()

    def connect_to_server(self, user_name):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)
        username = user_name.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)
        win = create_window(user_name, client_socket)
        win.game()
        
        # If message is not empty - send it
    def login(self):
        # get the data and store it into tuple (data)
        
        name = self.userid.get()
        
        # validations
        if self.userid.get() == "":
            messagebox.showinfo("Alert!","Enter UserID First")
        else:
            if name == "get_record":
                self.get_record()
            else:
                messagebox.showinfo("Message", "歡迎,"+name)
                self.win.destroy()
                #x = dashboard.DashboardWindow()
                self.connect_to_server(name)
            
    def get_record(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        client_socket.setblocking(False)
        message = "get_record".encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
        message = ""
        # 剛建立好連線須給他時間才能接收 不然會出錯
        time.sleep(0.05)
        while True: 
            if message != "":
                break
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip()) 
            message = client_socket.recv(message_length).decode('utf-8')
            records = message.split("/")
            player1_name_list = []
            player2_name_list = []
            player1_score_list = []
            player2_score_list = []
            for record in records:
                item = record.split(",")
                player1_name_list.append(item[0])
                player2_name_list.append(item[1])
                player1_score_list.append(item[2])
                player2_score_list.append(item[3])

            win = record_window(player1_name_list, player2_name_list, player1_score_list, player2_score_list)
            win.create_window()
                # print(player1_name, player2_name, player1_score, player2_score)





# 遊戲視窗
class create_window: 
    def __init__(self, user_name, client_socket):
        self.player1_name = ""
        self.player2_name = ""
        self.whos_turn = "?"
        self.board_state = ""
        self.user_name = user_name
        self.client_socket = client_socket
        self.is_start = False
        self.is_your_turn = False
        self.your_identity = "guest"#是玩家1還是玩家2或是guest
        self.is_end = "not_end"


    # 驗證這步棋是否有效
    def verify_move(self, str_board, size, player, loc):
        another_player = not player
        #超出邊界return false
        board = []
        temp = []
        str_board_state = ""
        return_true = False

        for i in range(len(str_board)):
            temp.append(int(str_board[i]))
            if i % 6 == 5:
                board.append(temp)
                temp = []

        if(loc[0] < 0 or loc[0] >= size or loc[1] < 0 or loc[1] >= size or board[loc[0]][loc[1]] == 1 or board[loc[0]][loc[1]] == 2 ):
            return False,""
        diection = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
        

        for dir_x,dir_y in diection:
            loc_x = loc[0]
            loc_y = loc[1]
            next_to_location = True
            while True:
                loc_x += dir_x
                loc_y += dir_y
                
                # 超出邊界而不符合條件時 則找其他方向
                if(loc_x < 0 or loc_x >= size or loc_y < 0 or loc_y >= size):
                    break
                # 下一步棋是空的時 則找其他方向
                elif (board[loc_x][loc_y] == 0):
                    break
                # 下一步棋是對手的棋時則繼續尋找
                elif(board[loc_x][loc_y] == another_player):
                    continue
                # 如果下一步棋是同色又是第一步的話 則找其他方向
                elif(board[loc_x][loc_y] == player and next_to_location):
                    break
                elif(board[loc_x][loc_y] == player and not next_to_location):
                    return_true = True
                    temp_loc_x = loc_x
                    temp_loc_y = loc_y
                    while(True):
                        temp_loc_x -= dir_x
                        temp_loc_y -= dir_y
                        board[temp_loc_x][temp_loc_y] = player
                        if (temp_loc_x == loc[0] and temp_loc_y == loc[1]):
                            break          
                next_to_location = False

        for i in range(6):
            for j in range(6):
                str_board_state += str(board[i][j])

        if return_true == True:
            return True, str_board_state
        else:
            return False,""

    # 更新頁面
    def update_screen(self):
        if self.player1_name != "" and self.player2_name != "":
            self.is_start = True
        # 輪到你的回合就可以下一步棋
        if self.your_identity == self.whos_turn:
            print("你的回合")
            self.is_your_turn = True

        window_surface = pygame.display.set_mode((700, 700))

        

        # 建立 window 視窗畫布，大小為 800x600
        
        # 設置視窗標題為 Hello World:)
        pygame.display.set_caption('黑白棋 player:{}'.format(self.user_name))
        # 清除畫面並填滿背景色
        window_surface.fill((255, 255, 255))
        font = pygame.font.Font('font/msjhbd.ttf', 36)

        # 開始之後才製作棋盤
        if self.is_start == True:
            grid_width = 80
            grid_height = 80
            for i in range(6):
                for j in range(6):
                    rect_list=[100+i*80,100+j*80,grid_width,grid_height]#Rect(left,top,width,height)
                    pygame.draw.rect(window_surface,[51,204,51],rect_list,0)
            
            for i in range(7):
                for j in range(7):
                    pygame.draw.line(window_surface,(0,0,0),(100,100+j*80),(580,100+j*80),10)
                    pygame.draw.line(window_surface,(0,0,0),(100+i*80,100),(100+i*80,580),10)
            
            for i in range(len(self.board_state)):
                x = i % 6
                y = math.floor(i / 6)
                # 黑棋
                if self.board_state[i] == "1":
                    pygame.draw.circle(window_surface,[0,0,0],[140+x*80,140+y*80],30,0)
                # 白棋
                if self.board_state[i] == "2":
                    pygame.draw.circle(window_surface,[0,0,0],[140+x*80,140+y*80],30,1)

            # 顯示現在輪到誰
            if self.whos_turn == "player1":
                pygame.draw.circle(window_surface,[10,10,10],[540,60],30,0)
            elif self.whos_turn == "player2":
                pygame.draw.circle(window_surface,[0,0,0],[540,620],30,1)


        textImage1 = font.render("請點此加入遊戲", True, (0,0,0))
        textImage2 = font.render("等待玩家...", True, (0,0,0)) 
        if self.player1_name == "" and self.your_identity != "player2":
            window_surface.blit(textImage1, (230, 30))
        elif self.player1_name == "" and self.your_identity == "player2":
            window_surface.blit(textImage2, (230, 30))
        else:
            if self.your_identity == "player1":
                window_surface.blit(font.render(self.player1_name + " (你)", True, (0,0,0)), (230, 30)) 
            else:
                window_surface.blit(font.render(self.player1_name, True, (0,0,0)), (230, 30)) 
        

        if self.player2_name == "" and self.your_identity != "player1":
            window_surface.blit(textImage1, (230, 600))  
        elif self.player2_name == "" and self.your_identity == "player1":
            window_surface.blit(textImage2, (230, 600))
        else:
            if self.your_identity == "player2":
                window_surface.blit(font.render(self.player2_name + " (你)", True, (0,0,0)), (230, 600)) 
            else:
                window_surface.blit(font.render(self.player2_name, True, (0,0,0)), (230, 600)) 
        pygame.display.update()

    # 得到棋盤目前資訊
    def get_info_from_server(self):
        message = ""
        while True:
            if message != "":
                break
            message_header = self.client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = self.client_socket.recv(message_length).decode('utf-8')
            message = message.split("/")
            self.player1_name = message[0]
            self.player2_name = message[1]
            self.whos_turn = message[2]
            self.board_state = message[3]
            self.is_end = message[4]
            

    # 送資料給server
    # 資料格式
    #{name} #訪客登入
    #player1:{name} #訪客成為玩家
    # board_state/player1/000000000000001200002100000000000000 #代表player1改變完棋盤位置後回傳棋盤狀態
    def send_message_to_server(self, message):
        message_header = f"{len(message):<{HEADER_LENGTH}}"
        self.client_socket.send((message_header + message).encode("utf-8"))

# 遊戲從這裡開始
    def game(self):
        pygame.init()
        # 只接收server第一個訊息
        self.get_info_from_server()
        # 更新頁面
        self.update_screen()
        is_already_choose = False
        
        # 事件迴圈監聽事件，進行事件處理
        while True:
            message = ""
            # 迭代整個事件迴圈，若有符合事件則對應處理
            for event in pygame.event.get():
                # 當使用者結束視窗，程式也結束
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            # 處理滑鼠點擊事件
            mouse_position = pygame.mouse.get_pos()
            try:
                message_header = self.client_socket.recv(HEADER_LENGTH)
                if not len(message_header):
                    print('Connection closed by the server')
                    sys.exit()

                message_length = int(message_header.decode('utf-8').strip())
                # Receive and decode username
                message = self.client_socket.recv(message_length).decode('utf-8')
                
                if message:
                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    print(message)
                    message = message.split("/")
                    self.player1_name = message[0].strip()
                    self.player2_name = message[1].strip()
                    self.whos_turn = message[2].strip()
                    self.board_state = message[3].strip()
                    self.is_end = message[4].strip()
                    self.update_screen()
                # 更新畫面，等所有操作完成後一次更新（若沒更新，則元素不會出現）
                
                
            
            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()
        
            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))
                sys.exit()

            # 判斷是否結束
            if self.is_end != "end":
                # 決定1號玩家
                if(mouse_position[0] >= 0 and mouse_position[1] >= 0 and mouse_position[0] <= 700 and mouse_position[1] <= 100 and event.type == pygame.MOUSEBUTTONUP and self.player1_name == "" and not is_already_choose):
                    message = "player1:{}".format(self.user_name)
                    self.send_message_to_server(message)
                    is_already_choose = True
                    self.your_identity = "player1"
                    print("已成為1號玩家")
                # 決定2號玩家
                if(mouse_position[0] >= 0 and mouse_position[1] >= 600 and mouse_position[0] <= 700 and mouse_position[1] <= 700 and event.type == pygame.MOUSEBUTTONUP and self.player2_name == "" and not is_already_choose):
                    message = "player2:{}".format(self.user_name)
                    self.send_message_to_server(message)
                    
                    is_already_choose = True
                    self.your_identity = "player2"
                    print("已成為2號玩家")
                
                # 取得點擊位置
                if self.is_your_turn == True and event.type == pygame.MOUSEBUTTONUP:
                    x = math.floor((mouse_position[0] - 100) / 80)
                    y = math.floor((mouse_position[1] - 100) / 80)
                    
                    if x >= 0 and x <= 5 and y >= 0 and y <= 5:
                        
                        is_qualified, temp_str_board = self.verify_move(self.board_state, 6, 1, [y,x])
                        
                        if self.your_identity == "player1" :
                            is_qualified, temp_str_board = self.verify_move(self.board_state, 6, 1, [y,x])
                            if is_qualified == True:
                                self.is_your_turn = False
                                message = "board_state/player1/" + temp_str_board
                                self.send_message_to_server(message)

                        elif self.your_identity == "player2":
                            is_qualified, temp_str_board = self.verify_move(self.board_state, 6, 2, [y,x])
                            if is_qualified == True:
                                self.is_your_turn = False
                                message = "board_state/player2/" + temp_str_board
                                self.send_message_to_server(message)
            # 遊戲結算
            else:
                self.is_end = "not_end"
                print("遊戲結束")
                black = 0
                white = 0
                for i in self.board_state:
                    if i == "1":
                        black += 1
                    elif i == "2":
                        white += 1
                print(black,white)
            
                resulf_win = result_window(self.player1_name, self.player2_name, black, white)
                resulf_win.create_window()
                
                # 初始化棋盤
                self.player1_name = ""
                self.player2_name = ""
                self.whos_turn = "?"
                self.board_state = ""
                self.is_start = False
                self.is_your_turn = False
                self.your_identity = "guest"#是玩家1還是玩家2或是guest
                self.is_end = "not_end"
                is_already_choose = False
                
     

def main():
    log = LoginWindow()
    log.add_frame()

main()