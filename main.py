import tkinter as tk
from tkinter import messagebox
from mido import MidiFile, MidiTrack, Message
import pygame
import os

# Initialize pygame for MIDI playback
pygame.mixer.init()

# Function to convert note names to MIDI numbers
def generate_note_to_midi():
    note_mapping = {}
    base_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    for octave in range(0, 8):  # MIDI supports octaves from 0 to 7
        for i, note in enumerate(base_notes):
            midi_number = 12 * (octave + 1) + i
            note_name = f"{note}{octave}"
            note_mapping[note_name] = midi_number
    return note_mapping

# Generate the full note-to-MIDI mapping
note_to_midi = generate_note_to_midi()

# Function to create MIDI file (temporary or permanent)
def create_midi_file(notes, filename, tempo, note_duration, is_preview=False):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Program change to piano sound (default instrument)
    track.append(Message('program_change', program=0, time=0))

    # Define note durations in ticks
    duration_mapping = {
        'Quarter Note': 480,
        'Half Note': 960,
        'Whole Note': 1920
    }

    note_ticks = duration_mapping[note_duration]

    # Split notes by commas
    note_pairs = [pair.strip() for pair in notes.split(',')]

    for note_pair in note_pairs:
        try:
            note1, note2 = note_pair.split()  # Split note pair by space
            if note1 in note_to_midi and note2 in note_to_midi:
                track.append(Message('note_on', note=note_to_midi[note1], velocity=64, time=0))
                track.append(Message('note_off', note=note_to_midi[note1], velocity=64, time=note_ticks))
                track.append(Message('note_on', note=note_to_midi[note2], velocity=64, time=0))
                track.append(Message('note_off', note=note_to_midi[note2], velocity=64, time=note_ticks))
            else:
                messagebox.showerror("Error", f"Invalid note: {note1} or {note2}")
                return
        except ValueError:
            messagebox.showerror("Error", f"Invalid note pair: {note_pair}")
            return

    # If this is a preview, save to a temporary file
    if is_preview:
        temp_file = "temp_preview.mid"
        mid.save(temp_file)
        return temp_file
    else:
        # Save the MIDI file
        mid.save(f"{filename}.mid")
        messagebox.showinfo("Success", f"MIDI file saved as {filename}.mid")
        return None

# Function to handle button click for saving the MIDI
def generate_midi():
    notes = entry_notes.get()
    filename = entry_filename.get()
    tempo = entry_tempo.get()
    note_duration = duration_var.get()

    if not notes or not filename or not tempo or not note_duration:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    create_midi_file(notes, filename, tempo, note_duration)

# Function to handle preview
def preview_midi():
    notes = entry_notes.get()
    tempo = entry_tempo.get()
    note_duration = duration_var.get()

    if not notes or not tempo or not note_duration:
        messagebox.showerror("Error", "All fields are required for preview!")
        return

    # Create the preview MIDI file
    temp_midi_file = create_midi_file(notes, "preview", tempo, note_duration, is_preview=True)

    if temp_midi_file:
        # Play the MIDI file using pygame
        try:
            pygame.mixer.music.load(temp_midi_file)
            pygame.mixer.music.play()

            # Delete the temp file after playback finishes
            while pygame.mixer.music.get_busy():
                root.update()  # Use root.update() to keep the UI responsive
                pygame.time.Clock().tick(10)

            os.remove(temp_midi_file)  # Clean up the temporary MIDI file after playback
        except pygame.error as e:
            messagebox.showerror("Error", f"Unable to play MIDI: {e}")

# Function to draw the note pair on the canvas
def draw_note_pair(note1, note2, x, y):
    # Simple text representation of notes
    canvas.create_text(x, y, text=note1, font=("Arial", 16))
    canvas.create_text(x, y + 20, text=note2, font=("Arial", 16))

# Function to add notes to the canvas
def add_note_pair():
    note1 = entry_note1.get()
    note2 = entry_note2.get()
    
    if note1 in note_to_midi and note2 in note_to_midi:
        # Draw the notes on the canvas
        x = 50 + (len(note_pairs) * 100)  # Increment x position based on number of notes
        y = 50
        draw_note_pair(note1, note2, x, y)

        # Add the note pair to the sequence
        note_pairs.append(f"{note1} {note2}")
        
        # Update the notes entry with the new sequence
        entry_notes.delete(0, tk.END)
        entry_notes.insert(0, ', '.join(note_pairs))
    else:
        messagebox.showerror("Error", "Invalid note names!")

# Set up the main window
root = tk.Tk()
root.title("MIDI File Creator with Canvas")
root.configure(cursor="arrow")  # Set default cursor to arrow

# Create a canvas for note visualization
canvas = tk.Canvas(root, width=800, height=200, bg="white")
canvas.pack()

# List to hold note pairs
note_pairs = []

# Entry fields for individual note inputs
label_note1 = tk.Label(root, text="Enter Note 1:")
label_note1.pack()

entry_note1 = tk.Entry(root, width=10)
entry_note1.pack()
entry_note1.bind("<FocusIn>", lambda event: entry_note1.select_range(0, tk.END))
entry_note1.focus_set()  # Set initial focus to this entry field

label_note2 = tk.Label(root, text="Enter Note 2:")
label_note2.pack()

entry_note2 = tk.Entry(root, width=10)
entry_note2.pack()
entry_note2.bind("<FocusIn>", lambda event: entry_note2.select_range(0, tk.END))

# Button to add the note pair to the canvas and note sequence
add_note_button = tk.Button(root, text="Add Note Pair", command=add_note_pair)
add_note_button.pack()
add_note_button.bind("<Return>", lambda event: add_note_pair())  # Allow pressing Enter to add

# Entry fields for final note sequence, file name, and tempo
label_notes = tk.Label(root, text="Final Note Sequence:")
label_notes.pack()

entry_notes = tk.Entry(root, width=50)
entry_notes.pack()

label_filename = tk.Label(root, text="Enter Output File Name:")
label_filename.pack()

entry_filename = tk.Entry(root, width=50)
entry_filename.pack()
entry_filename.bind("<FocusIn>", lambda event: entry_filename.select_range(0, tk.END))

label_tempo = tk.Label(root, text="Enter Tempo (BPM):")
label_tempo.pack()

entry_tempo = tk.Entry(root, width=50)
entry_tempo.pack()
entry_tempo.bind("<FocusIn>", lambda event: entry_tempo.select_range(0, tk.END))

# Dropdown menu for selecting note duration
label_duration = tk.Label(root, text="Select Note Duration:")
label_duration.pack()

duration_var = tk.StringVar(value="Quarter Note")  # Default value is Quarter Note
dropdown_duration = tk.OptionMenu(root, duration_var, "Quarter Note", "Half Note", "Whole Note")
dropdown_duration.pack()

# Button to generate MIDI file
generate_button = tk.Button(root, text="Generate MIDI", command=generate_midi)
generate_button.pack()
generate_button.bind("<Return>", lambda event: generate_midi())  # Allow pressing Enter to generate

# Button to preview MIDI file
preview_button = tk.Button(root, text="Preview MIDI", command=preview_midi)
preview_button.pack()
preview_button.bind("<Return>", lambda event: preview_midi())  # Allow pressing Enter to preview

# Start the main loop
root.mainloop()

