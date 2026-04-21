import customtkinter as ctk
import threading
import pygame
import os
import time
import numpy as np
from music21 import stream, note

# Deep Neon Blue Theme Colors
MIDNIGHT_BLUE = "#0A192F"
NEON_BLUE = "#00D2FF"
SOFT_GLOW = "#112240"
TEXT_WHITE = "#E6F1FF"
GLOW_GREEN = "#39FF14"

class MusicAIGenerationFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        # --- UPDATE: Header Corner Text ---
        self.title("CODEALPHA - MUSIC GEN AI STUDIO")
        self.geometry("820x720")
        self.configure(fg_color=MIDNIGHT_BLUE)
        pygame.mixer.init()

        # Header Title
        self.label = ctk.CTkLabel(self, text="MUSIC AI GENERATION", 
                                 font=("Trebuchet MS", 40, "bold"), 
                                 text_color=NEON_BLUE)
        self.label.pack(pady=20)

        # Mood Selector
        self.mood_label = ctk.CTkLabel(self, text="Select AI Composition Mood:", text_color=TEXT_WHITE, font=("Arial", 14))
        self.mood_label.pack()
        
        self.mood_opt = ctk.CTkSegmentedButton(self, values=["Cyberpunk", "Deep Space", "Ambient"],
                                              selected_color=NEON_BLUE, unselected_color=SOFT_GLOW,
                                              font=("Arial", 12))
        self.mood_opt.set("Ambient")
        self.mood_opt.pack(pady=10)

        # Waveform Visualizer
        self.viz_frame = ctk.CTkFrame(self, fg_color=SOFT_GLOW, corner_radius=15, border_color=NEON_BLUE, border_width=1)
        self.viz_frame.pack(pady=10, padx=40, fill="both")
        
        self.wave_text = ctk.CTkLabel(self.viz_frame, text="▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂", 
                                     font=("Arial", 30), text_color=NEON_BLUE)
        self.wave_text.pack(pady=25)

        # Typewriter Log Box
        self.info_box = ctk.CTkTextbox(self, width=680, height=200, font=("Consolas", 14), 
                                      fg_color="#020C1B", text_color=NEON_BLUE, border_color=SOFT_GLOW)
        self.info_box.pack(pady=10)
        self.info_box.insert("0.0", ">>> INITIALIZING CODEALPHA ENGINE...\n>>> READY FOR COMPOSITION.")

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self, width=600, progress_color=NEON_BLUE)
        self.progress.pack(pady=15)
        self.progress.set(0)

        # --- Control Buttons (With Blink effect) ---
        self.btn_gen = ctk.CTkButton(self, text="Compose Unique Track", 
                                    fg_color=NEON_BLUE, text_color=MIDNIGHT_BLUE, 
                                    font=("Arial", 18, "bold"), height=55, corner_radius=10,
                                    command=self.blink_compose)
        self.btn_gen.pack(pady=10)

        self.btn_export = ctk.CTkButton(self, text="Export Last generated MIDI", 
                                       fg_color=SOFT_GLOW, text_color=TEXT_WHITE,
                                       height=35, command=self.blink_export)
        self.btn_export.pack(pady=5)

        self.btn_stop = ctk.CTkButton(self, text="Stop Stream", fg_color="#FF4B2B", 
                                     height=40, corner_radius=10, command=self.blink_stop)
        self.btn_stop.pack(pady=10)

    # --- Feature: Blinking Logic ---
    def blink_effect(self, button_obj, original_color, blink_color, final_action):
        button_obj.configure(fg_color=blink_color)
        self.after(200, lambda: button_obj.configure(fg_color=original_color))
        self.after(300, final_action)

    def blink_compose(self):
        self.btn_gen.configure(state="disabled")
        self.blink_effect(self.btn_gen, NEON_BLUE, GLOW_GREEN, self.start_ai_flow)

    def blink_stop(self):
        self.blink_effect(self.btn_stop, "#FF4B2B", "#FFFFFF", self.stop_stream)

    def blink_export(self):
        self.blink_effect(self.btn_export, SOFT_GLOW, NEON_BLUE, self.export_midi_file)

    def start_ai_flow(self):
        self.info_box.delete("0.0", "end")
        threading.Thread(target=self.generation_engine, daemon=True).start()

    def generation_engine(self):
        mood = self.mood_opt.get()
        self.type_log(f"[AI] Analyzing {mood} neural patterns...")
        
        # Music creation logic
        s = stream.Stream()
        if mood == "Cyberpunk": notes_pool = [48, 51, 53, 55, 58, 60] 
        elif mood == "Deep Space": notes_pool = [60, 62, 64, 67, 69, 72] 
        else: notes_pool = [72, 74, 76, 79, 81, 84]
        
        for i in range(35):
            if i % 5 == 0: self.progress.set(i/35)
            n = note.Note(np.random.choice(notes_pool))
            n.quarterLength = np.random.choice([0.5, 1.0, 1.5])
            s.append(n)
        
        s.write('midi', fp="output.mid")
        
        pygame.mixer.music.load("output.mid")
        pygame.mixer.music.play()
        
        threading.Thread(target=self.wave_animation, daemon=True).start()
        self.display_lyrics(mood)
        self.btn_gen.configure(state="normal")

    def export_midi_file(self):
        try:
            mood = self.mood_opt.get()
            final_name = f"final_{mood.lower()}_composition.mid"
            import shutil
            shutil.copyfile("output.mid", final_name)
            self.type_log(f"[EXPORT] Successfully saved as: {final_name}")
        except:
            self.type_log("[EXPORT] Error: Compose a track first.")

    def wave_animation(self):
        frames = ["▂ ▃ ▄ ▅ ▆ ▇ █", "▃ ▄ ▅ ▆ ▇ █ ▇", "▄ ▅ ▆ ▇ █ ▇ ▆", "▅ ▆ ▇ █ ▇ ▆ ▅"]
        while pygame.mixer.music.get_busy():
            for f in frames:
                if not pygame.mixer.music.get_busy(): break
                self.wave_text.configure(text=f + f + f)
                time.sleep(0.1)

    def type_log(self, text):
        for char in text:
            self.info_box.insert("end", char)
            self.info_box.see("end")
            time.sleep(0.02)
        self.info_box.insert("end", "\n")

    def display_lyrics(self, mood):
        lyrics = {
            "Cyberpunk": ["Neon city, binary rain...", "Lost in digital pain...", "System override initiated."],
            "Deep Space": ["Floating in the void...", "Stars whispering code...", "Galactic harmony found."],
            "Ambient": ["Soft waves of data...", "Calm sequence start...", "Tranquil AI thoughts."]
        }
        for line in lyrics[mood]:
            if not pygame.mixer.music.get_busy(): break
            self.type_log(f"♪ {line}")
            time.sleep(2.5)

    def stop_stream(self):
        pygame.mixer.music.stop()
        self.wave_text.configure(text="▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂")
        self.type_log("[SYSTEM] Stream stopped by user.")

if __name__ == "__main__":
    app = MusicAIGenerationFinal()
    app.mainloop()