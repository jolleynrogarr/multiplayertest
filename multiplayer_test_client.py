#multiplayer test by jolley rogarr
# 21 july 2025
import pygame, socket, threading, json

pygame.init()

#PREHISTORY VARIABLES

black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode((800,800))

local_username = input("Enter username")
username = local_username

pygame.display.set_caption(f"MULTIPLAYER TEST {username}")

font = pygame.font.SysFont("arial", 20)
text = font.render(username, True, white)

square_x = 30
square_y = 30
text_x = 30
text_y = 10

#SERVER
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5555))

def send_position():
    while True:
        data = {
            "username": username,
            "x": square_x,
            "y": square_y
            }
        try:
            client.send(json.dumps(data).encode())
        except:
            break
        pygame.time.wait(50)

threading.Thread(target=send_position, daemon=True).start()

other_players = {}
username = None

def receive_data():
    while True:
        try:
            data = client.recv(4096).decode()
            players = json.loads(data)
            
            for p in players:
                if local_username != username:
                    other_players[p["username"]] = (p["x"], p["y"])
        except:
            break
        
threading.Thread(target=receive_data, daemon=True).start()

#LOOP
running = True
while running:
    
    screen.fill(black)
    
    for event in pygame.event.get():
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            square_x -= 10
            text_x -= 10
        if keys[pygame.K_d]:
            square_x += 10
            text_x += 10
        if keys[pygame.K_w]:
            square_y -= 10
            text_y -= 10
        if keys[pygame.K_s]:
            square_y += 10
            text_y += 10
        
        if event.type == pygame.QUIT:
            running = False
            
    for name,pos in other_players.items():
        pygame.draw.rect(screen, (255, 255, 255), (*pos, 100, 100))
        if local_username != username:
            text = font.render(name, True, (255,255,255))
            screen.blit(text, (pos[0], pos[1] - 20))
        
    screen.blit(text, (text_x, text_y))
    pygame.display.update()
            
pygame.quit()