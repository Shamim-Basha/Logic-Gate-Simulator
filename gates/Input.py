import pygame
from gates.Ports import Port
from utils.popup import Popup
from utils.colors import COLORS

class Input:
    def __init__(self,x,y,screen) -> None:
        self.x = x
        self.y = y
        self.type = "switch" 
        self.screen = screen
        self.port = Port(x+20+30,y,self,"output")
        self.output = self.port
        self.color = COLORS["RED"]
        self.font = pygame.font.SysFont("arial",20,1)
        
        
    def draw(self):
        pygame.draw.rect(self.screen,COLORS["BLACK"],(self.x+16,self.y-2,30,4))
        for port in self.port.connected_to:
            pygame.draw.line(self.screen,self.color,(port.x,port.y),(self.port.x,self.port.y),5)
        pygame.draw.circle(self.screen,COLORS["OUTPUT"],(self.port.x,self.port.y),5)
        if self.type == "push":
            pygame.draw.circle(self.screen,self.color,(self.x,self.y),20)
            pygame.draw.circle(self.screen,COLORS["BLACK"],(self.x,self.y),20,4)
        else:
            pygame.draw.rect(self.screen,self.color,(self.x-16,self.y-16,36,36))
            pygame.draw.rect(self.screen,COLORS["BLACK"],(self.x-20,self.y-20,40,40),4)
        text = self.font.render(f"{str(int(self.port.value))}",1,COLORS["BLACK"])
        self.screen.blit(text,(self.x-(text.get_width()/2),self.y-(text.get_height()/2)))
        
    def move(self,x,y):
        self.x = x
        self.y= y
        self.port.x = x+50
        self.port.y = y

    def switch(self):
        x,y = pygame.mouse.get_pos()
        if (self.x-20<=x<=self.x+20 and self.y-20<=y<=self.y+20):
            self.port.value = not self.port.value
            self.color = COLORS["GREEN"] if self.port.value else COLORS["RED"]
    
    def convert(self):
        self.type = "push" if self.type == "switch" else "switch"
        if self.port.value:
            self.port.value = 0
            self.color = COLORS["RED"]
        return "remove"
    
    def remove(self):
        if self.port.connected_from:
            self.port.connected_from.connected_to.remove(self.port)
        for port in self.port.connected_to:
            port.connected_from = None
        self.port.connected_to = []
        self.port.connected_from = None
        return "remove"
    
    def mouse_in_bound(self,x,y,obj):
        return (x>12 and x<self.screen.get_width()-(25) and y>12/2+50 and y<self.screen.get_height()-(12))
    
    def mouse_hovered(self):
        x,y = pygame.mouse.get_pos()
        return self.x-25<=x<=self.x+50 and y>self.y-25<=y<=self.y+25
    
    def event_handler(self,event,selected_gate,selected_port,input_to_remove,popup):
        x,y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            l,_,r = pygame.mouse.get_pressed()
            if l and self.mouse_hovered():
                self.switch()
                
            if self.port.mouse_hovered():
                if l:
                    selected_port = self.port
                if r:
                    for port in self.port.connected_to:
                        port.connected_from = None
                    self.port.connected_to = []
                        
            if not selected_port and self.mouse_hovered():
                if l:
                    selected_gate = self
                if r:
                    popup = Popup(x,y,self.screen,[("Delete",lambda:self),("Change_Type",lambda: Popup(x,y,self.screen,[("Push" if self.type=="switch" else "Switch",lambda: self.convert())])),("Remove_All_Connection",lambda:self.remove())])
                
        if event.type == pygame.MOUSEBUTTONUP:
            if self.type == "push":
                self.switch()
            if selected_port:
                if self!=selected_port.gate:
                    if self.port.mouse_hovered():
                        self.port.connect(selected_port)
        
        if event.type == pygame.MOUSEMOTION:
            if selected_gate and self.mouse_in_bound(x,y,selected_gate):
                selected_gate.move(x,y)
                
        return selected_gate,selected_port,input_to_remove,popup
            
        