from tkinter import *
from tkinter import messagebox
from MySpaceDecisionTree import MySpaceDecisionTree

# ----------------------------------------------------------
# CREATE MAIN WINDOW
# ----------------------------------------------------------
window = Tk()
window.geometry("650x950")
window.title("Space Landing Safety Predictor")

# Create Decision Tree object
decisionTree = MySpaceDecisionTree()

# ----------------------------------------------------------
# BUTTON FUNCTIONS
# ----------------------------------------------------------

def trainData():
    try:
        newSeedValue = int(seedsVar.get())
        decisionTree.updateSeed(newSeedValue)
        decisionTree.trainData()
        messagebox.showinfo("Training Complete", "Model trained successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def testData():
    text.delete("1.0", "end")
    try:
        text.insert(END, decisionTree.readCategories() + "\n\n")

        matrix, accuracy = decisionTree.testData()

        text.insert(END, "Confusion Matrix:\n")
        text.insert(END, f"{matrix[0]}\n")
        text.insert(END, f"{matrix[1]}\n\n")
        text.insert(END, f"Accuracy: {round(accuracy * 100, 2)}%\n")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def makeNewPrediction():
    try:
        # Convert atmosphere dropdown into numerical scoring system
        atmosphere_map = {"Good": 7, "Moderate": 5, "Bad": 2}
        atmosphere = atmosphere_map[atmosphereVar.get()]

        temperature = int(entryTemp.get())
        gravity = float(entryGravity.get())
        radiation = float(entryRadiation.get())
        magnetic = float(entryMagnetic.get())
        wind = float(entryWind.get())
        toxicity = float(entryToxicity.get())

        prediction = decisionTree.makePrediction(
            atmosphere, temperature, gravity,
            radiation, magnetic, wind, toxicity
        )

        result = "SAFE to Land" if prediction == 1 else "UNSAFE to Land"

        entryResult.delete(0, END)
        entryResult.insert(END, result)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------------------------------------------------------
# GUI LAYOUT
# ----------------------------------------------------------

frame = Frame(window, width=600, height=850)
frame.place(x=25, y=120)

label0 = Label(window, text="Space Landing Safety Predictor",
               fg="white", bg="darkblue",
               font=("Arial", 20, "bold"))
label0.place(x=120, y=30)

label01 = Label(window, text="Select Seed Value for Random Training",
                fg="red", font=("Arial", 12, "bold"))
label01.place(x=120, y=80)

# ----------------------------------------------------------
# SEED DROPDOWN
# ----------------------------------------------------------

label1 = Label(frame, text="Seed Value",
               fg="blue", font=("Arial", 12, "bold"))
label1.grid(row=0, column=0, sticky=W)

seedsVar = StringVar()
seedsVar.set("1")

seedOptions = ["1", "2", "3", "4", "5"]
combo1 = OptionMenu(frame, seedsVar, *seedOptions)
combo1.grid(row=0, column=1, sticky=W)

# ----------------------------------------------------------
# TRAIN & TEST BUTTONS
# ----------------------------------------------------------

button1 = Button(frame, text="Train Model",
                 font=("Arial", 12, "bold"),
                 command=trainData)
button1.grid(row=1, column=0, pady=10, sticky=W+E)

button2 = Button(frame, text="Test Model",
                 font=("Arial", 12, "bold"),
                 command=testData)
button2.grid(row=1, column=1, pady=10, sticky=W+E)

# ----------------------------------------------------------
# OUTPUT BOX
# ----------------------------------------------------------

label3 = Label(frame, text="Model Output",
               fg="blue", font=("Arial", 12, "bold"))
label3.grid(row=2, column=0, pady=10, sticky=W)

text = Text(frame, height=10, width=45)
text.grid(row=2, column=1, ipadx=80)

# ----------------------------------------------------------
# NEW PREDICTION SECTION
# ----------------------------------------------------------

label03 = Label(frame, text="Enter New Planet Conditions",
                fg="darkgreen", font=("Arial", 14, "bold"))
label03.grid(row=4, column=0, columnspan=2, pady=20, sticky=W+E)

# ATMOSPHERE
labelA = Label(frame, text="Atmosphere Quality",
               fg="blue", font=("Arial", 12, "bold"))
labelA.grid(row=5, column=0, sticky=W)

atmosphereVar = StringVar()
atmosphereVar.set("Moderate")

atmOptions = ["Good", "Moderate", "Bad"]
comboA = OptionMenu(frame, atmosphereVar, *atmOptions)
comboA.grid(row=5, column=1, sticky=W)

# TEMPERATURE
labelT = Label(frame, text="Temperature (°C)",
               fg="blue", font=("Arial", 12, "bold"))
labelT.grid(row=6, column=0, sticky=W)

entryTemp = Entry(frame)
entryTemp.grid(row=6, column=1)

# GRAVITY
labelG = Label(frame, text="Gravity (m/s²)",
               fg="blue", font=("Arial", 12, "bold"))
labelG.grid(row=7, column=0, sticky=W)

entryGravity = Entry(frame)
entryGravity.grid(row=7, column=1)

# RADIATION
labelR = Label(frame, text="Radiation Level",
               fg="blue", font=("Arial", 12, "bold"))
labelR.grid(row=8, column=0, sticky=W)

entryRadiation = Entry(frame)
entryRadiation.grid(row=8, column=1)

# MAGNETIC FIELD
labelM = Label(frame, text="Magnetic Field Strength",
               fg="blue", font=("Arial", 12, "bold"))
labelM.grid(row=9, column=0, sticky=W)

entryMagnetic = Entry(frame)
entryMagnetic.grid(row=9, column=1)

# WIND
labelW = Label(frame, text="Wind Speed",
               fg="blue", font=("Arial", 12, "bold"))
labelW.grid(row=10, column=0, sticky=W)

entryWind = Entry(frame)
entryWind.grid(row=10, column=1)

# TOXICITY
labelX = Label(frame, text="Toxicity Level",
               fg="blue", font=("Arial", 12, "bold"))
labelX.grid(row=11, column=0, sticky=W)

entryToxicity = Entry(frame)
entryToxicity.grid(row=11, column=1)

# PREDICTION BUTTON
button3 = Button(frame, text="Predict Landing Safety",
                 font=("Arial", 12, "bold"),
                 command=makeNewPrediction)
button3.grid(row=12, column=0, pady=20, sticky=W+E)

entryResult = Entry(frame, font=("Arial", 14, "bold"))
entryResult.grid(row=12, column=1, sticky=W+E)

# ----------------------------------------------------------
# START GUI LOOP
# ----------------------------------------------------------
window.mainloop()
