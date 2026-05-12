# -*- coding: utf-8 -*-
import customtkinter as ctk
import threading
import time
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

dashscope.api_key = "sk-36ee1c702e194855b9588f646a5836cc"
dashscope.base_websocket_api_url = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"

OUTPUT_DIR = Path("sound")
OUTPUT_DIR.mkdir(exist_ok=True)


class VoiceTTSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Voice TTS Generator")
        self.geometry("700x550")
        self.resizable(True, True)
        self._generating = False
        self._last_audio_path: Path | None = None

        # --- Voice name ---
        row_name = ctk.CTkFrame(self, fg_color="transparent")
        row_name.pack(fill="x", padx=20, pady=(20, 5))
        ctk.CTkLabel(row_name, text="Output File Name:", width=130, anchor="w").pack(side="left")
        self.name_entry = ctk.CTkEntry(row_name, placeholder_text="e.g. my_audio")
        self.name_entry.pack(side="left", fill="x", expand=True)
        self.name_entry.insert(0, "output")

        # --- Text area ---
        ctk.CTkLabel(self, text="Text Content:", anchor="w").pack(fill="x", padx=20, pady=(15, 3))
        self.textbox = ctk.CTkTextbox(self, height=280)
        self.textbox.pack(fill="both", expand=True, padx=20)

        # --- Buttons ---
        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=15)

        self.btn_upload = ctk.CTkButton(btn_row, text="Upload .txt", command=self._upload_file, width=120)
        self.btn_upload.pack(side="left", padx=(0, 10))

        self.btn_generate = ctk.CTkButton(
            btn_row, text="Generate Audio", command=self._generate, width=150,
            fg_color="#2ecc71", hover_color="#27ae60",
        )
        self.btn_generate.pack(side="left", padx=(0, 10))

        self.btn_export = ctk.CTkButton(
            btn_row, text="Export As...", command=self._export_as, width=120,
            fg_color="#3498db", hover_color="#2980b9", state="disabled",
        )
        self.btn_export.pack(side="left")

        # --- Status bar ---
        self.status_label = ctk.CTkLabel(self, text="Status: Ready", anchor="w", height=30)
        self.status_label.pack(fill="x", padx=20, pady=(0, 10))

    # ---- Upload .txt file ----
    def _upload_file(self):
        path = filedialog.askopenfilename(
            title="Select a text file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            text = Path(path).read_text(encoding="utf-8")
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", text)
            self._set_status(f"Loaded: {Path(path).name}")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    # ---- Generate audio ----
    def _generate(self):
        text = self.textbox.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Empty", "Please enter or upload text first.")
            return
        # Collapse whitespace the same way as voice.py
        text = "".join(line.strip() for line in text.splitlines())
        if not text:
            messagebox.showwarning("Empty", "Text content is empty after cleanup.")
            return

        self._generating = True
        self.btn_generate.configure(state="disabled", text="Generating...")
        self._set_status("Generating audio, please wait...")

        threading.Thread(target=self._do_generate, args=(text,), daemon=True).start()

    def _do_generate(self, text: str):
        start = time.perf_counter()
        try:
            synthesizer = SpeechSynthesizer(
                model="cosyvoice-v3.5-plus",
                voice="cosyvoice-v3.5-plus-bailian-b4c014c43af24f829370644f10de3cc2",
            )
            audio = synthesizer.call(text, timeout_millis=120000)
        except TimeoutError:
            self.after(0, lambda: self._on_generate_error("Generation timed out (120s). Try shorter text."))
            return
        except Exception as exc:
            self.after(0, lambda: self._on_generate_error(str(exc)))
            return

        name = self.name_entry.get().strip() or "output"
        filename = OUTPUT_DIR / f"{name}.m4a"
        with open(filename, "wb") as f:
            f.write(audio)

        elapsed = time.perf_counter() - start
        self._last_audio_path = filename
        self.after(0, lambda: self._on_generate_done(filename, elapsed))

    def _on_generate_done(self, path: Path, elapsed: float):
        self._generating = False
        self.btn_generate.configure(state="normal", text="Generate Audio")
        self.btn_export.configure(state="normal")
        self._set_status(f"Done! Saved to {path} ({elapsed:.1f}s)")

    def _on_generate_error(self, msg: str):
        self._generating = False
        self.btn_generate.configure(state="normal", text="Generate Audio")
        self._set_status("Failed.")
        messagebox.showerror("Generation Error", msg)

    # ---- Export As (copy to user-chosen location) ----
    def _export_as(self):
        if not self._last_audio_path or not self._last_audio_path.exists():
            messagebox.showwarning("No Audio", "Generate audio first.")
            return
        dest = filedialog.asksaveasfilename(
            title="Export Audio",
            defaultextension=".m4a",
            filetypes=[("M4A Audio", "*.m4a"), ("All files", "*.*")],
            initialfile=self._last_audio_path.name,
        )
        if not dest:
            return
        import shutil
        shutil.copy2(self._last_audio_path, dest)
        self._set_status(f"Exported to {dest}")
        messagebox.showinfo("Exported", f"Audio exported to:\n{dest}")

    # ---- Helpers ----
    def _set_status(self, msg: str):
        self.status_label.configure(text=f"Status: {msg}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = VoiceTTSApp()
    app.mainloop()
