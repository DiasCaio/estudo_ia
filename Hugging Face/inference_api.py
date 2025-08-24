'''O inference_api é um módulo do hugging face para utilizarmos modelos de forma serverless, ou seja, sem consumir os nossos 
recursos computacionais. Podemos usar através do requests ou através da própria classe do hugging face, que será como usaremos nesse arquivo.
'''
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
cliente = InferenceClient()

texto = """
The Greek alphabet has been used to write the Greek language since the late 9th or early 8th century BC.[2][3] It was derived from the earlier Phoenician alphabet,[4] and is the earliest known alphabetic script to systematically write vowels as well as consonants.[5] In Archaic and early Classical times, the Greek alphabet existed in many local variants, but, by the end of the 4th century BC, the Ionic-based Euclidean alphabet, with 24 letters, ordered from alpha to omega, had become standard throughout the Greek-speaking world[6] and is the version that is still used for Greek writing today.[7]

The uppercase and lowercase forms of the 24 letters are:

Α α, Β β, Γ γ, Δ δ, Ε ε, Ζ ζ, Η η, Θ θ, Ι ι, Κ κ, Λ λ, Μ μ, Ν ν, Ξ ξ, Ο ο, Π π, Ρ ρ, Σ σ ς, Τ τ, Υ υ, Φ φ, Χ χ, Ψ ψ, Ω ω
The Greek alphabet is the ancestor of several scripts, such as the Latin, Gothic, Coptic, and Cyrillic scripts.[8] Throughout antiquity, Greek had only a single uppercase form of each letter. It was written without diacritics and with little punctuation.[9] By the 9th century, Byzantine scribes had begun to employ the lowercase form, which they derived from the cursive styles of the uppercase letters.[10] Sound values and conventional transcriptions for some of the letters differ between Ancient and Modern Greek usage because the pronunciation of Greek has changed significantly between the 5th century BC and the present. Additionally, Modern and Ancient Greek now use different diacritics, with ancient Greek using the polytonic orthography and modern Greek keeping only the stress accent (acute) and the diaeresis.

Apart from its use in writing the Greek language, in both its ancient and its modern forms, the Greek alphabet today also serves as a source of international technical symbols and labels in many domains of mathematics, science, and other fields.
"""


resposta = cliente.summarization(texto, model="facebook/bart-large-cnn")

print(resposta)