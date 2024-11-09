import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit layout
st.title("Match the Position Based on Wavelength")
st.write("Adjust the planet's angle to match the given wavelength by aligning the star and planet correctly.")

# Constants
star_mass = 1.0       # Mass of the star (in solar mass units)
planet_mass = 0.001   # Mass of the planet (similar to Jupiter)
star_distance = 0.5   # Distance of star from the center (in arbitrary units)
planet_distance = 1.0 # Distance of planet from the center (in arbitrary units)
base_wavelength = 656.3  # Base H-alpha line in nm
c = 299792.458  # Speed of light in km/s

# Set up Doppler shift calculation
max_velocity = 30  # Max velocity for Doppler effect in km/s

# Random target wavelength for the game goal
np.random.seed(42)  # Seed for reproducibility
target_shift = np.random.choice([0.05, -0.05])  # Randomly choose a redshift or blueshift
target_wavelength = base_wavelength * (1 + target_shift)

# Instructions and initial setup
st.write(f"**Goal:** Adjust the planet's angle to make the wavelength close to **{target_wavelength:.3f} nm**")

# Slider for student to adjust planet's angle
angle = st.slider("Planet angle (degrees)", 0, 360, 90)
angle_rad = np.deg2rad(angle)  # Convert angle to radians

# Calculate the coordinates of the star and planet around the center of mass
planet_x = planet_distance * np.cos(angle_rad)
planet_y = planet_distance * np.sin(angle_rad)
star_x = -star_distance * np.cos(angle_rad)
star_y = -star_distance * np.sin(angle_rad)

# Calculate the star's radial velocity and shifted wavelength
radial_velocity = max_velocity * np.cos(angle_rad)
doppler_shift = radial_velocity / c  # Doppler shift calculation
shifted_wavelength = base_wavelength * (1 - doppler_shift)

# Calculate the difference from target wavelength
wavelength_diff = abs(shifted_wavelength - target_wavelength)

# Scoring mechanism based on wavelength accuracy
if wavelength_diff < 0.002:
    score = "Excellent! You've matched the position perfectly."
elif wavelength_diff < 0.005:
    score = "Good! You're close to the correct position."
else:
    score = "Keep trying to get closer!"

# Display current wavelength and score feedback
st.write(f"**Current Wavelength:** {shifted_wavelength:.3f} nm")
st.write(f"**Difference from Target Wavelength:** {wavelength_diff:.3f} nm")
st.write(f"**Score:** {score}")

# Layout: two columns for side-by-side display
col1, col2 = st.columns(2)

# 1. Display the orbital motion plot with line-of-sight arrow
with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(0, 0, 'yo', markersize=5, label="Center of Mass")
    ax1.plot(planet_x, planet_y, 'bo', markersize=8, label="Planet")
    ax1.plot(star_x, star_y, 'ro', markersize=12, label="Star")
    ax1.arrow(0, -1.2, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', label="Line of Sight")
    ax1.text(0, 1.25, 'Line of Sight', color='gray', ha='center')
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal', 'box')
    ax1.legend()
    ax1.set_title("Orbital Motion with Your Angle")
    st.pyplot(fig1)

# 2. Display the wavelength shift (Doppler effect) graph with target wavelength
with col2:
    fig2, ax2 = plt.subplots()
    wavelengths = np.linspace(656.20, 656.40, 1000)
    target_spectrum = np.exp(-((wavelengths - target_wavelength) ** 2) / 0.00002)  # Gaussian curve for target line
    current_spectrum = np.exp(-((wavelengths - shifted_wavelength) ** 2) / 0.00002)  # Gaussian curve for current line
    
    ax2.plot(wavelengths, target_spectrum, 'b', alpha=0.3, label=f"Target λ: {target_wavelength:.3f} nm")
    ax2.plot(wavelengths, current_spectrum, 'r', alpha=0.7, label=f"Current λ: {shifted_wavelength:.3f} nm")
    
    ax2.axvline(target_wavelength, color='blue', linestyle='--', label="Target λ")
    ax2.axvline(shifted_wavelength, color='red', linestyle='--', label="Current λ")
    
    ax2.set_title("Wavelength Shift (Doppler Effect)")
    ax2.set_xlabel("Wavelength (nm)")
    ax2.set_ylabel("Intensity")
    ax2.set_xlim(656.20, 656.40)
    ax2.legend()
    st.pyplot(fig2)
