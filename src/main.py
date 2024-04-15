from globals import *
from body import *
from func import *
from settings import *
from shared_list import *



def mainloop():
    clock = pygame.time.Clock()
    

    
    
    def pygame_termination_handler(sig, frame):
        global tk_terminate, pygame_terminate
        tk_terminate.set()  # Assuming you have a threading.Event object
        pygame_terminate = True  # Flag for the Pygame thread
        print("Setting tk_terminate", tk_terminate.is_set())
        
    signal.signal(signal.SIGINT, pygame_termination_handler)


    global b
    shared_list = SharedList()
    b = create_bodies(BODIES_GEN)
    
    for i in range(len(b)):
        b[i].clear_trajectory()
        shared_list.add(b[i])

    ct = threading.Thread(target=control_thread, args=(shared_list,))
    ct.start()

    running = True
    i = 0
    tmp = []

    masses = [x.mass for x in b]
    new_calc = True

    if(not GRAVITY_ENABLED):
        print("Warning gravity not enabled")
        
    global pygame_terminate
    is_button_held = False
    elem_clicked = False
    elem_idx = -1
    mouse_data = []
    moving_space = False
    start_moving_space = (0,0)
    total_xy_off = (0,0)
    
    while not pygame_terminate:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame_terminate = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_button_held = False
                #print("Released")
                
                if(moving_space):
                    moving_space = False
                    #print("Started moving at", start_moving_space)
                    
                    now = pygame.mouse.get_pos()
                    #print("End at", now)
                    
                    total_xy_off = (total_xy_off[0]-(start_moving_space[0]-now[0]), total_xy_off[1]-(start_moving_space[1]-now[1]))
                    #print("Offset", total_xy_off)
                
                if(elem_clicked):
                    elem_clicked = False
                    shared_list.get(elem_idx).vx = 0
                    shared_list.get(elem_idx).vy = 0
                    
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_data.append({'x': mouse_x, 'y': mouse_y, 'timestamp': time.time()})
                    
                    acc = [k * 1 for k in get_drag_acceleration(mouse_data, 3000)]
                    
                    shared_list.get(elem_idx).accel(acc[0]*TIMESTEP, acc[1]*TIMESTEP)
                    
                    shared_list.get(elem_idx).clear_trajectory()
                
                    
                mouse_data = []
                control_queue.put("resume")
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_button_held = True
                
                control_queue.put("paused")
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("Clicked", mouse_x, mouse_y)
                print("Adjusted click", mouse_x-total_xy_off[0], mouse_y-total_xy_off[1])
                
                for i in range(shared_list.size()):
                    test = is_click_in_circle(mouse_x-total_xy_off[0], mouse_y-total_xy_off[1], shared_list.get(i).x, shared_list.get(i).y, shared_list.get(i).radius)
                    #print("Elem ",i,"clicked?", test)
                    if(test):
                        elem_clicked = True
                        elem_idx = i
                
                print("Elem clicked = ", elem_clicked)        
                if (not elem_clicked):
                    moving_space = True
                    start_moving_space = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEMOTION and is_button_held:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_data.append({'x': mouse_x, 'y': mouse_y, 'timestamp': time.time()})
                
                if(elem_clicked):
                    #print("Dragging", elem_idx)
                    shared_list.get(elem_idx).x = mouse_x-total_xy_off[0]
                    shared_list.get(elem_idx).y =  mouse_y-total_xy_off[1]
                    pass
                else:
                   # print("Draggin nothing")
                   pass
                


        screen.fill(BLACK)

        for elem in b:
            elem.draw(total_xy_off)

        pygame.display.flip()

        clock.tick(60)


        
        try:
            item = control_queue.get(block=False)
            if(item == "paused"):
                new_calc = False
                #print("Pausing")
            elif(item == "resume"):
                new_calc = True
                #print("Resuming")
            # Process the item:
        except queue.Empty:
            # Handle the case where the queue is empty (optional)
            pass
        
        if(new_calc):
            calc_forces(b)
            tmp = univ_collision(b, tmp)


    pygame.quit()


mainloop()