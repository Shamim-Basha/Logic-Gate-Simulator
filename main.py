import pygame
pygame.init()

from gates.Gates import Gate
from utils.navbar import Menu
from gates.Input import Input
from gates.Output import Output

from utils.colors import COLORS

#loading images
images = {
    "AND": pygame.image.load("./img/AND.svg"),
    "OR" : pygame.image.load("./img/OR.svg"),
    "NOT" : pygame.image.load("./img/NOT.svg"),
    "NAND" : pygame.image.load("./img/NAND.svg"),
    "NOR" : pygame.image.load("./img/NOR.svg"),
    "XOR" : pygame.image.load("./img/XOR.svg"),
    "XNOR" : pygame.image.load("./img/XNOR.svg"),
    "INPUT" : pygame.image.load("./img/input.png"),
    "OUTPUT" : pygame.transform.flip(pygame.image.load("./img/input.png"),1,0)
    }


#setting variables
pygame.display.set_caption("Logic Gate Simulator")
screen = pygame.display.set_mode((900,600),pygame.RESIZABLE)
gates_list = ["AND","OR","NOT","NAND","NOR","XOR","XNOR"]
font = pygame.font.SysFont("arial",10)
    
selected_gate = None
selected_input = None
selected_output = None
selected_port = None
selected = None
gate_to_remove = None
input_to_remove = None
output_to_remove = None
selected_menu = None
popup = None
to_remove = None
sub_popup = None
tooltip = None

menu = Menu(screen)
gates = [Gate(200,170,screen,images,"OR")]
inputs = [Input(100,120,screen),Input(100,220,screen)]
outputs = [Output(500,120,screen)]

inputs[0].port.connected_to.append(gates[0].input[0])
gates[0].input[0].connected_from = inputs[0].port
inputs[1].port.connected_to.append(gates[0].input[1])
gates[0].input[1].connected_from = inputs[1].port
gates[0].output.connected_to.append(outputs[0].port)
outputs[0].port.connected_from = gates[0].output

#loading images to menu
for key in images:
    menu.add_child(key,images[key])

def calculate_output():
    visited = {} #port :value
    def dfs(obj):
        if type(obj) == Input:
            return obj.port.value
        if obj in visited:
            return obj.output.value
        visited[obj] = 0
        for input in obj.input:
            if input in visited:
                input.value = visited[input]
            else:
                input.value = dfs(input.connected_from.gate) if input.connected_from else 0
                visited[input] = input.value
        obj.calculate()
        return obj.output.value
        
    for output in outputs:
        cur = output.port.connected_from if output.port.connected_from else None
        output.port.value = dfs(cur.gate) if cur else 0
        output.calculate()
    
    for input in inputs:
        for connection in input.port.connected_to:
            connection.value = input.port.value           
    for obj in gates+outputs:
        obj.calculate(update=True)

def draw_bg():
    screen.fill(COLORS["GREY"])
    text = font.render("by Shamim Basha @2024",1,COLORS["BLACK"])
    screen.blit(text,(screen.get_width()-text.get_width()-10,screen.get_height()-text.get_height()-20))

    
running = True
clock = pygame.time.Clock()
while running:            
    clock.tick(60)
    calculate_output()
    draw_bg()
    for obj in gates + inputs + outputs:
        obj.draw()
    for gate in gates:
        gate.draw(wires=False)
    menu.draw()
    if popup:
        popup.draw()
    if selected_menu:
        selected_menu.draw()
    if tooltip:
        tooltip.draw(screen)
    
    
    x,y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if not selected:
            selected,tooltip = menu.event_handler(event,selected,tooltip)
            if selected:
                if selected.title in gates_list:
                    gates.append(Gate(x,y,screen,images,selected.title))
                    selected_gate = gates[-1]
                elif selected.title == "INPUT":
                    inputs.append(Input(x,y,screen))
                    selected_input = inputs[-1]
                elif selected.title == "OUTPUT":
                    outputs.append(Output(x,y,screen))
                    selected_output = outputs[-1]
    
        for gate in gates:
            selected_gate,selected_port,gate_to_remove,popup = gate.event_handler(event,selected_gate,selected_port,gate_to_remove,popup)
            
        for input in inputs:
            selected_input,selected_port,input_to_remove,popup = input.event_handler(event,selected_input,selected_port,input_to_remove,popup)
        
        for output in outputs:
            selected_output,selected_port,output_to_remove,popup = output.event_handler(event,selected_output,selected_port,output_to_remove,popup)
        
        if popup:
            popup,to_remove,sub_popup = popup.event_handler(event,popup,to_remove,sub_popup)
            if to_remove=="remove" or type(to_remove) in [Gate,Input,Output]:
                popup = None
            if type(to_remove) == Gate:
                gate_to_remove = to_remove
            elif type(to_remove) == Input:
                input_to_remove = to_remove
            elif type(to_remove) == Output:
                output_to_remove = to_remove
            to_remove = None
        
            
        if event.type == pygame.MOUSEBUTTONUP:
            selected_gate ,selected_input ,selected_output ,selected_port ,selected = [None]*5
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    if sub_popup:
        popup = sub_popup
        sub_popup = None
                        
    if gate_to_remove:
        gate_to_remove.remove()
        gates.remove(gate_to_remove)
        gate_to_remove = None
    if input_to_remove:
        input_to_remove.remove()
        inputs.remove(input_to_remove)
        input_to_remove = None
    if output_to_remove:
        output_to_remove.remove()
        outputs.remove(output_to_remove)
        output_to_remove = None
        
    if selected_port:
        pygame.draw.line(screen,COLORS["RED"],(selected_port.x,selected_port.y),(x,y),5)    
            
    if selected_gate:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
    pygame.display.flip()
        
pygame.quit()