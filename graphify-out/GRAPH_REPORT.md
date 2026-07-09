# Graph Report - .  (2026-07-09)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 2063 nodes · 3468 edges · 154 communities (106 shown, 48 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 192 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ad964e60`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_rotor_assembly.py
- Rotor
- HolePatternSeal
- SealElement
- Material
- LabyrinthSeal
- test_shaft_element.py
- rotor_assembly.py
- ForcedResponseResults
- units.py
- load_data
- .run_modal
- TiltingPadResults
- TiltingPad
- MultiRotor
- Guyan
- test_stochastic_elements.py
- PointMass
- test_bearing_seal_element.py
- ThrustPad
- test_stochastic_rotor_assembly.py
- Path
- ModalResults
- ST_Material
- fluid_flow.py
- Crack
- CoAxialRotor
- test_hybrid_seal.py
- signal_utils.py
- Element
- ThrustPadResults
- test_examples.py
- ABC
- StaticResults
- PlainJournalResults
- CouplingElement
- SensitivityResults
- Shape
- ST_ShaftElement
- ST_Rotor
- .coefficients
- plot_utils.py
- calculate_stiffness_and_damping_coefficients
- FluidFlow
- ._thermal_coupling_iteration
- Probe
- ST_DiskElement
- BearingResults
- GearElementTVMS
- st_rotor_assembly.py
- test_plain_journal.py
- ._equilibrium_objective
- test_gear_element.py
- Mesh
- CampbellResults
- test_6dof_model.py
- MisalignmentFlex
- TimeResponseResults
- ST_ForcedResponseResults
- SqueezeFilmDamperResults
- test_fluid_flow.py
- fluid_flow_graphics.py
- MagneticBearingElement
- SqueezeFilmDamper
- PlainJournal
- test_transient_newmark.py
- DiskElement
- ._compute_stiffness
- .integrate_system
- test_disk_element.py
- .__init__
- MisalignmentRigid
- Rubbing
- UCSResults
- .load
- ST_TimeResponseResults
- ST_CampbellResults
- test_misalignment.py
- ._print_single_frequency_results
- ._forces
- ._temperature_convergence_loop
- utils.py
- FrequencyResponseResults
- ST_FrequencyResponseResults
- BearingFluidFlow
- calculate_short_stiffness_matrix
- CylindricalBearing
- test_probe.py
- TestTiltingPadGeometry
- test_units.py
- sinha_helpers.py
- ._get_coefficient_list
- _flooded
- .C
- BallBearingElement
- .from_table
- RollerBearingElement
- test_rubbing.py
- TestTiltingPadEquilibrium
- .G
- ._compute_involute_curve
- mod
- .run_ucs
- TestTiltingPadHydrodynamicForces
- render_diagrams.sh
- ._process_coefficient
- .from_table
- test_from_section
- .n
- TestTiltingPadDynamicCoefficients
- constants.py
- render_diagrams.sh
- run_notebooks.py
- .C
- .dof_mapping
- ._hover_info
- .M
- .plot
- .read_toml_data
- .__repr__
- disk_example
- .calculate_Id
- .calculate_mass
- .calculate_width
- .dof_mapping
- .__eq__
- .__hash__
- .Kdt
- .M
- ._patch
- .__repr__
- .__str__
- ._pairs_to_complex_array
- .unbalance_force_over_time
- .__eq__
- .add_nodes
- ._patch
- .__eq__
- .__repr__
- .__str__
- .dof_mapping
- .Kst
- .G
- test_save_load_skips_computation
- ross-rotordynamics

## God Nodes (most connected - your core abstractions)
1. `Rotor` - 126 edges
2. `BearingElement` - 92 edges
3. `ShaftElement` - 73 edges
4. `TiltingPad` - 59 edges
5. `DiskElement` - 41 edges
6. `Material` - 41 edges
7. `CoAxialRotor` - 35 edges
8. `ST_Rotor` - 32 edges
9. `Element` - 30 edges
10. `PointMass` - 30 edges

## Surprising Connections (you probably didn't know these)
- `test_rubbing()` --calls--> `Rubbing`  [INFERRED]
  ross/tests/test_rubbing.py → ross/faults/rubbing.py
- `test_mis_angular_resp()` --calls--> `Probe`  [INFERRED]
  ross/tests/test_misalignment.py → ross/probe.py
- `test_mis_comb_resp()` --calls--> `Probe`  [INFERRED]
  ross/tests/test_misalignment.py → ross/probe.py
- `test_mis_parallel_resp()` --calls--> `Probe`  [INFERRED]
  ross/tests/test_misalignment.py → ross/probe.py
- `test_mis_rigid_resp()` --calls--> `Probe`  [INFERRED]
  ross/tests/test_misalignment.py → ross/probe.py

## Import Cycles
- None detected.

## Communities (154 total, 48 thin omitted)

### Community 0 - "test_rotor_assembly.py"
Cohesion: 0.04
Nodes (13): r"""This function creates the model of a test rig rotor supported by magnetic be, rotor_amb_example(), get_dofs(), Tests the run_amb_sensitivity method for correctness of outputs and handling of, # TODO: Move this to test_results.py, test_a1_0_matrix_rotor2(), test_amb_controller(), test_amb_generic_controller() (+5 more)

### Community 1 - "Rotor"
Cohesion: 0.11
Nodes (42): BearingElement, A bearing element.      This class will create a bearing element.     Parameters, Create a disk element from geometry properties.          This class method will, coaxrotor_example(), Convert a rotor object to a ross-only rotor object.          This method removes, Create a rotor as example.      This function returns an instance of a simple ro, Create a coaxial rotor as example.      This function returns an instance of a c, Create a rotor as example.      This function returns an instance of a simple ro (+34 more)

### Community 2 - "HolePatternSeal"
Cohesion: 0.06
Nodes (35): HolePatternSeal, Plot pressure distribution for the hole pattern seal.          Parameters, Hole-pattern annular seal - Bulk flow model with dynamic coefficients.      This, holepattern(), holepattern_gas_composition(), holepattern_manual(), Test that thermodynamic properties are auto-derived correctly., Test that coefficients are in reasonable range.      Results may differ slightly (+27 more)

### Community 3 - "SealElement"
Cohesion: 0.08
Nodes (21): A seal element.      This class will create a seal element.     Parameters can b, Generate hover information for seal element.          Overrides the base class m, SealElement, Mass matrix for an instance of a rotor.          Parameters         ----------, Stiffness matrix for an instance of a rotor.          Parameters         -------, Dynamic stiffness matrix for an instance of a rotor.          Stiffness matrix a, Damping matrix for an instance of a rotor.          Parameters         ---------, Gyroscopic matrix for an instance of a rotor.          Returns         ------- (+13 more)

### Community 4 - "Material"
Cohesion: 0.07
Nodes (26): Material, Equality method for comparisons.          Parameters         ----------, Return a string representation of a material.          Returns         -------, Convert object into string.          Returns         -------         The object', Save material properties.          This is an auxiliary function to save the mat, Load material properties.          This is an auxiliary function to load all sav, Material used on shaft and disks.      Class used to create a material and defin, Load a material that is available in the data file.          Returns         --- (+18 more)

### Community 5 - "LabyrinthSeal"
Cohesion: 0.07
Nodes (31): LabyrinthSeal, Plot pressure distribution for the labyrinth seal.          Parameters         -, Labyrinth seal - Compressible flow model with rotordynamic coefficients.      Th, labyrinth(), labyrinth_gas_composition(), labyrinth_manual(), Test that coefficients are in reasonable range.      Results may differ slightly, Test that gas_composition and manual parameters give similar results.      They (+23 more)

### Community 6 - "test_shaft_element.py"
Cohesion: 0.05
Nodes (7): eb(), tap2(), tap_tim(), tap_tim_hollow(), tim(), tim2(), tim_6dof()

### Community 7 - "rotor_assembly.py"
Cohesion: 0.07
Nodes (22): HarmonicBalance, Harmonic Balance method for nonlinear rotor dynamic systems.          This class, Construct the harmonic force components in the frequency domain.          Parame, Compute unbalance forces in the frequency domain.          Parameters         --, Compute Fourier expansion of external time-domain forces.          Parameters, Assemble the total complex force vector for the HB system.          Parameters, Compute Fourier-expanded stiffness matrices for cracked shafts.          Paramet, Construct the Harmonic Balance matrix `H`.          Parameters         --------- (+14 more)

### Community 8 - "ForcedResponseResults"
Cohesion: 0.07
Nodes (22): ForcedResponseResults, _init_orbit(), Orbit, r"""Class used to construct orbits for a node in a mode or deflected shape., Calculates the amplitude for a given angle of the orbit.          Parameters, Plot frequency response.          This method plots the frequency response given, Class used to store results and provide plots for Forced Response analysis., Return the forced response (magnitude) in DataFrame format.          Parameters (+14 more)

### Community 9 - "units.py"
Cohesion: 0.14
Nodes (15): bearing_example(), Bearing Element module.  This module defines the BearingElement classes which wi, Create an example of bearing element.      This function returns an instance of, Create an example of seal element.      This function returns an instance of a s, seal_example(), This module deals with lubricants dictionary in the ROSS library., _compute_turbulence_props(), _temperature() (+7 more)

### Community 10 - "load_data"
Cohesion: 0.10
Nodes (17): Coupling Element module.  This module defines the CouplingElement class which wi, Save the element in a .toml or .json file.          This function will save the, Point mass module.  This module defines the PointMass class which will be used t, Save results in a .toml or .json file.          This function will save the simu, Save the rotor to a .toml or .json file.          This method persists the rotor, Shaft Element module.  This module defines the ShaftElement class which will be, Save results in a .toml or .json file.          This function will save the simu, dump_data() (+9 more)

### Community 11 - ".run_modal"
Cohesion: 0.08
Nodes (14): Verify if bearing elements coefficients are extrapolated.          This method t, Generate indexes to sort eigenvalues and eigenvectors.          Function used to, Calculate eigenvalues and eigenvectors.          This method will return the eig, Frequency response for a mdof system.          This method returns the frequency, Frequency response for a mdof system.          The `run_freq_response()` has bee, Forced response for a mdof system.          This method returns the unbalanced r, Calculate unbalance forces.          This is an auxiliary function the calculate, Unbalanced response for a mdof system.          This method returns the unbalanc (+6 more)

### Community 12 - "TiltingPadResults"
Cohesion: 0.06
Nodes (19): Plot film average temperature vs local pad angle for each pad.          Paramete, Plot babbitt surface temperature vs local pad angle for each pad.          Param, Display the optimization residuals per iteration for each frequency.          Pa, Return a scatter plot of field data at a fixed axial position.          Paramete, Return a 2-D contour plot of field data across all pads.          Parameters, Post-processing results for a TiltingPad bearing.      Parameters     ----------, Not available for SqueezeFilmDamper (analytical model).          The SFD does no, Print results table for one frequency index.          Parameters         ------- (+11 more)

### Community 13 - "TiltingPad"
Cohesion: 0.06
Nodes (22): Tilting-pad journal bearing - Thermo-Hydro-Dynamic (THD) model.      This class, Calculate film thicknesses at control volume faces.          Parameters, Calculate temporal derivative of film thickness.          Parameters         ---, Calculate viscosities at control volume faces using boundary conditions., Calculate viscosities at all control volume faces using vectorized operations., Calculate finite difference coefficients for Reynolds equation.          Paramet, Calculate source term for Reynolds equation right-hand side.          Parameters, Fill coefficients matrix for Reynolds equation finite difference system. (+14 more)

### Community 14 - "MultiRotor"
Cohesion: 0.08
Nodes (19): MultiRotor, A class representing a multi-rotor system.      This class creates a system comp, Set the tag for the current multi-rotor., Set a tag for the given element., Adjust node positions of the driven rotor., Set nodes and nodes_pos lists., Join matrices from the driving rotor and driven rotor to form the matrix of, Calculate unbalance forces.          This is an auxiliary function the calculate (+11 more)

### Community 15 - "Guyan"
Cohesion: 0.07
Nodes (18): Guyan, ModelReduction, PseudoModal, Register subclasses in the subclasses dictionary.          Parameters         --, Transform a square matrix from physical to modal space.          Parameters, Transform a vector from physical to modal space.          Parameters         ---, Transform a vector from modal to physical space.          Parameters         ---, Guyan reduction method.      This method can be used to reduce model of the roto (+10 more)

### Community 16 - "test_stochastic_elements.py"
Cohesion: 0.07
Nodes (14): Return an iterator for the container.          Returns         -------         A, Return the value for a given key from attribute_dict.          Parameters, Random bearing element.      Creates an object containing a list with random ins, Set new parameter values for the object.          Function to change a parameter, Generate a list of objects as random attributes.          This function creates, Plot histogram and the PDF.          This function creates a histogram to displa, Return an instance of a simple random bearing.      The purpose is to make avail, st_bearing_example() (+6 more)

### Community 17 - "PointMass"
Cohesion: 0.08
Nodes (18): point_mass_example(), PointMass, Return a string representation of a point mass element.          Returns, Convert object into string.          Returns         -------         The object', A point mass element.      This class will create a point mass element.     This, Mass matrix for an instance of a point mass element.          This method will r, Damping matrix for an instance of a point mass element.          This method wil, Stiffness matrix for an instance of a point mass element.          This method w (+10 more)

### Community 18 - "test_bearing_seal_element.py"
Cohesion: 0.07
Nodes (12): bearing0(), bearing1(), bearing_6dof(), bearing_constant(), test_bearing_6dof_equality(), test_bearing_error2(), test_bearing_error_speed_not_given(), test_bearing_len_2() (+4 more)

### Community 19 - "ThrustPad"
Cohesion: 0.09
Nodes (12): Thermo-Hydro-Dynamic (THD) Tilting Pad Thrust Bearing.      This class provides, Store the residual value for the current frequency.          - If 'iteration' is, Calculates the equilibrium position of the bearing          Parameters         -, Calculate viscosity interpolation coefficients.          Parameters         ----, Create an example of a thrust bearing with Thermo-Hydro-Dynamic effects.      Th, Execute the complete thermo-hydrodynamic analysis for the tilting pad thrust bea, Initialize data structures to store fields information for each frequency., Store field results for the current frequency.          This method stores the c (+4 more)

### Community 20 - "test_stochastic_rotor_assembly.py"
Cohesion: 0.08
Nodes (19): Return the value for a given key from attribute_dict.          Parameters, Set new parameter values for the object.          Function to change a parameter, Random point mass element.      Creates an object containing a list with random, Generate a list of objects as random attributes.          This function creates, Plot histogram and the PDF.          This function creates a histogram to displa, Return an instance of a simple random point mass.      The purpose is to make av, Return an iterator for the container.          Returns         -------         A, ST_PointMass (+11 more)

### Community 21 - "Path"
Cohesion: 0.11
Nodes (21): Path, Load a SensitivityResults object from a TOML file.          This method reconstr, rotor1(), rotor_amb(), test_save_load_campbell(), test_save_load_campbell_json(), test_save_load_convergence(), test_save_load_criticalspeed() (+13 more)

### Community 22 - "ModalResults"
Cohesion: 0.09
Nodes (14): ModalResults, Class used to store results and provide plots for Modal Analysis.      Two optio, Update mode shapes based on eigenvectors., Map the whirl to a value.          Parameters         ----------         whirl:, r"""Calculate kappa for a given node and natural frequency.          frequency i, r"""Evaluate kappa values.          This function evaluates kappa given the inde, r"""Get the whirl direction for each frequency.          Returns         -------, r"""Get the whirl value (0., 0.5, or 1.) for each frequency.          Returns (+6 more)

### Community 23 - "ST_Material"
Cohesion: 0.11
Nodes (19): Random disk element.          Creates an object containing a list with random in, Return an iterator for the container.          Returns         -------         A, Return the value for a given key from attribute_dict.          Parameters, Set new parameter values for the object.          Function to change a parameter, Generate a list of objects as random attributes.          This function creates, Create instance of Material with random parameters.      Class used to create a, Plot histogram and the PDF.          This function creates a histogram to displa, ST_Material (+11 more)

### Community 24 - "fluid_flow.py"
Cohesion: 0.13
Nodes (21): find_equilibrium_position(), This function finds the equilibrium position of the rotor such that the fluid fl, calculate_attitude_angle(), calculate_eccentricity_ratio(), calculate_rotor_load(), external_radius_function(), internal_radius_function(), modified_sommerfeld_number() (+13 more)

### Community 25 - "Crack"
Cohesion: 0.10
Nodes (14): Crack, Model a crack on a given shaft element of a rotor system.     The Gasch and Maye, Validate the maximum allowed crack depth ratio for each crack model.         Eac, Get terms of the compliance matrix.          Parameters         -----------, Compute stiffness matrix of the shaft element with crack in inertial coordinates, Stiffness matrix of the shaft element with crack in rotating coordinates, Stiffness matrix of the shaft element with crack in rotating coordinates, Compute stiffness matrix of the shaft element with crack in inertial coordinates (+6 more)

### Community 26 - "CoAxialRotor"
Cohesion: 0.09
Nodes (17): ConvergenceResults, CriticalSpeedResults, Level1Results, Class used to store results from run_critical_speed() method.      Parameters, Convert units for undamped critical speeds.          Parameters         --------, Convert units for damped critical speeds.          Parameters         ----------, Class used to store results and provide plots rotor summary.      This class aim, Results class.      This class is a general abstract class to be implemented in (+9 more)

### Community 27 - "test_hybrid_seal.py"
Cohesion: 0.08
Nodes (21): HybridSeal, Hybrid seal - Compressible flow model with rotordynamic coefficients.      This, Print summary of hybrid seal analysis results.          This method displays a c, Plot convergence history.          This method creates a unified figure with thr, Plot pressure distribution for the hybrid seal.          Parameters         ----, hybrid_seal(), hybrid_seal_gc(), Test that hybrid coefficients are proper series combination. (+13 more)

### Community 28 - "signal_utils.py"
Cohesion: 0.12
Nodes (24): add_awgn(), amplitude_spectrum(), bicoherence(), bispectrum(), _defaults(), downsample_to(), harmonic_amplitude(), psd_welch() (+16 more)

### Community 29 - "Element"
Cohesion: 0.09
Nodes (13): Element, Get all subclasses of the Element class.          Returns         -------, Element class.      This class is a general abstract class to be implemented in, Mass matrix.          Returns         -------         A matrix of floats., Frequency dependent damping coefficients matrix.          Parameters         ---, Frequency dependent stiffness coefficients matrix.          Parameters         -, Gyroscopic matrix.          Returns         -------         A matrix of floats., Present a summary for the element.          A pandas series with the element pro (+5 more)

### Community 30 - "ThrustPadResults"
Cohesion: 0.11
Nodes (11): Post-processing results for a ThrustPad bearing.      Parameters     ----------, Compute Cartesian coordinate grids from the polar mesh geometry.          Return, Interpolate field data onto a regular Cartesian grid.          Parameters, Print results table for one frequency index.          Parameters         -------, Print a table comparing axial dynamic coefficients across all frequencies., Return a 3-D surface plot of the pressure field.          Parameters         ---, Return a 2-D contour plot of the pressure field.          Parameters         ---, Return a 3-D surface plot of the temperature field.          Parameters (+3 more)

### Community 31 - "test_examples.py"
Cohesion: 0.13
Nodes (22): This function instantiate a rotor similar to the example  5.9.2, page 208 (Dynam, This function instantiate a rotor similar to the example  5.9.5, page 212 (Dynam, This function instantiate a rotor similar to the example  5.9.3, page 209 (Dynam, This function instantiate a rotor similar to the example  5.9.4, page 210 (Dynam, This function instantiate a overhung rotor similar to the example  5.9.9, page 2, This function instantiate a rotor similar to the example  5.9.1, page 206 (Dynam, rotor_example1(), rotor_example2() (+14 more)

### Community 32 - "ABC"
Cohesion: 0.11
Nodes (15): ABC, crack_example(), Create an example to evaluate the influence of transverse cracks in a     rotati, misalignment_flex_example(), misalignment_rigid_example(), Misalignment module.  This module defines misalignments of various types on the, Create an example of a flexible combined misalignment fault.      This function, Create an example of a rigid misalignment fault.      This function returns time (+7 more)

### Community 33 - "StaticResults"
Cohesion: 0.10
Nodes (11): Plot the 2D deflected shape diagram.          Parameters         ----------, Plot the 3D deflected shape diagram.          Parameters         ----------, Plot deflected shape diagrams.          This method returns a subplot with:, Class used to store results and provide plots for Static Analysis.      This cla, Plot the shaft static deformation.          This method plots:             defor, Plot the rotor free-body diagram.          Parameters         ----------, Plot the rotor shearing force diagram.          This method plots:             s, Plot the rotor bending moment diagram.          This method plots:             b (+3 more)

### Community 34 - "PlainJournalResults"
Cohesion: 0.10
Nodes (11): PlainJournalResults, Post-processing results for a PlainJournal bearing.      Parameters     --------, Print results table for one speed.          Parameters         ----------, Print a table comparing the full 2×2 dynamic coefficient matrix         across a, Return a 3-D surface plot of the pressure field (theta vs z).          Parameter, Return a 2-D contour plot of the pressure field (theta vs z).          Parameter, Return a 3-D surface plot of the temperature field (theta vs z).          Parame, Return a 2-D contour plot of the temperature field (theta vs z).          Parame (+3 more)

### Community 35 - "CouplingElement"
Cohesion: 0.10
Nodes (11): CouplingElement, Return a string representation of a coupling element.          Returns         -, A coupling element.      This class creates a coupling element from input data o, Read and parse data stored in a .toml or .json file.          Parameters, Mass matrix for an instance of a coupling element.          This method will ret, Stiffness matrix for an instance of a coupling element.          This method wil, Stiffness matrix for an instance of a coupling element.          For a coupling, Damping matrix for an instance of a coupling element.          This method will (+3 more)

### Community 36 - "SensitivityResults"
Cohesion: 0.12
Nodes (11): ndarray, Results from the sensitivity analysis for the rotor AMBs.      This class holds, Plots sensitivity analysis results.          This method generates a plot of the, Prepare sensitivity data for plotting based on user preferences.          This m, Plot time-domain results from sensitivity analysis.          This method generat, Build and add a trace for time-domain results to a Plotly figure.          This, Convert a NumPy ndarray to a Python list.          Parameters         ----------, Convert a Python list to a NumPy ndarray.          Parameters         ---------- (+3 more)

### Community 37 - "Shape"
Cohesion: 0.17
Nodes (10): Rotor shape 2d plot.          Parameters         ----------         orientation, Plot orbits in 3D.          Parameters         ----------         animation : bo, Class used to construct a mode or a deflected shape from a eigen or response vec, Classify the mode type.          Classifies the mode type as Lateral, Axial, or, Calculate orbits for each node in the shape., Calculate shape data for plotting.          Includes calculation of orbits and n, This function is used to fix the mode shape plot, especially for multi rotors, Plot axial mode shape.          Parameters         ----------         plot_dimen (+2 more)

### Community 38 - "ST_ShaftElement"
Cohesion: 0.11
Nodes (12): Get relevant attributes from a rotor system.          This auxiliary funtion get, Return an iterator for the container.          Returns         -------         A, Return the value for a given key from attribute_dict.          Parameters, Random shaft element.      Creates an object containing a generator with random, Set new parameter values for the object.          Function to change a parameter, Generate a list of objects as random attributes.          This function creates, Plot histogram and the PDF.          This function creates a histogram to displa, Return an instance of a simple random shaft element.      The purpose is to make (+4 more)

### Community 39 - "ST_Rotor"
Cohesion: 0.13
Nodes (11): object, Return an iterator for the container.          Returns         -------         A, Return the value for a given key from attribute_dict.          Parameters, Set new parameter values for the object.          Function to change a parameter, r"""A random rotor object.      This class will create several rotors according, Build new list of arguments from a random list of arguments.          This funti, Generate a list of random parameters.          This function creates a list of p, Generate a list of random objects from random attributes.          This function (+3 more)

### Community 40 - ".coefficients"
Cohesion: 0.13
Nodes (12): _assemble_energy_sparse_numba(), _assemble_reynolds_sparse_numba(), _calculate_turbulent_viscosity_numba(), Solve Reynolds equation for pressure field using finite difference method., Solve energy equation for the film temperature field using a sparse matrix solve, Update temperature field from solution vector.          Parameters         -----, Transform coordinates from inertial to pad coordinate system.          Parameter, Check matrix diagonal for zero elements and replace them with a small residual v (+4 more)

### Community 41 - "plot_utils.py"
Cohesion: 0.12
Nodes (17): _bispectrum_z(), plot_bispectrum_surface(), plot_trispectrum_balls(), plotly_bicoherence_surface(), plotly_bispectrum_surface(), plotly_spectrum(), plotly_time(), plotly_trispectrum_balls() (+9 more)

### Community 42 - "calculate_stiffness_and_damping_coefficients"
Cohesion: 0.17
Nodes (11): calculate_short_damping_matrix(), calculate_stiffness_and_damping_coefficients(), This function calculates the bearing stiffness and damping matrices numerically., This function calculates the damping matrix for the short bearing.     Parameter, move_rotor_center(), For a given step on x or y axis,     moves the rotor center and calculates new e, Instantiate a bearing using inputs from its fluid flow.          Parameters, This function instantiate a bearing using the fluid flow class and test if it ma (+3 more)

### Community 43 - "FluidFlow"
Cohesion: 0.13
Nodes (13): fluid_flow_example(), fluid_flow_example3(), fluid_flow_example4(), FluidFlow, r"""Generate dynamic coefficients for hydrodynamic bearings.      This class cal, This function calculates the pressure matrix analytically         for the cylind, This function calculates the constants that form the Poisson equation         of, This function assembles the matrix M and the independent vector f.         Param (+5 more)

### Community 44 - "._thermal_coupling_iteration"
Cohesion: 0.13
Nodes (9): Solve the thermo-hydrodynamic equations to determine equilibrium position and fi, Solve 2D steady-state heat conduction equation in pad.          Equation in cyli, Compute outlet temperature for pad n_p.          Mean temperature at the trailin, Compute circumferential volumetric flow Q_x at column `jj` of pad n_p., Compute Q_out for pad n_p: flow at the minimum film thickness location., Compute Q_in for pad n_p: flow at the leading edge (column 0).          Under fl, Compute inlet temperature of the next pad via hot-oil carry-over mixing (Temp_Mi, Perform coupled film-pad thermal iteration until convergence.          This meth (+1 more)

### Community 45 - "Probe"
Cohesion: 0.12
Nodes (9): Probe, Class of a probe.      This class will create a probe object to be used in the r, Return the node, angle, and direction of the probe.          Returns         ---, test_crack_gasch_resp(), test_crack_mayes_equality(), test_crack_mayes_resp(), test_probe_response(), test_harmonic_response() (+1 more)

### Community 46 - "ST_DiskElement"
Cohesion: 0.12
Nodes (12): Set new parameter values for the object.          Function to change a parameter, Generate a list of objects as random attributes.          This function creates, Random disk element.      Creates an object containing a list with random instan, Plot histogram and the PDF.          This function creates a histogram to displa, Return an instance of a simple random disk.      The purpose is to make availabl, Return an iterator for the container.          Returns         -------         A, Return the value for a given key from attribute_dict.          Parameters, st_disk_example() (+4 more)

### Community 47 - "BearingResults"
Cohesion: 0.12
Nodes (9): BearingResults, Print a formatted summary of the bearing analysis results.          Returns, Print a table comparing dynamic coefficients across frequencies.          Return, Return a 3-D surface plot of the pressure field.          Parameters         ---, Return a 2-D contour plot of the pressure field.          Parameters         ---, Return a 3-D surface plot of the temperature field.          Parameters, Return a 2-D contour plot of the temperature field.          Parameters, Abstract base class for fluid film bearing post-processing results.      Each be (+1 more)

### Community 48 - "GearElementTVMS"
Cohesion: 0.14
Nodes (9): GearElementTVMS, A gear element with Time-Varying Mesh Stiffness (TVMS) modeling.      This class, Create a gear element from geometry properties.          This class method will, Involute function          Calculates the involute function for a given angle. T, Transforms the pressure angle, used to build the involute profile,         into, Method for evaluating the stiffness commonly found in the         integrative fu, Method used in evaluating the stiffness commonly found in the         integrativ, Compute the y, x, area and I_y of the transition curve given a gamma         ang (+1 more)

### Community 49 - "st_rotor_assembly.py"
Cohesion: 0.23
Nodes (9): Bearing element module for STOCHASTIC ROSS.  This module creates an instance of, Disk element module for STOCHASTIC ROSS.  This module creates an instance of ran, Materials module.  This module defines the Material class and defines some of th, Point mass element module for STOCHASTIC ROSS.  This module creates an instance, plot_histogram(), Plotting module for elements.  This modules provides functions to plot the eleme, Plot histogram and the PDF.      This function creates a histogram to display th, STOCHASTIC ROSS Module.  This module creates random rotor instances and run stoc (+1 more)

### Community 50 - "test_plain_journal.py"
Cohesion: 0.12
Nodes (16): plain_journal_lund(), plain_journal_perturbation(), Fixture for PlainJournal with perturbation method, Test equilibrium position for lund method, Test coefficients for perturbation method, Test coefficients for lund method, Fixture for PlainJournal with lund method, Test basic parameters for perturbation method (+8 more)

### Community 51 - "._equilibrium_objective"
Cohesion: 0.13
Nodes (9): _calculate_hydrodynamic_forces_numba(), Objective function for complete equilibrium optimization.          This method s, Solve thermo-hydrodynamic fields for a single pad in equilibrium optimization., Calculate the equilibrium position for a single pad.          This method serves, Compute physical limits (alpha_min, alpha_max) for pad rotation angles         g, Validate and adjust pad rotation angle within physical limits.          Paramete, Calculate hydrodynamic forces and moments from pressure field.          Paramete, Calculate hydrodynamic forces and moments using Numba.      This function comput (+1 more)

### Community 52 - "test_gear_element.py"
Cohesion: 0.13
Nodes (6): GearElement, Create a gear element from geometry properties.          This class method will, Gear element patch.          Patch that will be used to draw the gear element us, A gear element.      This class creates a gear element from input data of inerti, gear(), gear_tvms()

### Community 53 - "Mesh"
Cohesion: 0.17
Nodes (8): Mesh, Represents the meshing behavior between two gears in contact     including stiff, Calculates the contact ratio of the gear pair.          Parameters         -----, Parameters         ---------         d_alpha : float             The angular dis, Calculate the variable stiffness of a gear pair.          This method computes t, Computes the mesh stiffness profile over a specified number of gear         mesh, Plots the gear mesh stiffness profile over one or more meshing periods., mesh()

### Community 54 - "CampbellResults"
Cohesion: 0.13
Nodes (9): CampbellResults, ClearanceResults, Class used to store results and provide plots for Campbell Diagram.      It's po, Sort by mode type.          Sort the Campbell result arrays (`wd`, `log_dec`, `d, Create Campbell Diagram figure using Plotly.          Parameters         -------, Helper method to plot Campbell diagram with mode shape.          Parameters, Results for clearance analysis.      Stores vibration amplitudes at bearing loca, Enable dict-like access for backward compatibility. (+1 more)

### Community 55 - "test_6dof_model.py"
Cohesion: 0.14
Nodes (3): input_run_time(), test_run_time(), test_time_resp_equality()

### Community 56 - "MisalignmentFlex"
Cohesion: 0.16
Nodes (9): Exception, MisalignmentFlex, Reaction forces of parallel misalignment.          ang_pos : array_like, Reaction forces of angular misalignment.          ang_pos : array_like, Model misalignment on a given flexible coupling element of a rotor system., Reaction forces of combined (parallel and angular) misalignment.          ang_po, Run analysis for the system with misalignment given an unbalance force., Run analysis for the rotor system with misalignment given an         unbalance f (+1 more)

### Community 57 - "TimeResponseResults"
Cohesion: 0.16
Nodes (8): Class used to store results and provide plots for Time Response Analysis.      T, Return the time response given a list of probes in DataFrame format.          Pa, Plot time response.          This method plots the time response given a list of, Calculate dFFT - discrete Fourier Transform.          Parameters         -------, Plot response in frequency domain.          This method plots the frequency doma, Reconstruct the time-domain response from frequency-domain results.          Ret, Get the time response results.          Returns         -------         time_res, TimeResponseResults

### Community 58 - "ST_ForcedResponseResults"
Cohesion: 0.21
Nodes (8): Store stochastic results and provide plots for Forced Response.      Parameters, Calculate the major axis for a node for each frequency.          Parameters, Plot stochastic frequency response.          This method plots the unbalance res, Plot stochastic frequency response.          This method plots the phase respons, Plot polar forced response using Plotly.          Parameters         ----------, Plot stochastic forced response using Plotly.          This method plots the for, Plot frequency response.          This method plots the frequency and phase resp, ST_ForcedResponseResults

### Community 59 - "SqueezeFilmDamperResults"
Cohesion: 0.18
Nodes (8): Post-processing results for a SqueezeFilmDamper bearing.      The SFD uses close, Print a table comparing SFD coefficients across all frequencies.          Parame, Not available for SqueezeFilmDamper (analytical model).          Raises, Not available for SqueezeFilmDamper (analytical model).          Raises, Not available for SqueezeFilmDamper (analytical model).          Raises, Not available for SqueezeFilmDamper (analytical model).          Raises, Generate and return all standard bearing result plots.          Calls the four a, SqueezeFilmDamperResults

### Community 60 - "test_fluid_flow.py"
Cohesion: 0.16
Nodes (18): calculate_oil_film_force(), This function calculates the forces of the oil film in the N and T directions, i, fluid_flow_example2(), This function returns a different instance of a simple fluid flow.     The purpo, fluid_flow_long_numerical(), fluid_flow_short_friswell(), fluid_flow_short_numerical(), This function instantiate a bearing using the fluid flow class and test if it ma (+10 more)

### Community 61 - "fluid_flow_graphics.py"
Cohesion: 0.20
Nodes (13): plot_eccentricity(), plot_pressure_surface(), plot_pressure_theta(), plot_pressure_theta_cylindrical(), plot_pressure_z(), plot_shape(), Plot the pressure distribution along the z-axis.      This function assembles pr, Plot the surface geometry of the rotor.      This function assembles a graphic r (+5 more)

### Community 62 - "MagneticBearingElement"
Cohesion: 0.17
Nodes (9): MagneticBearingElement, Magnetic Bearing Element.      This class represents an active magnetic bearing, Generate hover information for magnetic bearing element.          Overrides the, Compute AMB control force for one axis using the discrete controller.          T, Return the continuous-time (analog) controller transfer function.          This, Discretize the analog controller and initialize its state-space representation., magnetic_bearing(), test_magnetic_bearing_with_lead_controller_matches_frequency_response() (+1 more)

### Community 63 - "SqueezeFilmDamper"
Cohesion: 0.21
Nodes (6): Squeeze Film Damper (SFD) element in ROSS standard format.     Computes damping, Calculate coefficients for a sealed SFD without a groove.          Parameters, Calculate coefficients for an SFD with a groove and no end seals.          Param, Calculate coefficients for an SFD with both a groove and end seals.          Par, SqueezeFilmDamper, squeeze_film_damper()

### Community 64 - "PlainJournal"
Cohesion: 0.24
Nodes (6): PlainJournal, Plain journal bearing - Advanced thermo-hydro-dynamic model.      This class pro, This method runs the optimization to find the equilibrium position of         th, This method is used to create a relationship between viscosity and         tempe, Calculates the dynamic coefficients of stiffness "k" and damping "c".         Ba, In this method, the solution of the Reynolds equation is perturbed,         with

### Community 65 - "test_transient_newmark.py"
Cohesion: 0.73
Nodes (5): simulation_parameters(), test_for_cte_speed(), test_for_var_speed_1(), test_for_var_speed_2(), unbalance_force()

### Community 66 - "DiskElement"
Cohesion: 0.17
Nodes (7): DiskElement, A disk element.      This class creates a disk element from input data of inerti, Stiffness matrix for an instance of a disk element.          This method will re, Damping matrix for an instance of a disk element.          This method will retu, Gyroscopic matrix for an instance of a disk element.          This method will r, Calculate the polar moment of inertia of a disk from its geometry.          Para, test_static_bearing_with_disks()

### Community 67 - "._compute_stiffness"
Cohesion: 0.23
Nodes (6): Computes the stiffness in the direction of the applied force on the         gear, Calculate the stiffness contribution from the gear resistance from         shear, Calculate the stiffness contribution from the gear resistance from         bendi, Calculate the stiffness contribution from the gear resistance from         axial, Integrates a function over the transition region of the gear tooth.          Par, Integrates a function over the involute region of the gear tooth.          Param

### Community 68 - ".integrate_system"
Cohesion: 0.17
Nodes (6): Run Active Magnetic Bearing (AMB) sensitivity analysis.          This method per, Compute control forces for Active Magnetic Bearings (AMBs).          This method, Time integration for a rotor system.          This method returns the time respo, Prepare the magnetic bearing components and force function used during         t, Time response for a rotor.          This method returns the time response for a, Calculate the time response.          This function will take a rotor object and

### Community 69 - "test_disk_element.py"
Cohesion: 0.17
Nodes (4): disk(), disk_from_geometry(), test_save_load(), test_save_load_json()

### Community 70 - ".__init__"
Cohesion: 0.18
Nodes (5): Initialize all arrays used in the thermo-hydrodynamic analysis.          This me, Reset force arrays for each frequency iteration.          Returns         ------, Calculate viscosity interpolation coefficients.          Parameters         ----, Create 2D mesh for thermal analysis of pads.          Local coordinates:, Execute the complete thermo-hydrodynamic analysis for the tilting pad bearing.

### Community 71 - "MisalignmentRigid"
Cohesion: 0.25
Nodes (6): MisalignmentRigid, Model misalignment on a given rigid coupling element of a rotor system.      Cal, Calculate reaction forces of parallel misalignment.          Parameters, Calculate the dynamic force on given time step.          Paramenters         ---, Run analysis for the system with rubbing given an unbalance force.          Syst, test_mis_rigid()

### Community 72 - "Rubbing"
Cohesion: 0.22
Nodes (6): Model rubbing based on Finite Element Method on a given shaft element of a     r, Calculate the dynamic force on given time step.          Paramenters         ---, Run analysis for the system with rubbing given an unbalance force.          Syst, Calculate the force on the shaft element with rubbing.          Parameters, Rubbing, Run analysis for the rotor system with rubbing given an unbalance force.

### Community 73 - "UCSResults"
Cohesion: 0.18
Nodes (6): Helper method to update 3D mode shape plot.          Parameters         --------, Class used to store results and provide plots for UCS Analysis.      Parameters, Plot undamped critical speed map.          This method will plot the undamped cr, Plot (2D view) the mode shape.          Parameters         ----------         cr, Plot (3D view) the mode shapes.          Parameters         ----------         c, UCSResults

### Community 74 - ".load"
Cohesion: 0.18
Nodes (8): Read and parse data stored in a .toml file.          The data passed to this met, Load results from a .toml or .json file.          This function will load the si, compressor_example(), Load rotor from a .toml or .json file.          This method restores a rotor fro, Create a compressor as example.      This function returns an instance of a roto, rotor9(), test_save_load(), test_save_load_json()

### Community 75 - "ST_TimeResponseResults"
Cohesion: 0.18
Nodes (6): Store stochastic results and provide plots for Time Response and Orbit Response., Plot stochastic time response.          This method plots the time response give, Plot orbit response (2D).          This function plots orbits for a given node o, Plot orbit response (3D).          This function plots orbits for each node on t, ST_TimeResponseResults, Stochastic time response for multiples rotor systems.          This function wil

### Community 76 - "ST_CampbellResults"
Cohesion: 0.22
Nodes (6): Store stochastic results and provide plots for Campbell Diagram.      It's possi, Plot the damped natural frequencies vs frequency.          Parameters         --, Plot the log. decrement vs frequency.          Parameters         ----------, Plot Campbell Diagram.          This method plots Campbell Diagram.          Par, ST_CampbellResults, Stochastic Campbell diagram for multiples rotor systems.          This function

### Community 77 - "test_misalignment.py"
Cohesion: 0.18
Nodes (4): test_mis_angular_resp(), test_mis_comb_resp(), test_mis_parallel_resp(), test_mis_rigid_resp()

### Community 78 - "._print_single_frequency_results"
Cohesion: 0.20
Nodes (5): Print a formatted summary of thrust pad bearing results.          Iterates over, Print a formatted summary of plain journal bearing results.          Iterates ov, Print a formatted summary of SFD results for all frequencies.          Parameter, Print results table for one frequency index.          Parameters         -------, Print a formatted summary of tilting pad bearing results.          Iterates over

### Community 79 - "._forces"
Cohesion: 0.20
Nodes (6): This method is used to set the objective function of minimize optimization., Calculate the sommerfeld number. This dimensionless number is used to         ca, Solve the linear system Ax = b using sparse matrix solver., Calculates the forces in Y and X directions.          Parameters         -------, In this method, small perturbations are applied to the rotor around its equilibr, _solve()

### Community 80 - "._temperature_convergence_loop"
Cohesion: 0.20
Nodes (6): _calculate_pressure_gradients_numba(), Perform temperature convergence loop for thermo-hydrodynamic analysis., Calculate dimensionless viscosity based on temperature.          Parameters, Calculate pressure gradients using finite differences., Calculate interface conductance at film-pad inner surface.          Uses harmoni, Calculate pressure gradients using finite differences with Numba.      Parameter

### Community 81 - "utils.py"
Cohesion: 0.08
Nodes (29): Initialize the SensitivityResults instance.          This constructor processes, compute_abs_phase(), compute_fft(), compute_freq_resp(), _converge_newmark(), convert(), DataNotFoundError, get_data_from_figure() (+21 more)

### Community 83 - "FrequencyResponseResults"
Cohesion: 0.22
Nodes (5): FrequencyResponseResults, Class used to store results and provide plots for Frequency Response.      Param, Plot frequency response (magnitude) using Plotly.          This method plots the, Plot frequency response (phase) using Plotly.          This method plots the fre, Plot frequency response (polar) using Plotly.          This method plots the fre

### Community 84 - "ST_FrequencyResponseResults"
Cohesion: 0.22
Nodes (5): Store stochastic results and provide plots for Frequency Response.      Paramete, Plot stochastic frequency response (magnitude) using Plotly.          This metho, Plot stochastic frequency response (phase) using Plotly.          This method pl, Plot stochastic frequency response (polar) using Plotly.          This method pl, ST_FrequencyResponseResults

### Community 85 - "BearingFluidFlow"
Cohesion: 0.25
Nodes (3): BearingFluidFlow, Instantiate a bearing using inputs from its fluid flow.      .. deprecated:: 2.0, test_bearing_fluid_flow()

### Community 86 - "calculate_short_stiffness_matrix"
Cohesion: 0.33
Nodes (6): calculate_short_stiffness_matrix(), This function calculates the stiffness matrix for the short bearing.     Paramet, This function instantiate a bearing using the fluid flow class and test if it ma, This function instantiate a bearing using the fluid flow class and test if it ma, test_stiffness_matrix(), test_stiffness_matrix_numerical()

### Community 87 - "CylindricalBearing"
Cohesion: 0.29
Nodes (5): CylindricalBearing, Cylindrical hydrodynamic bearing - Simplified analytical model.      This class, Generate hover information for cylindrical bearing element.          Overrides t, Bearing element patch.          Patch that will be used to draw the bearing elem, test_cylindrical_hydrodynamic()

### Community 90 - "test_units.py"
Cohesion: 0.43
Nodes (4): auxiliary_function(), test_unit_Q_(), test_unit_Q_conversion(), test_units()

### Community 91 - "sinha_helpers.py"
Cohesion: 0.33
Nodes (5): get_harmonic_amplitude(), probe_dof_indices(), Shared post-processing helpers for the Sinha replication notebooks.  Provenance, Return the FFT amplitude at the frequency bin closest to ``target_freq_hz``., Return the global ``(dof_x, dof_y)`` indices for a probe node.      Accounts for

### Community 92 - "._get_coefficient_list"
Cohesion: 0.33
Nodes (3): List with all bearing coefficients as strings          Parameters         ------, Return frequency vs coefficients in table format.          Parameters         --, Equality method for comparisons.          Parameters         ----------

### Community 93 - "_flooded"
Cohesion: 0.67
Nodes (4): _calculate_discretization_coeffs(), _evaluate_bearing_clearance(), _flooded(), _starvation()

### Community 94 - ".C"
Cohesion: 0.33
Nodes (3): Mass matrix for an instance of a shaft element.          Returns         -------, Stiffness matrix for an instance of a shaft element.          Returns         --, Stiffness matrix for an instance of a shaft element.          Returns         --

### Community 95 - "BallBearingElement"
Cohesion: 0.40
Nodes (4): BallBearingElement, A bearing element for ball bearings.      This class will create a bearing eleme, Generate hover information for ball bearing element.          Overrides the base, test_ball_bearing_element()

### Community 96 - ".from_table"
Cohesion: 0.40
Nodes (3): Convert bearing parameters to toml.          Convert a table with parameters of, Instantiate a bearing using inputs from an Excel table.          A header with t, test_from_table()

### Community 97 - "RollerBearingElement"
Cohesion: 0.40
Nodes (5): A bearing element for roller bearings.      This class will create a bearing ele, RollerBearingElement, Test save/load round-trip for bearing subclasses.      Verifies that subclass-sp, test_roller_bearing_element(), test_save_load_subclasses()

### Community 102 - "mod"
Cohesion: 0.50
Nodes (3): mod(), Interpolates the mesh stiffness value at a given angular position.          Para, Calculates the remainder of a division, but replaces 0 with max_val.      Parame

### Community 103 - ".run_ucs"
Cohesion: 0.15
Nodes (10): Plot a rotor object.          This function will take a rotor object and plot it, Run Undamped Critical Speeds analyzes.          This method will run the undampe, Find the linked bearing element by node          Parameters         ----------, Return a new shaft element based on the current instance.          Any attribute, convert_6dof_to_4dof(), convert_6dof_to_torsional(), Convert a 6 dof rotor model to a model with only torsional dofs.      This funct, Removes specified degrees of freedom from the given matrix.      By default, thi (+2 more)

## Knowledge Gaps
- **2 isolated node(s):** `render_diagrams.sh script`, `ross-rotordynamics`
  These have ≤1 connection - possible missing edges or undocumented components.
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Rotor` connect `Rotor` to `test_rotor_assembly.py`, `SealElement`, `Material`, `LabyrinthSeal`, `rotor_assembly.py`, `ForcedResponseResults`, `units.py`, `.__eq__`, `.run_modal`, `load_data`, `.unbalance_force_over_time`, `MultiRotor`, `Guyan`, `.add_nodes`, `PointMass`, `ModalResults`, `Crack`, `CoAxialRotor`, `StaticResults`, `CouplingElement`, `SensitivityResults`, `Shape`, `ST_Rotor`, `Probe`, `st_rotor_assembly.py`, `CampbellResults`, `MisalignmentFlex`, `TimeResponseResults`, `MagneticBearingElement`, `test_transient_newmark.py`, `DiskElement`, `.integrate_system`, `Rubbing`, `UCSResults`, `.load`, `FrequencyResponseResults`, `BearingFluidFlow`, `CylindricalBearing`, `BallBearingElement`, `RollerBearingElement`, `.run_ucs`, `test_from_section`?**
  _High betweenness centrality (0.225) - this node is a cross-community bridge._
- **Why does `BearingElement` connect `Rotor` to `SealElement`, `rotor_assembly.py`, `units.py`, `load_data`, `.run_modal`, `TiltingPad`, `test_stochastic_elements.py`, `test_bearing_seal_element.py`, `ThrustPad`, `test_stochastic_rotor_assembly.py`, `CoAxialRotor`, `Element`, `st_rotor_assembly.py`, `MagneticBearingElement`, `SqueezeFilmDamper`, `PlainJournal`, `test_transient_newmark.py`, `.load`, `BearingFluidFlow`, `CylindricalBearing`, `._get_coefficient_list`, `BallBearingElement`, `.from_table`, `RollerBearingElement`, `.G`, `.run_ucs`, `._process_coefficient`, `test_from_section`, `.C`, `.dof_mapping`, `._hover_info`, `.M`, `.plot`, `.read_toml_data`, `.__repr__`?**
  _High betweenness centrality (0.182) - this node is a cross-community bridge._
- **Why does `TiltingPad` connect `TiltingPad` to `Rotor`, `TestTiltingPadEquilibrium`, `.__init__`, `.coefficients`, `units.py`, `TestTiltingPadHydrodynamicForces`, `TiltingPadResults`, `._thermal_coupling_iteration`, `TestTiltingPadDynamicCoefficients`, `._temperature_convergence_loop`, `._equilibrium_objective`, `TestTiltingPadGeometry`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `Rotor` (e.g. with `MultiRotor` and `CampbellResults`) actually correct?**
  _`Rotor` has 36 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `BearingElement` (e.g. with `Element` and `PlainJournal`) actually correct?**
  _`BearingElement` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ShaftElement` (e.g. with `CouplingElement` and `CoAxialRotor`) actually correct?**
  _`ShaftElement` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `TiltingPad` (e.g. with `BearingElement` and `TiltingPadResults`) actually correct?**
  _`TiltingPad` has 6 INFERRED edges - model-reasoned connections that need verification._