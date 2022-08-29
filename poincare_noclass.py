from tkinter import *
import mysql.connector
import csv # comma separated valules
import numpy as np
import matplotlib.pyplot as plt
import sys
from py_pol.jones_vector import Jones_vector, degrees
from py_pol.stokes import Stokes
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog


root = Tk()
root.title("Stokes Paramter plotter")
root.geometry("400x650")

test_label = Label(root, text="Test label!!")
test_label.grid(row=0, column=0, padx=10, pady=10)


root.mainloop()
