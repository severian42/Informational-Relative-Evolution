Introduction to the IRE Three-Body Simulation

Overview

The three-body problem is one of the most famous examples of deterministic chaos in physics. Small differences in initial conditions lead to drastically different trajectories over time, making long-term prediction notoriously difficult.
This experiment investigates whether the Information Relative Evolution (IRE) principle—which treats structured information as a physically relevant quantity—can be used to predict and analyze chaotic behavior beyond traditional Newtonian mechanics.

Key Differences from Classical Approaches

Beyond Newtonian Determinism:

Standard solvers track only mass, velocity, and force interactions.

This simulation adds an information coherence field ψ(x,t)\psi(x,t)ψ(x,t) to measure how structured the system’s state remains over time.

Introducing the IRE Field:

The IRE field ψ(x,t)\psi(x,t)ψ(x,t) is defined as: ψ(x,t)=e−12σ2∑i=13∣∣x−ri∣∣2⋅e−Ct/2\psi(x,t) = e^{-\frac{1}{2\sigma^2} \sum_{i=1}^{3} ||x - r_i||^2} \cdot e^{-C_t / 2}ψ(x,t)=e−2σ21​∑i=13​∣∣x−ri​∣∣2⋅e−Ct​/2 where:
σ\sigmaσ is a coherence scaling factor.

rir_iri​ are the positions of the three bodies.

CtC_tCt​ is the chaos measure, tracking orbital instability.

Measuring Chaos and Information Coherence:

The chaos measure CtC_tCt​ is defined as: Ct=∑i≠j∣vi×(rj−ri)∣∣∣rj−ri∣∣2+ϵC_t = \sum_{i \neq j} \frac{|v_i \times (r_j - r_i)|}{||r_j - r_i||^2 + \epsilon}Ct​=i=j∑​∣∣rj​−ri​∣∣2+ϵ∣vi​×(rj​−ri​)∣​ where viv_ivi​ are velocities and rj−rir_j - r_irj​−ri​ are relative displacements.

This quantifies how rapidly the system's order breaks down.

Prediction Accuracy Test:

The simulation compares IRE-enhanced predictions to standard Newtonian motion.

Uses Mean Squared Error (MSE) to quantify how well the system remains predictable.

Results & What This Means

The IRE field does not modify Newton’s laws, but it adds an additional predictive layer that identifies and tracks coherence patterns in chaotic systems.
This provides a new way to analyze determinism within chaotic systems, potentially improving long-term forecasting in multi-body dynamics.

Conclusion: Why This Matters

This simulation provides a controlled test of the IRE principle in one of physics’ most fundamental chaotic systems. If IRE-based coherence tracking improves predictability, it would suggest that structured information itself has measurable and deterministic properties, opening the door for new approaches in physics, AI, and complex systems modeling.
