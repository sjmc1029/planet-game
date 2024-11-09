import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Streamlit 레이아웃
st.title("파장에 따른 위치 맞추기 객관식 퀴즈")
st.write("제시된 파장에 맞는 행성과 별의 위치를 선택하세요. 퀴즈는 한 번만 가능합니다!")

# 상수 설정
star_distance = 0.5   # 별의 공전 반지름 (임의의 단위)
planet_distance = 1.0 # 행성의 공전 반지름 (임의의 단위)
base_wavelength = 656.3  # 기준 H-알파 파장 (nm)
c = 299792.458  # 빛의 속도 (km/s)
max_velocity = 30  # 최대 속도 (도플러 효과용, km/s)

# 퀴즈 진행 상태 초기화
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.questions = []

# 퀴즈 완료 여부 확인
if not st.session_state.quiz_completed:
    
    # 랜덤 문제 생성 함수
    def generate_question():
        angle_options = np.random.choice(range(0, 360, 45), 4, replace=False)
        correct_angle = np.random.choice(angle_options)
        
        # 목표 파장 계산
        correct_angle_rad = np.deg2rad(correct_angle)
        radial_velocity = max_velocity * np.cos(correct_angle_rad)
        doppler_shift = radial_velocity / c
        target_wavelength = base_wavelength * (1 - doppler_shift)
        
        # 문제와 정답, 선택지 반환
        return {
            "target_wavelength": target_wavelength,
            "correct_angle": correct_angle,
            "angle_options": angle_options
        }

    # 문제 로딩
    if st.session_state.current_question < 5:
        if len(st.session_state.questions) <= st.session_state.current_question:
            st.session_state.questions.append(generate_question())
        
        question = st.session_state.questions[st.session_state.current_question]
        
        # 문제 제시
        st.write(f"**문제 {st.session_state.current_question + 1}**: 다음 파장에 맞는 행성과 별의 위치를 선택하세요.")
        st.write(f"기준 파장: {base_wavelength:.3f} nm")
        st.write(f"목표 파장: {question['target_wavelength']:.3f} nm")

        # 스펙트럼 그래프를 왼쪽에 표시
        left_col, right_col = st.columns([1, 3])

        with left_col:
            fig, ax = plt.subplots(figsize=(3, 2))  # 크기 조정
            wavelengths = np.linspace(656.23, 656.366, 1000)
            target_spectrum = np.exp(-((wavelengths - question['target_wavelength']) ** 2) / 0.00002)
            baseline_spectrum = np.exp(-((wavelengths - base_wavelength) ** 2) / 0.00002)
            
            ax.plot(wavelengths, baseline_spectrum, 'k', alpha=0.3, label="Baseline λ")
            ax.plot(wavelengths, target_spectrum, 'r', alpha=0.7, label=f"Target λ: {question['target_wavelength']:.3f} nm")
            ax.axvline(base_wavelength, color='gray', linestyle='--', label="Baseline λ")
            ax.axvline(question['target_wavelength'], color='red', linestyle='--', label="Target λ")
            ax.set_title("Wavelength Shift")
            ax.set_xlabel("Wavelength (nm)")
            ax.set_ylabel("Intensity")
            ax.set_xlim(656.23, 656.366)
            ax.legend()
            st.pyplot(fig)

        # 오른쪽에 각도별 위치 그림을 선택지로 표시
        answer = None
        with right_col:
            st.write("행성과 별의 위치를 선택하세요:")
            options = []
            for i, angle in enumerate(question["angle_options"]):
                # 행성 및 별의 위치 계산
                angle_rad = np.deg2rad(angle)
                planet_x = planet_distance * np.cos(angle_rad)
                planet_y = planet_distance * np.sin(angle_rad)
                star_x = -star_distance * np.cos(angle_rad)
                star_y = -star_distance * np.sin(angle_rad)
                
                # 그래프 생성
                fig, ax = plt.subplots(figsize=(2, 2))  # 크기 조정
                ax.plot(0, 0, 'yo', markersize=5, label="Center of Mass")
                ax.plot(planet_x, planet_y, 'bo', markersize=8, label="Planet")
                ax.plot(star_x, star_y, 'ro', markersize=12, label="Star")
                ax.arrow(0, -1.2, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', label="Line of Sight")
                ax.set_xlim(-1.5, 1.5)
                ax.set_ylim(-1.5, 1.5)
                ax.set_aspect('equal', 'box')
                ax.set_title(f"{angle}°")
                options.append(fig)

            # 그림으로 객관식 보기 제공
            col1, col2 = st.columns(2)
            with col1:
                if st.button("선택: " + str(question["angle_options"][0]), key=f"btn_{question['angle_options'][0]}"):
                    answer = question["angle_options"][0]
                st.pyplot(options[0])

                if st.button("선택: " + str(question["angle_options"][1]), key=f"btn_{question['angle_options'][1]}"):
                    answer = question["angle_options"][1]
                st.pyplot(options[1])

            with col2:
                if st.button("선택: " + str(question["angle_options"][2]), key=f"btn_{question['angle_options'][2]}"):
                    answer = question["angle_options"][2]
                st.pyplot(options[2])

                if st.button("선택: " + str(question["angle_options"][3]), key=f"btn_{question['angle_options'][3]}"):
                    answer = question["angle_options"][3]
                st.pyplot(options[3])

        # 정답 확인
        if answer is not None:
            if answer == question["correct_angle"]:
                st.session_state.score += 20  # 정답 시 20점 추가
                st.write("정답입니다!")
            else:
                st.write("틀렸습니다.")
            st.session_state.current_question += 1

    # 모든 문제 완료 시 점수 표시 및 퀴즈 완료 표시
    else:
        st.session_state.quiz_completed = True
        st.write("퀴즈 완료!")
        st.write(f"최종 점수: {st.session_state.score} / 100점")
        st.write("퀴즈는 한 번만 가능합니다. 새로 고침해도 다시 풀 수 없습니다.")
        
else:
    # 퀴즈 완료 후 다시 시작할 수 없도록 메시지 표시
    st.write("퀴즈는 이미 완료되었습니다. 새로 고침해도 다시 풀 수 없습니다.")

