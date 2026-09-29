# Pong Game

Este proyecto es una implementación en Python del clásico juego **Pong**, desarrollada utilizando la librería **Pygame**. El proyecto está estructurado de forma modular y cuenta con soporte para modos de un jugador (contra la inteligencia artificial) y dos jugadores (multijugador local), así como un conjunto de pruebas unitarias y linters para asegurar la calidad del código.

---

## 📐 Arquitectura y Estructura del Proyecto

El código está organizado siguiendo las mejores prácticas de desarrollo en Python, utilizando la estructura `src/`:

```
.
├── main.py                # Punto de entrada principal para ejecutar el juego
├── pyproject.toml         # Configuración del proyecto, dependencias y herramientas
├── AGENTS.md              # Instrucciones y convenciones para agentes de desarrollo
├── src/
│   └── pong/
│       ├── __init__.py
│       └── game.py        # Lógica principal del juego (Paddle, Ball, AI, PongGame)
└── tests/
    ├── __init__.py
    └── test_game.py       # Pruebas unitarias para las mecánicas del juego
```

---

## 🎮 Componentes Principales

El archivo `src/pong/game.py` contiene la lógica central del juego mediante las siguientes clases:

- **`Paddle`**: Representa las paletas de los jugadores. Controla su movimiento, posicionamiento, límites en pantalla y puntuación.
- **`Ball`**: Maneja el estado de la pelota, su posición, dirección (`dx`, `dy`), velocidad dinámica (que aumenta gradualmente tras cada rebote), rebotado contra paredes y el tiempo de espera pre-saque (`BALL_SERVE_DELAY`).
- **`AI`**: Implementa una inteligencia artificial para el jugador derecho en el modo de 1 jugador. Rastrea la posición vertical de la pelota e introduce un margen de error configurable para hacer el juego justo y competitivo.
- **`PongGame`**: Clase principal del ciclo de juego (*game loop*). Administra la ventana de Pygame, los eventos de entrada de teclado, el menú de inicio, las colisiones, la puntuación, el estado de fin de juego y el renderizado en pantalla.

---

## 🕹️ Modos de Juego y Controles

El juego cuenta con un menú principal interactivo al iniciar:

### Modos
1. **Un Jugador (`1P vs AI`)**: El Jugador 1 compite contra la IA.
2. **Dos Jugadores (`2P Local`)**: Dos personas juegan localmente en la misma computadora.

### Controles
- **Menú Principal**:
  - `1` o `NumPad 1`: Seleccionar modo 1 Jugador.
  - `2` o `NumPad 2`: Seleccionar modo 2 Jugadores.
  - `Esc`: Salir del juego.

- **Durante la Partida**:
  - **Jugador Izquierdo (Jugador 1)**:
    - Mover arriba: `W` o `Flecha Arriba` (en modo 1P).
    - Mover abajo: `S` o `Flecha Abajo` (en modo 1P).
  - **Jugador Derecho (Jugador 2 - Solo modo 2P)**:
    - Mover arriba: `Flecha Arriba`.
    - Mover abajo: `Flecha Abajo`.
  - **Opciones Generales**:
    - `Esc`: Volver al menú principal.
    - `R`: Reiniciar la partida cuando haya finalizado.

---

## 🏆 Reglas del Juego

- **Puntuación para Ganar**: El primer jugador en alcanzar **10 puntos** gana la partida.
- **Aumento de Velocidad**: Cada vez que la pelota rebota en una paleta, su velocidad incrementa ligeramente hasta un límite máximo.
- **Ángulo de Rebote**: El ángulo con el que se devuelve la pelota depende del punto exacto del impacto sobre la paleta.

---

## 🚀 Requisitos e Instalación

### Requisitos Previos
- Python 3.10 o superior.

### Instalación

1. Crear y activar un entorno virtual de Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Linux/macOS
   # .venv\Scripts\activate   # En Windows
   ```

2. Instalar el paquete y sus dependencias de desarrollo:
   ```bash
   pip install -e ".[dev]"
   ```
   *(O alternativamente: `pip install pygame pytest ruff mypy`)*

---

## ▶️ Ejecución del Juego

Para iniciar el juego, ejecuta:

```bash
python main.py
```

---

## 🧪 Pruebas y Calidad de Código

El proyecto está configurado con varias herramientas para garantizar la calidad del código:

- **Ejecutar Pruebas Unitarias (`pytest`)**:
  ```bash
  pytest
  ```

- **Verificación de Estilo y Linting (`ruff`)**:
  ```bash
  ruff check .
  ruff format --check .
  ```

- **Comprobación de Tipos Estáticos (`mypy`)**:
  ```bash
  mypy .
  ```

- **Ejecutar todas las verificaciones en orden**:
  ```bash
  ruff check . && ruff format . && mypy . && pytest
  ```
