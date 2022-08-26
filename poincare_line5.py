import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import sys
from py_pol.jones_vector import Jones_vector, degrees
from py_pol.stokes import Stokes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

tab_num = 0

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry("900x700")
        #if you use Windows, let comment out go!
        #self.master.iconbitmap("./poincare32.ico")
        self.master = master
        self.master.title("Polarization plotter")
        self.create_main_tab()
        self.create_menubar()
        self.power_data_entry()
        self.deploy_calculate_button()
        self.master.protocol("WM_DELETE_WINDOW", self.delete_window)

    def create_main_tab(self):
        self.notebook = ttk.Notebook(self.master, height=1000)
        self.main_tab = tk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main menu")        
        #Deploy the widgets
        self.notebook.pack(fill="both")
    
    def create_result_tab(self):
        self.result_tab = tk.Frame(self.notebook)
        global tab_num
        tab_num = tab_num + 1
        self.notebook.add(self.result_tab, text=f"Result{tab_num}")
        self.calculate_power_to_stokes()
        self.create_poincare_sphere()
        self.create_ellipse()
        self.display_stokes_result()
        self.notebook.pack(fill="both")
        self.delete_entry_box()
        #self.create_status_bar(tab_num)

    def create_menubar(self):
        #Create menubar
        self.menubar = tk.Menu(self)
        
        #File menu
        self.menu_file =tk.Menu(self.menubar, tearoff=False)
        self.menu_file.add_command(label="Open ...", command = self.menu_file_open_click, accelerator="Ctrl+O")
        self.menu_file.add_command(label="Save As ...", command = self.menu_file_saveas_click, accelerator="Ctrl+S")
        self.menu_file.add_separator()
        self.menu_file.add_command(label = "Close", command = self.delete_window)

        #Pairing shorcut keys
        self.menu_file.bind("<Control-o>", self.menu_file_open_click)
        self.menu_file.bind("<Control-s>", self.menu_file_saveas_click)

        #Create checkbutton
        self.menu_disp = tk.Menu(self.menubar, tearoff = False)
        self.disp1_value = tk.BooleanVar()
        self.disp2_value = tk.BooleanVar()
        self.disp3_value = tk.BooleanVar()
        self.menu_disp.add_checkbutton( label = "Boolean1", command = self.menu_disp1_click, variable = self.disp1_value)
        self.menu_disp.add_checkbutton( label = "Boolean2", command = self.menu_disp2_click, variable = self.disp2_value)
        self.menu_disp.add_checkbutton( label = "Boolean3", command = self.menu_disp3_click, variable = self.disp3_value)
        
        # Create radiobutton
        self.radio_val = tk.IntVar() # ラジオボタンの値
        self.menu_select = tk.Menu(self.menubar, tearoff = False)
        self.menu_select.add_radiobutton(label = "Select 1", command = self.menu_select_click, variable = self.radio_val, value = 1)
        self.menu_select.add_radiobutton(label = "Select 2", command = self.menu_select_click, variable = self.radio_val, value = 2)
        self.menu_select.add_radiobutton(label = "Select 3", command = self.menu_select_click, variable = self.radio_val, value = 3)
        #Add each menus to a menubar
        self.menubar.add_cascade(label="File", menu = self.menu_file)
        self.menubar.add_cascade(label="Display", menu = self.menu_disp)
        self.menubar.add_cascade(label="Select", menu=self.menu_select)
        
        #Set a menubar with parent window
        self.master.config(menu = self.menubar)

    def menu_file_open_click(self, event=None):
        self.filename = filedialog.askopenfilename(
            title ="Open File",
            initialdir = "./"
        )

    def menu_file_saveas_click(self, event=None):
        print("Selected  Save as...")

    def menu_disp1_click(self):
        print("checked display1!")
        print(f"A state of check is {self.disp1_value.get()}")

    def menu_disp2_click(self):
        print("checked display2!")
        print(f"A state of check is {self.disp2_value.get()}")

    def menu_disp3_click(self):
        print("checked display3!")
        print(f"A state of check is {self.disp3_value.get()}")

    def menu_select_click(self):
        print(self.radio_val.get(), "was pushed")
    def delete_window(self):
        #display the final check message
        ret = messagebox.askyesno(
            title = "Checking of finishing the App",
            message="Are you really finishing the App?")

        if ret == True:
            #if yes is clicked
            self.master.destroy()

    #Make a menubar
    #menubar = tk.Menu(self)
    #file

    #Creating poincare sphere as a three-dimensional graph
    def create_poincare_sphere(self):
        self.frame = tk.Frame(self.result_tab)
        self.S = Stokes("poincarè sphere")
        #S.linear_light(azimuth=-45*degrees)
        self.S.from_components([self.S0_not_normalized, self.S1_not_normalized, self.S2_not_normalized, self.S3_not_normalized])
        self.ax, self.fig  = self.S.draw_poincare(kind="both", color_scatter="Intensity")# filename='poincare.svg')        
        #Relating the region of matplotlib  to widgit 
        self.fig_canvas = FigureCanvasTkAgg(self.fig, self.frame)
        #Making matplotlib's toolbar
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.frame)
        #pack the frame of matplotlib
        self.fig_canvas.get_tk_widget().pack(side=tk.RIGHT ,fill=tk.BOTH)
        #pack the frame
        self.frame.pack(side=tk.RIGHT)
        
    def create_ellipse(self):
        #create frame for drawing ellipse
        self.frame_ellipse = tk.Frame(self.result_tab)
        #Creating empty stokes vector
        self.E = Stokes("Polarization ellipse")
        #Substitute stokes components
        self.E.from_components( [self.S0_not_normalized, self.S1_not_normalized, self.S2_not_normalized, self.S3_not_normalized])
        #self.E.from_components( [self.S0_normalized, self.S1_normalized, self.S2_normalized, self.S3_normalized])
        #Creating ellipse from stokes vector 
        self.ax_ellipse, self.fig_ellipse = self.E.draw_ellipse(draw_arrow=True, figsize=(6,6))# filename="elliptic.svg")
        #Relating the plotting region to widget
        self.fig_canvas_ellipse = FigureCanvasTkAgg(self.ax_ellipse, self.frame_ellipse)
        #Creating matplotlib's toolbar
        self.toolbar_ellipse = NavigationToolbar2Tk(self.fig_canvas_ellipse, self.frame_ellipse)
        #pack a canvas
        self.fig_canvas_ellipse.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
        #pack a frame
        self.frame_ellipse.pack(side=tk.RIGHT, padx = 20)

    def deploy_calculate_button(self):
        calculate = tk.Frame(self.main_tab) # 各項目のlabelとentryを囲むrowフレームを生成
        calculate_button = tk.Button(calculate, text="Calculate", command=self.create_result_tab)
        #grid the calculate button
        calculate.pack(side=tk.TOP, fill=tk.X)
        calculate_button.pack(side = tk.LEFT,fill=tk.BOTH)
        
    def power_data_entry(self):
        # 各項目のlabelとentry
        #frame structure is 
        #power_data_entry_frame > S0_frame_entry > power_entry
        self.power_data_entry_frame = tk.Frame(self.main_tab)
        self.power_data_entry_frame.pack(side=tk.TOP,fill=tk.X)
        
        #Frame for S0
        self.S0_frame_entry = tk.Frame(self.power_data_entry_frame)
        self.power_label_S0 = tk.Label(self.S0_frame_entry,text="P0(Hizontal polarizer)",width=25,relief="sunken") # 各項目のlabelを生成
        self.power_entry_S0 = tk.Entry(self.S0_frame_entry,width=15) # 各項目のentryを生成
        self.uW_label_S0 = tk.Label(self.S0_frame_entry, text='uW',width=10,relief="sunken")

        self.S0_frame_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S0.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_entry_S0.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S0.pack(side=tk.LEFT,fill=tk.BOTH)

        #Frame for S1
        self.S1_frame_entry = tk.Frame(self.power_data_entry_frame)
        self.power_label_S1 = tk.Label(self.S1_frame_entry,text="P1(Vertical polarizer)",width=25,relief="sunken") # 各項目のlabelを生成
        self.power_entry_S1 = tk.Entry(self.S1_frame_entry,width=15) # 各項目のentryを生成
        self.uW_label_S1 = tk.Label(self.S1_frame_entry, text="uW",width=10,relief="sunken")

        self.S1_frame_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S1.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_entry_S1.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S1.pack(side=tk.LEFT,fill=tk.BOTH)

        #Frame for S2
        self.S2_frame_entry = tk.Frame(self.power_data_entry_frame)
        self.power_label_S2 = tk.Label(self.S2_frame_entry,text="P2(Diagonal polarizer)",width=25,relief="sunken") # 各項目のlabelを生成
        self.power_entry_S2 = tk.Entry(self.S2_frame_entry,width=15) # 各項目のentryを生成
        self.uW_label_S2 = tk.Label(self.S2_frame_entry, text="uW",width=10,relief="sunken")

        self.S2_frame_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S2.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_entry_S2.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S2.pack(side=tk.LEFT,fill=tk.BOTH)

        #Frame for S3
        self.S3_frame_entry = tk.Frame(self.power_data_entry_frame)
        self.power_label_S3 = tk.Label(self.S3_frame_entry,text="P3(λ/4 + Diagonal polarizer)",width=25,relief="sunken") # 各項目のlabelを生成
        self.power_entry_S3 = tk.Entry(self.S3_frame_entry,width=15) # 各項目のentryを生成
        self.uW_label_S3 = tk.Label(self.S3_frame_entry, text="uW",width=10,relief="sunken")

        self.S3_frame_entry.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S3.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_entry_S3.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S3.pack(side=tk.LEFT,fill=tk.BOTH)
        
#Display stokes parameters on a result tab
    def display_stokes_result(self):
        #Create power_data_display_frame
        self.power_data_display_frame = tk.Frame(self.result_tab)
        self.power_data_display_frame.pack(side=tk.TOP,fill=tk.X)

        #Frame for S0
        self.S0_result = self.power_entry_S0.get()
        self.display_S0_frame = tk.Frame(self.power_data_display_frame)
        self.power_label_S0 = tk.Label(self.display_S0_frame, text="S0(normalized)",width=25,relief="sunken") 
        self.power_result_S0 = tk.Label(self.display_S0_frame, text=str(self.S0_normalized), width=15,relief="raised")
        #self.uW_label_S0 = tk.Label(self.display_S0_frame, text="uW",width=10,relief="sunken")

        self.display_S0_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S0.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_result_S0.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S0.pack(side=tk.LEFT,fill=tk.BOTH)

        #Frame for S1
        self.display_S1_frame = tk.Frame(self.power_data_display_frame)
        self.power_label_S1 = tk.Label(self.display_S1_frame, text="S1(normalized)",width=25,relief="sunken") 
        self.power_result_S1 = tk.Label(self.display_S1_frame, text=str(self.S1_normalized), width=15,relief="raised")
        #self.uW_label_S1 = tk.Label(self.display_S1_frame, text="uW",width=10,relief="sunken")

        self.display_S1_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S1.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_result_S1.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S1.pack(side=tk.LEFT,fill=tk.BOTH)

        #Frame for S2
        self.display_S2_frame = tk.Frame(self.power_data_display_frame)
        self.power_label_S2 = tk.Label(self.display_S2_frame, text="S2(normalized)",width=25,relief="sunken") 
        self.power_result_S2 = tk.Label(self.display_S2_frame, text=str(self.S2_normalized), width=15,relief="raised")
        #self.uW_label_S2 = tk.Label(self.display_S2_frame, text="uW",width=10,relief="sunken")
        #Pack for S2
        self.display_S2_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S2.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_result_S2.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S2.pack(side=tk.LEFT,fill=tk.BOTH)

        #Frame for S3
        self.display_S3_frame = tk.Frame(self.power_data_display_frame)
        self.power_label_S3 = tk.Label(self.display_S3_frame, text="S3(normalized)",width=25,relief="sunken") 
        self.power_result_S3 = tk.Label(self.display_S3_frame, text=str(self.S3_normalized), width=15,relief="raised")
        #self.uW_label_S3 = tk.Label(self.display_S3_frame, text="uW",width=10,relief="sunken")

        #Pack for S3
        self.display_S3_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.power_label_S3.pack(side=tk.LEFT,fill=tk.BOTH) # labelウィジェットを配置
        self.power_result_S3.pack(side=tk.LEFT, fill=tk.X) # entryウィジェットを配置
        self.uW_label_S3.pack(side=tk.LEFT,fill=tk.BOTH)

#Calculate from input power to stokes parameters
    def calculate_power_to_stokes(self):
        #Substitute the measured power to P's variables
        self.P0 = float(self.power_entry_S0.get())
        self.P1 = float(self.power_entry_S1.get())
        self.P2 = float(self.power_entry_S2.get())
        self.P3 = float(self.power_entry_S3.get())        

        #Calculate not normalized stokes parameter
        self.S0_not_normalized = self.P0 + self.P1
        self.S1_not_normalized = self.P0 - self.P1
        self.S2_not_normalized = 2*self.P2 - self.S0_not_normalized
        self.S3_not_normalized = self.S0_not_normalized - 2*self.P3

        #Calculate normalized stokes parapmeter
        self.S0_normalized = self.S0_not_normalized/self.S0_not_normalized
        self.S1_normalized = self.S1_not_normalized/self.S0_not_normalized
        self.S2_normalized = self.S2_not_normalized/self.S0_not_normalized
        self.S3_normalized = self.S3_not_normalized/self.S0_not_normalized

        #Delete entry box when calculate button is put
    def delete_entry_box(self):
        self.power_entry_S0.delete(0, tk.END)
        self.power_entry_S1.delete(0, tk.END)
        self.power_entry_S2.delete(0, tk.END)        
        self.power_entry_S3.delete(0, tk.END)

    #Create status bar of resutl tab
    # def create_status_bar(self, tab_num):
    #     status = Label(root, text="Resutl" + str( +  of " + str(tab_num),  bd=1, relief="sunken", anchor=E)
    #     status.pack(side= tk.RIGHT,  sticky= W + E)                 

    def create_modeless_dialog(self):
        #making a modeless dialog box
        dlg_modeless = tk.Toplevel(self)
        dlg_modeless.title("Poincarè sphere!!")
        dlg_modeless.geometry("600x600")

if __name__== "__main__":
    root = tk.Tk()
    root.geometry("900x900")
    app = Application(master=root)
    app.mainloop()

