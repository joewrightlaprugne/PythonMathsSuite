import pygame
import sys
from random import choice
from shared import *
from tkinter import *
from tkinter import messagebox
from decimal import Decimal

global equations, inter, top, ArrayPosOfEqEntered
equations = []
inter = []
top = 1

global diffGraph, solGraph, solInterLayer, diffText, diffResultText

global allInters, allSolutions, complexSolutions
allInters = []
allSolutions = []
complexSolutions = []

global clock
clock = pygame.time.Clock()

global programMode, showGridUnits, showIntercepts, lineThickness # Settings
programMode = 1
showGridUnits = 1
showIntercepts = 1
lineThickness = 5

global x_min, x_max, y_min, y_max, centreX, centreY
x_min = 294
x_max = 1280
y_min = 298
y_max = 960
centreX = int(round((x_min+x_max)/2))
centreY = int(round((y_min+y_max)/2))

global x0, x1, x2, x3, y1, y2, zoomX, zoomY
x1 = -10 # x1, x2, y1, y2 are the bounds of the part of the graph displayed on screen
y1 = -10
x2 = 10
y2 = 10
x0 = -50 # x0, x3, y0, y3 are the bounds of the rendered portion of the graph
x3 = 50
y0 = -50
y3 = 50
zoomX = (x_max-x_min)/20
zoomY = (y_max-y_min)/20

global edit, delete # Icons
edit = pygame.image.load("files/edit.png")
delete = pygame.image.load("files/delete.png")
light = pygame.image.load("files/light.png")
dark = pygame.image.load("files/dark.png")
edit = pygame.transform.scale(edit, (32, 32)) # Hard-coded values
delete = pygame.transform.scale(delete, (32, 32))
light = pygame.transform.scale(light, (282, 464))
dark = pygame.transform.scale(dark, (282, 464))

global colours, BACKGROUND_GREY, HOVERING_GREEN, SELECTED_GREEN # Colours
colours = [(255, 0, 0), (255, 80, 0), (0, 255, 0), (0, 232, 255), (255, 0, 255), (147, 0, 255)] # All possible graph colours
BACKGROUND_GREY = (54, 54, 54)
HOVERING_GREEN = (99, 212, 155)
SELECTED_GREEN = (0, 184, 113)

pygame.init()
x = 50
y = 50
pygame.display.set_caption("Python Maths Suite")
screen = pygame.display.set_mode((1280,960))
# screen = pygame.display.set_mode((1280,960), pygame.RESIZABLE)
screen.fill(BACKGROUND_GREY)
pygame.display.update()

global verdana30, verdana25, verdana20, verdana15
verdana30 = pygame.font.SysFont("Verdana", 30)
verdana25 = pygame.font.SysFont("Verdana", 25)
verdana20 = pygame.font.SysFont("Verdana", 20)
verdana15 = pygame.font.SysFont("Verdana", 15)

def updateInterLayer(a, b, equation="", programMode=1):
    if equation == "":
        return interLayer
    inters = getIntersSingleEq(equation, equations, a, b)
    if programMode == 1:
        for inter in inters:
            allInters.append(inter)
            i = inter[0]
            j = inter[1]
            pygame.draw.circle(interLayer, (255, 255, 0), (zoomX*(i-x0), -zoomY*(j+y0)), 5)
        return interLayer
    else:
        for inter in inters:
            allSolutions.append(inter)
            i = inter[0]
            j = inter[1]
            pygame.draw.circle(solInterLayer, (255, 255, 0), (zoomX*(i-x0), -zoomY*(j+y0)), 5)
        return solInterLayer

def updateInterLayerB(a, b, equation=""):
    interLayer = pygame.Surface((zoomX*(x3-x0), zoomY*(y3-y0)), pygame.SRCALPHA, 32)
    interLayer = interLayer.convert_alpha()
    inters = getIntersBetweenAllEq(equations, a, b)
    for inter in inters:
        allInters.append(inter)
        i = inter[0]
        j = inter[1]
        pygame.draw.circle(interLayer, (255, 255, 0), (zoomX*(i-x0), -zoomY*(j+y0)), 5)
    return interLayer

def createBaseLayer(a, b):
    baseLayer = pygame.Surface((zoomX*(x3-x0), zoomY*(y3-y0)))
    baseLayer.fill(BACKGROUND_GREY)
    origin = (-zoomX*x0, -zoomY*y0)
    pygame.draw.line(baseLayer, (150, 150, 150), (origin[0], 0), (origin[0], zoomY*(y3-y0)), 5)
    pygame.draw.line(baseLayer, (150, 150, 150), (0, origin[1]), (zoomX*(x3-x0), origin[1]), 5)
    width = baseLayer.get_width()
    height = baseLayer.get_height()
    distance = 100000
    t = 1
    while (x2-x1)/distance < 15:
        if t:
            distance = distance/2
            t = 0
        else:
            distance = distance/5
            t = 1
    c = 1
    while -c*distance > x0 or c*distance < x3:
        pygame.draw.line(baseLayer, (128, 128, 128), (zoomX*((c*distance)-x0), 0), (zoomX*((c*distance)-x0), zoomY*(y3-y0)), 1)
        pygame.draw.line(baseLayer, (128, 128, 128), (zoomX*((-c*distance)-x0), 0), (zoomX*((-c*distance)-x0), zoomY*(y3-y0)), 1)

        pygame.draw.line(baseLayer, (128, 128, 128), (0, -(zoomY)*((c*distance)+y0)), (zoomX*(x3-x0), -(zoomY)*((c*distance)+y0)), 1)
        pygame.draw.line(baseLayer, (128, 128, 128), (0, -(zoomY)*((-c*distance)+y0)), (zoomX*(x3-x0), -(zoomY)*((-c*distance)+y0)), 1)
        c += 1
    
    return baseLayer

def createNumberlineH(a, b, debug=0):  
    numberLayer = pygame.Surface((zoomX*(b-a), 30), pygame.SRCALPHA, 32) # Hard-coded value
    numberLayer = numberLayer.convert_alpha()
    width = numberLayer.get_width()
    height = numberLayer.get_height()
    distance = 100000
    t = 1
    while (x2-x1)/distance < 15:
        if t:
            distance = distance/2
            t = 0
        else:
            distance = distance/5
            t = 1
    c = 2
    d = (255, 255, 255)
    if debug:
        d = (255, 0, 0)
    while -c*distance > a or c*distance < b:

        axisLabel = verdana15.render(str(c*distance), True, d)
        numberLayer.blit(axisLabel, (zoomX*((c*distance)-a)-axisLabel.get_width()/2, 10))
        
        axisLabel = verdana15.render(str(-c*distance), True, d)
        numberLayer.blit(axisLabel, (zoomX*((-c*distance)-a)-axisLabel.get_width()/2, 10))
        
        c += 2
    
    return numberLayer

def createNumberlineV(a, b, debug=0):
    numberLayer = pygame.Surface((300, zoomY*(b-a)), pygame.SRCALPHA, 32) # Hard-coded value
    numberLayer = numberLayer.convert_alpha()
    width = numberLayer.get_width()
    height = numberLayer.get_height()
    distance = 100000
    t = 1
    while (x2-x1)/distance < 15:
        if t:
            distance = distance/2
            t = 0
        else:
            distance = distance/5
            t = 1
    c = 2
    d = (255, 255, 255)
    ac = ""
    middle = int(round((a+b)/2))
    if debug:
        d = (255, 0, 0)
    while -c*distance > a or c*distance < b:

        axisLabel = verdana15.render(ac + str(2*middle + c*distance), True, d)
        numberLayer.blit(axisLabel, (5, -(zoomY)*((c*distance)+a)-axisLabel.get_height()/2))

        axisLabel = verdana15.render(ac + str(2*middle - c*distance), True, d)
        numberLayer.blit(axisLabel, (5, -(zoomY)*((-c*distance)+a)-axisLabel.get_height()/2))
        
        c += 2

    return numberLayer

def extendInterLayer(x, y):
    global interLayer, allInters
    width = interLayer.get_width()
    height = interLayer.get_height()

    v = x
    x = abs(x)
    w = y
    y = abs(y)
    if x > 0:
        
        newLayer = pygame.Surface((zoomX*x, height), pygame.SRCALPHA, 32) # zoom level = 200
        newLayer = newLayer.convert_alpha()
        origin = ((width + zoomX*x)*(-x0)/(x3-x0), (height + zoomY*y)*(y3)/(y3-y0))
        #####

        #####
        oldLayer = interLayer
        interLayer = pygame.Surface((oldLayer.get_width() + zoomX*x, oldLayer.get_height()), pygame.SRCALPHA, 32)
        interLayer = interLayer.convert_alpha()
        if v < 0:
            inters = getIntersBetweenAllEq(equations, x0+v, x0)
            for inter in inters:
                allInters.append(inter)
                i = inter[0]
                j = inter[1]
                point = ((width + zoomX*x)*(i-(x0+v))/(x3-(x0+v)), -(height + zoomY*y)*(y0+j)/(y3-y0))
                pygame.draw.circle(interLayer, (255, 255, 0), point, 5)
            interLayer.blit(newLayer, (0, 0))
            interLayer.blit(oldLayer, (newLayer.get_width(), 0))
        else:
            inters = getIntersBetweenAllEq(equations, x3, x3+v)
            for inter in inters:
                allInters.append(inter)
                i = inter[0]
                j = inter[1]
                point = ((width + zoomX*x)*(i-x0)/((x3+v)-x0), -(height + zoomY*y)*(y0+j)/(y3-y0))
                pygame.draw.circle(interLayer, (255, 255, 0), point, 5)
            interLayer.blit(oldLayer, (0, 0))
            interLayer.blit(newLayer, (oldLayer.get_width(), 0))

    if y > 0:
        
        newLayer = pygame.Surface((width, zoomY*y), pygame.SRCALPHA, 32) # zoom level = 200
        newLayer = newLayer.convert_alpha()
        origin = ((width + zoomX*x)*(-x0)/(x3-x0), (height + zoomY*y)*(y3)/(y3-y0))
        #####

        #####
        oldLayer = interLayer
        interLayer = pygame.Surface((oldLayer.get_width(), oldLayer.get_height() + zoomY*y), pygame.SRCALPHA, 32)
        interLayer = interLayer.convert_alpha()
        if w < 0:
            inters = getIntersBetweenAllEq(equations, x0, x3) # Can be optimised
            for inter in inters:
                allInters.append(inter)
                i = inter[0]
                j = inter[1]
                point = ((width + zoomX*x)*(i-x0)/(x3-x0), (height + zoomY*y)*(y0+w+j)/(y3-y0))
                pygame.draw.circle(interLayer, (255, 255, 0), point, 5)
            interLayer.blit(oldLayer, (0, 0))
            interLayer.blit(newLayer, (0, oldLayer.get_height()))
        else:
            inters = getIntersBetweenAllEq(equations, x3, x3+w)
            for inter in inters:
                allInters.append(inter)
                i = inter[0]
                j = inter[1]
                point = ((width + zoomX*x)*(i-x0)/(x3-x0), (height + zoomY*y)*(y3+w+j)/(y3-y0))
                pygame.draw.circle(interLayer, (255, 255, 0), point, 5)
            interLayer.blit(newLayer, (0, 0))
            interLayer.blit(oldLayer, (0, newLayer.get_height()))

    return interLayer

def extendBaseLayer(x, y):
    global baseLayer
    width = baseLayer.get_width()
    height = baseLayer.get_height()

    v = x
    x = abs(x)
    w = y
    y = abs(y)
    if x > 0:
        
        newLayer = pygame.Surface((zoomX*x, height), pygame.SRCALPHA, 32) # zoom level = 200
        newLayer = newLayer.convert_alpha()
        origin = ((width + zoomX*x)*(-x0)/(x3-x0), (height + zoomY*y)*(y3)/(y3-y0))
        pygame.draw.line(newLayer, (150, 150, 150), (origin[0], 0), (origin[0], zoomY*(y3-y0)), 5)
        pygame.draw.line(newLayer, (150, 150, 150), (0, origin[1]), (zoomX*(x3-x0), origin[1]), 5)
        
        distance = 100000
        t = 1
        while (x2-x1)/distance < 15:
            if t:
                distance = distance/2
                t = 0
            else:
                distance = distance/5
                t = 1
        c = 1
        while -c*distance > x0 or c*distance < x3:
            pygame.draw.line(newLayer, (128, 128, 128), ((zoomX)*((c*distance)-x0), 0), ((zoomX)*((c*distance)-x0), (zoomY)*(y3-y0)), 1)
            pygame.draw.line(newLayer, (128, 128, 128), ((zoomX)*((-c*distance)-x0), 0), ((zoomX)*((-c*distance)-x0), (zoomY)*(y3-y0)), 1)
            pygame.draw.line(newLayer, (128, 128, 128), (0, -(zoomY)*((c*distance)+y0)), ((zoomX)*(x3-x0), -(zoomY)*((c*distance)+y0)), 1)
            pygame.draw.line(newLayer, (128, 128, 128), (0, -(zoomY)*((-c*distance)+y0)), ((zoomX)*(x3-x0), -(zoomY)*((-c*distance)+y0)), 1)
            c += 1
        
        oldLayer = baseLayer
        baseLayer = pygame.Surface((oldLayer.get_width() + zoomX*x, oldLayer.get_height()), pygame.SRCALPHA, 32)
        baseLayer = baseLayer.convert_alpha()
        if v < 0:
            baseLayer.blit(newLayer, (0, 0))
            baseLayer.blit(oldLayer, (newLayer.get_width(), 0))
        else:
            baseLayer.blit(oldLayer, (0, 0))
            baseLayer.blit(newLayer, (oldLayer.get_width(), 0))
    if y > 0:
        
        newLayer = pygame.Surface((width, zoomY*y), pygame.SRCALPHA, 32) # zoom level = 200
        newLayer = newLayer.convert_alpha()
        origin = ((width + zoomX*x)*(-x0)/(x3-x0), (height + zoomY*y)*(y3)/(y3-y0))
        pygame.draw.line(newLayer, (150, 150, 150), (origin[0], 0), (origin[0], zoomY*(y3-y0)), 5)
        pygame.draw.line(newLayer, (150, 150, 150), (0, origin[1]), (zoomX*(x3-x0), origin[1]), 5)

        distance = 100000
        t = 1
        while (x2-x1)/distance < 15:
            if t:
                distance = distance/2
                t = 0
            else:
                distance = distance/5
                t = 1
        c = 1
        while -c*distance > x0 or c*distance < x3:
            pygame.draw.line(newLayer, (128, 128, 128), (zoomX*((c*distance)-x0), 0), (zoomX*((c*distance)-x0), zoomY*(y3-y0)), 1)
            pygame.draw.line(newLayer, (128, 128, 128), (zoomX*((-c*distance)-x0), 0), (zoomX*((-c*distance)-x0), zoomY*(y3-y0)), 1)

            pygame.draw.line(newLayer, (128, 128, 128), (0, -(zoomY)*((c*distance)+y0)), (zoomX*(x3-x0), -(zoomY)*((c*distance)+y0)), 1)
            pygame.draw.line(newLayer, (128, 128, 128), (0, -(zoomY)*((-c*distance)+y0)), (zoomX*(x3-x0), -(zoomY)*((-c*distance)+y0)), 1)
            c += 1

        
        oldLayer = baseLayer
        baseLayer = pygame.Surface((oldLayer.get_width(), oldLayer.get_height() + zoomY*y), pygame.SRCALPHA, 32)
        baseLayer = baseLayer.convert_alpha()
        if w > 0:
            baseLayer.blit(newLayer, (0, 0))
            baseLayer.blit(oldLayer, (0, newLayer.get_height()))
        else:
            baseLayer.blit(oldLayer, (0, 0))
            baseLayer.blit(newLayer, (0, oldLayer.get_height()))

    return baseLayer

def updateGraph():
    global showIntercepts, diffGraph, solGraph, solInterLayer
    blw = baseLayer.get_width()
    blh = baseLayer.get_height()
    screen.blit(baseLayer, (x_min, y_min), (blw*(x1-x0)/(x3-x0), blh*(y3-y2)/(y3-y0), x_max-x_min, y_max-y_min))
    if programMode == 2:
        try:
            screen.blit(diffGraph.Layer, (x_min, y_min), (blw*(x1-x0)/(x3-x0), blh*(y3-y2)/(y3-y0), x_max-x_min, y_max-y_min))
        except NameError:
            pass
    if programMode == 3:
        try:
            screen.blit(solGraph.Layer, (x_min, y_min), (blw*(x1-x0)/(x3-x0), blh*(y3-y2)/(y3-y0), x_max-x_min, y_max-y_min))
            if showIntercepts:
                screen.blit(solInterLayer, (x_min, y_min), (blw*(x1-x0)/(x3-x0), blh*(y3-y2)/(y3-y0), x_max-x_min, y_max-y_min))
        except NameError:
            pass
    if programMode == 1:
        for eq in equations:
            if eq.isCurrentlyPlotted:
                screen.blit(eq.Layer, (x_min, y_min), (blw*(x1-x0)/(x3-x0), blh*(y3-y2)/(y3-y0), x_max-x_min, y_max-y_min))
        if showIntercepts:
            screen.blit(interLayer, (x_min, y_min), (blw*(x1-x0)/(x3-x0), blh*(y3-y2)/(y3-y0), x_max-x_min, y_max-y_min))
    if showGridUnits:
        pygame.Surface.fill(numberLineLayer, (255, 255, 255, 0))
        origin = [-zoomX*x0, numberLineLayer.get_height()*(-y0)/(y3-y0)]
        if x2 < 0:
            origin[0] = blw*(x2-x0)/(x3-x0) - 20
        if x1 > 0:
            origin[0] = blw*(x1-x0)/(x3-x0)
        if y2 < 0:
            origin[1] = blh*(-y2-y0)/(y3-y0) + 15
        if y1 > 0:
            origin[1] = blh*(-y1-y0)/(y3-y0) - 30
        numberLineLayer.blit(numberLineH, (0, origin[1]))
        numberLineLayer.blit(numberLineV, (origin[0], 0))
        screen.blit(numberLineLayer, (x_min, y_min), (blw*(x1-x0)/(x3-x0), blh*(y3-y2)/(y3-y0), x_max-x_min, y_max-y_min))
    pygame.display.update()

global baseLayer, interLayer, numberLineH, numberLineV, numberLineLayer
baseLayer = createBaseLayer(x0, x3)
interLayer = pygame.Surface((zoomX*(x3-x0), zoomY*(y3-y0)), pygame.SRCALPHA, 32)
interLayer = interLayer.convert_alpha()
solInterLayer = pygame.Surface((zoomX*(x3-x0), zoomY*(y3-y0)), pygame.SRCALPHA, 32)
solInterLayer = interLayer.convert_alpha()
numberLineH = createNumberlineH(x0, x3)
numberLineV = createNumberlineV(x0, x3)
numberLineLayer = pygame.Surface((zoomX*(x3-x0), zoomY*(y3-y0)), pygame.SRCALPHA, 32)
numberLineLayer = numberLineLayer.convert_alpha()
updateGraph()

def shorten(x): # Shortens a number to make it fit on screen
    digitcount = 0
    x = str(x)
    for char in x:
        if char.isdigit():
            digitcount += 1
            if digitcount == 4:
                return '%.2E' % Decimal(x)
    return x

def short_text(x): # Shortens any string longer than 39 characters using "..."
    if len(x) > 39:
        return x[:39] + "..."
    else:
        return x

global enterEquation
global processInput

def processInput(): # Processes the input from the "plot equation" window
    global EqWindow, ArrayPosOfEqEntered, top, pixelArray, interLayer
    global x1, y1, x2, y2

    equation = EqWindow.userfield.get()
    EqWindow.master.destroy()

    side = equation.split("=")
    if len(side) > 2:
        messagebox.showerror("Error", "Too many equals signs")
        return
    if not verify(side[-1].strip()):
        messagebox.showerror("Error", "Invalid syntax")
        return
    equation = cleanInput(side[-1].strip())
    
    if ArrayPosOfEqEntered: # If an already existing function is being edited
        oldColour = equations[ArrayPosOfEqEntered-1].colour
        equations[ArrayPosOfEqEntered-1] = ""
        equations[ArrayPosOfEqEntered-1] = Equation(equation, oldColour)
        equations[ArrayPosOfEqEntered-1].createLayer(x0, x3, y0, y3)
        updateGraph()
    else:
        colour = choice(colours)
        newEquation = Equation(equation, colour)
        interLayer = updateInterLayer(x0, x3, newEquation)
        equations.append(newEquation)
        newEquation.createLayer(x0, x3, y0, y3)
        updateGraph()


    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(286, 0, 700, 250)) # Hard-coded values
    pygame.draw.line(screen, (255, 255, 255), (286, 0), (286, 960), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 60), (1280, 60), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 120), (1280, 120), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 180), (1280, 180), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 240), (1280, 240), 3)
    c = 0
    if len(equations) > 4:
        top = len(equations)-3
    for i in range(top, len(equations)+1):
       if c > 3:
           break
       equations[i-1].drawEquationName(c)
       c += 1
    
    return

class enterEquation(Frame): # Initialise the "enter equation" window

  global equations, ArrayPosOfEqEntered
    
  def __init__(self, number="", master=None):
    global ArrayPosOfEqEntered # Represents the position in the equations array of the equation entered
    ArrayPosOfEqEntered = number # Only defined if an already existing plot is being edited
    Frame.__init__(self, master, width=400, height=400)
    self.pack()
    self.createWidgets(number)
  def createWidgets(self, number): # Initialise all window controls
    self.master.geometry("400x150")
    self.master.title("Graphing: Enter equation")
    self.master.resizable(False, False)
    self.usertext = Label(self, text = "Enter equation:")
    self.usertext.place(x = 0, y = 0)
    self.tips = Label(self, anchor="w", justify="left", text = "Examples:\n\ny = e^x\nsin(x)\ny = x^2 + 1")
    self.tips.place(x = 0, y = 65)
    self.userfield = Entry(self)
    if number:
        self.userfield.insert(0, equations[number-1].func) # Allows the user to edit the equation's text
    self.userfield.place(x = 100, y = 0, width = 260)
    self.entrybutton = Button(self, text = "Submit", command = processInput)
    self.entrybutton.place(x=20, y=30)

class displayDerivative(Frame): # Initialise the "enter equation" window
    
    def __init__(self, inputFunction, derivative, explanation, master=None):
        Frame.__init__(self, master, width=400, height=500)
        self.inputFunction = inputFunction
        self.derivative = derivative
        self.explanation = explanation
        self.pack()
        self.createWidgets()
    
    def plotDerivativeInGraphing(self):
        global equations, programMode, interLayer
        self.master.destroy()
        colour = choice(colours)
        newEquation = Equation(self.derivative, colour)
        interLayer = updateInterLayer(x0, x3, newEquation)
        equations.append(newEquation)
        newEquation.createLayer(x0, x3, y0, y3)
        programMode = 1
        screen.fill(BACKGROUND_GREY)
        main()
        return

    def plotDerivative(self):
        global diffGraph, diffText, diffResultText
        colour = choice(colours)
        diffGraph = Equation(self.derivative, colour)
        diffGraph.createLayer(x0, x3, y0, y3)
        pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(288, 0, 1000, 240)) # Hide equation list
        diffText = verdana30.render("d/dx[" + self.inputFunction + "] =", True, SELECTED_GREEN)
        diffResultText = verdana30.render(self.derivative, True, SELECTED_GREEN)
        screen.blit(diffText, (300, 10)) # Hard-coded values
        screen.blit(diffResultText, (300, 50))
        updateGraph()
        self.master.destroy()
        return
      
    def createWidgets(self): # Initialise all window controls
        self.master.geometry("400x350")
        self.master.title("Results")
        self.master.resizable(False, False)
        self.usertext = Label(self, text = "Input: " + self.inputFunction)
        self.usertext.place(x = 10, y = 10)
        self.tips = Label(self, anchor="w", justify="left", text = "Derivative: " + self.derivative)
        self.tips.place(x = 10, y = 50)
        self.tips2 = Label(self, anchor="w", justify="left", text = "Explanation:\n" + self.explanation)
        self.tips2.place(x = 10, y = 100)
        self.plotbutton = Button(self, text = "Plot derivative", command = self.plotDerivative)
        self.plotbutton2 = Button(self, text = "Plot in Graphing section", command = self.plotDerivativeInGraphing)
        self.closebutton = Button(self, text = "Close", command = self.master.destroy)
        self.plotbutton.place(x=20, y=300)
        self.plotbutton2.place(x=120, y=300)
        self.closebutton.place(x=280, y=300)

class Logger():
    stdout = sys.stdout
    messages = ""

    def start(self): 
        sys.stdout = self

    def stop(self): 
        sys.stdout = self.stdout

    def write(self, text): 
        self.messages += text

def processDiff(): # Processes the input from the "differentiate" window
    global DiffWindow, ArrayPosOfEqEntered
    global x1, y1, x2, y2
    equation = DiffWindow.userfield.get()

    side = equation.split("=")
    if len(side) > 2:
        messagebox.showerror("Error", "Too many equals signs")
        return
    if not verify(side[-1].strip()):
        messagebox.showerror("Error", "Invalid syntax")
        return
    equation = cleanInput(side[-1].strip())
    
    log = Logger()
    log.start()
    result = D(equation)
    log.stop()
    DiffWindow.master.destroy()
    DiffResultWindow = displayDerivative(equation, result, log.messages)
    DiffResultWindow.mainloop()
    return

class enterDiff(Frame): # Initialise the "enter equation" window

  global equations, ArrayPosOfEqEntered
    
  def __init__(self, number="", master=None):
    global ArrayPosOfEqEntered # Represents the position in the equations array of the equation entered
    ArrayPosOfEqEntered = number # Only defined if an already existing plot is being edited
    Frame.__init__(self, master, width=400, height=400)
    self.pack()
    self.createWidgets(number)
  def createWidgets(self, number): # Initialise all window controls
    self.master.geometry("400x150")
    self.master.title("Differentiation: Enter equation")
    self.master.resizable(False, False)
    self.usertext = Label(self, text = "Enter equation:")
    self.usertext.place(x = 0, y = 0)
    self.tips = Label(self, anchor="w", justify="left", text = "Examples:\n\ny = e^x\nsin(x)\ny = x^2 + 1")
    self.tips.place(x = 0, y = 65)
    self.userfield = Entry(self)
    if number:
        self.userfield.insert(0, equations[number-1].func) # Allows the user to edit the equation's text
    self.userfield.place(x = 100, y = 0, width = 260)
    self.entrybutton = Button(self, text = "Submit", command = processDiff)
    self.entrybutton.place(x=20, y=30)
    
def processSolve(): ### CLEAN
    global solWindow, solGraph, solInterLayer
    equ = solWindow.eqfield.get()
    lbound = solWindow.xfield1.get()
    ubound = solWindow.xfield2.get()
    solWindow.master.destroy()
    
    try:
        lbound = float(lbound)
        ubound = float(ubound)
    except ValueError:
        messagebox.showerror("Error", "Invalid bounds")
        return
    if lbound >= ubound:
        messagebox.showerror("Error", "Invalid bounds")
        return
    if equ.count("=") != 1:
        messagebox.showerror("Error", "Invalid syntax")
        return

    try:
        solutions = getAllSolsIntervalR(equ, lbound, ubound)
    except TypeError:
        messagebox.showerror("Error", "Invalid equation")
        return
        
    if solutions == []:
        messagebox.showinfo("No solutions found", "No solutions to the equation could be found in this range")
        return
    output = "The solutions to " + equ + " between " + str(lbound) + " and " + str(ubound) + " are:\n\n"
    for item in solutions:
        output += str(item[0]) + ", "
    messagebox.showinfo("Solutions", output[:-2])

    part = equ.split("=")
    colour = choice(colours)
    solGraph = Equation(part[0] + " - " + part[1], colour)
    solGraph.createLayer(x0, y3, y0, y3)
    solInterLayer = updateInterLayer(lbound, ubound, solGraph, 3)
    updateGraph()
    return

class enterSolve(Frame):
  global solGraph
  def __init__(self, master=None):
    Frame.__init__(self, master, width=400, height=400)
    self.pack()
    self.createWidgets()
  def createWidgets(self):
    self.master.geometry("300x150")
    self.master.title("Enter equation")
    self.master.resizable(False, False)
    self.eqtext = Label(self, text = "Enter one-variable equation in x:")
    self.eqtext.place(x = 0, y = 0)
    self.eqfield = Entry(self)
    self.eqfield.place(x = 5, y = 25, width = 260)
    self.xtext = Label(self, text = " < x < ")
    self.xtext.place(x = 35, y = 55)
    self.xfield1 = Entry(self)
    self.xfield1.place(x = 5, y = 55, width = 30)
    self.xfield2 = Entry(self)
    self.xfield2.place(x = 75, y = 55, width = 30)
    self.entrybutton = Button(self, text = "Solve", command = processSolve)
    self.entrybutton.place(x = 35, y = 85)

def processComplex():
    global CmpWindow, complexSolutions
    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(x_min, y_min, x_max-x_min, y_max-y_min))
    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(290, 245, 990, 42)) # Hard-coded values
    pygame.draw.line(screen, (255, 255, 255), ((x_min+x_max)/2, y_min), ((x_min+x_max)/2, y_max), 3)
    pygame.draw.line(screen, (255, 255, 255), (x_min, (y_min+y_max)/2), (x_max, (y_min+y_max)/2), 3)
    
    equation = CmpWindow.eqfield.get()
    originaleq = equation
    try:
        re1 = float(CmpWindow.Refield1.get())
        re2 = float(CmpWindow.Refield2.get())
        im1 = float(CmpWindow.Imfield1.get())
        im2 = float(CmpWindow.Imfield2.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid bounds")
        return
    if re1 >= re2 or im1 >= im2:
        messagebox.showerror("Error", "Invalid bounds")
        return
    
    CmpWindow.master.destroy()
    for string in ["i\*\((.*?)\)", "\(([^();]+)\)\*i", "i\*[^\s\(\)]*", "[^\s\(\)]*\*i"]:
        d = re.compile(string)
        dec = d.finditer(equation)

        for match in dec:
            current = match.group(0)
            equation = equation.replace(current, "complex(0, " + current.replace("i*", "").replace("*i", "") + ")")
    equation = equation.replace("^", "**").replace("sin", "sn").replace("sinh", "snh").replace("i", "complex(0, 1)").replace("snh", "sinh").replace("sn", "sin")

    side = equation.split("=")
    if len(side) > 2:
        messagebox.showerror("Error", "Too many equals signs")
        return
    if not verify(side[0].strip(), 1) or not verify(side[1].strip(), 1):
        messagebox.showerror("Error", "Invalid syntax")
        return
    
    solutions = getAllSolsIntervalC(equation, re1, re2, im1, im2)
    if solutions == []:
        messagebox.showinfo("No solutions found", "No solutions to the equation could be found in this range")
        return
    complexSolutions = []
    output = "The solutions to " + originaleq + " in this range are:\n\n"
    biggestx = 0.1
    biggesty = 0.1
    for item in solutions:
        if abs(item.real) > abs(biggestx):
            biggestx = item.real
        if abs(item.imag) > abs(biggesty):
            biggesty = item.imag

    for item2 in solutions:
        real = str(item2.real)
        im = str(item2.imag)
        centreX = (x_max+x_min)/2
        centreY = (y_min+y_max)/2
        q = centreX + (item2.real*(x_max-x_min-20)/2)/abs(biggestx)
        r = centreY + (item2.imag*(y_max-y_min-20)/2)/-abs(biggesty)
        pygame.draw.line(screen, (0, 0, 0), (centreX, centreY), (q, r), 7)
        pygame.draw.circle(screen, SELECTED_GREEN, (q, r), 7, 7)
        complexSolutions.append((q, r, real, im))
        pygame.display.update()
        output += (real + "+" + im + "i").replace("+", " + ").replace("-", " - ").strip(" ").replace("+  -", "-").replace(" - ", "E").replace("- ", "-").replace("E", " - ") + ", "
    biggestx *= 1.1
    biggesty *= 1.1
    XUnitsPerPixel = (2*biggestx)/(x_max-x_min)
    YUnitsPerPixel = (2*biggesty)/(y_max-y_min)
    output = output.replace("+  -", "-")
    textsurface = verdana20.render(originaleq + ", " + str(re1) + " < Re(z) < " + str(re2) + ", " + str(im1) + " < Im(z) < " + str(re2), True, (255, 255, 0))
    screen.blit(textsurface, (295, 242))
    position = verdana20.render("Click on a solution to see its coordinates", True, (255, 255, 255))
    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(295, 265, 700, position.get_height())) # Hard-coded values
    screen.blit(position, (295, 265))
    pygame.display.update()
    messagebox.showinfo("Solutions", output[:-2])
    return

class enterComplex(Frame): # Triggered when the "Solve" button on the "Complex" window is pressed
  def __init__(self, master=None):
    Frame.__init__(self, master, width=400, height=400)
    self.pack()
    self.createWidgets()
  def createWidgets(self): # Create the window and add all the entry boxes, text and buttons
    self.master.geometry("300x200")
    self.master.title("Enter equation")
    self.master.resizable(False, False)
    self.eqtext = Label(self, text = "Enter one-variable equation in z:")
    self.eqtext.place(x = 0, y = 0)
    self.eqfield = Entry(self)
    self.eqfield.place(x = 5, y = 25, width = 260)
    self.Retext = Label(self, text = " < Re < ")
    self.Retext.place(x = 35, y = 55)
    self.Refield1 = Entry(self)
    self.Refield1.place(x = 5, y = 55, width = 30)
    self.Refield2 = Entry(self)
    self.Refield2.place(x = 80, y = 55, width = 30)
    self.Imtext = Label(self, text = " < Im < ")
    self.Imtext.place(x = 35, y = 80)
    self.Imfield1 = Entry(self)
    self.Imfield1.place(x = 5, y = 80, width = 30)
    self.Imfield2 = Entry(self)
    self.Imfield2.place(x = 80, y = 80, width = 30)
    self.entrybutton = Button(self, text = "Solve", command = processComplex) # The "Solve" button forwards the data currently in the entry boxes to processComplex()
    self.entrybutton.place(x = 35, y = 105)

def main(): # Main program, called when the program is started
    global top
    global equations
    global x1, x2, y1, y2, lineThickness, showGridUnits, showIntercepts, x0, x3, y0, y3, baseLayer, interLayer, programMode, numberLineH, numberLineV, numberLineLayer
    c = 0
    mouseDownAt = (-1, -1)
    tick = pygame.image.load("files/g_tick.png")
    notick = pygame.image.load("files/g_notick.png")
    # Hard-coded values (should change)
    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(286, 0, 700, 250))
    pygame.draw.line(screen, (255, 255, 255), (286, 0), (286, 960), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 60), (1280, 60), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 120), (1280, 120), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 180), (1280, 180), 3)
    pygame.draw.line(screen, (255, 255, 255), (286, 240), (1280, 240), 3)
    pygame.display.update()
    addnew = verdana30.render("Add an equation", True, SELECTED_GREEN)
    

    gridunittext = verdana25.render("Show grid units", True, (255, 255, 255))
    intercepttext = verdana25.render("Show intercepts", True, (255, 255, 255))
##    scaletext = verdana30.render("Scale:", True, (255, 255, 255))
##    screen.blit(scaletext, (10, 470))
##    scaleX = verdana20.render(str(roundSF(x1, 2)) + " < x < " + str(roundSF(x2, 2)), True, (255, 255, 255))
##    scaleY = verdana20.render(str(roundSF(y1, 2)) + " < y < " + str(roundSF(y2, 2)), True, (255, 255, 255))
##    screen.blit(scaleX, (0, 520))
##    screen.blit(scaleY, (0, 550))
    
    screen.blit(addnew, (x_min, y_min - addnew.get_height() - 10))
    screen.blit(gridunittext, (45, 670))
    screen.blit(intercepttext, (45, 710))
    screen.blit(dark, (0, 0))
    screen.blit(tick, (10, 670)) # Add sidebar controls
    screen.blit(tick, (10, 710))
    pygame.draw.rect(screen, SELECTED_GREEN, pygame.Rect(0, 0, 285, 112)) # Hard-coded values
    screen.blit(light, (0, 0), (0, 0, 285, 112))
    for i in range(top, len(equations)+1):
       if c > 3:
           break
       equations[i-1].drawEquationName(c)
       c += 1
    pygame.display.update()
    global EqWindow
    global DiffWindow
    global solWindow
    
    lastpos = pygame.mouse.get_pos()
    hoveringOver = 0
    while True: # This is the loop that the program spends its idle time in
        events = pygame.event.get()
        mouseStatus = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        
        if mouseStatus[0] and programMode != 4 and x_min < pos[0] < x_max and y_min < pos[1] < y_max:
            r1 = (lastpos[0]-pos[0])*(x2-x1)/(x_max - x_min)
            r2 = (lastpos[1]-pos[1])*(y2-y1)/(y_min - y_max)
            x1 += r1
            x2 += r1
            y1 += r2
            y2 += r2
            lastpos = pos
            if x0 > x1:
                baseLayer = extendBaseLayer((x1 - x0) + 2*(x1-x2), 0)
                interLayer = extendInterLayer((x1 - x0) + 2*(x1-x2), 0)
                newpart = createNumberlineH(x0 - 2*(x2-x1), x0)
                oldpart = numberLineH
                numberLineH = pygame.Surface((newpart.get_width() + oldpart.get_width(), 30), pygame.SRCALPHA, 32) # zoom level = 200
                numberLineH = numberLineH.convert_alpha()
                numberLineH.blit(newpart, (0, 0))
                numberLineH.blit(oldpart, (newpart.get_width(), 0))
                numberLineLayer = pygame.Surface((zoomX*(2*(x2-x1)+x3-x0), zoomY*(y3-y0)), pygame.SRCALPHA, 32)
                numberLineLayer = numberLineLayer.convert_alpha()
                for eq in equations:
                    eq.extendLayer((x1 - x0) + 2*(x1-x2), 0)
                x0 += (x1 - x0) + 2*(x1-x2)
            if x3 < x2:
                baseLayer = extendBaseLayer((x2 - x3) + 2*(x2-x1), 0)
                interLayer = extendInterLayer((x2 - x3) + 2*(x2-x1), 0)
                newpart = createNumberlineH(x3, x3 + 2*(x2-x1))
                oldpart = numberLineH
                numberLineH = pygame.Surface((newpart.get_width() + oldpart.get_width(), 30), pygame.SRCALPHA, 32) # zoom level = 200
                numberLineH = numberLineH.convert_alpha()
                numberLineH.blit(oldpart, (0, 0))
                numberLineH.blit(newpart, (oldpart.get_width(), 0))
                numberLineLayer = pygame.Surface((zoomX*(2*(x2-x1)+x3-x0), zoomY*(y3-y0)), pygame.SRCALPHA, 32)
                numberLineLayer = numberLineLayer.convert_alpha()
                for eq in equations:
                    eq.extendLayer((x2 - x3) + 2*(x2-x1), 0)
                x3 += (x2 - x3) + 2*(x2-x1)
            if y0 > y1:
                baseLayer = extendBaseLayer(0, (y1 - y0) + 2*(y1-y2))
                interLayer = extendInterLayer(0, (y1 - y0) + 2*(y1-y2))
                newpart = createNumberlineV(y0 - 2*(y2-y1), y0)
                oldpart = numberLineV
                numberLineV = pygame.Surface((300, newpart.get_height() + oldpart.get_height()), pygame.SRCALPHA, 32) # zoom level = 200
                numberLineV = numberLineV.convert_alpha()
                numberLineV.blit(oldpart, (0, 0))
                numberLineV.blit(newpart, (0, oldpart.get_height()))
                numberLineLayer = pygame.Surface((zoomX*(x3-x0), zoomY*(2*(y2-y1)+y3-y0)), pygame.SRCALPHA, 32)
                numberLineLayer = numberLineLayer.convert_alpha()
                for eq in equations:
                    eq.extendLayer(0, (y1 - y0) + 2*(y1-y2))
                y0 += (y1 - y0) + 2*(y1-y2)
                screen.blit(numberLineH, (0, 0))
            if y3 < y2:
                baseLayer = extendBaseLayer(0, (y2 - y3) + 2*(y2-y1))
                interLayer = extendInterLayer(0, (y2 - y3) + 2*(y2-y1))
                newpart = createNumberlineV(y3, y3 + 2*(y2-y1))
                oldpart = numberLineV
                numberLineV = pygame.Surface((300, newpart.get_height() + oldpart.get_height()), pygame.SRCALPHA, 32) # zoom level = 200
                numberLineV = numberLineV.convert_alpha()
                numberLineV.blit(newpart, (0, 0))
                numberLineV.blit(oldpart, (0, newpart.get_height()))
                numberLineLayer = pygame.Surface((zoomX*(x3-x0), zoomY*(2*(y2-y1)+y3-y0)), pygame.SRCALPHA, 32)
                numberLineLayer = numberLineLayer.convert_alpha()
                for eq in equations:
                    eq.extendLayer(0, (y2 - y3) + 2*(y2-y1))
                y3 += (y2 - y3) + 2*(y2-y1)
            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(x_min, y_min, x_max-x_min, y_max-y_min))
            updateGraph()
            pygame.display.update()
        if not mouseStatus[0]:
            mouseDownAt = (-1, -1)
            lastpos = pygame.mouse.get_pos()

        if 0 < pos[0] < 283 and 0 < pos[1] < 108 and programMode != 1 and hoveringOver != 1: ## Graphing
            pygame.draw.rect(screen, HOVERING_GREEN, pygame.Rect(0, 0, 285, 112)) # Hard-coded values
            screen.blit(light, (0, 0), (0, 0, 285, 112))
            pygame.display.update()
            hoveringOver = 1
        if not (0 < pos[0] < 283 and 0 < pos[1] < 108) and programMode != 1 and hoveringOver == 1:
            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 0, 285, 112)) # Hard-coded values
            screen.blit(dark, (0, 0), (0, 0, 285, 112))
            pygame.display.update()
            hoveringOver = 0
            
        if 0 < pos[0] < 283 and 116 < pos[1] < 224 and programMode != 2 and hoveringOver != 2: ## User clicks on "differentiation"
            pygame.draw.rect(screen, HOVERING_GREEN, pygame.Rect(0, 116, 285, 112)) # Hard-coded values
            screen.blit(light, (0, 116), (0, 116, 285, 112))
            pygame.display.update()
            hoveringOver = 2
        if not (0 < pos[0] < 283 and 116 < pos[1] < 224) and programMode != 2 and hoveringOver == 2:
            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 116, 285, 112)) # Hard-coded values
            screen.blit(dark, (0, 116), (0, 116, 285, 112))
            pygame.display.update()
            hoveringOver = 0
            
        if 0 < pos[0] < 283 and 232 < pos[1] < 339 and programMode != 3 and hoveringOver != 3: ## User clicks on "solve"
            pygame.draw.rect(screen, HOVERING_GREEN, pygame.Rect(0, 232, 285, 112)) # Hard-coded values
            screen.blit(light, (0, 232), (0, 232, 285, 112))
            pygame.display.update()
            hoveringOver = 3
        if not (0 < pos[0] < 283 and 232 < pos[1] < 339) and programMode != 3 and hoveringOver == 3:
            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 232, 285, 112)) # Hard-coded values
            screen.blit(dark, (0, 232), (0, 232, 285, 112))
            pygame.display.update()
            hoveringOver = 0
            
        if 0 < pos[0] < 283 and 348 < pos[1] < 454 and programMode != 4 and hoveringOver != 4: ## User clicks on "complex"
            pygame.draw.rect(screen, HOVERING_GREEN, pygame.Rect(0, 348, 285, 112)) # Hard-coded values
            screen.blit(light, (0, 348), (0, 348, 285, 112))
            pygame.display.update()
            hoveringOver = 4
        if not (0 < pos[0] < 283 and 348 < pos[1] < 454) and programMode != 4 and hoveringOver == 4:
            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 348, 285, 112)) # Hard-coded values
            screen.blit(dark, (0, 348), (0, 348, 285, 112))
            pygame.display.update()
            hoveringOver = 0
        
        for event in events: # Constantly get a list of events (mouse clicks and key presses)
            pos = pygame.mouse.get_pos()
                    
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 4 and pos[0] > 290 and pos[1] > 293: # If the user scrolls up while the mouse is on the plot (zooming not yet implemented)
                if programMode > 2:
                    continue
            if (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 5 and pos[0] > 290 and pos[1] > 293: # If the user scrolls down while the mouse is on the plot (zooming not yet implemented)
                if programMode > 2:
                    continue
            if (event.type == pygame.MOUSEBUTTONDOWN) and 3 < event.button < 6 and pos[0] > 286 and pos[1] < 240: # Scrolling up/down
                if programMode != 1:
                    continue
                if event.button == 4:
                    if top == 1:
                        continue
                    top -= 1
                else:
                    if top+1 > len(equations):
                        continue
                    top += 1
                pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(286, 0, 1100, 250)) # Hard-coded values
                pygame.draw.line(screen, (255, 255, 255), (286, 0), (286, 960), 3)
                pygame.draw.line(screen, (255, 255, 255), (286, 60), (1280, 60), 3)
                pygame.draw.line(screen, (255, 255, 255), (286, 120), (1280, 120), 3)
                pygame.draw.line(screen, (255, 255, 255), (286, 180), (1280, 180), 3)
                pygame.draw.line(screen, (255, 255, 255), (286, 240), (1280, 240), 3)
                c = 0
                for i in range(top, len(equations)+1):
                   if c > 3:
                       break
                   equations[i-1].drawEquationName(c)
                   c += 1

            if (event.type == pygame.MOUSEBUTTONDOWN) and event.button == 1:
                x = roundSF(x1 + (x2-x1)*(pos[0]-x_min)/(x_max-x_min), 5) # Calculate the grid coordinates of the pixel the user clicked on
                y = roundSF(y2 - (y2-y1)*(pos[1]-y_min)/(y_max-y_min), 5)
                positiontext = verdana30.render("Position: ", True, (255, 255, 255)) # Display these coordinates
                position = verdana20.render(str(x) + ", " + str(y), True, (255, 255, 255)) # Temporary
                pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(10, 470, 275, 100)) # Hard-coded values
                if pos[0] > 289 and pos[1] > 293 and programMode < 4:
                    screen.blit(positiontext, (10, 470))
                    screen.blit(position, (10, 520))
                pygame.display.update()

                
                if 0 < pos[0] < 283 and 0 < pos[1] < 108:
                    if programMode == 1:
                        continue
                    programMode = 1
                    screen.fill(BACKGROUND_GREY)
                    main()
                    return
                if 0 < pos[0] < 283 and 116 < pos[1] < 224:
                    if programMode == 2:
                        continue
                    programMode = 2

                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 0, 285, 448))
                    screen.blit(dark, (0, 0), (0, 0, 285, 448))
                    pygame.draw.rect(screen, SELECTED_GREEN, pygame.Rect(0, 116, 285, 112)) # Hard-coded values
                    screen.blit(light, (0, 116), (0, 116, 285, 112))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(290, 245, 990, 42))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(288, 0, 1000, 240)) # Hide equation list
                    try:
                        screen.blit(diffText, (300, 10))
                        screen.blit(diffResultText, (300, 50))
                    except NameError:
                        pass
                    addnew = verdana30.render("Enter a function", True, SELECTED_GREEN)
                    screen.blit(addnew, (x_min, y_min - addnew.get_height() - 10))
                    updateGraph()
                    pygame.display.update()
                if 0 < pos[0] < 283 and 232 < pos[1] < 339: ## User clicks on "solve"
                    if programMode == 3:
                        continue
                    programMode = 3

                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 0, 285, 448))
                    screen.blit(dark, (0, 0), (0, 0, 285, 448))
                    pygame.draw.rect(screen, SELECTED_GREEN, pygame.Rect(0, 232, 285, 112)) # Hard-coded values
                    screen.blit(light, (0, 232), (0, 232, 285, 112))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(290, 245, 990, 42))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(288, 0, 1000, 240)) # Hide equation list
                    addnew = verdana30.render("Solve an equation", True, SELECTED_GREEN)
                    screen.blit(addnew, (x_min, y_min - addnew.get_height() - 10))
                    updateGraph()
                    pygame.display.update()
                if 0 < pos[0] < 283 and 348 < pos[1] < 454: ## User clicks on "complex"
                    programMode = 4
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 0, 285, 448))
                    screen.blit(dark, (0, 0), (0, 0, 285, 448))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(0, 348, 285, 112))
                    pygame.draw.rect(screen, SELECTED_GREEN, pygame.Rect(0, 348, 285, 112)) # Hard-coded values
                    screen.blit(light, (0, 348), (0, 348, 285, 112))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(290, 245, 990, 42))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(288, 0, 1000, 240)) # Hide equation list
                    addnew = verdana30.render("Solve an equation", True, SELECTED_GREEN)
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(x_min, y_min, x_max-x_min, y_max-y_min))
                    screen.blit(addnew, (x_min, y_min - addnew.get_height() - 10))
                    pygame.display.update()
                    global CmpWindow
                    CmpWindow = enterComplex() # Create complex window
                    CmpWindow.mainloop()

                if 1190 < pos[0] < 1222: # Hard-coded values
                    if programMode != 1:
                        continue
                    for i in range(0, 4):
                        if 12+i*60 < pos[1] < 44+i*60:
                            if programMode > 2 or top+i > len(equations):
                                break
                            EqWindow = enterEquation(top+i) # Create an "enter equation" window already containing the text of the equation being edited
                            EqWindow.mainloop()

                if 1235 < pos[0] < 1267: # Hard-coded values
                    if programMode != 1:
                        continue
                    for i in range(0, 4):
                        if 12+i*60 < pos[1] < 44+i*60:
                            if top+i > len(equations):
                                break
                            del equations[top+i-1]
                            ## equations.pop(top+i-1)
                            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(286, 0, 1000, 250)) # Hard-coded values
                            pygame.draw.line(screen, (255, 255, 255), (286, 0), (286, 960), 3)
                            pygame.draw.line(screen, (255, 255, 255), (286, 60), (1280, 60), 3)
                            pygame.draw.line(screen, (255, 255, 255), (286, 120), (1280, 120), 3)
                            pygame.draw.line(screen, (255, 255, 255), (286, 180), (1280, 180), 3)
                            pygame.draw.line(screen, (255, 255, 255), (286, 240), (1280, 240), 3)
                            c = 0
                            for i in range(top, len(equations)+1):
                               if c > 3:
                                   break
                               equations[i-1].drawEquationName(c)
                               c += 1
                            interLayer = updateInterLayerB(x0, x3)
                            updateGraph()

                if pos[0] > 289 and 234 < pos[1] < 284: ## User clicks on "enter new equation"
                    if programMode == 1:
                        EqWindow = enterEquation() # Create window
                        EqWindow.mainloop()
                    if programMode == 2:
                        DiffWindow = enterDiff() # Create window
                        DiffWindow.mainloop()
                    if programMode == 3:
                        solWindow = enterSolve() # Create solve window
                        solWindow.mainloop()
                    if programMode == 4:
                        CmpWindow = enterComplex() # Create solve window
                        CmpWindow.mainloop()
                if 11 < pos[0] < 34 and 670 < pos[1] < 693: # If the user toggles "show grid units"
                    if programMode > 2:
                        continue
                    showGridUnits = 1 - showGridUnits
                    if showGridUnits == 1:
                        screen.blit(tick, (10, 670))
                    else:
                        screen.blit(notick, (10, 670))
                    A = ["off", "on"]
                    updateGraph()
                    pygame.display.flip()

                if 11 < pos[0] < 34 and 710 < pos[1] < 733: # If the user toggles "show intercepts"
                    if programMode > 2:
                        continue
                    showIntercepts = 1 - showIntercepts
                    if showIntercepts == 1:
                        screen.blit(tick, (10, 710))
                    else:
                        screen.blit(notick, (10, 710))
                    pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(x_min, y_min, x_max-x_min, y_max-y_min))
                    updateGraph()
                    pygame.display.flip()

                if 10 < pos[0] < 242 and 595 < pos[1] < 623: # Change scale (not yet implemented)
                    pass
                
                x = x1 + (x2-x1)*(pos[0]-x_min)/(x_max-x_min)
                y = y2 - (y2-y1)*(pos[1]-y_min)/(y_max-y_min)
                pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(10, 560, 275, 100)) # Hard-coded values
                if programMode == 1:
                    for inter in allInters:
                        if abs(inter[0] - x) < 0.2 and abs(inter[1] - y) < 0.2 and x_min < pos[0] < x_max and y_min < pos[1] < y_max:
                            positiontext = verdana30.render("Intercept: ", True, (255, 255, 255)) # Display these coordinates
                            position = verdana20.render(str(roundSF(inter[0], 6)) + ", " + str(roundSF(inter[1], 6)), True, (255, 255, 255)) # Temporary
                            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(10, 565, 275, 100)) # Hard-coded values
                            screen.blit(positiontext, (10, 565))
                            screen.blit(position, (10, 615))
                            pygame.display.update()

                if programMode == 3:
                    for inter in allSolutions:
                        if abs(inter[0] - x) < 0.2 and abs(inter[1] - y) < 0.2 and x_min < pos[0] < x_max and y_min < pos[1] < y_max:
                            positiontext = verdana30.render("Solution: ", True, (255, 255, 255)) # Display these coordinates
                            position = verdana20.render(str(roundSF(inter[0], 6)) + ", " + str(roundSF(inter[1], 6)), True, (255, 255, 255)) # Temporary
                            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(10, 565, 275, 100)) # Hard-coded values
                            screen.blit(positiontext, (10, 565))
                            screen.blit(position, (10, 615))
                            pygame.display.update()

                if programMode == 4:
                    for solution in complexSolutions:
                        if abs(pos[0] - solution[0]) < 6 and abs(pos[1] - solution[1]) < 6 and x_min < pos[0] < x_max and y_min < pos[1] < y_max:
                            position = verdana20.render("Solution: " + str(solution[2]) + " + " + str(solution[3]) + "i", True, (255, 255, 255)) # Temporary
                            pygame.draw.rect(screen, BACKGROUND_GREY, pygame.Rect(295, 265, 700, position.get_height())) # Hard-coded values
                            screen.blit(position, (295, 265))
                            pygame.display.update()
                        

        clock.tick(120)

class Equation:
    global verdana30
    def __init__(self, func, colour, xIntercepts=[], yIntercepts=[], isCurrentlyPlotted=1, generatedRange=(0, 0), generatedPoints=[]):
        self.func = func
        self.colour = colour
        self.xIntercepts = xIntercepts
        self.yIntercepts = yIntercepts
        self.isCurrentlyPlotted = isCurrentlyPlotted
        self.generatedRange = generatedRange
        self.generatedPoints = generatedPoints

    def drawEquationName(self, slotNo):
        textsurface = verdana30.render("y = " + self.func, True, self.colour)
        screen.blit(edit, (1190, 12 + slotNo*60))
        screen.blit(delete, (1235, 12 + slotNo*60))
        screen.blit(textsurface, (300, 10 + slotNo*60)) # Hard-coded values
        pygame.display.flip()

    def generatePoints(self, a, b, d=0.005):
        y = 0
        r = []
        eq = self.func
        for i in range(0, int(round((b-a)/d))):
            x = a + i*d
            try:
              y = evaluateWrapper(eq, x)
            except ZeroDivisionError:
                y = "D"
            except ValueError:
                y = "D"
            except OverflowError:
                y = "D"
            if isinstance(y, complex):
                y = "D"
            if y is None:
                y = "D"
            r.append((x, y))
        self.generatedRange = (a, b)
        return r

    def generateSurface(self, xL, xU, yL, yU):
        points = self.generatePoints(xL, xU)
        newSurface = pygame.Surface((zoomX*(xU-xL), zoomY*(yU-yL)), pygame.SRCALPHA, 32) # zoom level = 200
        newSurface = newSurface.convert_alpha()
        plotPoints = []
        currentPiece = []
        for i in range(0, len(points)):
            if points[i][1] == "D":
                if len(currentPiece) > 0:
                    plotPoints.append(currentPiece)
                    currentPiece = []
                continue
            a = zoomX*(points[i][0]-xL)
            b = zoomY*(yU-points[i][1])
            currentPiece.append([a, b])
        if len(currentPiece) > 0:
            plotPoints.append(currentPiece)
            currentPiece = []
        for piece in plotPoints:
            if len(piece) == 0:
                continue
            if len(piece) == 1:
                pygame.draw.circle(newSurface, SELECTED_GREEN, (piece[0][0], piece[0][1]), 3)
                continue
            pygame.draw.lines(newSurface, self.colour, False, piece, lineThickness)
        return newSurface

    def createLayer(self, xL, xU, yL, yU):
        self.Layer = self.generateSurface(xL, xU, yL, yU)
        return

    def extendLayer(self, x, y):
        width = self.Layer.get_width()
        height = self.Layer.get_height()

        if x < 0:
            w = x
            x = abs(x)
            newLayer = self.generateSurface(x0-x, x0, y0, y3)
            oldLayer = self.Layer
            self.Layer = pygame.Surface((oldLayer.get_width() + zoomX*x, oldLayer.get_height()), pygame.SRCALPHA, 32)
            self.Layer = self.Layer.convert_alpha()
            self.Layer.blit(newLayer, (0, 0))
            self.Layer.blit(oldLayer, (newLayer.get_width(), 0))
            x = w
            
        if x > 0:
            newLayer = self.generateSurface(x3, x3+x, y0, y3)
            oldLayer = self.Layer
            self.Layer = pygame.Surface((oldLayer.get_width() + zoomX*x, oldLayer.get_height()), pygame.SRCALPHA, 32)
            self.Layer = self.Layer.convert_alpha()
            self.Layer.blit(oldLayer, (0, 0))
            self.Layer.blit(newLayer, (oldLayer.get_width(), 0))
            
        if y > 0:
            newLayer = self.generateSurface(x0, x3, y0, y3+y)
            oldLayer = self.Layer
            self.Layer = pygame.Surface((oldLayer.get_width(), oldLayer.get_height() + zoomY*y), pygame.SRCALPHA, 32)
            self.Layer = self.Layer.convert_alpha()
            self.Layer.blit(newLayer, (0, 0))
            self.Layer.blit(oldLayer, (0, newLayer.get_height()))

        if y < 0:
            y = abs(y)
            newLayer = self.generateSurface(x0, x3, y0-y, y3)
            oldLayer = self.Layer
            self.Layer = pygame.Surface((oldLayer.get_width(), oldLayer.get_height() + newLayer.get_height()), pygame.SRCALPHA, 32)
            self.Layer = self.Layer.convert_alpha()
            self.Layer.blit(oldLayer, (0, 0))
            self.Layer.blit(newLayer, (0, oldLayer.get_height()))
        
main()
