import pygame
from gates.Ports import Port
from utils.popup import Popup
from utils.colors import COLORS

class Output:
    def __init__(self,x,y,screen) -> None:
        self.x = x
        self.y = y
        self.screen = screen
        self.port = Port(x-20-30,y,self,"input")
        self.input = self.port
        self.color = COLORS["INPUT"]
        self.font = pygame.font.SysFont("arial",20,1)
        
        
    def draw(self):
        pygame.draw.rect(self.screen,COLORS["BLACK"],(self.x-16-30,self.y-2,30,4))
        for port in self.port.connected_to:
            pygame.draw.line(self.screen,"#0f0fff",(port.x,port.y),(port.connected_from.x,port.connected_from.y),5)
        pygame.draw.circle(self.screen,COLORS["INPUT"],(self.port.x,self.port.y),5)
        pygame.draw.circle(self.screen,self.color,(self.x,self.y),20)
        pygame.draw.circle(self.screen,COLORS["BLACK"],(self.x,self.y),20,4)
        text = self.font.render(f"{str(int(self.port.value))}",1,COLORS["BLACK"])
        self.screen.blit(text,(self.x-(text.get_width()/2),self.y-(text.get_height()/2)))
        
    def move(self,x,y):
        self.x = x
        self.y= y
        self.port.x = x-50
        self.port.y = y
    
    def calculate(self,update=False):
        self.port.value = self.port.connected_from.value if self.port.connected_from else 0
        self.color = COLORS["GREEN"] if self.port.value else COLORS["RED"]
    
    def remove(self):
        if self.port.connected_from:
            self.port.connected_from.connected_to.remove(self.port)
        for port in self.port.connected_to:
            port.connected_from = None
        self.port.connected_to = []
        self.port.connected_from = None
        return "remove"
    
    def mouse_in_bound(self,x,y,obj):
        return (x>50 and x<self.screen.get_width()-(25) and y>12/2+50 and y<self.screen.get_height()-(12))
    
    def mouse_hovered(self):
        x,y = pygame.mouse.get_pos()
        return self.x-55<=x<=self.x+25 and y>self.y-25<=y<=self.y+25
    
    def event_handler(self,event,selected_gate,selected_port,output_to_remove,popup):
        x,y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            l,_,r = pygame.mouse.get_pressed()
                
            if self.port.mouse_hovered():
                if l:
                    selected_port = self.port
                if r:
                    if self.port.connected_from:
                        self.port.connected_from.connected_to.remove(self.port)
                    self.port.connected_from = None
                        
            if not selected_port and self.mouse_hovered():
                if l:
                    selected_gate = self
                if r:
                    popup = Popup(x,y,self.screen,[("Delete",lambda:self),("N/A",lambda: Popup(x,y,self.screen,[("1",lambda:None),("2",lambda:None)])),("Remove_All_Connection",lambda:self.remove())])
                
        if event.type == pygame.MOUSEBUTTONUP:
            if selected_port:
                if self!=selected_port.gate:
                    if self.port.mouse_hovered():
                        self.port.connect(selected_port)
        
        if event.type == pygame.MOUSEMOTION:
            if selected_gate and self.mouse_in_bound(x,y,selected_gate):
                selected_gate.move(x,y)
                
        return selected_gate,selected_port,output_to_remove,popup
            
        