import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit layout
st.title("Match the Position Based on Wavelength")
st.write("Adjust the planet's angle to match the given wavelength by aligning the star and planet correctly. You have only one chance!")

# Constants
star_mass = 1.0       # Mass of the star (in solar mass units)
planet_mass = 0.001   # Mass of the planet (similar to Jupiter)
star_distance = 0.5   # Distance of star from the center (in arbitrary units)
planet_distance = 1.0 # Distance of planet from the center (in arbitrary units)
base_wavelength = 656.3  # Base H-alpha line in nm
c = 299792.458  # Speed of light in km/s

# Display base wavelength
st.write(f"**Base Wavelength:** {base_wavelength:.3f} nm")

# Set up Doppler shift calculation
max_velocity = 30  # Max velocity for Doppler effect in km/s

# Generate a random target wavelength for the game goal if not already set
if "target_wavelength" not in st.session_state:
    random_shift = np.random.uniform(-0.0001, 0.0001)  # Small random shift for realistic values
    st.session_state["target_wavelength"] = base_wavelength * (1 + random_shift)

target_wavelength = st.session_state["target_wavelength"]

# Display goal information and input for the planet's angle
st.write(f"**Goal:** Adjust the planet's angle to make the wavelength close to **{target_wavelength:.3f} nm**")

# Check if angle is already submitted to prevent further edits
if "locked" not in st.session_state:
    angle = st.number_input("Enter the planet's angle (degrees):", min_value=0, max_value=360, step=1, format="%d")
    submit = st.button("Submit")
    if submit:
        st.session_state["locked"] = True
        st.session_state["angle"] = angle
else:
    angle = st.session_state["angle"]
    st.write(f"**Angle is locked at:** {angle} degrees")

# Calculate the angle in radians
angle_rad = np.deg2rad(angle)

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
    score = "Keep trying to get closer next time!"

# Display current wavelength and score feedback
st.write(f"**Your Guessed Wavelength:** {shifted_wavelength:.3f} nm")
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
    wavelengths = np.linspace(656.23, 656.366, 1000)  # Narrowed range for greater contrast
    target_spectrum = np.exp(-((wavelengths - target_wavelength) ** 2) / 0.00002)  # Gaussian curve for target line
    current_spectrum = np.exp(-((wavelengths - shifted_wavelength) ** 2) / 0.00002)  # Gaussian curve for current line
    
    ax2.plot(wavelengths, target_spectrum, 'b', alpha=0.3, label=f"Target λ: {target_wavelength:.3f} nm")
    ax2.plot(wavelengths, current_spectrum, 'r', alpha=0.7, label=f"Your Guessed λ: {shifted_wavelength:.3f} nm")
    
    ax2.axvline(target_wavelength, color='blue', linestyle='--', label="Target λ")
    ax2.axvline(shifted_wavelength, color='red', linestyle='--', label="Guessed λ")
    
    ax2.set_title("Wavelength Shift (Doppler Effect)")
    ax2.set_xlabel("Wavelength (nm)")
    ax2.set_ylabel("Intensity")
    ax2.set_xlim(656.23, 656.366)  # Updated x-axis range
    ax2.legend()
    st.pyplot(fig2)
