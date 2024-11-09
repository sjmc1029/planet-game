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

# 고정된 문제 파장 및 정답 각도
fixed_questions = [
    {"wavelength": 656.234, "correct_angles": [0]},
    {"wavelength": 656.300, "correct_angles": [90, 270]},
    {"wavelength": 656.366, "correct_angles": [180]},
    {"wavelength": 656.254, "correct_angles": [45, 315]}
]

# 퀴즈 진행 상태 초기화
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answered = False  # 각 문제 정답 제출 여부

# 퀴즈 완료 여부 확인
if not st.session_state.quiz_completed:

    # 현재 문제 로딩
    if st.session_state.current_question < len(fixed_questions):
        question = fixed_questions[st.session_state.current_question]
        
        # 문제 제시
        st.markdown(f"**<span style='color:yellow'>문제 {st.session_state.current_question + 1}</span>**: 다음 파장에 맞는 행성과 별의 위치를 선택하세요.", unsafe_allow_html=True)
        st.write(f"기준 파장: {base_wavelength:.3f} nm")
        st.write(f"목표 파장: {question['wavelength']:.3f} nm")

        # 스펙트럼 그래프를 왼쪽에 표시
        left_col, right_col = st.columns([2, 1])  # 왼쪽(파장 그래프)을 4배 크게 설정

        with left_col:
            fig, ax = plt.subplots(figsize=(6, 4))  # 파장 그래프 크기를 더 크게 설정
            wavelengths = np.linspace(656.23, 656.366, 1000)
            target_spectrum = np.exp(-((wavelengths - question['wavelength']) ** 2) / 0.00002)
            baseline_spectrum = np.exp(-((wavelengths - base_wavelength) ** 2) / 0.00002)
            
            ax.plot(wavelengths, baseline_spectrum, 'k', alpha=0.3, label="Baseline λ")
            ax.plot(wavelengths, target_spectrum, 'r', alpha=0.7, label=f"Target λ: {question['wavelength']:.3f} nm")
            ax.axvline(base_wavelength, color='gray', linestyle='--', label="Baseline λ")
            ax.axvline(question['wavelength'], color='red', linestyle='--', label="Target λ")
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
            angle_options = [0, 45, 90, 180, 225, 270, 315]
            for i, angle in enumerate(angle_options[:4]):  # 상위 4개 각도만 사용
                # 행성 및 별의 위치 계산
                angle_rad = np.deg2rad(angle)
                planet_x = planet_distance * np.cos(angle_rad)
                planet_y = planet_distance * np.sin(angle_rad)
                star_x = -star_distance * np.cos(angle_rad)
                star_y = -star_distance * np.sin(angle_rad)
                
                # 그래프 생성
                fig, ax = plt.subplots(figsize=(1.5, 1.5))  # 선택지 그림을 작게 설정
                ax.plot(0, 0, 'yo', markersize=5, label="Center of Mass")
                ax.plot(planet_x, planet_y, 'bo', markersize=8, label="Planet")
                ax.plot(star_x, star_y, 'ro', markersize=12, label="Star")
                ax.arrow(0, -1.2, 0, 1.2, head_width=0.1, head_length=0.1, fc='gray', ec='gray', label="Line of Sight")
                ax.set_xlim(-1.5, 1.5)
                ax.set_ylim(-1.5, 1.5)
                ax.set_aspect('equal', 'box')
                options.append(fig)

            # 그림으로 객관식 보기 제공 (각도는 표시하지 않음)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("선택", key=f"btn_{angle_options[0]}"):
                    answer = angle_options[0]
                st.pyplot(options[0])

                if st.button("선택", key=f"btn_{angle_options[1]}"):
                    answer = angle_options[1]
                st.pyplot(options[1])

            with col2:
                if st.button("선택", key=f"btn_{angle_options[2]}"):
                    answer = angle_options[2]
                st.pyplot(options[2])

                if st.button("선택", key=f"btn_{angle_options[3]}"):
                    answer = angle_options[3]
                st.pyplot(options[3])

        # 정답 확인 및 다음 문제 버튼 활성화
        if answer is not None and not st.session_state.answered:
            # 복수 정답 처리
            if answer in question["correct_angles"]:
                st.session_state.score += 25  # 정답 시 25점 추가
                st.write("정답입니다!")
            else:
                st.write("틀렸습니다.")
            st.session_state.answered = True  # 정답 제출 완료 상태로 변경

        # 다음 문제 버튼 (정답 제출 후 활성화)
        if st.session_state.answered and st.button("다음 문제"):
            st.session_state.current_question += 1
            st.session_state.answered = False

    # 모든 문제 완료 시 점수 표시 및 퀴즈 완료 표시
    else:
        st.session_state.quiz_completed = True
        st.write("퀴즈 완료!")
        st.write(f"최종 점수: {st.session_state.score} / 100점")
        st.write("퀴즈는 한 번만 가능합니다. 새로 고침해도 다시 풀 수 없습니다.")
        
else:
    # 퀴즈 완료 후 다시 시작할 수 없도록 메시지 표시
    st.write("퀴즈는 이미 완료되었습니다. 새로 고침해도 다시 풀 수 없습니다.")

