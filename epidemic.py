import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class SIRModel:
    def __init__(self, beta=0.3, gamma=0.1, population=1000, init_infected=1):
        self.beta = beta              # infection rate
        self.gamma = gamma            # recovery rate
        self.population = population
        self.init_infected = init_infected
        self.init_susceptible = population - init_infected
        self.init_recovered = 0

    def deriv(self, y, t):
        # y = [S, I, R]
        S, I, R = y
        N = S + I + R
        dSdt = -self.beta * S * I / N
        dIdt = self.beta * S * I / N - self.gamma * I
        dRdt = self.gamma * I
        return [dSdt, dIdt, dRdt]

    def run_simulation(self, days=160):
        y0 = [self.init_susceptible, self.init_infected, self.init_recovered]
        t = np.linspace(0, days, days)
        result = odeint(self.deriv, y0, t)
        S, I, R = result.T
        return t, S, I, R


class SIRSimulationGUI:
    def __init__(self, master):
        self.master = master
        master.title("SIR Epidemic Model")
        master.geometry("950x680")

        self.model = SIRModel()
        self._setup_controls()
        self._setup_plot()
        self.update_plot()

    def _setup_controls(self):
        frm = ttk.Frame(self.master)
        frm.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

        ttk.Label(frm, text="Parameters", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Infection rate slider
        ttk.Label(frm, text="Infection Rate (beta)").pack(anchor=tk.W)
        self.beta_val = tk.DoubleVar(value=0.3)
        beta_slider = ttk.Scale(frm, from_=0.1, to=1.0, variable=self.beta_val, orient=tk.HORIZONTAL, length=180)
        beta_slider.pack(pady=5)
        self.beta_label = ttk.Label(frm, text=f"β = {self.beta_val.get():.2f}")
        self.beta_label.pack(anchor=tk.W, pady=(0, 12))

        # Recovery rate slider
        ttk.Label(frm, text="Recovery Rate (gamma)").pack(anchor=tk.W)
        self.gamma_val = tk.DoubleVar(value=0.1)
        gamma_slider = ttk.Scale(frm, from_=0.05, to=0.5, variable=self.gamma_val, orient=tk.HORIZONTAL, length=180)
        gamma_slider.pack(pady=5)
        self.gamma_label = ttk.Label(frm, text=f"γ = {self.gamma_val.get():.2f}")
        self.gamma_label.pack(anchor=tk.W, pady=(0, 12))

        # Population slider
        ttk.Label(frm, text="Population Size").pack(anchor=tk.W)
        self.pop_val = tk.IntVar(value=1000)
        pop_slider = ttk.Scale(frm, from_=100, to=10000, variable=self.pop_val, orient=tk.HORIZONTAL, length=180)
        pop_slider.pack(pady=5)
        self.pop_label = ttk.Label(frm, text=f"N = {self.pop_val.get()}")
        self.pop_label.pack(anchor=tk.W, pady=(0, 12))

        # Initial infected slider
        ttk.Label(frm, text="Initial Infected").pack(anchor=tk.W)
        self.infected_val = tk.IntVar(value=1)
        infected_slider = ttk.Scale(frm, from_=1, to=100, variable=self.infected_val, orient=tk.HORIZONTAL, length=180)
        infected_slider.pack(pady=5)
        self.infected_label = ttk.Label(frm, text=f"I₀ = {self.infected_val.get()}")
        self.infected_label.pack(anchor=tk.W, pady=(0, 12))

        # Simulation days slider
        ttk.Label(frm, text="Simulation Days").pack(anchor=tk.W)
        self.days_val = tk.IntVar(value=160)
        days_slider = ttk.Scale(frm, from_=50, to=365, variable=self.days_val, orient=tk.HORIZONTAL, length=180)
        days_slider.pack(pady=5)
        self.days_label = ttk.Label(frm, text=f"Days = {self.days_val.get()}")
        self.days_label.pack(anchor=tk.W, pady=(0, 15))

        # Buttons
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, pady=10)

        run_btn = ttk.Button(btn_frame, text="Run Simulation", command=self.update_plot)
        run_btn.pack(fill=tk.X, pady=(0, 8))

        reset_btn = ttk.Button(btn_frame, text="Reset", command=self.reset_params)
        reset_btn.pack(fill=tk.X)

        # Text box for peak stats
        stats_box = ttk.LabelFrame(frm, text="Peak Stats", padding=10)
        stats_box.pack(fill=tk.X, pady=15)
        self.stats_text = tk.Text(stats_box, width=25, height=6, wrap=tk.WORD)
        self.stats_text.pack()

        # Link sliders to update labels
        for slider, label, var, prefix in [
            (beta_slider, self.beta_label, self.beta_val, 'β'),
            (gamma_slider, self.gamma_label, self.gamma_val, 'γ'),
            (pop_slider, self.pop_label, self.pop_val, 'N'),
            (infected_slider, self.infected_label, self.infected_val, 'I₀'),
            (days_slider, self.days_label, self.days_val, 'Days')
        ]:
            slider.config(command=lambda val, lbl=label, v=var, p=prefix: self._update_label(lbl, v, p))

    def _update_label(self, label, var, prefix):
        if isinstance(var.get(), float):
            label.config(text=f"{prefix} = {var.get():.2f}")
        else:
            label.config(text=f"{prefix} = {var.get()}")

    def _setup_plot(self):
        plot_frame = ttk.Frame(self.master)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.fig = Figure(figsize=(7, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_plot(self):
        # Update model params from sliders
        self.model.beta = self.beta_val.get()
        self.model.gamma = self.gamma_val.get()
        self.model.population = self.pop_val.get()
        self.model.init_infected = self.infected_val.get()
        self.model.init_susceptible = self.model.population - self.model.init_infected

        t, S, I, R = self.model.run_simulation(self.days_val.get())

        self.ax.clear()
        self.ax.plot(t, S, 'b-', label='Susceptible')
        self.ax.plot(t, I, 'r-', label='Infected')
        self.ax.plot(t, R, 'g-', label='Recovered')

        self.ax.set_title("SIR Model Simulation")
        self.ax.set_xlabel("Days")
        self.ax.set_ylabel("Population")
        self.ax.legend()
        self.ax.grid(True, linestyle='--', alpha=0.5)

        # Calculate some statistics
        peak_idx = np.argmax(I)
        peak_inf = I[peak_idx]
        peak_day = t[peak_idx]
        final_rec = R[-1]
        attack_rate = final_rec / self.model.population * 100
        r0 = self.model.beta / self.model.gamma

        stats = (
            f"Peak Infected: {int(peak_inf)}\n"
            f"Peak Day: {int(peak_day)}\n"
            f"Final Recovered: {int(final_rec)}\n"
            f"Attack Rate: {attack_rate:.1f}%\n"
            f"Basic Reproduction Number (R₀): {r0:.2f}\n"
            f"Simulation Duration: {self.days_val.get()} days"
        )

        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats)

        self.canvas.draw()

    def reset_params(self):
        # Reset all sliders to defaults
        self.beta_val.set(0.3)
        self.gamma_val.set(0.1)
        self.pop_val.set(1000)
        self.infected_val.set(1)
        self.days_val.set(160)

        # Update labels immediately
        self._update_label(self.beta_label, self.beta_val, 'β')
        self._update_label(self.gamma_label, self.gamma_val, 'γ')
        self._update_label(self.pop_label, self.pop_val, 'N')
        self._update_label(self.infected_label, self.infected_val, 'I₀')
        self._update_label(self.days_label, self.days_val, 'Days')

        self.update_plot()


def main():
    root = tk.Tk()
    app = SIRSimulationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
