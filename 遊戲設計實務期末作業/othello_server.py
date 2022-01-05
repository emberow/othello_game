from os import truncate
import socket
import select
import db
HEADER_LENGTH = 10
def server_boardcast(clients, content):
    # message = player1_name/player2_name
    #已經包含4個"/"
    message_length = 4
    for i in content:
        message_length += len(content[i])
    message = f"{message_length:<{HEADER_LENGTH}}" + content['player1_name'] + "/" + content['player2_name'] + "/" + content['whos_turn'] + "/" + content["board_state"] + "/" + content["is_end"]
    print(message)
    for client_socket in clients:
        client_socket.send(message.encode("utf-8"))

def verify_move(str_board, size, player, loc):
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

        # 如果超出邊界 或者是下的這步棋已經被下過時 回傳false
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
                # 如果下一步棋是同色 又不是第一步時 改變中間經過的棋子顏色
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

# 判斷player是否沒有下一步可以走
def judge_is_over(board_state, player):
    for x in range(6):
        for y in range(6):
            is_varified, str_board_state = verify_move(board_state, 6, player, [x,y])
           
            #找到下一步可以走
            if is_varified == True:
                return False
    return True

class server:
    def create_server(self):
        IP = "127.0.0.1"
        PORT = 12345
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP, PORT))
        server_socket.listen()
        sockets_list = [server_socket]
        clients = {}
        print(f'Listening for connections on {IP}:{PORT}...')
        player_socket = {"player1_socket" : "", "player2_socket" : ""}
        board_state = "000000000000001200002100000000000000"
        content = {"player1_name" : "", "player2_name" : "", "whos_turn" : "player1", "board_state" : board_state, "is_end" : "not_end"}
        
        while True:
            # Calls Unix select() system call or Windows select() WinSock call with three parameters:
            #   - rlist - sockets to be monitored for incoming data
            #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
            #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
            # Returns lists:
            #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
            #   - writing - sockets ready for data to be send thru them
            #   - errors  - sockets with some exceptions
            # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
            read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        
        
            # Iterate over notified sockets
            for notified_socket in read_sockets:
                # If notified socket is a server socket - new connection, accept it
                if notified_socket == server_socket:
        
                    # Accept new connection
                    # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                    # The other returned object is ip/port set
                    client_socket, client_address = server_socket.accept()
        
                    # Client should send his name right away, receive it
                    user = receive_message(client_socket)
        
                    # If False - client disconnected before he sent his name
                    if user is False:
                        continue
                    
                    user_name = user['data'].decode('utf-8')
                    
                    # 該用戶只是查詢對戰紀錄 所以不將客戶資料儲存到sockets_list裡面
                    if user_name == "get_record":
                        # 得到最後10筆對戰紀錄
                        # 格式為 player1, player2, player1_score, player2_score, time/player1, player2, player1_score, player2_score, time/...
                        records = db.get_10_record()
                        message = ""
                        message_length = 0
                        for record in records:
                            for item in record:
                                message_length += len(str(item))
                                message += str(item)
                                #item不是最後一筆資料時
                                if item != record[-1]:
                                    message_length += 1
                                    message += ","
                            if record != records[-1]:
                                message_length += 1
                                message += "/"
                        
                        message = f"{message_length:<{HEADER_LENGTH}}" + message
                        print(message)
                        client_socket.send(message.encode("utf-8"))
                    else:
                        # Add accepted socket to select.select() list
                        sockets_list.append(client_socket)
                        # Also save username and username header
                        clients[client_socket] = user
                        print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                        # 傳送給剛連進來的客戶目前資訊
                        message_length = 4 
                        for i in content:
                            message_length += len(content[i])
                        message = f"{message_length:<{HEADER_LENGTH}}" + content['player1_name'] + "/" + content['player2_name'] + "/" + content['whos_turn'] + "/" + content["board_state"] + "/" + content["is_end"]
                        client_socket.send(message.encode("utf-8"))
        

                else:
                    message = receive_message(notified_socket)

                    if message is False:
                        print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                        sockets_list.remove(notified_socket)

                        print(clients[notified_socket],player_socket["player2_socket"])
                    # 當關掉視窗的為玩家時改變player_name，並通知所有玩家消息
                        if clients[notified_socket] == player_socket["player1_socket"]:
                            
                            content["player1_name"] = ""
                            print("player1已退出",content)
                            server_boardcast(clients, content)
                        elif clients[notified_socket] == player_socket["player2_socket"]:
                            
                            content["player2_name"] = ""
                            print("player2已退出",content)
                            server_boardcast(clients, content)
                        del clients[notified_socket]
                        continue
        
                    # Get user by notified socket, so we will know who sent the message
                    user = clients[notified_socket]
        
                    print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                    
                    
                    if "player1:" in message["data"].decode("utf-8"):
                        player1_name = message["data"].decode("utf-8")[8:]
                        player_socket["player1_socket"] = user
                        content["player1_name"] = player1_name
                        server_boardcast(clients, content)
                        print("player1:{} 就緒".format(player1_name))
                    elif "player2:" in message["data"].decode("utf-8"):
                        player2_name = message["data"].decode("utf-8")[8:]
                        player_socket["player2_socket"] = user
                        content["player2_name"] = player2_name
                        server_boardcast(clients, content)
                        print("player2:{} 就緒".format(player2_name))
                    elif "board_state/player1/" in message["data"].decode("utf-8"):
                        board_state = message["data"].decode("utf-8")[20:]
                        content["board_state"] = board_state
                        content["whos_turn"] = "player2"
                        
                        if judge_is_over(board_state, 2):
                            content["is_end"] = "end"
                            server_boardcast(clients, content)
                        else:
                            server_boardcast(clients, content)

                    elif "board_state/player2/" in message["data"].decode("utf-8"):
                        board_state = message["data"].decode("utf-8")[20:]
                        content["board_state"] = board_state
                        content["whos_turn"] = "player1"
                        server_boardcast(clients, content)
                        if judge_is_over(board_state, 1):
                            content["is_end"] = "end"
                            server_boardcast(clients, content)
                        else:
                            server_boardcast(clients, content)
                    
                    if content["is_end"] == "end":
                        player1_score = 0
                        player2_score = 0
                        player1_name = content["player1_name"]
                        player2_name = content["player2_name"]
                        for i in content["board_state"]:
                            if i == "1":
                                player1_score += 1
                            elif i == "2":
                                player2_score += 1

                        db.upload_record(player1_name, player2_name, player1_score, player2_score)
                        
                        # 初始化
                        player_socket = {"player1_socket" : "", "player2_socket" : ""}
                        board_state = "000000000000001200002100000000000000"
                        content = {"player1_name" : "", "player2_name" : "", "whos_turn" : "player1", "board_state" : board_state, "is_end" : "not_end"}
                        server_boardcast(clients, content)
                                

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
 
    except:
        return False

    




def main():
    s = server()
    s.create_server()
main()
    
