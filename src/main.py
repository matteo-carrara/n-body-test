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
    while not pygame_terminate:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame_terminate = True



        screen.fill(BLACK)

        for elem in b:
            elem.draw()

        pygame.display.flip()

        clock.tick(60)


        
        try:
            item = control_queue.get(block=False)
            if(item == "paused"):
                new_calc = False
                print("Pausing")
            elif(item == "resume"):
                new_calc = True
                print("Resuming")
            # Process the item:
        except queue.Empty:
            # Handle the case where the queue is empty (optional)
            pass
        
        if(new_calc):
            calc_forces(b)
            tmp = univ_collision(b, tmp)


    pygame.quit()


mainloop()