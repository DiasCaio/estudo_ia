#Arquivo de exemplo base do hugging face, apenas copiei as instruções e coloquei aqui para ver o resultado
#O conteúdo foi explicado no curso da hashtag

from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch

modelo = pipeline("text-to-speech", "microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
# You can replace this embedding with your own as well.
prompt = "test prompt for speech synthesis"
speech = modelo(prompt, forward_params={"speaker_embeddings": speaker_embedding})

sf.write("speech.wav", speech["audio"], samplerate=speech["sampling_rate"])
