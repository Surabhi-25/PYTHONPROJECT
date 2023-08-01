import threading
import random
import time
import tkinter as tk

class TypeSpeedGUI:

    def __init__(self): #constructor of class
        self.root=tk.Tk()
        self.root.title("How fast do you think you type?")
        self.root.geometry("800x600") #window

        self.texts=open("texts.txt", "r").read().split("\n")

        self.frame=tk.Frame(self.root)


        self.sample_label=tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 24))
         #use self.frame later
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry=tk.Entry(self.frame,width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1,column=0, columnspan=2, padx=5, pady=10 )
        self.input_entry.bind("<KeyPress>", self.start)



        self.speed_label=tk.Label(self.frame, text="SPEED: \n 0.00 cps \n 0.00 cpm \n 0.00 wps \n 0.00 wpm", font=("Helvetica", 22))
        self.speed_label.grid(row=2,column=0, columnspan=2, padx=5, pady=10)


        self.reset_button=tk.Button(self.frame, text="Reset",font=("Helvetica", 24), command=self.reset)
        self.reset_button.grid(row=3,column=0, columnspan=2, padx=5, pady=10)


        # self.start_time = tk.time.time()  


        self.frame.pack(expand=True)
        #make the window expansive
        self.counter=0
       
        self.running=False
        #set counter to 0 and window state to NOT running as default
        self.seconds =0
        #set counter to 0 and window state to NOT running as default

        self.time_elapsed = tk.Label(self.frame,text="00:00",font=("Helvetica", 24)) 
        self.time_elapsed.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
    
        self.root.mainloop()
        


    def start(self, event):
        if not self.running: #if we havent started typing yet
            if not event.keycode in [16, 17, 18]: #if the key pressed is not alt, shift or control buttons
                self.running=True#change self.running to true
               
                t=threading.Thread(target=self.time_thread) # start counter thread--target specifies the function that will be executed in the new thread
                t.start()
                


        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
                 #if entered character is not equal to displayed text, display it in red
            self.input_entry.config(fg="red")   
        else:
            self.input_entry.config(fg="black") 


        if self.input_entry.get()==self.sample_label.cget('text')[:-1]:
            self.running=False
            self.root.after_cancel(timer_id)
            self.input_entry.config(fg="green")  
                 #if entered character is equal to displayed text, display it in green         



    def time_thread(self): 
         self.update_timer()
         while self.running:
            time.sleep(0.1)
            self.counter+=0.1 
            cps=len(self.input_entry.get())/self.counter 
                #characters per  seconds
            cpm=cps*60 
                #characters per minute
            wps=len(self.input_entry.get().split(" "))/self.counter
                 #words per seconds
            wpm=wps*60 
                #words per minute 
         
            self.speed_label.config(text=f"SPEED: \n{cps:.2f} CPS \n {cpm:.2f} CPM \n {wps:.2f} WPS \n {wpm:.2f} WPM\n ")
    

    def update_timer(self):
        self.seconds += 1
        time_str = f"{self.seconds // 60:02d}:{self.seconds % 60:02d}"
        self.time_elapsed.config(text=time_str)
        global timer_id
        timer_id = self.root.after(1000, self.update_timer)

    def reset(self):
        self.running=False
        self.counter=0
        self.seconds=0
        self.speed_label.config(text="SPEED: \n 0.00 cps \n 0.00 cpm \n 0.00 wps \n 0.00 wpm")
        self.time_elapsed.config(text="00:00")
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)    

    
    
         

TypeSpeedGUI() #creates an instance




