# TimeToRelax
es una aplicación diseñada para ayudar a los usuarios a tomar descansos mientras trabajan frente a una pantalla. Muestra un pantallazo de descanso configurable que anima al usuario a detenerse y relajarse, y permite pausar y reanudar el temporizador según las preferencias del usuario

## Características

- **Pantallazo de descanso**: Se muestra un fondo de pantalla de color sólido con un mensaje animando al usuario a tomarse un descanso.
- **Configuración personalizable**: Ajustes como color, opacidad, tecla de desactivación, tiempo de aparición y monitor seleccionado.
- **Interfaz en bandeja del sistema**: El icono en la bandeja del sistema permite acceder a opciones rápidas como Pausar/Reanudar y Configuración.
- **Pausa y reanudación**: Permite al usuario pausar o reanudar el temporizador desde el menú de la bandeja del sistema.

## Cómo funciona

1. **Configuración inicial**: Al ejecutar el programa, se cargan configuraciones desde el archivo `config.json` (si existe) o se crea uno nuevo.
2. **Pantallazo de descanso**: Transcurrido el tiempo configurado, se muestra un pantallazo de descanso en los monitores seleccionados.
3. **Pausa/Reanudar**: El usuario puede pausar o reanudar el temporizador de descanso a través del menú en la bandeja del sistema.
4. **Tecla de desactivación**: El usuario puede desactivar el pantallazo de descanso presionando la tecla configurada (por defecto, `space`).

## Botones en el Menú de la Bandeja del Sistema

El menú en la bandeja del sistema cuenta con los siguientes botones:
* Letras:  a, b, c, ..., z
* Números: 0, 1, 2, ..., 9
* Teclas especiales:
* Espacio: space
* Retroceso: backspace
* Enter: enter
* Escape: esc
* Tabulación: tab
* Teclas de función: f1, f2, ..., f12
* Teclas de flecha: up, down, left, right
* Otros símbolos:
* Guión bajo: -
* Igual: =
* Puntuación: ,, ., ;, :

## Requisitos

Para ejecutar TimeToRelax, necesitas tener instalados los siguientes paquetes de Python:

```bash
pip install keyboard pystray pillow screeninfo
