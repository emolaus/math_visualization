# pyvista-anim

A small Python 3.12 architecture for mathematical PyVista animations using `StructuredGrid`.

## Install

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Run interactive animation

```bash
pyvista-anim --time 4 --framerate 25
```

Or:

```bash
python -m pyvista_anim.cli --time 4 --framerate 25
```

## Render movie

```bash
pyvista-anim --movie --name wave.mp4 --time 4 --framerate 25
```

You may need a working PyVista/VTK rendering setup and movie writer support in your environment.

## Single frame

```bash
pyvista-anim --singleframe --debugval 1.5
```
## Feature desires
* Remove dependence on elevation warping
* Parameter Animations with easing curves
* Treat animations like transformations so that they can be composed: S*T*A
* Wave animation on elevation