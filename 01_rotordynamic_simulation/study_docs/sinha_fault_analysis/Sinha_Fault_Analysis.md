# Sinha Rotor Fault Analysis — Code Analysis Report

This report documents the architecture, execution flow, and design of the
`sinha_fault_analysis.ipynb` notebook, which simulates and compares three
rotordynamic conditions using the ROSS library:

1. **Healthy baseline** — pure unbalance response
2. **Transverse crack** — breathing crack via the Mayes model
3. **Parallel misalignment** — flexible coupling misalignment

---

## 1. Execution Flow

The notebook follows a linear pipeline: load the rotor model, define constants,
run three independent simulations, then overlay their frequency spectra for
fault diagnosis.

![Execution Flow](execution_flow.png)

### Step-by-step summary

| Step | Code Cell | Action |
|------|-----------|--------|
| 1 | `setup` | Import `ross`, `numpy`, `plotly`; load rotor from `sinha_rotor.toml` |
| 2 | `constants` | Define speed (750 RPM), time vector, crack/misalignment parameters |
| 3 | `healthy-sim` | Build force matrix `F_healthy`, map DOFs, call `run_time_response()` |
| 4 | `healthy-plot-dfft` | Plot DFFT spectrum, annotate 1X–4X harmonics |
| 5 | `crack-sim` | Call `rotor.run_crack()` with Mayes model, `depth_ratio=0.43` |
| 6 | `crack-plot-*` | Plot time response and DFFT — observe 2X, 3X peaks |
| 7 | `mis-sim` | Call `rotor.run_misalignment()` with flexible coupling parameters |
| 8 | `mis-plot-*` | Plot time response and DFFT — observe 1X, 2X peaks |
| 9 | `comparison-overlay` | Overlay all three DFFT spectra on one figure |

### Key code pattern: DOF indexing

The force matrix has one column per degree of freedom. For a standard 4-DOF-per-node
model, the translational DOFs of node `n` are:

```python
dof_x = rotor.number_dof * disk_node      # x-translation
dof_y = rotor.number_dof * disk_node + 1   # y-translation
```

This mapping is critical for correctly injecting unbalance forces into the
global force vector.

---

## 2. Class Diagram

The diagram below shows the ROSS classes involved in the fault analysis
notebook and their relationships.

![UML Class Diagram](uml_class_diagram.png)

### Core classes

| Class | Module | Role |
|-------|--------|------|
| `Element` (ABC) | `ross/element.py` | Base class for all rotor elements; defines `M()`, `K()`, `C()`, `G()` |
| `ShaftElement` | `ross/shaft_element.py` | Euler–Bernoulli / Timoshenko beam element |
| `DiskElement` | `ross/disk_element.py` | Rigid disk with mass and inertia |
| `BearingElement` | `ross/bearing_seal_element.py` | Linearized spring-damper support |
| `Rotor` | `ross/rotor_assembly.py` | Assembles global matrices; provides `run_*()` analysis methods |
| `Crack` | `ross/faults/crack.py` | Breathing crack fault — Mayes/Gasch models |
| `MisalignmentFlex` | `ross/faults/misalignment.py` | Flexible coupling parallel/angular misalignment |
| `MisalignmentRigid` | `ross/faults/misalignment.py` | Rigid coupling misalignment |
| `TimeResponseResults` | `ross/results.py` | Time-domain results container with `plot_1d()`, `plot_dfft()`, etc. |
| `Probe` | `ross/probe.py` | Measurement probe definition (node + angle) |

### Inheritance and composition

- `ShaftElement`, `DiskElement`, `BearingElement` all inherit from `Element`.
- `Rotor` **composes** lists of these elements.
- `TimeResponseResults` inherits from `Results`.
- Fault classes (`Crack`, `MisalignmentFlex`) hold a **reference** to the
  `Rotor` and delegate time integration back to `rotor.run_time_response()`.

---

## 3. Instantiation (Sequence) Diagram

This diagram shows the object creation timeline and method call sequence
when the notebook executes.

![Instantiation Diagram](instantiation_diagram.png)

### Key interactions

1. **`Rotor.load()`** reads the TOML file, reconstructs each element via
   `read_toml_data()`, and assembles them into a `Rotor` instance.

2. **Healthy simulation** manually builds a force matrix and calls
   `rotor.run_time_response()` directly. The Newmark-beta integrator
   produces `(t, yout, xout)` wrapped in `TimeResponseResults`.

3. **Crack simulation** delegates to `Rotor.run_crack()`, which:
   - Creates a `Crack` object with intact (`Ko`) and open (`Kc`) stiffness matrices.
   - Calls `Crack.run()`, which injects a parametric stiffness callback via
     `add_to_RHS` into `run_time_response()`.

4. **Misalignment simulation** delegates to `Rotor.run_misalignment()`, which:
   - Creates a `MisalignmentFlex` object with coupling geometry.
   - Calls `MisalignmentFlex.run()`, which pre-computes reaction forces and
     adds them to the force matrix before calling `run_time_response()`.

5. All three paths converge to `TimeResponseResults`, which provides
   `plot_1d()` and `plot_dfft()` for visualization.

---

## 4. Use Case Diagram

The diagram captures the analyst's interaction with the fault analysis system.

![Use Case Diagram](use_case_diagram.png)

### Actors and use cases

| Actor | Use Cases |
|-------|-----------|
| **Engineer / Analyst** | Load model, define parameters, run simulations, compare spectra, diagnose faults |

| Use Case | Description |
|----------|-------------|
| Load Rotor Model | Deserialize the calibrated Sinha rotor from `sinha_rotor.toml` |
| Define Simulation Parameters | Set speed, time vector, crack depth, misalignment offset, etc. |
| Run Healthy Baseline | Simulate pure unbalance response (1X only) |
| Run Crack Fault | Simulate breathing crack (Mayes model) — generates 2X + 3X |
| Run Misalignment Fault | Simulate parallel misalignment — generates 1X + 2X |
| Plot Time-Domain Response | Visualize displacement vs. time at a probe location |
| Plot Frequency Spectrum | Compute and display DFFT of the response |
| Annotate Harmonics | Add 1X–4X vertical markers to frequency plots |
| Overlay and Compare | Superimpose healthy, cracked, and misaligned spectra |
| Diagnose Fault Type | Interpret harmonic patterns to identify the fault |

---

## 5. Code Issues and Observations

### 5.1 Undefined variables in the healthy simulation cell

The cell `healthy-sim` references variables that are **never defined** in the
notebook:

| Variable | Used as | Problem |
|----------|---------|---------|
| `disk_node` | Node index for DOF calculation | Not defined; the cell that defined it (`common-params`) is commented out as a docstring |
| `speed` | Shaft speed in rad/s | Not defined; `SPEED` is defined (as a pint Quantity in RPM) but never converted to `speed` |
| `t` | Time vector | Not defined; `T` is defined but `t` (lowercase) is referenced |
| `unb_phase` | Unbalance phase angle | Not defined; `UNBALANCE_PHASE` exists but `unb_phase` is not assigned |
| `unb_node` | Unbalance node list | Not defined; was in the commented-out cell |
| `unb_mag` | Unbalance magnitude list | Not defined; was in the commented-out cell |
| `probe` | Probe object list | Not defined; was in the commented-out cell |
| `freq_range` | Frequency range for DFFT | Not defined; `FREQ_RANGE` exists but `freq_range` is not assigned |

**Root cause**: The cell `common-params` (which defined `disk_node`, `unb_node`,
`unb_mag`, `unb_phase`, `probe`, `speed`) is entirely wrapped in a triple-quoted
string, making it a no-op. The constants cell defines uppercase names (`SPEED`,
`T`, `UNBALANCE_PHASE`, `FREQ_RANGE`) but the simulation cells reference
lowercase names.

**Impact**: The notebook will fail with `NameError` when the healthy simulation
cell is executed. Downstream cells (crack, misalignment, comparison) also
depend on these variables and will fail.

### 5.2 Inconsistent crack depth

The markdown states `depth_ratio = 0.2` (20%), but the code uses
`depth_ratio=0.43` (43%). The markdown and code should be consistent.

### 5.3 Missing variable bridge

A cell is needed between the constants and the simulation to bridge the
uppercase constants to the working variables:

```python
speed = SPEED.to("rad/s").m
t = T
disk_node = rotor.disk_elements[0].n
unb_node = [disk_node]
unb_mag = [UNBALANCE_MAG]
unb_phase = [UNBALANCE_PHASE.m]
probe_node = rotor.bearing_elements[1].n - 1
probe = [rs.Probe(node=probe_node, angle=0.0)]
freq_range = FREQ_RANGE
```

### 5.4 Helper function location

`annotate_harmonics()` is defined **after** the healthy simulation cell but
is called for all three cases. This is fine for sequential execution but
could be clearer if moved to the setup section.

### 5.5 Empty trailing markdown cell

The final cell (`id: 6826de5f`) is an empty markdown cell that serves no
purpose and should be removed.

---

## 6. Recommendations

1. **Uncomment and activate the `common-params` cell** or create a new
   bridging cell that maps uppercase constants to the lowercase working
   variables used in all simulation cells.

2. **Reconcile the crack depth**: update either the markdown text or the
   `depth_ratio` parameter so they match.

3. **Move `annotate_harmonics()`** to the setup section so it is defined
   before any plotting cell.

4. **Remove the empty trailing cell** for cleanliness.

5. **Add a cell that prints rotor summary** (`rotor.plot_rotor()` or
   `print(f"Nodes: {rotor.nodes}, DOFs: {rotor.ndof}")`) after loading,
   to give the reader immediate context about the model size.

---

## Appendix: File Manifest

| File | Description |
|------|-------------|
| `execution_flow.mermaid` | Flowchart of the notebook's logic |
| `uml_class_diagram.mermaid` | Class diagram of ROSS components used |
| `instantiation_diagram.mermaid` | Sequence diagram of object creation |
| `use_case_diagram.mermaid` | Use case diagram for the analyst workflow |
| `render_diagrams.sh` | Script to render `.mermaid` → `.png` via `mmdc` |
| `Sinha_Fault_Analysis.md` | This report |
