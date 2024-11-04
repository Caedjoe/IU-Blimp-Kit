import socket
import pygame

pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

server_ip = '192.168.4.1'
server_port = 80


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((server_ip, server_port))
print('connected')

running = True

ud_scale = 0.5
fb_scale = 0.5
lr_scale = 0.4

while running:
    left_stick_x = joystick.get_axis(0)
    left_stick_y = joystick.get_axis(1)
    
    right_stick_x = joystick.get_axis(3)
    right_stick_y = joystick.get_axis(4)
    if abs(right_stick_x) < .05:
      right_stick_x = 0.0
      
    updowncommand = round(left_stick_y*ud_scale, 2)
    forwardcommand = round(right_stick_y*fb_scale * 0.5, 2)
    leftcommand = round(-right_stick_x*lr_scale * 0.5, 2)
    rightcommand = round(right_stick_x*lr_scale * 0.5, 2)  

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
    print(message)
    pygame.event.pump()

    pygame.time.delay(25)
    
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
