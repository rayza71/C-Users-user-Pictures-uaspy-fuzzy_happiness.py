import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ------------------------------------------
# Implementasi Sistem Fuzzy
# ------------------------------------------

# 1. Definisi Variabel Input dan Output
speed = ctrl.Antecedent(np.arange(0, 11, 1), 'speed')  # Kecepatan Pelayanan
food_quality = ctrl.Antecedent(np.arange(0, 11, 1), 'food_quality')  # Kualitas Makanan
ambience = ctrl.Antecedent(np.arange(0, 11, 1), 'ambience')  # Suasana Restoran
happiness = ctrl.Consequent(np.arange(0, 11, 1), 'happiness')  # Tingkat Kebahagiaan

# 2. Fungsi Keanggotaan
speed['slow'] = fuzz.trapmf(speed.universe, [0, 0, 3, 5])
speed['average'] = fuzz.trimf(speed.universe, [3, 5, 7])
speed['fast'] = fuzz.trapmf(speed.universe, [5, 7, 10, 10])

food_quality['poor'] = fuzz.trapmf(food_quality.universe, [0, 0, 3, 5])
food_quality['average'] = fuzz.trimf(food_quality.universe, [3, 5, 7])
food_quality['excellent'] = fuzz.trapmf(food_quality.universe, [5, 7, 10, 10])

ambience['bad'] = fuzz.trapmf(ambience.universe, [0, 0, 3, 5])
ambience['okay'] = fuzz.trimf(ambience.universe, [3, 5, 7])
ambience['good'] = fuzz.trapmf(ambience.universe, [5, 7, 10, 10])

happiness['unhappy'] = fuzz.trapmf(happiness.universe, [0, 0, 3, 5])
happiness['neutral'] = fuzz.trimf(happiness.universe, [3, 5, 7])
happiness['happy'] = fuzz.trapmf(happiness.universe, [5, 7, 10, 10])

# 3. Aturan Fuzzy
rule1 = ctrl.Rule(speed['slow'] | food_quality['poor'] | ambience['bad'], happiness['unhappy'])
rule2 = ctrl.Rule(speed['average'] & food_quality['average'] & ambience['okay'], happiness['neutral'])
rule3 = ctrl.Rule(speed['fast'] & food_quality['excellent'] & ambience['good'], happiness['happy'])

# 4. Sistem Kontrol Fuzzy
happiness_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
happiness_simulation = ctrl.ControlSystemSimulation(happiness_ctrl)

# ------------------------------------------
# Sistem Penilaian Tingkat Kebahagiaan Pelanggan
# ------------------------------------------

def get_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0 <= value <= 10:
                return value
            else:
                print("Masukkan angka antara 0-10.")
        except ValueError:
            print("Masukkan angka yang valid.")

# Input Nilai dari Pengguna
print("Masukkan Nilai Input (0-10):")
speed_value = get_input("Kecepatan Pelayanan: ")
food_quality_value = get_input("Kualitas Makanan: ")
ambience_value = get_input("Suasana Restoran: ")

# Berikan Input ke Sistem Fuzzy
happiness_simulation.input['speed'] = speed_value
happiness_simulation.input['food_quality'] = food_quality_value
happiness_simulation.input['ambience'] = ambience_value

# Hitung Hasil Fuzzy
happiness_simulation.compute()

# Tampilkan Output
output_happiness = happiness_simulation.output['happiness']
if output_happiness <= 3:
    happiness_level = "Unhappy"
elif output_happiness <= 7:
    happiness_level = "Neutral"
else:
    happiness_level = "Happy"

print(f"\nTingkat Kebahagiaan Pelanggan: {output_happiness:.2f} (0-10)")
print(f"Kategori: {happiness_level}")

# ------------------------------------------
# Visualisasi Hasil Keanggotaan
# ------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

speed.view(ax=axs[0, 0])
axs[0, 0].set_title("Fungsi Keanggotaan: Speed")

food_quality.view(ax=axs[0, 1])
axs[0, 1].set_title("Fungsi Keanggotaan: Food Quality")

ambience.view(ax=axs[1, 0])
axs[1, 0].set_title("Fungsi Keanggotaan: Ambience")

happiness.view(sim=happiness_simulation, ax=axs[1, 1])
axs[1, 1].set_title("Hasil Keanggotaan: Happiness")

plt.tight_layout()
plt.show()
