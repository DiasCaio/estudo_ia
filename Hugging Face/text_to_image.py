#Arquivo de exemplo base do hugging face, apenas copiei as instruções e coloquei aqui para ver o resultado
#O conteúdo foi explicado no curso da hashtag


from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5")

pipe = pipe.to("cuda")

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = pipe(prompt).images[0]

image.save("generated_image.png")
