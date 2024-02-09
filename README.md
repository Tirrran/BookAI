Для корректной работы программы, требуется дополнительно установить библиотеки **Diffusers**, **Torch**, **Translate**, **Pillow**(PIL) и **Vosk**. 

Если программа будет использоваться на видеокарте, то необходимо докачать **Cuda Toolkit** , заменить с **pipe.to("cpu")** на **pipe.to("cuda")** и изменить "**pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")**" на "**pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")**". 

**ВАЖНО!!!** Для работы на видеокарте требуется минимум 4ГБ видеопамяти!
