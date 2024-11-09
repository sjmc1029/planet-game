import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit 레이아웃
st.title("파장에 따른 위치 맞추기 게임")
st.write("행성의 각도를 조절하여 주어진 목표 파장을 맞추세요. 기회는 한 번뿐입니다!")

# 상수 설정
star_mass = 1.0       # 별의 질량 (태양 질량 단위)
planet_mass = 0.001   # 행성의 질량 (목성 정도의 질량)
star_distance = 0.5   # 별의 공전 반지름 (임의의 단위)
planet_distance = 1.0 # 행성의 공전 반지름 (임의의 단위)
base_wavelength = 656.3  # 기준 H-알파 파장 (nm)
c = 299792.458  # 빛의 속도 (km/s)

# 기준 파장 표시
st.write(f"**기준 파장:** {base_wavelength:.3f} nm")

# 도플러 효과 계산 설정
max_velocity = 30  # 최대 속도 (도플러 효과용, km/s)

# 게임 목표용 랜덤 파장 생성
if "target_wavelength" not in st.session_state:
    random_shift = np.random.uniform(-0.0001, 0.0001)  # 소규모 랜덤 이동
    st.session_state["target_wavelength"] = base_wavelength * (1 + random_shift)

target_wavelength = st.session_state["target_wavelength"]

# 목표 파장 및 각도 입력
st.write(f"**목표:** 행성의 각도를 조절하여 파장을 **{target_wavelength:.3f} nm**에 가깝게 맞추세요.")

# 각도가 이미 제출되었는지 확인
if "locked" not in st.session_state:
    angle = st.number_input("행성의 각도를 입력하세요 (도 단위):", min_value=0, max_value=360, step=1, format="%d")
    submit = st.button("제출")
    if submit:
        st.session_state["locked"] = True
        st.session_state["angle"] = angle
else:
    angle = st.session_state["angle"]
    st.write(f"**각도가 고정되었습니다:** {angle} 도")

# 각도를 라디안으로 변환
angle_rad = np.deg2rad(angle)

# 별과 행성의 좌표 계산
planet_x = planet_distance * np.cos(angle_rad)
planet_y = planet_distance * np.sin(angle_rad)
star_x = -star_distance * np.cos(angle_rad)
star_y = -star_distance * np.sin(angle_rad)

# 별의 시선 속도와 파장 이동 계산
radial_velocity = max_velocity * np.cos(angle_rad)
doppler_shift = radial_velocity / c  # 도플러 이동 계산
shifted_wavelength = base_wavelength * (1 - doppler_shift)

# 목표 파장과의 차이 계산
wavelength_diff = abs(shifted_wavelength - target_wavelength)

# 파장 정확도에 따른 점수
if wavelength_diff < 0.002:
    score = "훌륭합니다! 정확하게 맞추었습니다."
elif wavelength_diff < 0.005:
    score = "좋아요! 거의 정확합니다."
else:
    score = "다음 기회에 더 정확하게 맞춰보세요."

# 현재 파장 및 점수 피드백
st.write(f"**현재 파장:** {shifted_wavelength:.3f} nm")
st.write(f"**목표 파장과의 차이:** {wavelength_diff:.3f} nm")
st.write(f"**점수:** {score}")

# 레이아웃: 나란히 배치
col1, col2 = st.columns(2)

# 1. 궤도 그래프
with col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(0, 0, 'yo', markersize=5, label="공통 질량 중심")
    ax1.plot(planet_x, planet_y, 'bo', markersize=8, label="행성")
    ax1.plot(star_x, star_y, 'ro', markersize=12, label="별")
    ax1.arrow(0, -1.2, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', label="시선 방향")
    ax1.text(0, 1.25, '시선 방향', color='gray', ha='center')
    
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal', 'box')
    ax1.legend()
    ax1.set_title("행성과 별의 궤도")
    st.pyplot(fig1)

# 2. 도플러 효과 파장 그래프
with col2:
    fig2, ax2 = plt.subplots()
    wavelengths = np.linspace(656.23, 656.366, 1000)
    target_spectrum = np.exp(-((wavelengths - target_wavelength) ** 2) / 0.00002)
    current_spectrum = np.exp(-((wavelengths - shifted_wavelength) ** 2) / 0.00002)
    
    ax2.plot(wavelengths, target_spectrum, 'b', alpha=0.3, label=f"목표 λ: {target_wavelength:.3f} nm")
    ax2.plot(wavelengths, current_spectrum, 'r', alpha=0.7, label=f"현재 λ: {shifted_wavelength:.3f} nm")
    
    ax2.axvline(target_wavelength, color='blue', linestyle='--', label="목표 λ")
    ax2.axvline(shifted_wavelength, color='red', linestyle='--', label="현재 λ")
    
    ax2.set_title("도플러 효과에 따른 파장 이동")
    ax2.set_xlabel("파장 (nm)")
    ax2.set_ylabel("강도")
    ax2.set_xlim(656.23, 656.366)
    ax2.legend()
    st.pyplot(fig2)
