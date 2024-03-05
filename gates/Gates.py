import pygame
from gates.Ports import Port
from utils.popup import Popup
from utils.colors import COLORS

class Gate:
    def __init__(self,x,y,screen,images,type) -> None:
        self.x = x
        self.y = y
        self.images = images
        self.type = type
        self.img = images[type]
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.output = Port(x+self.width, y+(self.height/2),self,"output")
        self.input = [Port(x,y+(self.height/4),self),Port(x,y+(3*self.height/4),self)] if type!= "NOT" else [Port(x,y+(self.height/2),self)]
        self.screen = screen
        
    def draw(self,wires=True):
        self.screen.blit(self.img,(self.x,self.y))
        color = COLORS["FALSE"] if self.output.value else COLORS["TRUE"]
        if wires:
            for _port in self.get_ports():
                for port in  _port.connected_to:
                    pygame.draw.line(self.screen,color,(port.x,port.y),(_port.x,_port.y),5)
        pygame.draw.circle(self.screen,COLORS["OUTPUT"],(self.output.x,self.output.y),5)
        if self.type != "NOT":
            pygame.draw.circle(self.screen,COLORS["INPUT"],(self.x,self.y+(3*self.height/4)),5)
            pygame.draw.circle(self.screen,COLORS["INPUT"],(self.x,self.y+(self.height/4)),5)
        else:
            pygame.draw.circle(self.screen,COLORS["INPUT"],(self.x,self.y+(self.height/2)),5)
        
    def move(self,x,y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
        self.output.set_pos(self.x+self.width, self.y+(self.height/2))
        if self.type != "NOT":
            self.input[0].set_pos(self.x,self.y+(self.height/4))
            self.input[1].set_pos(self.x,self.y+(3*self.height/4))
        else:
            self.input[0].set_pos(self.x,self.y+(self.height/2))
    
    def calculate(self,update=False):
        if update:
            for input in self.input:
                input.value = input.connected_from.value if input.connected_from else 0
        match self.type:
            case "AND":
                self.output.value = self.input[0].value and self.input[1].value
            case "OR":
                self.output.value = self.input[0].value or self.input[1].value
            case "NOT":
                self.output.value = not self.input[0].value
            case "NAND":
                self.output.value = not (self.input[0].value and self.input[1].value)
            case "NOR":
                self.output.value = not (self.input[0].value or self.input[1].value)
            case "XOR":
                self.output.value = self.input[0].value ^ self.input[1].value
            case "XNOR":
                self.output.value = not(self.input[0].value ^ self.input[1].value)
    
    def remove(self):
        for port in self.get_ports():
            if port.connected_from:
                port.connected_from.connected_to.remove(port)
            for p in port.connected_to:
                p.connected_from = None
            port.connected_to = []
            port.connected_from = None
        return "remove"
        
    def get_ports(self):
        ports = [self.output]
        ports.extend(self.input)
        return ports
    
    def convert(self,type):
        if self.type != type:
            self.img = self.images[type]
            if self.type == "NOT" or type == "NOT":
                for input in self.input:
                    input.connected_from.connected_to.remove(input) if input.connected_from else ""
                    input.connected_from = None
            if type == "NOT":
                self.input = [Port(self.x,self.y+(self.height/2),self)]
            elif self.type == "NOT":
                self.input = [Port(self.x,self.y+(self.height/4),self),Port(self.x,self.y+(3*self.height/4),self)]
            self.type = type
        return "remove"
        
    
    def mouse_hovered(self):
        x,y = pygame.mouse.get_pos()
        return x>self.x and x<self.x+self.width and y>self.y and y<self.y+self.height

    def mouse_in_bound(self,x,y,obj):
        return (x>obj.width/2 and x<self.screen.get_width()-(obj.width/2) and y>obj.height/2+50 and y<self.screen.get_height()-(obj.height/2))
    
    def event_handler(self,event,selected_gate,selected_port,gate_to_remove,popup):
        x,y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            l,_,r = pygame.mouse.get_pressed()
            for port in self.get_ports():
                if port.mouse_hovered():
                    if l:
                        selected_port = port
                    if r:
                        if port.type == "output":
                            for _port in port.connected_to:
                                _port.connected_from = None
                            port.connected_to = []
                        else:
                            if port.connected_from:
                                port.connected_from.connected_to.remove(port)
                            port.connected_from = None
                        
            if not selected_port and self.mouse_hovered():
                if l:
                    selected_gate = self
                if r:
                    popup = Popup(x,y,self.screen,[("Delete",lambda:self),("Convert_To",lambda: Popup(x,y,self.screen,[("AND",lambda : self.convert("AND")),("OR",lambda : self.convert("OR")),("NOT",lambda : self.convert("NOT")),("NAND",lambda : self.convert("NAND")),("NOR",lambda : self.convert("NOR")),("XOR",lambda : self.convert("XOR")),("XNOR",lambda : self.convert("XNOR"))])),("Remove_All_Connection",lambda:self.remove())])
                
        if event.type == pygame.MOUSEBUTTONUP:
            if selected_port:
                if self!=selected_port.gate:
                    for port in self.get_ports():
                        if port.mouse_hovered():
                            port.connect(selected_port)
        
        if event.type == pygame.MOUSEMOTION:
            if selected_gate and self.mouse_in_bound(x,y,selected_gate):
                selected_gate.move(x,y)
                
        return selected_gate,selected_port,gate_to_remove,popup