import socket
import pygame

###Start of simple configuration values
#------------------------------
ud_scale = 0.5 #up down strength scale
fb_scale = 0.7 #forward backward strength scale
lr_scale = 0.5 #left right strength scale

flip_up_down = False
flip_forward_backward = False
flip_left_right = False

left_right_deadband = .05


###End of simple configuration values
#------------------------------






#Initialize controller
pygame.init()
pygame.joystick.init()


joystick = pygame.joystick.Joystick(0)
joystick.init()

#Connect Wifi Socket
server_ip = '192.168.4.1'
server_port = 80
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))
print('connected')

running = True



while running:
    #receive joystick data
    left_stick_x = joystick.get_axis(0)
    left_stick_y = joystick.get_axis(1)
    
    right_stick_x = joystick.get_axis(3)
    right_stick_y = joystick.get_axis(4)

    #if the joystick is near center, set the value to 0
    if abs(right_stick_x) < left_right_deadband:
      right_stick_x = 0.0
      
    updowncommand = round((left_stick_y*ud_scale)*(flip_up_down*(-1)), 2)
    forwardcommand = round((right_stick_y*fb_scale * 0.5)*(flip_forward_backward*(-1)), 2)
    leftcommand = round((-right_stick_x*lr_scale * 0.5)*(flip_left_right*(-1)), 2)
    rightcommand = round((right_stick_x*lr_scale * 0.5)*(flip_left_right*(-1)), 2)  

    #command structure
    #Left,Up/Down,Right*
    #"77,80,72*"
    
    command_string = f"A{forwardcommand+leftcommand},{updowncommand},{forwardcommand+rightcommand}*"

    client_socket.send(command_string.encode('utf-8'))

    datachar = ''
    message = ''
    
    while datachar != '!':
      message += datachar 
      datachar = client_socket.recv(1).decode('utf-8')
    #print(message)
    pygame.event.pump()

    pygame.time.delay(10)
    
    buttons = joystick.get_numbuttons()
    
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1:
                print("B button pressed, exiting...")
                pygame.quit()
                running = False
                client_socket.send('E'.encode('utf-8'))

# Close socket and terminate the program
client_socket.close()
print('Program Terminated')
