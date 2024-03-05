import pygame

class Port:
    def __init__(self,x,y,gate,type="input") -> None:
        self.x = x
        self.y = y
        self.type = type
        self.value = 0
        self.gate = gate
        self.connected_to = []
        self.connected_from = None
        
    def set_pos(self,x,y):
        self.x = x
        self.y = y
    
    def mouse_hovered(self):
        x,y = pygame.mouse.get_pos()
        return self.x-10<=x<=self.x+10 and self.y-10<=y<=self.y+10
    
    def connect(self,port):
        if self.type != port.type:
            if self.type == "input":
                if self.connected_from:
                    self.connected_from.connected_to.remove(self)
                self.connected_from = port
                port.connected_to.append(self)
            elif self.type == "output":
                if port.connected_from:
                    port.connected_from.connected_to.remove(port)
                self.connected_to.append(port)
                port.connected_from = self
            return True
        return False