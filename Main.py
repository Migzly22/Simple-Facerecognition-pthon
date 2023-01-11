import os
import cv2
import numpy as np
import tkinter as tk
import customtkinter as ct
from PIL import Image, ImageTk
import face_recognition as fr


BASE_DIR= os.path.dirname(os.path.abspath(__file__))
path = BASE_DIR + '\ImageList'



#Set the initial themes of the app window 
ct.set_appearance_mode("Dark")
#ct.set_default_color_theme(BASE_DIR + "\\themes.json")


class App(ct.CTk):
    WIDTH =730
    HEIGHT = 680

    def __init__(self): 
        super().__init__()


        self.listlist()


        self.title("ALT F4") 
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable (width=False, height=False)
        
        """UPPER PART OF THE GUI"""
        self.frametop = ct.CTkFrame(master= self, height=(App.HEIGHT*.8)-60, width=(App.WIDTH)-60, corner_radius=0) 
        self.frametop.grid(row=0, column=0, padx = 30, pady=20, sticky="nswe")

        self.frame = np.random.randint(0,255, [100, 100, 3], dtype='uint8') 
        self.frame_img = ImageTk.PhotoImage(Image.fromarray(self.frame))


        self.img_holder = ct.CTkLabel(master = self.frametop, text="", bg_color="gray", font=("Roboto Medium", -14), width=640, height = 480) # text_font=("Roboto Medium", -14)
        self.img_holder.grid(row=0, column=0,  pady=15, padx=15)



        """BOTTOM PART OF THE GUI"""
        self.framebot = ct.CTkFrame(master= self, height=(App.HEIGHT*.2)-30, width=(App.WIDTH)-60, corner_radius=50) 
        self.framebot.grid(row=1, column=0, padx = 30, sticky="nswe")

        self.cmd_capture = ct.CTkButton(master=self.framebot , text="📸", font=("Roboto Medium", 40), corner_radius= 100 , command=self.saveimg_prompt) #, command=self.saveimg_prompt
        self.cmd_capture.place(bordermode=tk.INSIDE, relx=0.48, rely=0.5, anchor = tk.CENTER, width=80, height=80) 

        
        self.cam_active = False
        self.cancel = False

        self.specialcase()
        self.open_camera()
 

#this part is for the button logics saving and retaking image
    def listlist(self):
        self.images = []
        self.classNames = []
        myList = os.listdir(path)

        for cls in myList:
            curlmg = cv2.imread(f'{path}/{cls}')
            self.images.append(curlmg)
            self.classNames.append(os.path.splitext(cls)[0])

        print(self.classNames)
        


    def saveimg_prompt(self):
        self.cancel = True
        self.cmd_capture.place_forget()

        self.save = ct.CTkButton(master=self.framebot , text="💾", font=("Roboto Medium", 40), corner_radius= 100 , command=self.savingimg) #, command=self.saveimg_prompt
        self.save.place(bordermode=tk.INSIDE, relx=0.2, rely=0.5, anchor = tk.CENTER, width=80, height=80) 

        self.titlepart = ct.CTkEntry(master=self.framebot, font = ("Roboto Medium", 15), placeholder_text="Filename")
        self.titlepart.place(anchor=tk.CENTER, relx=0.5, rely=0.5, width=210, height=30) 

        self.tryagain = ct.CTkButton(master=self.framebot , text="↻", font=("Roboto Medium", 40), corner_radius= 100 , command=self.retake) #, command=self.saveimg_prompt
        self.tryagain.place(bordermode=tk.INSIDE, relx=0.8, rely=0.5, anchor = tk.CENTER, width=80, height=80) 

    
    def retake(self):
        self.cancel = False
        self.save.place_forget()
        self.tryagain.place_forget()
        self.titlepart.place_forget()

        self.cmd_capture.place(bordermode=tk.INSIDE, relx=0.48, rely=0.5, anchor = tk.CENTER, width=80, height=80) 
        self.img_holder.after (10, self.show_frame)

    def savingimg(self):
        global prevImg
        filetitle = self.titlepart.get()

        if(len(filetitle) != 0):
            if not(filetitle in self.classNames):

                # Resize image before saving

                filepath = path + f"\{filetitle}.png"
                

                basewidth = 600
                wpercent = (basewidth/float (prevImg.size[0]))
                hsize = int((float (prevImg.size[1])*float (wpercent)))
                prevImg = prevImg.resize((basewidth,hsize), Image.Resampling.LANCZOS)
                prevImg.save(filepath)

                self.listlist()
                self.specialcase()

                self.create_toplevel2("Image saved successfully")
                #tk.messagebox.showinfo(title="Success", message= f"File save at {path}\{filetitle}.png")
                self.retake()
            else:
                self.create_toplevel("Filename Already Exist")
                #tk.messagebox.showerror(title="Error Message", message="Filename Already Exist")
        else:
            self.create_toplevel("Please Enter Filename First")
            #tk.messagebox.showerror(title="Error Message", message="Please A Filename First")

    def create_toplevel(self,msg):
        window = ct.CTkToplevel(self)
        window.geometry("400x200")
        window.title("Error Message")

        # create label on CTkToplevel window
        icon = ct.CTkLabel(window,
                               text = "X",
                               width=50,
                               height=50,
                               font=("Roboto Medium", -20),
                               fg_color=("red", "red"),
                               text_color="white",
                               corner_radius=100)
        icon.place(relx=0.2, rely=0.4, anchor=tk.CENTER)

        label = ct.CTkLabel(window, text=msg, text_color="gray", font=("Roboto Medium", -20)) # text_font=("Roboto Medium", -14)
        label.place(bordermode=tk.INSIDE, relx=0.6, rely=0.4, anchor = tk.CENTER) 
        
        button = ct.CTkButton(window,
                                 width=100,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Exit",
                                 command=window.destroy)
        button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def create_toplevel2(self,msg):
        window = ct.CTkToplevel(self)
        window.geometry("400x200")
        window.title("Message")

        # create label on CTkToplevel window
        icon = ct.CTkLabel(window,
                               text = "✓",
                               width=50,
                               height=50,
                               font=("Roboto Medium", -20),
                               fg_color=("green", "green"),
                               text_color="white",
                               corner_radius=100)
        icon.place(relx=0.2, rely=0.4, anchor=tk.CENTER)

        label = ct.CTkLabel(window, text=msg, text_color="gray", font=("Roboto Medium", -20)) # text_font=("Roboto Medium", -14)
        label.place(bordermode=tk.INSIDE, relx=0.6, rely=0.4, anchor = tk.CENTER) 
        
        button = ct.CTkButton(window,
                                 width=100,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="Exit",
                                 command=window.destroy)
        button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

#This part is for the OpenCV (I hate it even though ive passed this part my brain still doesnt understand how it works. I guess TRIAL AND ERROR is more useful than searching something and doesnt even understand a single thing)

    def open_camera(self):
        # Open camera feed for capturing image 
        if self.cam_active == False:
            global prevImg
            self.cam_active = True
            self.cam_index = self.load_cam_index()
            print("Using camera feed to take pictures.")

            self.start_resize_cam()
            #success, frame = self.cap.read()
            #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)


            
            _, frame = self.cap.read()
            #cv2image = cv2.resize(frame,(0,0), None, 0.25, 0.25)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

            # Assign camera feed/frames to an image holder 
            prevImg = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=prevImg) 
            #self.img_holder.imgtk = imgtk 

            #additional my version



            self.img_holder.configure(image=imgtk)
            #self.cmd_capture.focus()
            

            if not self.cancel:
                self.img_holder.after(10, self.show_frame)

        else:
            print("Using camera feed to take pictures.")

    def load_cam_index(self):
        # Create and access file containing list of previously used camera 
        self.cam_list = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
        try:
            f = open(self.cam_list, 'r')
            return int(f.readline())
        except:
            return 0

    def start_resize_cam(self):
        # Start capturing and resizing camera resolution
        self.cap = cv2.VideoCapture(self.cam_index)
        #self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        #self.cap.set(cv2.CAP_PROP_FPS, 25)

    def show_frame(self):
        # Continously update image being loaded to a label 
        global prevImg

        _, img = self.cap.read()

        imgs = cv2.resize(img,(0,0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
        faceCurFrame = fr.face_locations(imgs)
        encodeCurFrame = fr.face_encodings(imgs, faceCurFrame)
        bool = False

        
        for  encodeFace, faceLoc in zip (encodeCurFrame, faceCurFrame):
            matches = fr.compare_faces(self.encodeListKnown, encodeFace)
            faceDis = fr.face_distance(self.encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

           
            if matches[matchIndex]:
                name = self.classNames[matchIndex].upper()
                print(name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1 *4, x2*4, y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                imgcreate = cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX, 0.65,(255,0,0),2)
                bool = True



        if (bool):
            prevImg = Image.fromarray(imgcreate)
            imgtk = ImageTk.PhotoImage(image=prevImg)
            bool = False
        else:
            imgs = cv2.resize(img,(640,480), None, 0.25, 0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGBA)
            prevImg = Image.fromarray(imgs)
            imgtk = ImageTk.PhotoImage(image=prevImg)

        self.img_holder.imgtk = imgtk
        self.img_holder.configure(image=imgtk)


        if not self.cancel:
            self.img_holder.after (10, self.show_frame)

    def specialcase(self):
        self.encodeListKnown = self.findEncodings()
        print('Encoding Complete')

    def findEncodings(self):
        encodeList =[]
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            encodeList.append(encode)
        
        return encodeList





if __name__ == "__main__": 
    app = App()
    app.mainloop()

