# SIR Epidemic Simulation

![e510250d-4119-43ec-81e0-f58b8dfd13b2](https://github.com/user-attachments/assets/b7722649-56e4-4652-983f-fc58f64fc69d)

An interactive Python simulation of the classic **SIR (Susceptible–Infected–Recovered)** epidemiological model. Explore how diseases spread through populations with real-time parameter adjustment and live visualization.

## Built With
- **Python 3.7+**
- **Matplotlib** - Interactive plotting and visualization
- **Tkinter** - Cross-platform GUI framework
- **SciPy** - Numerical integration for solving differential equations
- **NumPy** - Mathematical computations

---

## What is the SIR Model?

The **SIR model** is a fundamental compartmental model in epidemiology that tracks how infectious diseases spread through populations by dividing individuals into three states:

- **S(t)** – **Susceptible** individuals (can catch the disease)
- **I(t)** – **Infected** individuals (currently sick and contagious)  
- **R(t)** – **Recovered** individuals (immune after recovery)

### Mathematical Foundation

The model uses a system of ordinary differential equations (ODEs):

```
dS/dt = -β × S × I / N
dI/dt = β × S × I / N - γ × I  
dR/dt = γ × I
```

**Where:**
- **β (beta)** = infection rate (how easily the disease spreads)
- **γ (gamma)** = recovery rate (how quickly people recover)
- **N** = total population (S + I + R = constant)

### Disease Flow
```
Susceptible → Infected → Recovered
     (β)         (γ)
```

---

## Features

### Interactive Controls
- **Real-time sliders** for all key parameters
- **Run/Reset buttons** for simulation control
- **Live plot updates** as you adjust parameters

### Adjustable Parameters
- **Infection Rate (β)**: 0.1 - 1.0
- **Recovery Rate (γ)**: 0.05 - 0.5  
- **Population Size**: 100 - 10,000
- **Initial Infected**: 1 - 100
- **Simulation Duration**: 50 - 365 days

### Real-Time Statistics
- **Peak Infected**: Maximum simultaneous infections
- **Peak Day**: When the outbreak peaks
- **Attack Rate**: Percentage of population infected
- **R₀ Value**: Basic reproduction number (β/γ)

---


## Example Results

![image](https://github.com/user-attachments/assets/46260c8c-baf2-4ffe-bac1-8f207d2d1f23)

**Default simulation shows:**
- **Blue curve (Susceptible)**: Starts at 999, decreases as people get infected
- **Red curve (Infected)**: Peaks around day 38 with ~301 people infected
- **Green curve (Recovered)**: Grows to ~950 people by the end


---



## References & Further Reading

- [Kermack, W. O., & McKendrick, A. G. (1927).](https://jxshix.people.wm.edu/2009-harbin-course/classic/Kermack-McKendrick-1927-I.pdf)
- **[Epidemiological Models](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology)** - Comprehensive overview


---
>  This project includes AI-assisted content.
Some images were generated using AI tools (Chatgpt), and portions of the code were reviewed or optimized with the help of AI (ChatGPT). All outputs have been manually tested and validated.

---
## License

This project is open source and available under the [MIT License].
