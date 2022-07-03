from tkinter import *
from PIL import ImageTk,Image

import sqlite3
import time
import os
import sys
from random import choice
from pathlib import Path

# R: I have no idea what the heck this is, but it fixes the no $DISPLAY problem
if os.environ.get('DISPLAY', '') == '':
    #print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


# R: Initializes the tkinter menu and establishes connection with clothing database
def init():
    # R: Initial almighty tkinter window object
    root = Tk()
    root.title('Laundry Tracker Zero')
    
    ## Note ##
    # R: root.winfo_screenwidth() or root.winfo_screenheight() gets full width/height.
    # R: X-axis starts from the very left and goes to the very right (root.winfo_screenwidth)
    full_width = root.winfo_screenwidth()
    full_height = root.winfo_screenheight()

    ## Comment ##
    # R: Configuring the main screen dimensions and location
    width = int(full_width / 3) # 1/3 width
    height = int(2 * (full_height / 3)) # 2/3 height
    xaxis = int((full_width/2) - (width/2)) # full - half screen - half width of widget
    yaxis = int((full_height/2) - (height/2)) # full - half screen - half height of widget
    root.geometry(f"{width}x{height}+{xaxis}+{yaxis}")
    
    # R: Butterfly Wordart 
    #wordart_image = PhotoImage(file='assets/butterfly_perfect1.png')
    #wordart_label = Label(root, image=wordart_image)
    #wordart_label.place(x=230, y=0, relwidth=1, relheight=.4)
    
    # R: Butterfly cartoon
    #butterfly_image = PhotoImage(file='assets/butterfly_glitch.png')
    #butterfly_label = Label(root, image=butterfly_image)
    #butterfly_label.place(x=235, y=220, relwidth=.4, relheight=.4)
    
    # R: Checking to see if there is a database and creating one if there is not 
    # R: Creating file or getting file if it already exists
    filePath = 'clothes.db'
    path = Path(filePath)
    if path.is_file():
        print(f'Clothing found at {path}')
    else:
        print('Clothing file not found. Creating clothes.db file')

    # R: Creates the file only if it does not exist
    path.touch(exist_ok=True)
    
    # R: Creating table within file if not found in the file
    conn = sqlite3.connect('clothes.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS clothes (
		cloth_name text,
		article text,
        outerwear boolean,
        tempurature integer,
        formality integer,
		dirty boolean
		)""")

    ######### R: Variable Trackers #########
    # R: Values to be passed into the generate clothes function for optional/conditional functionality
    # R: These pyvars must be "getted" ie. outerwear_choice.get()
    article_choice = StringVar()
    article_choice.set(None)
    temp_choice = IntVar()
    temp_choice.set(0)
    formality_choice = IntVar()
    formality_choice.set(0)
    outerwear_choice = BooleanVar()
    outerwear_choice.set(0)
    dirty_choice = BooleanVar()
    dirty_choice.set(0)

    ######### R: Labels and Entries (Add Clothes config) #########

    # R: Clothing Name section
    cloth_name = Entry(root, width=20)
    cloth_name.grid(row=0, column=1, padx=(0,50), pady=(10, 0))
    cloth_name_label = Label(root, text="Clothing Name")
    cloth_name_label.grid(row=0, column=0, padx=(10,0), pady=(10, 0))

    # R: Article Section
    article = Entry(root, width=20)
    article.grid(row=1, column=1, padx=(0,50))
    article_label = Label(root, text="Article")
    article_label.grid(row=1, column=0, padx=(10,0))

    # R: Outerwear Section
    outerwear_radio = Radiobutton(root, text="Outerwear", variable=outerwear_choice, value=1)
    outerwear_radio.grid(row=2, column=1,padx=(0, 50))
    outerwear_label = Label(root, text="Outerwear")
    outerwear_label.grid(row=2, column=0, padx=(10,0))

    # R: Tempurature Section
    tempurature = Entry(root, width=20)
    tempurature.grid(row=3, column=1, padx=(0,50))
    tempurature_label = Label(root, text="Tempurature (1-5)")
    tempurature_label.grid(row=3, column=0, padx=(10,0))

    # R: Formality Section
    formality = Entry(root, width=20)
    formality.grid(row=4, column=1, padx=(0,50))
    formality_label = Label(root, text="Formality (1-3)")
    formality_label.grid(row=4, column=0, padx=(10,0))

    # R: Dirty Section
    dirty_radio = Radiobutton(root, text="Dirty", variable=dirty_choice, value=1)
    dirty_radio.grid(row=5, column=1,padx=(0, 50))
    dirty_label = Label(root, text="Dirty")
    dirty_label.grid(row=5, column=0, padx=(10,0))

    # R: Add photo Section
	file_explorer_label = Label(root, text = "Add Photo from file")
	file_explorer_label.grid(row=6, column=0, padx=(10,0))
  
      
	file_explorer = Button(root,
                        text = "Browse Files",
                        command = browseFiles)
    
    

    ######### R: Remove Section #########

    # R: Remove section
    # R: There should be three spaces between the labels above and the bottom ones below. Between the bottom ones, there should be two spaces.
    # R: And then again there should be two spaces between the ones below that 
    delete_box_label = Label(root, text="Delete Cloth Name")
    # R: ALL THE WIDGETS ARE DEPENDENT ON THIS LABEL FOR THE ALIGNMENT (padx = (x,0))
    delete_box_label.grid(row=11, column=0, pady=5, padx=(60,0))
    delete_box = Entry(root, width=20)
    delete_box.grid(row=11, column=1, pady=5, padx=(0,50))


    ######### R: Edit Section #########
    
    # R: Edit section
    edit_box_label = Label(root, text="Edit Cloth Name")
    edit_box_label.grid(row=13, column=0, pady=5, padx=(45,0))
    edit_box = Entry(root, width=20)
    edit_box.grid(row=13, column=1, pady=5, padx=(0,50))
    

    ######### R: Generate Section #########

    # R: Create Radio Buttons
    hoodie_radio = Radiobutton(root, text="Hoodie?", variable=outerwear_choice, value="Hoodie")
    hoodie_radio.grid(row=15, column=0, pady=5, padx=(135,0))
    jacket_radio = Radiobutton(root, text="Jacket?", variable=outerwear_choice, value="Jacket")
    jacket_radio.grid(row=15, column=1, pady=5, padx=(0,120))
    hot_radio = Radiobutton(root, text="Hot", variable=temp_choice, value=1)
    hot_radio.grid(row=17, column=0, padx=(75,0))
    room_temp_radio = Radiobutton(root, text="Room Temp", variable=temp_choice, value=2)
    room_temp_radio.grid(row=18, column=0, padx=(131,0))
    cold_radio = Radiobutton(root, text="Cold", variable=temp_choice, value=3)
    cold_radio.grid(row=19, column=0, padx=(81,0))
    very_cold_radio = Radiobutton(root, text="Very Cold", variable=temp_choice, value=4)
    very_cold_radio.grid(row=20, column=0, padx=(115,0))
    
    ######### R: Buttons #########

    # R: Ordering:
       # R: Add
       # R: Remove
       # R: Edit
       # R: Generate
    # R: ipadx means *inner* padding of the button (x-axis-wise)

    # R: Create Submit Button
    submit_btn = Button(root, text="Add Clothes To Database", command=lambda : submit(cloth_name, article, outerwear_choice, tempurature, formality, dirty_choice))
    submit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=80, ipadx=100)

    #Create A Delete Button
    delete_btn = Button(root, text="Remove Clothing from Database", command=lambda : delete())
    delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=75)

    # R: Create an Edit Button
    edit_btn = Button(root, text="Edit Clothing", command=lambda : edit())
    edit_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=140)

    # R: Create a Generate Button
    generate_btn = Button(root, text="Generate Clothes to Wear", command=lambda : generate(outerwear_choice.get(), temp_choice.get()))
    generate_btn.grid(row=14, column=0, columnspan=2, pady=10, padx=10, ipadx=98)

    # R: Commit Changes and quit.
    conn.commit()
    conn.close()
    
    # R: Executes the tkinter display
    root.mainloop()

# R: Create Update function to update a record
# R: Auxillary function that does not show a window, only updates the sql database
def update():

	# R: Create a database or connect to one
	conn = sqlite3.connect('clothes.db')
        
	# R: Create cursor
	c = conn.cursor()

	record_id = edit_box.get()

	c.execute("""UPDATE clothes SET
		cloth_name = :cloth_name,
		article = :article,
		outerwear = :outerwear,
        tempurature = :tempurature,
        formality = :formality,
		dirty= :dirty 

		WHERE cloth_name = :target_cloth""",
		{
		'cloth_name': cloth_name_editor.get(),
		'article': article_editor.get(),
		'outerwear': outerwear_editor.get(),
        'tempurature': tempurature_editor.get(),
        'formality': formality_editor.get(),
		'dirty': dirty_editor.get(),
		'target_cloth': target_cloth
		})

	#Commit Changes
	conn.commit()

	# R: Close Connection and editor window
	conn.close()
	editor.destroy()

# R: Create function to mark the chosen clothes dirty
def mark_dirty(con, generator, dirty_clothes):

    c = con.cursor()

    # R: Marking the outerwear dirty if it was included in the chosen clothes (with Outerwear)
    if(len(dirty_clothes) > 4):
        c.execute("""UPDATE clothes SET
            dirty = 1
            WHERE cloth_name IN (:outerwear, :top, :undies, :bottom, :sock)""",
        {
                'outerwear': dirty_clothes[0],
                'top': dirty_clothes[1],
                'undies': dirty_clothes[2],
                'bottom': dirty_clothes[3],
                'sock': dirty_clothes[4]
        })

    # R: Marking the outerwear dirty if it was included in the chosen clothes (without Outerwear)
    else:
        c.execute("""UPDATE clothes SET
            dirty = 1
            WHERE cloth_name IN (:top, :undies, :bottom, :sock)""",
        {
                'top': dirty_clothes[0],
                'undies': dirty_clothes[1],
                'bottom': dirty_clothes[2],
                'sock': dirty_clothes[3]
        })

    # R: CONN BUG (Do we want to close() here?)
    # R: Commit
    con.commit()
    generator.destoy()


# R: Create Edit function to update a record (this creates a second window)
def edit():
    global editor
    editor = Tk()
    editor.title('Update Clothing')
    editor.geometry("400x300")
    # R: Create a database or connect to one
    conn = sqlite3.connect('clothes.db')
    # R: Create cursor
    c = conn.cursor()
    
    global target_cloth
    target_cloth = edit_box.get()
    # R: Query the database
    c.execute("SELECT * FROM clothes WHERE cloth_name = :target_cloth", {"target_cloth": target_cloth})
    clothing = c.fetchall()
    
    #Create Global Variables for text box names
    global cloth_name_editor
    global article_editor
    global outerwear_editor
    global tempurature_editor
    global formality_editor
    global dirty_editor

    ######### R: Labels and Entries (Edit clothes Config) #########

    # R: cloth_name section
    cloth_name_editor = Entry(editor, width=30)
    cloth_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    cloth_name_label = Label(editor, text="Clothing Name")
    cloth_name_label.grid(row=0, column=0, pady=(10, 0))

    # R: article section
    article_editor = Entry(editor, width=30)
    article_editor.grid(row=1, column=1)
    article_label = Label(editor, text="Article")
    article_label.grid(row=1, column=0)

    # R: outerwear section
    outerwear_editor = Entry(editor, width=30)
    outerwear_editor.grid(row=2, column=1)
    outerwear_label = Label(editor, text="Outerwear?")
    outerwear_label.grid(row=2, column=0)

    # R: tempurature section
    tempurature_editor = Entry(editor, width=30)
    tempurature_editor.grid(row=3, column=1)
    tempurature_label = Label(editor, text="Tempurature Level?")
    tempurature_label.grid(row=3, column=0)

    # R: formality section
    formality_editor = Entry(editor, width=30)
    formality_editor.grid(row=4, column=1)
    formality_label = Label(editor, text="Formality")
    formality_label.grid(row=4, column=0)

    # R: dirty section
    dirty_editor = Entry(editor, width=30)
    dirty_editor.grid(row=5, column=1)
    dirty_label = Label(editor, text="Dirty?")
    dirty_label.grid(row=5, column=0)
    
    # R: Display the cloth to be edited
    for cloth in clothing:
     cloth_name_editor.insert(0, cloth[0])
     article_editor.insert(0, cloth[1])
     outerwear_editor.insert(0, cloth[2])
     tempurature_editor.insert(0, cloth[3])
     formality_editor.insert(0, cloth[4])
     dirty_editor.insert(0, cloth[5])
    
    # R: STYLE BUG
    # R: Does nothing currently with the settings above 
    # R: Create a Save Button To Save edited record
    edit_btn = Button(editor, text="Update Cloth", command=update)
    edit_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

# R: Redo the query with different random numbers
def redo(con, generator):
    con.close()
    generator.destroy()
    generate(outerwear_choice.get())

# R: If there are no clean clothes
def no_clean_clothes():
    ew = Tk()
    ew.title('Do your Laundry')
    ew.geometry("500x500")
    nasty = Label(ew, text="You have no clean clothes you stinker!")
    nasty.place(relx=.5, rely=.5, anchor="center")

# R: Function for handling the read of the file from the file browser
def retrieveFile():
	curr_dir = os.getcwd()
	filename = filedialog.askopenfilename(initialdir = curr_dir,
                                          title = "Select a File",
                                          filetypes = (("Text files", "*.txt*"),
                                                       ("all files", "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)


# R: Generate the clothing and ask again if disapproved. If approved mark dirty.
def generate(outerwear_choice, temp_choice):
    global generator
    generator = Tk()
    generator.title('Produced Clothing')
    # R: Full Screen vvvvvvv
    #generator.geometry(f"{width}x{height}+0+0")
    generator.geometry("400x300")
    # R: Create a database or connect to one
    conn = sqlite3.connect('clothes.db')
    # R: Create cursor
    c = conn.cursor()
    
    # R: Query the database for clean clothes 
    c.execute("SELECT * FROM clothes WHERE dirty == 0")

    # R: Checking to see if there was any clean clothing found in db
    clothing = c.fetchall()
    if not clothing:
        conn.close()
        no_clean_clothes()
        generator.destroy()
        return

    ### R: TODO ###
    # R: Implement the "Classic Outfits" option. (changing the query may be more efficient than looping)
    # R: Perhaps we should think about choosing between showing partial outfits if certain sections of clothing are all dirty. Or 
    # R: just completely denying if there are no clothes to suggest for any section. (there will be an error if we try to use random.choice)
    # R: Outerwear and Outfit specification are optional.
    # R: If outerwear is selected, then you should run "choice", if not, just set outerwear to "No Outerwear"
    # R: The outerwear_choice variable will be equal to the STRING "None" if it is not selected.
    # R: Tuple Structure
    # R: cloth_name cloth[0]
    # R: article cloth[1]
    # R: outerwear cloth[2]
    # R: tempurature cloth[3]
    # R: formality cloth[4]
    # R: dirty cloth[5]



    # R: Randomly selecting outerwear that is a [Jacket, Hoodie, Coat, etc.]
    if(outerwear_choice != "None"):
        outerwear = choice([cloth[0] for cloth in clothing if cloth[1] == outerwear_choice])
    else:
        outerwear = "No Outerwear"

    # R: If tempurature choice is not wildcard 0, we get only that
    # R: tempuratrue choice for any clothing that will be selected.
    if(temp_choice > 0):
        clothing = [cloth for cloth in clothing if cloth[6] == temp_choice]

    # R: Selecting and putting one outfit together into an outfit
    top = choice([cloth[0] for cloth in clothing if cloth[1] == "Top"])
    undies = choice([cloth[0] for cloth in clothing if cloth[1] == "Undies" ])
    bottom = choice([cloth[0] for cloth in clothing if cloth[1] == "Bottom" ])
    sock = choice([cloth[0] for cloth in clothing if cloth[1] == "Socks"])
    outfit_chosen = [outerwear, top, undies, bottom, sock]
    
    # R: Create Text Labels
    outerwear_name_label = Label(generator, text=outerwear)
    outerwear_name_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))
    top_name_label = Label(generator, text=top)
    top_name_label.grid(row=1, column=0, columnspan=2)
    undies_name_label = Label(generator, text=undies)
    undies_name_label.grid(row=2, column=0, columnspan=2)
    bottom_name_label = Label(generator, text=bottom)
    bottom_name_label.grid(row=3, column=0, columnspan=2)
    sock_name_label = Label(generator, text=sock)
    sock_name_label.grid(row=4, column=0, columnspan=2)
    
    # R: Create a Save Button To Save edited record
    # R: You MUST use a lambda function when setting the command for some reason, or else it will run the command function,
    # R: even without pressing any of the buttons.
    approve_btn = Button(generator, text="Approve?", command=lambda : mark_dirty(conn, generator, outfit_chosen))
    approve_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=125)
    disapprove_btn = Button(generator, text="Disapprove?", command=lambda : redo(conn, generator))
    disapprove_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=115)

# R: Create Function to Delete A Record
def delete():
    # R: Clear the delete box
	delete_box.delete(0, END)

    # R: Get cursor
	conn = sqlite3.connect('clothes')
	c = conn.cursor()

	# R: Delete a record.
	c.execute("DELETE from clothes WHERE cloth_name = " + remove_box.get())

    # R: Commit and quit.
	conn.commit()
	conn.close()


def validateSubmission(cloth_name, article, outerwear_choice, tempurature, formality, dirty_choice):
    # R: NOTE: You should parse tempurature and formality into integer since they are text boxes.
    # R: Validate article
    valid_articles = [
                        "Sweater",
                        "Hoodie",
                        "T-Shirt",
                        "Flip-flops",
                        "Shorts",
                        "Pants",
                        "Jeans",
                        "Sneakers",
                        "Shoes",
                        "Coat",
                        "Blazer",
                        "Cap",
                        "Beanie",
                        "Socks",
                        "Shirts",
                        "Scarf",
                        "Swimsuit",
                        "Jacket",
                        "Boots",
                        "Polo"]
    if article.get() not in valid_articles:
        print("Invalid article in submission", file=sys.stderr)
        print(f'Expected one of the articles and was given {article.get()}')
        return False
    
    # R: Validate outerwear
    if outerwear_choice.get() not in [0, 1]:
        print("Invalid outerwear_choice in submission", file=sys.stderr)
        print(f'Expected [0, 1] and was given {outerwear_choice.get()}')
        return False

    # R: Validate tempurature
    if int(tempurature.get()) not in [1, 2, 3, 4, 5]:
        print("Invalid tempurature in submission", file=sys.stderr)
        print(f'Expected [1, 2, 3, 4, 5] and was given {tempurature.get()}')
        return False

    # R: Validate formality
    if int(formality.get()) not in [1, 2, 3]:
        print("Invalid formality in submission", file=sys.stderr)
        print(f'Expected [1, 2, 3] and was given {formality.get()}')
        return False

    # R: Validate dirty_choice
    if dirty_choice.get() not in [0, 1]:
        print("Invalid dirty_choice in submission", file=sys.stderr)
        print(f'Expected [0, 1] and was given {dirty_choice.get()}')
        return False

    return True
    

# R: This is the initially open window
# R: Create Submit Function For database
def submit(cloth_name, article, outerwear_choice, tempurature, formality, dirty_choice):

        # R: Validate the submission (validation will print errors)
        if not validateSubmission(cloth_name, article, outerwear_choice, tempurature, formality, dirty_choice):
            return

        # R: Create a database or connect to one
        conn = sqlite3.connect('clothes.db')
        c = conn.cursor()
        
        # R: Insert Into Table
        c.execute("INSERT INTO clothes VALUES (:cloth_name, :article, :outerwear, :tempurature, :formality, :dirty)",
        {
            'cloth_name': cloth_name.get(),
            'article': article.get(),
            'outerwear': outerwear_choice.get(),
            'tempurature': int(tempurature.get()),
            'formality': int(formality.get()),
            'dirty': dirty_choice.get()
        })
        
        
        # R: Commit Changes
        conn.commit()
        
        # R: Close Connection 
        conn.close()
        
        # R: Clear The Text Boxes
        cloth_name.delete(0, END)
        article.delete(0, END)
        tempurature.delete(0, END)
        formality.delete(0, END)

        # R: Clear the radio buttons
        outerwear_choice.set(0)
        dirty_choice.set(0)

# R: Not very useful right now
# R: Create Query Function
#def query():
#
#	# R: Create a database or connect to one
#	conn = sqlite3.connect('clothes.db')
#
#	# R: Create cursor
#	c = conn.cursor()
#
#	# R: Query the database
#	c.execute("SELECT * FROM clothes")
#	records = c.fetchall()
#	print(records)
#
# R:        ### R: TODO ###
# R:        # R: Temporarily commenting this out so I can see which indexes I should access before I display them
#	# R: Loop Thru Results
#	#print_records = ''
#	#for record in records:
#	#	print_records += str(record[0]) + " " + str(record[1]) + " " + "\t" +str(record[6]) + "\n"
#
#	#query_label = Label(root, text=print_records)
#	#query_label.grid(row=12, column=0, columnspan=2)
#
#	#Commit Changes
#	conn.commit()
#
#	# R: Close Connection 
#	conn.close()


if __name__ == "__main__":
    init()
