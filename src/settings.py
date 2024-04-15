from globals import *




def control_thread(shared_list):
    global b
    print("Got shared list", shared_list.size())
    for i in range(shared_list.size()):
        print(shared_list.get(i))
    
    SIM_PAUSED = threading.Lock()
    
    control_window = tk.Tk()
    control_window.title("Pygame Controls")
    tk_width=600
    control_window.geometry(str(tk_width)+"x400")
    
    
    my_label = tk.Label(control_window)
    my_label.grid(row=2+shared_list.size(), column=1)

    def set_label_running():
        my_label.config(text="PAUSE TO CHANGE VALUES", bg="yellow", font=("normal",))
    
    set_label_running()
        
    
    
    def pause_sim():
        if not SIM_PAUSED.acquire(blocking=False):
            #print("Lock is currently busy, skipping acquisition")
            pass
        
        control_queue.put("paused")
        my_label.config(text="SIM PAUSED", bg="red", font=("bold",))
        #print("Paused = ", SIM_PAUSED)
        

    def resume_sim():
        try:
            SIM_PAUSED.release()
        except RuntimeError:
            #print("Already unlocked")
            pass
        control_queue.put("resume")
        set_label_running()
        #print("Paused = ", SIM_PAUSED)
        

    
    button1 = tk.Button(control_window, text="||", width=5, height=2, font=("Arial", 16), bg="blue", fg="white", command=pause_sim)
    button1.grid(row=0, column=1)  # Place the button at row 0, column 1
    
    button2 = tk.Button(control_window, text=">", width=5, height=2, font=("Arial", 16), bg="blue", fg="white", command=resume_sim)
    button2.grid(row=0, column=2)  # Place the button at row 0, column 1

    entries = []
    
    def univ_modified(row, col):
        newdata = entries[row][col].get()
        print("Modified", row, col, newdata)
        
        if(col == 0):
            shared_list.get(row-1).x = float(newdata)
            shared_list.get(row-1).clear_trajectory()
        elif(col == 1):
            shared_list.get(row-1).y = float(newdata)
            shared_list.get(row-1).clear_trajectory()
        elif(col == 2):
            shared_list.get(row-1).vx = float(newdata)
        elif(col == 3):
            shared_list.get(row-1).vy = float(newdata)
        elif(col == 4):
            shared_list.get(row-1).mass = float(newdata)
        elif(col == 5):
            shared_list.get(row-1).radius = float(newdata)
        else:
            print("BUGED VALUE")
            return
        
        
        

    data = ["X", "Y", "vx", "vy", "m", "rad"]
    
    
    rows = BODIES_GEN+1
    cols = len(data)
    print("cols", cols)
    ideal_cell_width = ((tk_width + 100) // cols) // 10
    print(ideal_cell_width)
    
    
    for i in range(rows):
        tmp = []
        
        for j in range(cols):
            entry = tk.Entry(control_window, width=ideal_cell_width)
            entry.grid(row=i+1, column=j)
            entry.config(state="normal")
            entry.insert(0, "")
            tmp.append(entry)
            # Bind function to update data on edit
            if(i>0):
                entry.bind("<Return>", lambda event, row=i, col=j: univ_modified(row, col))
        
        entries.append(tmp)
            
    
    
    for i in range(cols):
        entries[0][i].insert(0, data[i])
        
    # Function to update cell value
    def update_cell(row, col, value):
        entries[row][col].delete(0, tk.END)
        entries[row][col].insert(0, value)
        
    def update_table():
        global b
        #print("update table", b)
        #print("Paused = ", SIM_PAUSED)
        
        row = 1

        for i in range(shared_list.size()):
            body = shared_list.get(i)
            tmp = [round(body.x, 0), round(body.y,0), round(body.vx,1), round(body.vy,1), "{:.1e}".format(body.mass), round(body.radius, 1)]
            for col in range(len(tmp)):
                update_cell(row, col, tmp[col])
            row +=1

    while not tk_terminate.is_set():
        tk_terminate.wait(timeout=0.0)
        
        

        if not SIM_PAUSED.acquire(blocking=False):
            #print("Lock is currently busy, skipping acquisition")
            pass
        else:
            #print("Lock acquired, updating table")
            update_table()
            SIM_PAUSED.release()
            #print("Lock released table updated")

    
        
        
        

        control_window.update()
    

    control_window.destroy()

    

    control_window.mainloop()


