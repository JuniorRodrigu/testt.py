import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import pygame

# Initialize Pygame
pygame.init()

# Load the piano sound for collision (replace 'piano_E_note.mp3' with your actual file)
piano_sound = pygame.mixer.Sound('tok.mp3')

# Define initial parameters
raio_externo = 5
raio_bolinha = 0.5
posicao_inicial = (0, raio_externo - raio_bolinha)
velocidade_inicial = [0, 0]
gravidade = -0.01
fator_aumento = 0.1
max_trail_length = 1000  # Maximum length of the trail
contagem_colisoes = 0  # Collision counter

# Variable to control the sound playback
tempo_de_som = 1.0  # Duration of 1 second for sound playback

# Create the figure and axis
fig, ax = plt.subplots()
ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.set_aspect('equal', 'box')
ax.set_xlim(-raio_externo, raio_externo)
ax.set_ylim(-raio_externo, raio_externo)

# Draw the larger circular area with a white background
circulo_area = plt.Circle((0, 0), raio_externo, color='white', fill=True)
ax.add_patch(circulo_area)

# Draw the ball
bolinha = plt.Circle(posicao_inicial, raio_bolinha, color='red', zorder=2)
ax.add_patch(bolinha)

# Initialize the ball's trail
trail = np.empty((0, 2), float)

# Create the LineCollection with black color and line width equal to the diameter of the ball
lines = LineCollection([], colors='black', linestyles='solid', linewidths=2 * raio_bolinha)
ax.add_collection(lines)


# Function to check collision with the border of the circular area and play the sound
def verificar_colisao(x, y):
    global raio_bolinha, velocidade_inicial, trail, contagem_colisoes
    distancia_centro = np.sqrt(x**2 + y**2)
    if distancia_centro >= raio_externo - raio_bolinha:
        # Increase the collision count
        contagem_colisoes += 1

        # Play the piano sound for 1 second
        piano_sound.play(maxtime=int(tempo_de_som * 1000))

        # Reflect the velocity and add a spin
        vetor_normal = np.array([x, y]) / np.linalg.norm([x, y])
        velocidade_inicial -= 2 * np.dot(velocidade_inicial, vetor_normal) * vetor_normal
        velocidade_inicial += 0.05 * np.array([-vetor_normal[1], vetor_normal[0]])
        x, y = (raio_externo - raio_bolinha - 0.1) * vetor_normal
        raio_bolinha += fator_aumento
        bolinha.set_radius(raio_bolinha)

    # Add the current position to the trail
    trail = np.append(trail, [[x, y]], axis=0)
    if trail.shape[0] > max_trail_length:
        trail = trail[-max_trail_length:]  # Keep only the last points

    # Update the LineCollection with the new trail
    lines.set_segments([trail])
    lines.set_array(np.linspace(0, 1, trail.shape[0]))

    bolinha.set_center((x, y))
    return bolinha, lines

# Function to update the position of the ball and draw the trail
def update(frame):
    global raio_bolinha, velocidade_inicial, trail
    x, y = bolinha.center
    velocidade_inicial[1] += gravidade
    x += velocidade_inicial[0]
    y += velocidade_inicial[1]

    return verificar_colisao(x, y)

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=1440, interval=0, blit=False)

# Show the animation
plt.show()
