import tkinter as tk
from diffusers import AutoPipelineForText2Image
import torch
from PIL import Image, ImageTk
import threading
from translate import Translator
from vosk import Model, KaldiRecognizer
import json
import pyaudio

#stable diffusion выбор на чём будет производиться генерация изображения
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
pipe.to("cpu")

#tkinter интерфейс
root = tk.Tk()
root.geometry('800x900+200+100')
root.title("Книжная панорамма")
root.resizable(width=False, height=False)

imageOpen = Image.open("./interface/in.png")
imageOpen = imageOpen.resize((800, 800))
imageOpen = ImageTk.PhotoImage(imageOpen)

label = tk.Label(root)
label.pack()
label = tk.Label(image = imageOpen)
label.image = imageOpen
label.place(x = -2, y = 100)
label.config(text=label)

#translator переводчик
translator = Translator(from_lang="ru", to_lang="en")

# функция работы ввода микрофона
def micro():
    model = Model(r"./vosk-model-small-ru-0.22")
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    def listen():
        while True:
            print(".")
            data = stream.read(4000, exception_on_overflow=False)
            if (rec.AcceptWaveform(data) and len(data) > 0):
                answer = json.loads(rec.Result())
                print(answer['text'])
                if answer['text']:
                    yield answer['text']

    for text in listen():
        if text == 'стоп':
            quit()
        else:
            translation = translator.translate(text)
            print(translation)
            generate(translation)

# функция генерации изображения
def generate(text):
    image_gen = pipe(prompt = text, num_inference_steps=1, guidance_scale=0.0).images[0]
    image_gen.save("./img.png")

    imageOpen = Image.open("./img.png")
    imageOpen = imageOpen.resize((800, 800))
    imageOpen = ImageTk.PhotoImage(imageOpen)

    label = tk.Label(image = imageOpen)
    label.image = imageOpen
    label.place(x = -2, y = 100)
    label.config(text=label)

#thearding
t1 = threading.Thread(target=micro, daemon=True)
t1.join

#tk start button 
button = tk.Button(root, text="Старт", command=t1.start, width=10, height=2, font="20")
button.place(y=30)
button.pack()

root.mainloop()
