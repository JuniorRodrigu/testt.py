from pydub import AudioSegment

# Carregar o arquivo de áudio
# Use um dos métodos abaixo para corrigir o caminho do arquivo
# Método 1: Barras duplas
# audio = AudioSegment.from_file("C:\\Users\\Suporte Royal\\Desktop\\tiktok\\tok.mp3")

# Método 2: String bruta (raw string)
audio = AudioSegment.from_file(r"C:\Users\Suporte Royal\Desktop\tiktok\tok.mp3")

# Duração de cada segmento em milissegundos (1000 ms = 1 segundo)
segment_duration = 1000 

# Dividir e salvar os segmentos
for i in range(len(audio) // segment_duration):
    start = i * segment_duration
    end = start + segment_duration
    segment = audio[start:end]
    segment.export(f"segment_{i+1}.mp3", format="mp3")
