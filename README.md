# pythonMusicMaker
## Musical Interval Midi Creation Tool

This project is a Python application that allows users to create MIDI files by visually adding note pairs through a simple graphical user interface (GUI). The application includes features for drawing the notes on a canvas, previewing the sequence, and generating MIDI files. The interface is built using `tkinter`, and MIDI file generation and playback are managed using the `mido` and `pygame` libraries.

## Features
- **Interactive Canvas**: Users can add note pairs which are displayed on a canvas for easy visualization.
- **MIDI Generation**: The application can generate MIDI files based on the note sequence provided by the user.
- **Playback Preview**: Users can preview the MIDI sequence before saving it.
- **User-Friendly GUI**: Built using `tkinter`, providing a simple and intuitive way to create music.

## Installation

### Prerequisites
- Python 3.6 or higher
- Required Python libraries:
  - `tkinter` (usually included with Python)
  - `mido` and `python-rtmidi` for MIDI file generation
  - `pygame` for MIDI playback

### Installation Steps
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/midi-file-creator.git
   cd midi-file-creator
   ```

2. Install the required libraries:
   ```sh
   pip install mido python-rtmidi pygame
   ```

## Usage
1. Run the Python script:
   ```sh
   python midi_creator_with_canvas.py
   ```

2. Enter the note pairs using the provided input fields (`Note 1` and `Note 2`).
   - Click **Add Note Pair** to add the pair to the canvas and build the sequence.

3. Set the **Tempo** and **Note Duration** using the provided fields.

4. Click **Preview MIDI** to listen to the sequence before saving.

5. Click **Generate MIDI** to save the sequence as a `.mid` file.

## Example
- **Note Input**: Enter note pairs like `C4 C#4`, `D4 E4`, etc.
- **Visual Feedback**: The canvas will display each note pair as you add them, allowing you to visualize the sequence.
- **File Saving**: After previewing, enter a filename and click **Generate MIDI** to save your work.

## File Structure
- `midi_creator_with_canvas.py`: The main Python script for running the MIDI File Creator application.

## Dependencies
- `tkinter`: Used for GUI creation.
- `mido` and `python-rtmidi`: Used to create and manipulate MIDI files.
- `pygame`: Used to provide MIDI playback for previewing the notes before saving.

## Contributing
Feel free to contribute to the project by submitting issues or pull requests. Any enhancements, bug fixes, or suggestions are welcome!

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any questions or suggestions, please contact hello at nusu dot app.

