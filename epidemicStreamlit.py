import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import streamlit as st

class SIRModel:
    def __init__(self, beta, gamma, population, init_infected):
        self.beta = beta
        self.gamma = gamma
        self.population = population
        self.init_infected = init_infected
        self.init_susceptible = population - init_infected
        self.init_recovered = 0

    def deriv(self, y, t):
        S, I, R = y
        N = S + I + R
        dSdt = -self.beta * S * I / N
        dIdt = self.beta * S * I / N - self.gamma * I
        dRdt = self.gamma * I
        return [dSdt, dIdt, dRdt]

    def run_simulation(self, days):
        y0 = [self.init_susceptible, self.init_infected, self.init_recovered]
        t = np.linspace(0, days, days)
        result = odeint(self.deriv, y0, t)
        return t, result.T

st.title("SIR Epidemic Simulator")

beta = st.slider("Infection Rate (β)", 0.1, 1.0, 0.3, 0.01)
gamma = st.slider("Recovery Rate (γ)", 0.05, 0.5, 0.1, 0.01)
population = st.slider("Population Size", 100, 10000, 1000, 100)
init_infected = st.slider("Initial Infected", 1, 100, 1)
days = st.slider("Simulation Days", 50, 365, 160)

model = SIRModel(beta, gamma, population, init_infected)
t, (S, I, R) = model.run_simulation(days)

fig, ax = plt.subplots()
ax.plot(t, S, label="Susceptible")
ax.plot(t, I, label="Infected")
ax.plot(t, R, label="Recovered")
ax.set_xlabel("Days")
ax.set_ylabel("Population")
ax.set_title("SIR Model")
ax.legend()
ax.grid(True)
st.pyplot(fig)

peak_day = t[np.argmax(I)]
peak_infected = np.max(I)
attack_rate = R[-1] / population * 100
r0 = beta / gamma

st.subheader("Peak Stats")
st.write(f"Peak Infected: {int(peak_infected)}")
st.write(f"Peak Day: {int(peak_day)}")
st.write(f"Final Recovered: {int(R[-1])}")
st.write(f"Attack Rate: {attack_rate:.2f}%")
st.write(f"R₀: {r0:.2f}")
