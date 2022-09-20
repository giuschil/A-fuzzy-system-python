import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import math
from  fuzzy import FuzzyInferenceSystem


glu_low_var, glu_med_var, glu_high_var = [56, 100, 125], [68.2, 117, 145], [109.9, 146, 198]
ins_low_var, ins_med_var, ins_high_var = [0, 55.11, 87.67], [63.63, 98.42, 191.6], [95.34, 188.3, 586]
bmi_low_var, bmi_med_var, bmi_high_var = [18, 22, 30.8], [31.07, 37.07, 45.01], [36.43, 44.43, 67]
dpf_low_var, dpf_med_var, dpf_high_var = [0.085, 0.5322, 1.132], [0.547, 1.03, 1.717], [1.09, 1.476, 2.4]
age_young_var, age_med_var, age_old_var = [18, 25, 30], [30, 45, 55], [55, 65, 75]
uri_low_var, uri_med_var, uri_high_var = [0.5, 50, 800], [500, 1300, 2000], [1500, 2500, 5000]
dm_vlow_var, dm_low_var, dm_med_var, dm_high_var, dm_vhigh_var = [0, 0.1, 0.2], [0.1524, 0.2524, 0.3], [0.287, 0.333, 0.3997], [0.355, 0.623, 0.762], [0.731, 0.831, 1]
filename = ""
suggestions = [
    "Medical practitioner justification is the person is Non-diabetic.",
    "You look normal.",
    "Medical practitioner justification is the person may be diabetic.",
    "Medical practitioner justification is the person is diabetic.",
    "Medical practitioner justification is the person is exactly diabetic."
]
fuzzy = FuzzyInferenceSystem(1)
class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Fuzzy Expert System") # set title of the window
 
        container = tk.Frame(self) # create the container contains all sub_windows
        container.pack(side="top", fill="both", expand=True) # pack it
        container.grid_rowconfigure(0, weight=1) # this is like 1x1 grid
        container.grid_columnconfigure(0, weight=1)
 
        self.frames = {} # store references to all sub_windows
 
        for Frame in (Fuzzy,Settings): # for each page class
            frame = Frame(container, self) # create page
            self.frames[Frame] = frame     # store into frames
            frame.grid(row=0, column=0, sticky='nsew') # pack it into container
        self.show_frame(Fuzzy) # set HomePage as default
 
        #create the menu bar
        menu_bar = tk.Menu(self)
        #create fuzzy menu
        fuzzy_menu = tk.Menu(menu_bar)
        fuzzy_menu.add_command(label='Fuzzy', compound='left', command=lambda : self.show_frame(Fuzzy))
        fuzzy_menu.add_separator()
        fuzzy_menu.add_command(label='Exit', compound='left', command=lambda : exit())
        menu_bar.add_cascade(label='Fuzzy', menu=fuzzy_menu)
        #create settings menu
        settings_menu = tk.Menu(menu_bar)
        settings_menu.add_command(label='Settings', compound='left', command=lambda : self.show_frame(Settings))
        menu_bar.add_cascade(label='Settings', menu=settings_menu)
        self.config(menu=menu_bar) # after you create it, you have to set it as menu_bar
        #create info menu 
        #info_menu = tk.Menu(menu_bar)
        #info_menu.add_command(label='Info', compound='left', command=lambda : self.show_frame(Informa))
        #menu_bar.add_cascade(label='Info', menu=info_menu)
        #self.config(menu=menu_bar) # after you create it, you have to set it as menu_bar
        
         
        def exit():
            if messagebox.askokcancel('Quit?', 'Really Quit?'):
                self.destroy()
            return 'break'
 
    def show_frame(self, Frame):
        frame = self.frames[Frame] # get the reference to page
        frame.tkraise() # raise it to the top

        
class Fuzzy(tk.Frame):
    def __init__(self, parent, controller):
        global glu_low_var, glu_med_var, glu_high_var
        global ins_low_var, ins_med_var, ins_high_var
        global bmi_low_var, bmi_med_var, bmi_high_var
        global dpf_low_var, dpf_med_var, dpf_high_var
        global age_young_var, age_med_var, age_old_var
        global uri_low_var, uri_med_var, uri_high_var
        global dm_vlow_var, dm_low_var, dm_med_var, dm_high_var, dm_vhigh_var
        global filename
 
        tk.Frame.__init__(self, parent)
        ###############################################
        input_frame = tk.LabelFrame(self, text="Input")
        input_frame.grid(row=0, column=0, sticky='wens', padx=10, pady=20)
        
        # Glucose INPUTs
        self.button_question_mark_1 = tk.Button(input_frame, text='?', command=lambda : glu_ask_handler())
        self.button_question_mark_1.grid(row=0, column=0, sticky='e', padx=(5,0), pady = (20, 0))
        tk.Label(input_frame, text='Glucose Level(mg/dl)').grid(row=0, column=1, sticky='e', padx=10, pady = (20, 0))
        self.glu_slider_var = tk.DoubleVar()
        self.glu_slider = tk.Scale(input_frame, variable=self.glu_slider_var, orient=tk.HORIZONTAL, from_=56, to=198, resolution=1, command=lambda e: glu_slider_handler())
        self.glu_slider.grid(row=1, column=0, columnspan=2, sticky=tk.W + tk.E, padx=(5,0), pady = (0, 0))
        self.glu_entry_var = tk.StringVar()
        self.glu_entry = tk.Entry(input_frame, width=12, textvariable=self.glu_entry_var)
        self.glu_entry.bind('<Key>', lambda e: glu_entry_handler())
        self.glu_entry.grid(row=1, column=2, sticky=tk.S, padx=(0,5), pady = (0, 0))
        
        # Insulin INPUTs
        self.button_question_mark_2 = tk.Button(input_frame, text='?', command=lambda : ins_ask_handler())
        self.button_question_mark_2.grid(row=2, column=0, sticky='e', padx=(5,0), pady = (20, 0))
        tk.Label(input_frame, text='Insulin Level (muU/ml)').grid(row=2, column=1, sticky='e', padx=10, pady = (20, 0))
        self.ins_slider_var = tk.DoubleVar()
        self.ins_slider = tk.Scale(input_frame, variable=self.ins_slider_var, orient=tk.HORIZONTAL, from_=0, to=586, resolution=1, command=lambda e: ins_slider_handler())
        self.ins_slider.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E, padx=(5,0), pady = (0, 0))
        self.ins_entry_var = tk.StringVar()
        self.ins_entry = tk.Entry(input_frame, width=12, textvariable=self.ins_entry_var)
        self.ins_entry.bind('<Key>', lambda e: ins_entry_handler())
        self.ins_entry.grid(row=3, column=2, sticky=tk.S, padx=(0,5), pady = (0, 0))        
                 
        
        # BMI INPUTs
        self.button_question_mark_3 = tk.Button(input_frame, text='?', command=lambda : bmi_ask_handler())
        self.button_question_mark_3.grid(row=4, column=0, sticky='e', padx=(5,0), pady = (20, 0))
        tk.Label(input_frame, text='Body Mass Index(kg/m^2)').grid(row=4, column=1, sticky='e', padx=10, pady = (20, 0))
        self.bmi_slider_var = tk.DoubleVar()
        self.bmi_slider = tk.Scale(input_frame, variable=self.bmi_slider_var, orient=tk.HORIZONTAL, from_=18, to=67, resolution=1, command=lambda e: bmi_slider_handler())
        self.bmi_slider.grid(row=5, column=0, columnspan=2, sticky=tk.W + tk.E, padx=(5,0), pady = (0, 0))
        self.bmi_entry_var = tk.StringVar()
        self.bmi_entry = tk.Entry(input_frame, width=12, textvariable=self.bmi_entry_var)
        self.bmi_entry.bind('<Key>', lambda e: bmi_entry_handler())
        self.bmi_entry.grid(row=5, column=2, sticky=tk.S, padx=(0,5), pady = (0, 0))
 
        # DPF INPUTs
        self.button_question_mark_4 = tk.Button(input_frame, text='?', command=lambda : dpf_ask_handler())
        self.button_question_mark_4.grid(row=6, column=0, sticky='e', padx=(5,0), pady = (20, 0))
        tk.Label(input_frame, text='DPF').grid(row=6, column=1, sticky='e', padx=10, pady = (20, 0))
        self.dpf_slider_var = tk.DoubleVar()
        self.dpf_slider = tk.Scale(input_frame, variable=self.dpf_slider_var, orient=tk.HORIZONTAL, from_=0.085, to=2.4, resolution=0.01, command=lambda e: dpf_slider_handler())
        self.dpf_slider.grid(row=7, column=0, columnspan=2, sticky=tk.W + tk.E, padx=(5,0), pady = (0, 0))
        self.dpf_entry_var = tk.StringVar()
        self.dpf_entry = tk.Entry(input_frame, width=12, textvariable=self.dpf_entry_var)
        self.dpf_entry.bind('<Key>', lambda e: dpf_entry_handler())
        self.dpf_entry.grid(row=7, column=2, sticky=tk.S, padx=(0,5), pady = (0, 0))
 
        # age INPUTs
        self.button_question_mark_5 = tk.Button(input_frame, text='?', command=lambda : age_ask_handler())
        self.button_question_mark_5.grid(row=8, column=0, sticky='e', padx=(5, 0), pady = (20, 0))
        tk.Label(input_frame, text='Age').grid(row=8, column=1, sticky='e', padx=10, pady = (20, 0))
        self.age_slider_var = tk.DoubleVar()
        self.age_slider = tk.Scale(input_frame, variable=self.age_slider_var, orient=tk.HORIZONTAL, from_=18, to=70,
                                  resolution=1, command=lambda e: age_slider_handler())
        self.age_slider.grid(row=9, column=0, columnspan=2, sticky=tk.W + tk.E, padx=(5,0), pady = (0, 0))
        self.age_entry_var = tk.StringVar()
        self.age_entry = tk.Entry(input_frame, width=12, textvariable=self.age_entry_var)
        self.age_entry.bind('<Key>', lambda e: age_entry_handler())
        self.age_entry.grid(row=9, column=2, sticky=tk.S, padx=(0,5), pady = (0, 0))
        
        # Urine INPUTs
        self.button_question_mark_6 = tk.Button(input_frame, text='?', command=lambda : uri_ask_handler())
        self.button_question_mark_6.grid(row=10, column=0, sticky='e', padx=(5, 0), pady = (20, 0))
        tk.Label(input_frame, text='Urine (ml/day)').grid(row=10, column=1, sticky='e', padx=10, pady = (20, 0))
        self.uri_slider_var = tk.DoubleVar()
        self.uri_slider = tk.Scale(input_frame, variable=self.uri_slider_var, orient=tk.HORIZONTAL, from_=0, to=5000,
                                       resolution=10, command=lambda e: uri_slider_handler())
        self.uri_slider.grid(row=11, column=0, columnspan=2, sticky=tk.W + tk.E, padx=(5,0), pady = (0, 0))
        self.uri_entry_var = tk.StringVar()
        self.uri_entry = tk.Entry(input_frame, width=12, textvariable=self.uri_entry_var)
        self.uri_entry.bind('<Key>', lambda e: uri_entry_handler())
        self.uri_entry.grid(row=11, column=2, sticky=tk.S, padx=(0,5), pady = (0, 0))        
 
        start_button = tk.Button(input_frame, text='Diagnose', command=lambda : start_handler())
        start_button.grid(row=12, column = 0, columnspan = 3,  sticky=tk.E+tk.W, padx=(40,40), pady = (20, 20))
        
        
        
        ##################################################
        output_frame = tk.LabelFrame(self, text="Output")
        output_frame.grid(row=0, column=1, sticky='news', padx=10, pady=20)
        tk.Label(output_frame, text='Diabete Mellitus Level:').grid(row=0, column=0, sticky='e', padx=(5,0), pady = (20, 0))
        self.dm_entry_var = tk.StringVar()
        self.dm_entry = tk.Entry(output_frame, textvariable=self.dm_entry_var)
        self.dm_entry.grid(row=0, column=1, sticky='w', pady = (20, 0))
        
        self.dmlevelabel = tk.Label(output_frame)
        self.dmlevelabel.grid(row = 1, column = 0, columnspan = 4, padx = (10, 10), pady = 6)
        
        
        tk.Label(output_frame, text='Graph for defuzzification:').grid(row=2, column=0, sticky='w', padx=(5,0), pady = (20, 0))
        temp = tk.Frame(output_frame, borderwidth=3, relief=tk.RAISED)
        temp.grid(row=3, column=0, columnspan=4, rowspan=2, padx=(5,5), pady = (0, 10))
        
        self.canvas = tk.Canvas(temp, width=830, height=500, bg='#ddddff')
        self.canvas.grid(row = 0, column = 0, columnspan = 4)   
        self.canvas.create_line(0, 480, 830, 480, width='2', fill='#666666')        # x->(20~820), y->(30~480)
        self.canvas.create_line(20, 0, 20, 500, width='2', fill='#666666')
        #grid for cordinate
        # Horizontal grids
        for i in range (1, 11):
            self.canvas.create_line(0, 480 - 45*i, 830, 480 - 45*i, width='1', fill='#cccccc')
            self.canvas.create_text(30, 470 - 45*i, text = str("%.1f" % (i/10)))
        # Vertical grids
        for i in range (1, 11):
            self.canvas.create_line(20 + 80*i, 0, 20 + 80*i, 500, width='1', fill='#cccccc')
            self.canvas.create_text(20 + 80*i, 490, text = str("%.1f" % (i/10)))
        self.canvas.create_text(800, 450, text = 'DM Level')
        self.canvas.create_text(100, 40, text = 'Degree of membership')
    
        
        tk.Label(output_frame, text='You should ask your doctor if DM level >= 0.6').grid(row=5, column=0, columnspan=2, sticky='ne', padx=5)
 
        
 
        ###############--Handlers--###############
        def glu_entry_handler(event=None):
            try:
                self.glu_slider_var.set(float(self.glu_entry_var.get()))
            except:
                pass
 
        def glu_slider_handler(event=None):
            self.glu_entry_var.set(str("%.2f" % (self.glu_slider_var.get())))
            
        def ins_entry_handler(event=None):
            try:
                self.ins_slider_var.set(float(self.ins_entry_var.get()))
            except:
                pass
 
        def ins_slider_handler(event=None):
            self.ins_entry_var.set(str("%.2f" % (self.ins_slider_var.get())))    
        
        def bmi_entry_handler(event=None):
            try:
                self.bmi_slider_var.set(float(self.bmi_entry_var.get()))
            except:
                pass
 
        def bmi_slider_handler(event=None):
            self.bmi_entry_var.set(str("%.2f" % (self.bmi_slider_var.get())))
        
        def dpf_entry_handler(event=None):
            try:
                self.dpf_slider_var.set(float(self.dpf_entry_var.get()))
            except:
                pass
 
        def dpf_slider_handler(event=None):
            self.dpf_entry_var.set(str("%.2f" % (self.dpf_slider_var.get())))        
        
 
        def age_entry_handler(event=None):
            try:
                self.age_slider_var.set(float(self.age_entry_var.get()))
            except:
                pass
 
        def age_slider_handler(event=None):
            self.age_entry_var.set(str("%.2f" % (self.age_slider_var.get())))
            
        def uri_entry_handler(event=None):
            try:
                self.uri_slider_var.set(float(self.uri_entry_var.get()))
            except:
                pass
 
        def uri_slider_handler(event=None):
            self.uri_entry_var.set(str("%.2f" % (self.uri_slider_var.get())))        
 
        def start_handler():
            global filename
            
            fuzzy.set_glu(glu_low_var, glu_med_var, glu_high_var)
            fuzzy.set_ins(ins_low_var, ins_med_var, ins_high_var)
            fuzzy.set_bmi(bmi_low_var, bmi_med_var, bmi_high_var)
            fuzzy.set_dpf(dpf_low_var, dpf_med_var, dpf_high_var)
            fuzzy.set_age(age_young_var, age_med_var, age_old_var)
            fuzzy.set_uri(uri_low_var, uri_med_var, uri_high_var)
            fuzzy.set_dm(dm_vlow_var, dm_low_var, dm_med_var, dm_high_var, dm_vhigh_var)
            fuzzy.make_rules(filename)
            output, x_axis, y_axis = fuzzy.mamdianiInference(self.glu_slider_var.get(), self.ins_slider_var.get(), self.bmi_slider_var.get(), self.dpf_slider_var.get(), self.age_slider_var.get(), self.uri_slider_var.get())
            
            result = ["Very Low", "Low", "Medium", "High", "Very High"]
            self.dm_entry_var.set(str("%.2f" % output))
            resString = "Possibility of suffering from diabetes for this person is "
            
            if 0 <= output < 0.2:
                self.dmlevelabel.config(text= resString + "Very Low")
            elif 0.2 <= output < 0.4:
                self.dmlevelabel.config(text= resString + "Low")
            elif 0.4 <= output < 0.6:
                self.dmlevelabel.config(text=resString + "Medium")
            elif 0.6 <= output < 0.8:
                self.dmlevelabel.config(text= resString + "High")
            else:
                self.dmlevelabel.config(text= resString + "Very High")
            self.canvas.delete("all")
            self.canvas.create_line(0, 480, 830, 480, width='1', fill='#888888')        # x->(20~820), y->(30~480)
            self.canvas.create_line(20, 0, 20, 500, width='1', fill='#888888')            
            #grid for cordinate
            # Horizontal grids
            for i in range (1, 11):
                self.canvas.create_line(0, 480 - 45*i, 830, 480 - 45*i, width='1', fill='#cccccc')
                self.canvas.create_text(30, 470 - 45*i, text = str("%.1f" % (i/10)))
            # Vertical grids
            for i in range (1, 11):
                self.canvas.create_line(20 + 80*i, 0, 20 + 80*i, 500, width='1', fill='#cccccc')
                self.canvas.create_text(20 + 80*i, 490, text = str("%.1f" % (i/10)))
            self.canvas.create_text(800, 450, text = 'DM Level')
            self.canvas.create_text(100, 40, text = 'Degree of membership')
            
            for i in range(1, len(x_axis)):         # x->(20~820), y->(30~480)
                self.canvas.create_line(800*x_axis[i - 1] + 20, 480 - 450*y_axis[i - 1], 800*x_axis[i] + 20, 480 - 450*y_axis[i], width='3', fill='blue')
            self.canvas.create_line(800*output + 20, 0, 800*output + 20, 480, width='2', fill='red')
            self.canvas.create_text(800*output + 50, 200, text = 'Centroid')
 
        def bmi_ask_handler():
            messagebox.showinfo("BMI", "Body mass index (BMI) is a measure of body fat based on height and weight that applies to adult men and women.\n" "kg/m^2")
        def dpf_ask_handler():
            messagebox.showinfo("DPF", "diabetes pedigree function")
 
        def age_ask_handler():
            messagebox.showinfo("age", "Age of user")
 
class Settings(tk.Frame):
    def __init__(self, parent, controller):
 
        tk.Frame.__init__(self, parent)
        ####################################### variable - member functions frame
        var_func_frame = tk.LabelFrame(self, text='Variables - Member Functions')
        var_func_frame.grid(row=0, column=0, padx = (15, 15), pady = 20)             
        
        # glucose member functions frame
        glu_memfunc_frame = tk.LabelFrame(var_func_frame, text='Glucose Level')
    
        tk.Label(glu_memfunc_frame, text='Low:').grid(row=0, column=0, sticky='e')
        self.glu_low_var = tk.StringVar()
        self.glu_low_var.set("[56, 100, 125]")
        glu_low_entry = tk.Entry(glu_memfunc_frame, textvariable=self.glu_low_var, width=10)
        glu_low_entry.grid(row=0, column=1, sticky='we')
        tk.Label(glu_memfunc_frame, text='Medium:').grid(row=1, column=0, sticky='e')
        self.glu_med_var = tk.StringVar()
        self.glu_med_var.set('[68.2, 117, 145]')
        glu_mod_entry = tk.Entry(glu_memfunc_frame, textvariable=self.glu_med_var, width=10)
        glu_mod_entry.grid(row=1,column=1)
        tk.Label(glu_memfunc_frame, text='High:').grid(row=2, column=0, sticky='e')
        self.glu_high_var = tk.StringVar()
        self.glu_high_var.set('[109.9, 146, 198]')
        glu_high_entry = tk.Entry(glu_memfunc_frame, textvariable=self.glu_high_var, width=10)
        glu_high_entry.grid(row=2, column=1)
        glu_memfunc_frame.grid(row=0, column=0, padx=5, pady=5)
        plot_glu_button = tk.Button(glu_memfunc_frame, text='Plot', command=lambda :plot_glu())
        plot_glu_button.grid(row=3, column=0, columnspan=2)   
        
        # ins member functions frame
        ins_memfunc_frame = tk.LabelFrame(var_func_frame, text='Insulin Index')
    
        tk.Label(ins_memfunc_frame, text='Low:').grid(row=0, column=0, sticky='e')
        self.ins_low_var = tk.StringVar()
        self.ins_low_var.set("[0, 55.11, 87.67]")
        ins_low_entry = tk.Entry(ins_memfunc_frame, textvariable=self.ins_low_var, width=10)
        ins_low_entry.grid(row=0, column=1, sticky='we')
        tk.Label(ins_memfunc_frame, text='Medium:').grid(row=1, column=0, sticky='e')
        self.ins_med_var = tk.StringVar()
        self.ins_med_var.set('[63.63, 98.42, 191.6]')
        ins_mod_entry = tk.Entry(ins_memfunc_frame, textvariable=self.ins_med_var, width=10)
        ins_mod_entry.grid(row=1,column=1)
        tk.Label(ins_memfunc_frame, text='High:').grid(row=2, column=0, sticky='e')
        self.ins_high_var = tk.StringVar()
        self.ins_high_var.set('[95.34, 188.3, 586]')
        ins_high_entry = tk.Entry(ins_memfunc_frame, textvariable=self.ins_high_var, width=10)
        ins_high_entry.grid(row=2, column=1)
        ins_memfunc_frame.grid(row=0, column=1, padx=5, pady=5)
        plot_ins_button = tk.Button(ins_memfunc_frame, text='Plot', command=lambda :plot_ins())
        plot_ins_button.grid(row=3, column=0, columnspan=2)        

        # bmi member functions frame
        bmi_memfunc_frame = tk.LabelFrame(var_func_frame, text='Body Mass Index' )        
        
        tk.Label(bmi_memfunc_frame, text='Low:').grid(row=0, column=0, sticky='e')
        self.bmi_low_var = tk.StringVar()
        self.bmi_low_var.set("[18, 22, 30.8]")
        bmi_low_entry = tk.Entry(bmi_memfunc_frame, textvariable=self.bmi_low_var, width=10)
        bmi_low_entry.grid(row=0, column=1, sticky='we')
        tk.Label(bmi_memfunc_frame, text='Medium:').grid(row=1, column=0, sticky='e')
        self.bmi_med_var = tk.StringVar()
        self.bmi_med_var.set('[31.07, 37.07, 45.01]')
        bmi_mod_entry = tk.Entry(bmi_memfunc_frame, textvariable=self.bmi_med_var, width=10)
        bmi_mod_entry.grid(row=1,column=1)
        tk.Label(bmi_memfunc_frame, text='High:').grid(row=2, column=0, sticky='e')
        self.bmi_high_var = tk.StringVar()
        self.bmi_high_var.set('[36.43, 44.43, 67]')
        bmi_high_entry = tk.Entry(bmi_memfunc_frame, textvariable=self.bmi_high_var, width=10)
        bmi_high_entry.grid(row=2, column=1)
        bmi_memfunc_frame.grid(row=0, column=2, padx=5, pady=5)
        plot_bmi_button = tk.Button(bmi_memfunc_frame, text='Plot', command=lambda :plot_bmi())
        plot_bmi_button.grid(row=3, column=0, columnspan=2) 
                
        
        # dpf member functions frame
        dpf_memfunc_frame = tk.LabelFrame(var_func_frame, text='Diabete Pedigree Function' )
        
        tk.Label(dpf_memfunc_frame, text='Low:').grid(row=0, column=0, sticky='e')
        self.dpf_low_var = tk.StringVar()
        self.dpf_low_var.set("[0.085, 0.5322, 1.132]")
        dpf_low_entry = tk.Entry(dpf_memfunc_frame, textvariable=self.dpf_low_var, width=10)
        dpf_low_entry.grid(row=0, column=1, sticky='we')
        tk.Label(dpf_memfunc_frame, text='Medium:').grid(row=1, column=0, sticky='e')
        self. dpf_med_var = tk.StringVar()
        self.dpf_med_var.set('[0.547, 1.03, 1.717]')
        dpf_nor_entry = tk.Entry(dpf_memfunc_frame, textvariable=self.dpf_med_var, width=10)
        dpf_nor_entry.grid(row=1, column=1)
        tk.Label(dpf_memfunc_frame, text='High:').grid(row=2, column=0, sticky='e')
        self.dpf_high_var = tk.StringVar()
        self.dpf_high_var.set('[1.09, 1.476, 2.4]')
        dpf_high_entry = tk.Entry(dpf_memfunc_frame, textvariable=self.dpf_high_var, width=10)
        dpf_high_entry.grid(row=2, column=1)
        dpf_memfunc_frame.grid(row=0, column=3, padx=5, pady=5)
        plot_dpf_button = tk.Button(dpf_memfunc_frame, text='Plot', command=lambda : plot_dpf())
        plot_dpf_button.grid(row=3, column=0, columnspan=2)
        
        # age member functions frame
        age_memfunc_frame = tk.LabelFrame(var_func_frame, text='Age')
        
        tk.Label(age_memfunc_frame, text='Young:').grid(row=0, column=0, sticky='e')
        self.age_young_var = tk.StringVar()
        self.age_young_var.set("[18, 25, 30]")
        age_young_entry = tk.Entry(age_memfunc_frame, textvariable=self.age_young_var, width=10)
        age_young_entry.grid(row=0, column=1, sticky='we')
        tk.Label(age_memfunc_frame, text='Medium:').grid(row=1, column=0, sticky='e')
        self.age_med_var = tk.StringVar()
        self.age_med_var.set('[30, 45, 55]')
        age_med_entry = tk.Entry(age_memfunc_frame, textvariable=self.age_med_var, width=10)
        age_med_entry.grid(row=1, column=1)
        tk.Label(age_memfunc_frame, text='Old:').grid(row=2, column=0, sticky='e')
        self.age_old_var = tk.StringVar()
        self.age_old_var.set('[55, 65, 75]')
        age_old_entry = tk.Entry(age_memfunc_frame, textvariable=self.age_old_var, width=10)
        age_old_entry.grid(row=2, column=1)
        age_memfunc_frame.grid(row=0, column=4, padx=5, pady=5)
        plot_age_button = tk.Button(age_memfunc_frame, text='Plot', command=lambda : plot_age())
        plot_age_button.grid(row=3, column=0, columnspan=2)
        
        # uri member functions frame
        uri_memfunc_frame = tk.LabelFrame(var_func_frame, text='Urine')
    
        tk.Label(uri_memfunc_frame, text='Low:').grid(row=0, column=0, sticky='e')
        self.uri_low_var = tk.StringVar()
        self.uri_low_var.set("[0.5, 50, 800]")
        uri_small_entry = tk.Entry(uri_memfunc_frame, textvariable=self.uri_low_var, width=10)
        uri_small_entry.grid(row=0, column=1, sticky='we')
        tk.Label(uri_memfunc_frame, text='Medium:').grid(row=1, column=0, sticky='e')
        self.uri_med_var = tk.StringVar()
        self.uri_med_var.set('[500, 1300, 2000]')
        uri_med_entry = tk.Entry(uri_memfunc_frame, textvariable=self.uri_med_var, width=10)
        uri_med_entry.grid(row=1, column=1)
        tk.Label(uri_memfunc_frame, text='High:').grid(row=2, column=0, sticky='e')
        self.uri_high_var = tk.StringVar()
        self.uri_high_var.set('[1500, 2500, 5000]')
        uri_large_entry = tk.Entry(uri_memfunc_frame, textvariable=self.uri_high_var, width=10)
        uri_large_entry.grid(row=2, column=1)
        uri_memfunc_frame.grid(row=0, column=5, padx=5, pady=5)
        plot_uri_button = tk.Button(uri_memfunc_frame, text='Plot', command=lambda : plot_uri())
        plot_uri_button.grid(row=3, column=0, columnspan=2)        
        
        # DM member functions frame
        dm_memfunc_frame = tk.LabelFrame(var_func_frame, text='DM Level')
        
        tk.Label(dm_memfunc_frame, text='Very Low:').grid(row=0, column=0, sticky='e')
        self.dm_vlow_var = tk.StringVar()
        self.dm_vlow_var.set("[0, 0.1, 0.2]")
        dm_vlow_entry = tk.Entry(dm_memfunc_frame, textvariable=self.dm_vlow_var, width=20)
        dm_vlow_entry.grid(row=0, column=1, sticky='we')
        
        tk.Label(dm_memfunc_frame, text='Low:').grid(row=1, column=0, sticky='e')
        self.dm_low_var = tk.StringVar()
        self.dm_low_var.set('[0.1524, 0.2524, 0.3]')
        dm_low_entry = tk.Entry(dm_memfunc_frame, textvariable=self.dm_low_var, width=20)
        dm_low_entry.grid(row=1, column=1)
        
        tk.Label(dm_memfunc_frame, text='Medium:').grid(row=2, column=0, sticky='e')
        self.dm_med_var = tk.StringVar()
        self.dm_med_var.set('[0.287, 0.333, 0.3997]')
        dm_med_entry = tk.Entry(dm_memfunc_frame, textvariable=self.dm_med_var, width=20)
        dm_med_entry.grid(row=2, column=1)
        
        
        tk.Label(dm_memfunc_frame, text='High:').grid(row=3, column=0, sticky='e')
        self.dm_high_var = tk.StringVar()
        self.dm_high_var.set("[0.355, 0.623, 0.762]")
        dm_high_entry = tk.Entry(dm_memfunc_frame, textvariable=self.dm_high_var, width=20)
        dm_high_entry.grid(row=3, column=1, sticky='we')
        
        tk.Label(dm_memfunc_frame, text='Very High:').grid(row=4, column=0, sticky='e')
        self.dm_vhigh_var = tk.StringVar()
        self.dm_vhigh_var.set("[0.731, 0.831, 1]")
        dm_vhigh_entry = tk.Entry(dm_memfunc_frame, textvariable=self.dm_vhigh_var, width=14)
        dm_vhigh_entry.grid(row=4, column=1, sticky='we') 
        dm_memfunc_frame.grid(row=0, column=6, padx=5, pady=5)
        
        plot_dm_button = tk.Button(dm_memfunc_frame, text='Plot', command=lambda : plot_dm())
        plot_dm_button.grid(row=5, column=0, columnspan=2)
        
        # select the type of membership function
        select_type_frame = tk.LabelFrame(var_func_frame, text='Membeship function')
        
        types = [
            ("Triangle ", 1),
            ("Trapezoid", 2),
            ("Gaussian ", 3),
        ]
        
        def ShowChoice(text, v):
            print(text, v.get())
        def SetVariables(text, v):
            global glu_low_var, glu_med_var, glu_high_var
            global ins_low_var, ins_med_var, ins_high_var
            global bmi_low_var, bmi_med_var, bmi_high_var
            global dpf_low_var, dpf_med_var, dpf_high_var
            global age_young_var, age_med_var, age_old_var
            global uri_low_var, uri_med_var, uri_high_var
            global dm_vlow_var, dm_low_var, dm_med_var, dm_high_var, dm_vhigh_var
            typeV = v.get()
            fuzzy.set_functype(typeV)
            if typeV == 1:
                self.glu_low_var.set("[56, 100, 125]")
                glu_low_var = [56, 100, 125] 
                self.glu_med_var.set('[68.2, 117, 145]')
                glu_med_var = [68.2, 117, 145]
                self.glu_high_var.set('[109.9, 146, 198]')
                glu_high_var = [109.9, 146, 198]
                
                self.ins_low_var.set("[0, 55.11, 87.67]")
                ins_low_var = [0, 55.11, 87.67]
                self.ins_med_var.set('[63.63, 98.42, 191.6]')
                ins_med_var = [63.63, 98.42, 191.6]
                self.ins_high_var.set('[95.34, 188.3, 586]')
                ins_high_var = [95.34, 188.3, 586]
                
                self.bmi_low_var.set("[18, 22, 30.8]")
                bmi_low_var = [18, 22, 30.8]
                self.bmi_med_var.set('[31.07, 37.07, 45.01]')
                bmi_med_var = [31.07, 37.07, 45.01]
                self.bmi_high_var.set('[36.43, 44.43, 67]')
                bmi_high_var = [36.43, 44.43, 67]
                
                self.dpf_low_var.set("[0.085, 0.5322, 1.132]")
                dpf_low_var = [0.085, 0.5322, 1.132]
                self.dpf_med_var.set('[0.547, 1.03, 1.717]')
                dpf_med_var = [0.547, 1.03, 1.717]
                self.dpf_high_var.set('[1.09, 1.476, 2.4]')
                dpf_high_var = [1.09, 1.476, 2.4]
                
                self.age_young_var.set("[18, 25, 30]")
                age_young_var = [18, 25, 30]
                self.age_med_var.set('[30, 45, 55]')
                age_med_var = [30, 45, 55]
                self.age_old_var.set('[55, 65, 75]')
                age_old_var = [55, 65, 75]
                
                self.uri_low_var.set("[0.5, 50, 800]")
                uri_low_var = [0.5, 50, 800]
                self.uri_med_var.set('[500, 1300, 2000]')
                uri_med_var = [500, 1300, 2000]
                self.uri_high_var.set('[1500, 2500, 5000]')
                uri_high_var = [1500, 2500, 5000]
                
                self.dm_vlow_var.set("[0, 0.1, 0.2]")
                dm_vlow_var = [0, 0.1, 0.2]
                self.dm_low_var.set('[0.1524, 0.2524, 0.3]')
                dm_low_var = [0.1524, 0.2524, 0.3]
                self.dm_med_var.set('[0.287, 0.333, 0.3997]')
                dm_med_var = [0.287, 0.333, 0.3997]
                self.dm_high_var.set("[0.355, 0.623, 0.762]")
                dm_high_var = [0.355, 0.623, 0.762]
                self.dm_vhigh_var.set("[0.731, 0.831, 1]")
                dm_vhigh_var = [0.731, 0.831, 1]
            elif typeV == 2:  # in case of trapezoidal type
                self.glu_low_var.set("[56, 95, 105, 125]")
                glu_low_var = [56, 95, 105, 125] 
                self.glu_med_var.set('[68.2, 103, 126, 145]')
                glu_med_var = [68.2, 103, 126, 145]
                self.glu_high_var.set('[109.9, 135, 156, 198]')
                glu_high_var = [109.9, 135, 156, 198]
                
                self.ins_low_var.set("[0, 50.11, 60, 87.67]")
                ins_low_var = [0, 50.11, 60, 87.67]
                self.ins_med_var.set('[63.63, 90, 109.42, 191.6]')
                ins_med_var = [63.63, 90, 109.42, 191.6]
                self.ins_high_var.set('[95.34, 160, 388.3, 586]')
                ins_high_var = [95.34, 160, 388.3, 586]
                
                self.bmi_low_var.set("[18, 20, 24, 30.8]")
                bmi_low_var = [18, 20, 24, 30.8]
                self.bmi_med_var.set('[31.07, 35, 40.07, 45.01]')
                bmi_med_var = [31.07, 35, 40.07, 45.01]
                self.bmi_high_var.set('[36.43, 40, 54.43, 67]')
                bmi_high_var = [36.43, 40, 54.43, 67]
                
                self.dpf_low_var.set("[0.085, 0.4322, 0.6, 1.132]")
                dpf_low_var = [0.085, 0.4322, 0.6, 1.132]
                self.dpf_med_var.set('[0.547, 0.9, 1.33, 1.717]')
                dpf_med_var = [0.547, 0.9, 1.33, 1.717]
                self.dpf_high_var.set('[1.09, 1.2, 1.976, 2.4]')
                dpf_high_var = [1.09, 1.2, 1.976, 2.4]
                
                self.age_young_var.set("[18, 22, 27, 30]")
                age_young_var = [18, 22, 27, 30]
                self.age_med_var.set('[30,35,45,50]')
                age_med_var = [30,35,40,45]
                self.age_old_var.set('[50, 55, 65, 75]')
                age_old_var = [26, 27, 29, 30]
                
                self.uri_low_var.set("[0.5, 30, 160, 800]")
                uri_low_var = [0.5, 30, 160, 800]
                self.uri_med_var.set('[500, 1000, 1500, 2000]')
                uri_med_var = [500, 1000, 1500, 2000]
                self.uri_high_var.set('[1500, 2100, 2900, 5000]')
                uri_high_var = [1500, 2100, 2900, 5000]
                
                self.dm_vlow_var.set("[0, 0.07, 0.14, 0.2]")
                dm_vlow_var = [0, 0.07, 0.14, 0.2]
                self.dm_low_var.set('[0.1524, 0.2, 0.2524, 0.3]')
                dm_low_var = [0.1524, 0.2, 0.2524, 0.3]
                self.dm_med_var.set('[0.287, 0.31, 0.353, 0.3997]')
                dm_med_var = [0.287, 0.31, 0.353, 0.3997]
                self.dm_high_var.set("[0.355, 0.4, 0.623, 0.762]")
                dm_high_var = [0.355, 0.4, 0.623, 0.762]
                self.dm_vhigh_var.set("[0.731, 0.80, 0.891, 1]")
                dm_vhigh_var = [0.731, 0.80, 0.891, 1] 
            elif typeV == 3:    # In case of gaussian type
                self.glu_low_var.set("[90, 8]")
                glu_low_var = [90, 8] 
                self.glu_med_var.set('[100, 10]')
                glu_med_var = [100, 10]
                self.glu_high_var.set('[140, 15]')
                glu_high_var = [140, 15]
                
                self.ins_low_var.set("[50, 11]")
                ins_low_var = [50, 11]
                self.ins_med_var.set('[100, 20]')
                ins_med_var = [100, 20]
                self.ins_high_var.set('[310, 50]')
                ins_high_var = [310, 50]
                
                self.bmi_low_var.set("[22, 2]")
                bmi_low_var = [22, 2]
                self.bmi_med_var.set('[37, 3]')
                bmi_med_var = [37, 3]
                self.bmi_high_var.set('[49, 4]')
                bmi_high_var = [49, 4]
                
                self.dpf_low_var.set("[0.5, 0.25]")
                dpf_low_var = [0.5, 0.25]
                self.dpf_med_var.set('[1.1, 0.2]')
                dpf_med_var = [1.1, 0.2]
                self.dpf_high_var.set('[1.5, 0.3]')
                dpf_high_var = [1.5, 0.3]
                
                self.age_young_var.set("[25, 0.5]")
                age_young_var = [25, 0.5]
                self.age_med_var.set('[40, 0.5]')
                age_med_var = [26, 0.5]
                self.age_old_var.set('[60, 0.8]')
                age_old_var = [27, 0.8]
                
                self.uri_low_var.set("[400, 130]")
                uri_low_var = [400, 130]
                self.uri_med_var.set('[1300, 210]')
                uri_med_var = [1300, 210]
                self.uri_high_var.set('[2500, 500]')
                uri_high_var = [2500, 500]
                
                self.dm_vlow_var.set("[0.1, 0.03]")
                dm_vlow_var = [0.1, 0.03]
                self.dm_low_var.set('[0.22, 0.03]')
                dm_low_var = [0.22, 0.03]
                self.dm_med_var.set('[0.33, 0.03]')
                dm_med_var = [0.33, 0.03]
                self.dm_high_var.set("[0.62, 0.03]")
                dm_high_var = [0.62, 0.03]
                self.dm_vhigh_var.set("[0.83, 0.04]")
                dm_vhigh_var = [0.83, 0.04]            
        self.vartypes = tk.IntVar()
        self.vartypes.set(types[0][1])
        
        tk.Label(select_type_frame, text='Select one type:').pack()
        
        for txt, val in types:
            tk.Radiobutton(select_type_frame, text=txt, variable=self.vartypes, value=val,
                command=lambda t=txt, v=self.vartypes: SetVariables(t, v)).pack(anchor=tk.N)
        select_type_frame.grid(row=0, column=7, padx=5, pady=5)   
 
        ######################################## rules frame
        rules_frame = tk.LabelFrame(self, text='Rules')
        rules_frame.grid(row=1, column=0, sticky='news', padx=(15,15), pady=(0, 20))
        def browsefunc():
            global filename
            filename = filedialog.askopenfilename()
            pathlabel.config(text=filename)
            rules_text.configure(state='normal')
            rules_text.delete(1.0, tk.END)
            with open(filename) as file:
                rules_text.insert(1.0, file.read())
            rules_text.configure(state='disabled')
        
        browsebutton = tk.Button(rules_frame, text="Browse for Rules", command=browsefunc)
        browsebutton.grid(row = 0, column = 0, padx = 10, pady = 6)
        
        pathlabel = tk.Label(rules_frame)
        pathlabel.grid(row = 0, column = 1, padx = 10, pady = 6)
        temp = tk.Frame(rules_frame, borderwidth=2, relief=tk.RAISED)
        temp.grid(row=1, column=0, columnspan = 2, padx=10, pady=6)
        rules_var = tk.StringVar()
        # load rules
        rules_text = tk.Text(temp, wrap='word', width=140, height=25, cursor='plus')
        rules_text.grid(row=0,column=0)      
        
 
        ####### event handlers
        def plot_dm():
            v=self.vartypes
            vtypes = v.get()
            if vtypes == 1:
                x_vlow = eval(self.dm_vlow_var.get())
                x_low = eval(self.dm_low_var.get())
                x_med = eval(self.dm_med_var.get())
                x_high = eval(self.dm_high_var.get())
                x_vhigh = eval(self.dm_vhigh_var.get())
                y_vlow = [1, 1, 0]
                y_low = [0, 1, 0]
                y_med = [0, 1, 0]
                y_high = [0, 1, 0]
                y_vhigh = [0, 1, 1]
                plt.plot(x_vlow , y_vlow, color='blue', label='Very Low')
                plt.plot(x_low, y_low, color='green', label='Low')
                plt.plot(x_med, y_med, color='red', label='Medium')
                plt.plot(x_high, y_high, color='yellow', label='High')
                plt.plot(x_vhigh, y_vhigh, color='black', label='Very High')
                plt.title("Fuzzy numbers for DM")
                plt.legend()
                plt.show()
            elif vtypes == 2:
                x_vlow = eval(self.dm_vlow_var.get())
                x_low = eval(self.dm_low_var.get())
                x_med = eval(self.dm_med_var.get())
                x_high = eval(self.dm_high_var.get())
                x_vhigh = eval(self.dm_vhigh_var.get())
                y_vlow = [1, 1, 1, 0]
                y_low = [0, 1, 1, 0]
                y_med = [0, 1, 1, 0]
                y_high = [0, 1, 1, 0]
                y_vhigh = [0, 1, 1, 1]
                plt.plot(x_vlow , y_vlow, color='blue', label='Very Low')
                plt.plot(x_low, y_low, color='green', label='Low')
                plt.plot(x_med, y_med, color='red', label='Medium')
                plt.plot(x_high, y_high, color='yellow', label='High')
                plt.plot(x_vhigh, y_vhigh, color='black', label='Very High')
                plt.title("Fuzzy numbers for DM")
                plt.legend()
                plt.show()
            elif vtypes == 3:
                x_axis = np.linspace(0, 1, 200)
                
                vlow = eval(self.dm_vlow_var.get())
                y_vlow = []
                for i in range(0,200):
                    y_vlow.append( math.exp(-(x_axis[i]-vlow[0])**2/(2*vlow[1]*vlow[1])))                
                
                low = eval(self.dm_low_var.get())
                y_low = []
                for i in range(0,200):
                    y_low.append( math.exp(-(x_axis[i]-low[0])**2/(2*low[1]*low[1])))                
                
                med = eval(self.dm_med_var.get())
                y_med = []
                for i in range(0,200):
                    y_med.append( math.exp(-(x_axis[i]-med[0])**2/(2*med[1]*med[1])))
                
                high = eval(self.dm_high_var.get())
                y_high = []
                for i in range(0,200):
                    y_high.append( math.exp(-(x_axis[i]-high[0])**2/(2*high[1]*high[1])))
                
                vhigh = eval(self.dm_vhigh_var.get())
                y_vhigh = []
                for i in range(0,200):
                    y_vhigh.append( math.exp(-(x_axis[i]-vhigh[0])**2/(2*vhigh[1]*vhigh[1])))
                plt.plot(x_axis, y_vlow, color='blue', label='Very Low')
                plt.plot(x_axis, y_low, color='green', label='Low')
                plt.plot(x_axis, y_med, color='red', label='Medium')
                plt.plot(x_axis, y_high, color='yellow', label='High')
                plt.plot(x_axis, y_vhigh, color='black', label='Very High')
                plt.legend()
                plt.title("Fuzzy numbers for DM")
                plt.show()                
        def plot_glu():
            v=self.vartypes
            vtypes = v.get()
            if vtypes == 1:
                x_low = eval(self.glu_low_var.get())
                x_med = eval(self.glu_med_var.get())
                x_high = eval(self.glu_high_var.get())
                y_low = [1, 1, 0]
                y_med = [0, 1, 0]
                y_high = [0, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Glucose")
                plt.show()
            elif vtypes == 2:
                x_low = eval(self.glu_low_var.get())
                x_med = eval(self.glu_med_var.get())
                x_high = eval(self.glu_high_var.get())
                y_low = [1, 1, 1, 0]
                y_med = [0, 1, 1, 0]
                y_high = [0, 1, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Glucose")
                plt.show()
            elif vtypes == 3:
                low = eval(self.glu_low_var.get())
                med = eval(self.glu_med_var.get())
                high = eval(self.glu_high_var.get())
                steps = int(100*(high[0] + 4*high[1] - low[0] + 4*low[1]))
                x_axis = np.linspace(low[0] - 4*low[1], high[0] + 4*high[1], steps)
                
                
                y_low = []
                for i in range(0,steps):
                    y_low.append( math.exp(-(x_axis[i]-low[0])**2/(2*low[1]*low[1])))                
                
                
                y_med = []
                for i in range(0,steps):
                    y_med.append( math.exp(-(x_axis[i]-med[0])**2/(2*med[1]*med[1])))
                
                
                y_high = []
                for i in range(0,steps):
                    y_high.append( math.exp(-(x_axis[i]-high[0])**2/(2*high[1]*high[1])))                
                
                plt.plot(x_axis, y_low, color='blue', label='Low')
                plt.plot(x_axis, y_med, color='green', label='Medium')
                plt.plot(x_axis, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Glucose")
                plt.show()
        def plot_ins():
            v=self.vartypes
            vtypes = v.get()
            if vtypes == 1:
                x_low = eval(self.ins_low_var.get())
                x_med = eval(self.ins_med_var.get())
                x_high = eval(self.ins_high_var.get())
                y_low = [1, 1, 0]
                y_med = [0, 1, 0]
                y_high = [0, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Insulin")
                plt.show()
            elif vtypes == 2:
                x_low = eval(self.ins_low_var.get())
                x_med = eval(self.ins_med_var.get())
                x_high = eval(self.ins_high_var.get())
                y_low = [1, 1, 1, 0]
                y_med = [0, 1, 1, 0]
                y_high = [0, 1, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Insulin")
                plt.show()
            elif vtypes == 3:
                low = eval(self.ins_low_var.get())
                med = eval(self.ins_med_var.get())
                high = eval(self.ins_high_var.get())
                steps = int(100*(high[0] + 4*high[1] - low[0] + 4*low[1]))
                x_axis = np.linspace(low[0] - 4*low[1], high[0] + 4*high[1], steps)
                
                
                y_low = []
                for i in range(0,steps):
                    y_low.append( math.exp(-(x_axis[i]-low[0])**2/(2*low[1]*low[1])))                
                
                
                y_med = []
                for i in range(0,steps):
                    y_med.append( math.exp(-(x_axis[i]-med[0])**2/(2*med[1]*med[1])))
                
                
                y_high = []
                for i in range(0,steps):
                    y_high.append( math.exp(-(x_axis[i]-high[0])**2/(2*high[1]*high[1])))                
                
                plt.plot(x_axis, y_low, color='blue', label='Low')
                plt.plot(x_axis, y_med, color='green', label='Medium')
                plt.plot(x_axis, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Insulin")
                plt.show() 
        def plot_bmi():
            v=self.vartypes
            vtypes = v.get()
            if vtypes == 1:
                x_low = eval(self.bmi_low_var.get())
                x_med = eval(self.bmi_med_var.get())
                x_high = eval(self.bmi_high_var.get())
                y_low = [1, 1, 0]
                y_med = [0, 1, 0]
                y_high = [0, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for BMI(Body Mass Index)")
                plt.show()
            elif vtypes == 2:
                x_low = eval(self.bmi_low_var.get())
                x_med = eval(self.bmi_med_var.get())
                x_high = eval(self.bmi_high_var.get())
                y_low = [1, 1, 1, 0]
                y_med = [0, 1, 1, 0]
                y_high = [0, 1, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for BMI(Body Mass Index)")
                plt.show()
            elif vtypes == 3:
                low = eval(self.bmi_low_var.get())
                med = eval(self.bmi_med_var.get())
                high = eval(self.bmi_high_var.get())
                steps = int(100*(high[0] + 4*high[1] - low[0] + 4*low[1]))
                x_axis = np.linspace(low[0] - 4*low[1], high[0] + 4*high[1], steps)
                
                
                y_low = []
                for i in range(0,steps):
                    y_low.append( math.exp(-(x_axis[i]-low[0])**2/(2*low[1]*low[1])))                
                
                
                y_med = []
                for i in range(0,steps):
                    y_med.append( math.exp(-(x_axis[i]-med[0])**2/(2*med[1]*med[1])))
                
                
                y_high = []
                for i in range(0,steps):
                    y_high.append( math.exp(-(x_axis[i]-high[0])**2/(2*high[1]*high[1])))                
                
                plt.plot(x_axis, y_low, color='blue', label='Low')
                plt.plot(x_axis, y_med, color='green', label='Medium')
                plt.plot(x_axis, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for BMI(Body Mass Index)")
                plt.show()
        def plot_dpf():
            v=self.vartypes
            vtypes = v.get()
            if vtypes == 1:
                x_low = eval(self.dpf_low_var.get())
                x_med = eval(self.dpf_med_var.get())
                x_high = eval(self.dpf_high_var.get())
                y_low = [1, 1, 0]
                y_med = [0, 1, 0]
                y_high = [0, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("(Diabetes Pedigree Function)DPF")
                plt.show()
            elif vtypes == 2:
                x_low = eval(self.dpf_low_var.get())
                x_med = eval(self.dpf_med_var.get())
                x_high = eval(self.dpf_high_var.get())
                y_low = [1, 1, 1, 0]
                y_med = [0, 1, 1, 0]
                y_high = [0, 1, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("(Diabetes Pedigree Function)DPF")
                plt.show()
            elif vtypes == 3:
                low = eval(self.dpf_low_var.get())
                med = eval(self.dpf_med_var.get())
                high = eval(self.dpf_high_var.get())
                steps = int(100*(high[0] + 4*high[1] - low[0] + 4*low[1]))
                x_axis = np.linspace(low[0] - 4*low[1], high[0] + 4*high[1], steps)
                
                
                y_low = []
                for i in range(0,steps):
                    y_low.append( math.exp(-(x_axis[i]-low[0])**2/(2*low[1]*low[1])))                
                
                
                y_med = []
                for i in range(0,steps):
                    y_med.append( math.exp(-(x_axis[i]-med[0])**2/(2*med[1]*med[1])))
                
                
                y_high = []
                for i in range(0,steps):
                    y_high.append( math.exp(-(x_axis[i]-high[0])**2/(2*high[1]*high[1])))                
                
                plt.plot(x_axis, y_low, color='blue', label='Low')
                plt.plot(x_axis, y_med, color='green', label='Medium')
                plt.plot(x_axis, y_high, color='red', label='High')
                plt.legend()
                plt.title("(Diabetes Pedigree Function)DPF")
                plt.show() 
        def plot_age():
            v=self.vartypes
            vtypes = v.get()
            if vtypes == 1:
                x_low = eval(self.age_young_var.get())
                x_med = eval(self.age_med_var.get())
                x_high = eval(self.age_old_var.get())
                y_low = [1, 1, 0]
                y_med = [0, 1, 0]
                y_high = [0, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Age")
                plt.show()
            elif vtypes == 2:
                x_low = eval(self.age_young_var.get())
                x_med = eval(self.age_med_var.get())
                x_high = eval(self.age_old_var.get())
                y_low = [1, 1, 1, 0]
                y_med = [0, 1, 1, 0]
                y_high = [0, 1, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Age")
                plt.show()
            elif vtypes == 3:
                low = eval(self.age_young_var.get())
                med = eval(self.age_med_var.get())
                high = eval(self.age_old_var.get())
                steps = int(100*(high[0] + 4*high[1] - low[0] + 4*low[1]))
                x_axis = np.linspace(low[0] - 4*low[1], high[0] + 4*high[1], steps)
                
                
                y_low = []
                for i in range(0,steps):
                    y_low.append( math.exp(-(x_axis[i]-low[0])**2/(2*low[1]*low[1])))                
                
                
                y_med = []
                for i in range(0,steps):
                    y_med.append( math.exp(-(x_axis[i]-med[0])**2/(2*med[1]*med[1])))
                
                
                y_high = []
                for i in range(0,steps):
                    y_high.append( math.exp(-(x_axis[i]-high[0])**2/(2*high[1]*high[1])))                
                
                plt.plot(x_axis, y_low, color='blue', label='Low')
                plt.plot(x_axis, y_med, color='green', label='Medium')
                plt.plot(x_axis, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Age")
                plt.show()
        def plot_uri():
            v=self.vartypes
            vtypes = v.get()
            if vtypes == 1:
                x_low = eval(self.uri_low_var.get())
                x_med = eval(self.uri_med_var.get())
                x_high = eval(self.uri_high_var.get())
                y_low = [1, 1, 0]
                y_med = [0, 1, 0]
                y_high = [0, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Urine")
                plt.show()
            elif vtypes == 2:
                x_low = eval(self.uri_low_var.get())
                x_med = eval(self.uri_med_var.get())
                x_high = eval(self.uri_high_var.get())
                y_low = [1, 1, 1, 0]
                y_med = [0, 1, 1, 0]
                y_high = [0, 1, 1, 1]
                plt.plot(x_low , y_low, color='blue', label='Low')
                plt.plot(x_med, y_med, color='green', label='Medium')
                plt.plot(x_high, y_high, color='red', label='High')
                plt.legend()
                plt.title("Fuzzy numbers for Urine")
                plt.show()
            elif vtypes == 3:
                low = eval(self.uri_low_var.get())
                med = eval(self.uri_med_var.get())
                high = eval(self.uri_high_var.get())
                steps = int(100*(high[0] + 4*high[1] - low[0] + 4*low[1]))
                x_axis = np.linspace(low[0] - 4*low[1], high[0] + 4*high[1], steps)
                
                
                y_low = []
                for i in range(0,steps):
                    y_low.append( math.exp(-(x_axis[i]-low[0])**2/(2*low[1]*low[1])))                
                
                
                y_med = []
                for i in range(0,steps):
                    y_med.append( math.exp(-(x_axis[i]-med[0])**2/(2*med[1]*med[1])))
                
                
                y_high = []
                for i in range(0,steps):
                    y_high.append( math.exp(-(x_axis[i]-high[0])**2/(2*high[1]*high[1])))                
                
                plt.plot(x_axis, y_low, color='blue', label='Low')
                plt.plot(x_axis, y_med, color='green', label='Medium')
                plt.plot(x_axis, y_high, color='red', label='High')
                plt.title("Fuzzy numbers for Urine")
                plt.legend()
                plt.show()        
        def glu_low_change_handler(event=None):
            global glu_low_var
            v = self.vartypes
            vtypes = v.get()            
            try:
                arr = eval(self.glu_low_var.get())
                if vtypes == 1: # In case of Triangle type
                    if len(arr) != 3:
                        raise Exception("Invalid Arguments. It has 3 args")
                    if float(arr[0]) < float(arr[1]) and float(arr[1]) < float(arr[2]):
                        if float(arr[0]) > 55 and float(arr[2]) < 200:
                            glu_low_var = map(float, arr)
                        else:
                            raise Exception("Values Out Of Range (55, 200)")
                    else:
                        raise Exception("Incerrect Order of values")
                elif vtypes == 2: # In case of Trapezoid type
                    if len(arr) != 4:
                        raise Exception("Invalid Arguments. It has 4 args")
                    if float(arr[0]) < float(arr[1]) and float(arr[1]) < float(arr[2]) and float(arr[2]) < float(arr[3]):
                        if float(arr[0]) > 55 and float(arr[3]) < 200:
                            glu_low_var = map(float, arr)
                        else:
                            raise Exception("Values Out Of Range (55, 200)")
                    else:
                        raise Exception("Incerrect Order of values")
                elif vtypes == 3: # In case of Gaussian type
                    if len(arr) != 2:
                        raise Exception("Invalid Arguments. It has 2 args. First is mean, Second is sigma")
                    if float(arr[0]) > 55 and float(arr[0]) < 200:
                        glu_low_var = map(float, arr)
                    else:
                        raise Exception("Mean Values Out Of Range (55, 200)")               
                    
            except Exception as e:
                messagebox.showerror("Error", e) # display error message
                self.glu_low_var.set("[55, 100, 125]") # set back to default value
                glu_low_var = [55, 100, 125]
 
        glu_low_entry.bind('<Return>', glu_low_change_handler)
        
        def glu_med_change_handler(event=None):
            global glu_med_var
            v = self.vartypes
            vtypes = v.get()            
            try:
                arr = eval(self.glu_med_var.get())
                if vtypes == 1: # In case of Triangle type
                    if len(arr) != 3:
                        raise Exception("Invalid Arguments. It has 3 args")
                    if float(arr[0]) < float(arr[1]) and float(arr[1]) < float(arr[2]):
                        if float(arr[0]) > 55 and float(arr[2]) < 200:
                            glu_med_var = map(float, arr)
                        else:
                            raise Exception("Values Out Of Range (55, 200)")
                    else:
                        raise Exception("Incerrect Order of values")
                elif vtypes == 2: # In case of Trapezoid type
                    if len(arr) != 4:
                        raise Exception("Invalid Arguments. It has 4 args")
                    if float(arr[0]) < float(arr[1]) and float(arr[1]) < float(arr[2]) and float(arr[2]) < float(arr[3]):
                        if float(arr[0]) > 55 and float(arr[3]) < 200:
                            glu_med_var = map(float, arr)
                        else:
                            raise Exception("Values Out Of Range (55, 200)")
                    else:
                        raise Exception("Incerrect Order of values")
                elif vtypes == 3: # In case of Gaussian type
                    if len(arr) != 2:
                        raise Exception("Invalid Arguments. It has 2 args. First is mean, Second is sigma")
                    if float(arr[0]) > 55 and float(arr[0]) < 200:
                        glu_med_var = map(float, arr)
                    else:
                        raise Exception("Mean Values Out Of Range (55, 200)")               
                    
            except Exception as e:
                messagebox.showerror("Error", e) # display error message
                self.glu_med_var.set("[68.2, 117, 145]") # set back to default value
                glu_med_var = [68.2, 117, 145]
 
        glu_mod_entry.bind('<Return>', glu_med_change_handler)
        
        def glu_high_change_handler(event=None):
            global glu_high_var
            v = self.vartypes
            vtypes = v.get()            
            try:
                arr = eval(self.glu_high_var.get())
                if vtypes == 1: # In case of Triangle type
                    if len(arr) != 3:
                        raise Exception("Invalid Arguments. It has 3 args")
                    if float(arr[0]) < float(arr[1]) and float(arr[1]) < float(arr[2]):
                        if float(arr[0]) > 55 and float(arr[2]) < 200:
                            glu_high_var = map(float, arr)
                        else:
                            raise Exception("Values Out Of Range (55, 200)")
                    else:
                        raise Exception("Incerrect Order of values")
                elif vtypes == 2: # In case of Trapezoid type
                    if len(arr) != 4:
                        raise Exception("Invalid Arguments. It has 4 args")
                    if float(arr[0]) < float(arr[1]) and float(arr[1]) < float(arr[2]) and float(arr[2]) < float(arr[3]):
                        if float(arr[0]) > 55 and float(arr[3]) < 200:
                            glu_high_var = map(float, arr)
                        else:
                            raise Exception("Values Out Of Range (55, 200)")
                    else:
                        raise Exception("Incerrect Order of values")
                elif vtypes == 3: # In case of Gaussian type
                    if len(arr) != 2:
                        raise Exception("Invalid Arguments. It has 2 args. First is mean, Second is sigma")
                    if float(arr[0]) > 55 and float(arr[0]) < 200:
                        glu_high_var = map(float, arr)
                    else:
                        raise Exception("Mean Values Out Of Range (55, 200)")               
                    
            except Exception as e:
                messagebox.showerror("Error", e) # display error message
                
                if vtypes == 1: # In case of Triangle type
                    self.glu_high_var.set("[110, 146, 198]") # set back to default value
                    glu_high_var = [110, 146, 198]
                elif vtypes == 2: # In case of Trapezoid type
                    self.glu_high_var.set("[110, 146, 198]") # set back to default value
                    glu_high_var = [110, 146, 198]
                elif vtypes == 3: # In case of Gaussian type
                    self.glu_high_var.set("[110, 146, 198]") # set back to default value
                    glu_high_var = [110, 146, 198]                
 
        glu_high_entry.bind('<Return>', glu_high_change_handler)        
        
        def bmi_low_change_handler(event=None):
            global bmi_low_var
            try:
                arr = eval(self.bmi_low_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 35:
                        raise Exception("Values Out Of Range")
                else:
                    bmi_low_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.bmi_low_var.set("[0, 15, 22]") # set back to default value
                bmi_low_var = [0, 15, 22]
        bmi_low_entry.bind("<Return>", bmi_low_change_handler)
 
        def bmi_mod_change_handler(event=None):
            global bmi_med_var
            try:
                arr = eval(self.bmi_med_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 35:
                        raise Exception("Values Out Of Range")
                else:
                    bmi_med_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.bmi_med_var.set("[15, 22, 29]") # set back to default value
                bmi_med_var = [15, 22, 29]
 
        bmi_mod_entry.bind('<Return>', bmi_mod_change_handler)
 
        def bmi_high_change_handler(event=None):
            global bmi_high_var
            try:
                arr = eval(self.bmi_high_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 35:
                        raise Exception("Values Out Of Range")
                else:
                    bmi_high_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.bmi_high_var.set("[22, 29, 35]") # set back to default value
                bmi_high_var = [22, 29, 35]
        bmi_high_entry.bind('<Return>', bmi_high_change_handler)
        
        def dpf_low_change_handler(event=None):
            global bf_low_var
            try:
                arr = eval(self.bf_low_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 35:
                        raise Exception("Values Out Of Range")
                else:
                    bf_low_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.bf_low_var.set("[0, 15, 22]") # set back to default value
                bf_low_var = [0, 15, 22]
        dpf_low_entry.bind("<Return>", dpf_low_change_handler)
 
        def dpf_nor_change_handler(event=None):
            global bf_nor_var
            try:
                arr = eval(self.bf_nor_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 35:
                        raise Exception("Values Out Of Range")
                else:
                    bf_low_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.bf_nor_var.set("[15, 22, 29]") # set back to default value
                bf_low_var = [12, 22, 29]
        dpf_nor_entry.bind('<Return>', dpf_nor_change_handler)
 
        def dpf_high_change_handler(event=None):
            global bf_high_var
            try:
                arr = eval(self.dpf_high_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 35:
                        raise Exception("Values Out Of Range")
                else:
                    bf_high_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.bf_high_var.set("[22, 29, 35]") # set back to default value
                bf_high_var = [22, 29, 35]
        dpf_high_entry.bind('<Return>', dpf_high_change_handler)
        
        def age_young_change_handler(event=None):
            global age_young_var
            try:
                arr = eval(self.age_young_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 120:
                        raise Exception("Values Out Of Range")
                else:
                    age_young_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.age_young_var.set("[0, 30, 60]") # set back to default value
                age_young_var = [0, 30, 60]
        age_young_entry.bind('<Return>', age_young_change_handler)
 
        def age_med_change_handler(event=None):
            global age_med_var
            try:
                arr = eval(self.age_med_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 120:
                        raise Exception("Values Out Of Range")
                else:
                    age_med_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.age_med_var.set("[30, 60, 90]") # set back to default value
                age_med_var = [30, 60, 90]
        age_med_entry.bind('<Return>', age_med_change_handler)
 
        def age_old_change_handler(event=None):
            global age_old_var
            try:
                arr = eval(self.age_old_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 120:
                        raise Exception("Values Out Of Range")
                else:
                    age_old_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.age_old_var.set("[60, 90, 120]") # set back to default value
                age_old_var = [60, 90, 120]
        age_old_entry.bind('<Return>', age_old_change_handler)
        
        def dm_vlow_change_handler(event=None):
            global dm_vlow_var
            try:
                arr = eval(self.dm_vlow_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 100:
                        raise Exception("Values Out Of Range")
                else:
                    dm_vlow_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.dm_vlow_var.set("[0, 20, 40]") # set back to default value
                dm_vlow_var = [0, 20, 40]
        dm_vlow_entry.bind('<Return>', dm_vlow_change_handler)
 
        def dm_low_change_handler(event=None):
            global dm_low_var
            try:
                arr = eval(self.dm_low_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 100:
                        raise Exception("Values Out Of Range")
                else:
                    dm_low_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.dm_low_var.set("[20, 40, 60]") # set back to default value
                dm_low_var = [20, 40, 60]
        dm_low_entry.bind('<Return>', dm_low_change_handler)
 
        def dm_med_change_handler(event=None):
            global dm_med_var
            try:
                arr = eval(self.dm_med_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 100:
                        raise Exception("Values Out Of Range")
                else:
                    dm_med_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.dm_med_var.set("[60, 80, 100]") # set back to default value
                dm_med_var = [60, 80, 100]
        dm_med_entry.bind('<Return>', dm_med_change_handler)
        
        def dm_high_change_handler(event=None):
            global dm_high_var
            try:
                arr = eval(self.dm_high_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 100:
                        raise Exception("Values Out Of Range")
                else:
                    dm_high_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.dm_high_var.set("[60, 80, 100]") # set back to default value
                dm_high_var = [60, 80, 100]
        dm_high_entry.bind('<Return>', dm_high_change_handler) 
        
        def dm_vhigh_change_handler(event=None):
            global dm_vhigh_var
            try:
                arr = eval(self.dm_vhigh_var.get())
                if len(arr) != 3:
                    raise Exception("Invalid Arguments")
                for item in arr:
                    temp = float(item)
                    if temp < 0 or temp > 100:
                        raise Exception("Values Out Of Range")
                else:
                    dm_vhigh_var = map(float, arr)
            except Exception as e:
                messagebox.showerror("Error", e.message) # display error message
                self.dm_vhigh_var.set("[60, 80, 100]") # set back to default value
                dm_vhigh_var = [60, 80, 100]
        dm_vhigh_entry.bind('<Return>', dm_high_change_handler)        
  

if __name__ == '__main__':
    root = MainWindow()
    root.mainloop()
    
