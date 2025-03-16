import streamlit as st
import pandas as pd
import datetime
import os

# Заголовок приложения
st.title("Дневник силовых тренировок")

# Пути к файлам с данными
WORKOUTS_FILE = "тренировок.csv"
EXERCISE_SETS_FILE = "наборы_упражнений.csv"

# Загрузка данных о тренировках из файла
def load_workouts():
    if os.path.exists(WORKOUTS_FILE):
        return pd.read_csv(WORKOUTS_FILE)
    else:
        return pd.DataFrame(columns=["Номер тренировки", "Дата", "Набор упражнений"])

# Сохранение данных о тренировках в файл
def save_workouts(data):
    data.to_csv(WORKOUTS_FILE, index=False)

# Загрузка наборов упражнений из файла
def load_exercise_sets():
    if os.path.exists(EXERCISE_SETS_FILE):
        return pd.read_csv(EXERCISE_SETS_FILE)
    else:
        # Создаем начальные наборы упражнений, если файла нет
        initial_sets = {
            "Набор 1": [
                {"Упражнение": "Жим штанги лежа", "Повторения": 10, "Вес (кг)": 50, "Подходы": 3},
                {"Упражнение": "Приседания со штангой", "Повторения": 12, "Вес (кг)": 70, "Подходы": 4},
                {"Упражнение": "Тяга штанги в наклоне", "Повторения": 10, "Вес (кг)": 40, "Подходы": 3},
                {"Упражнение": "Жим гантелей сидя", "Повторения": 12, "Вес (кг)": 20, "Подходы": 3},
                {"Упражнение": "Подтягивания", "Повторения": 8, "Вес (кг)": 0, "Подходы": 3},
                {"Упражнение": "Отжимания на брусьях", "Повторения": 10, "Вес (кг)": 0, "Подходы": 3},
                {"Упражнение": "Сгибания рук со штангой", "Повторения": 12, "Вес (кг)": 30, "Подходы": 3},
                {"Упражнение": "Разгибания рук на блоке", "Повторения": 15, "Вес (кг)": 20, "Подходы": 3},
            ],
            "Набор 2": [
                {"Упражнение": "Становая тяга", "Повторения": 8, "Вес (кг)": 80, "Подходы": 4},
                {"Упражнение": "Жим ногами", "Повторения": 12, "Вес (кг)": 100, "Подходы": 4},
                {"Упражнение": "Подъем штанги на бицепс", "Повторения": 10, "Вес (кг)": 30, "Подходы": 3},
                {"Упражнение": "Французский жим", "Повторения": 12, "Вес (кг)": 25, "Подходы": 3},
                {"Упражнение": "Подъем гантелей в стороны", "Повторения": 15, "Вес (кг)": 10, "Подходы": 3},
                {"Упражнение": "Скручивания на пресс", "Повторения": 20, "Вес (кг)": 0, "Подходы": 3},
                {"Упражнение": "Гиперэкстензия", "Повторения": 15, "Вес (кг)": 0, "Подходы": 3},
                {"Упражнение": "Подъем на носки", "Повторения": 20, "Вес (кг)": 50, "Подходы": 3},
            ],
            "Набор 3": [
                {"Упражнение": "Жим штанги стоя", "Повторения": 10, "Вес (кг)": 40, "Подходы": 3},
                {"Упражнение": "Тяга штанги к подбородку", "Повторения": 12, "Вес (кг)": 30, "Подходы": 3},
                {"Упражнение": "Махи гантелями в наклоне", "Повторения": 15, "Вес (кг)": 10, "Подходы": 3},
                {"Упражнение": "Жим Арнольда", "Повторения": 12, "Вес (кг)": 15, "Подходы": 3},
                {"Упражнение": "Разводка гантелей лежа", "Повторения": 12, "Вес (кг)": 20, "Подходы": 3},
                {"Упражнение": "Скручивания с весом", "Повторения": 20, "Вес (кг)": 10, "Подходы": 3},
                {"Упражнение": "Боковые наклоны с гантелей", "Повторения": 15, "Вес (кг)": 15, "Подходы": 3},
                {"Упражнение": "Планка", "Повторения": 1, "Вес (кг)": 0, "Подходы": 3},
            ],
        }
        # Преобразуем в DataFrame
        data = []
        for set_name, exercises in initial_sets.items():
            for exercise in exercises:
                data.append([set_name, exercise["Упражнение"], exercise["Повторения"], exercise["Вес (кг)"], exercise["Подходы"]])
        exercise_sets = pd.DataFrame(data, columns=["Набор", "Упражнение", "Повторения", "Вес (кг)", "Подходы"])
        exercise_sets.to_csv(EXERCISE_SETS_FILE, index=False)
        return exercise_sets

# Сохранение наборов упражнений в файл
def save_exercise_sets(data):
    data.to_csv(EXERCISE_SETS_FILE, index=False)

# Загрузка данных
if "workouts" not in st.session_state:
    st.session_state.workouts = load_workouts()

if "exercise_sets" not in st.session_state:
    st.session_state.exercise_sets = load_exercise_sets()

# Преобразуем наборы упражнений в удобный формат
workout_sets = {}
for set_name, group in st.session_state.exercise_sets.groupby("Набор"):
    workout_sets[set_name] = group[["Упражнение", "Повторения", "Вес (кг)", "Подходы"]].to_dict("records")

# Номер тренировки (увеличивается с каждой новой тренировкой)
if "workout_counter" not in st.session_state:
    st.session_state.workout_counter = st.session_state.workouts["Номер тренировки"].max() + 1 if not st.session_state.workouts.empty else 1

# Форма для добавления новой тренировки
with st.form("workout_form"):
    st.write("Добавить новую тренировку")
    workout_date = st.date_input("Дата тренировки", datetime.date.today())
    workout_set = st.selectbox("Выберите набор упражнений", list(workout_sets.keys()))

    # Кнопка "Загрузить" для загрузки таблицы упражнений
    if st.form_submit_button("Загрузить"):
        st.session_state.selected_workout_set = workout_set  # Сохраняем выбранный набор

    # Если выбран набор, отображаем таблицу упражнений
    if "selected_workout_set" in st.session_state:
        exercises = workout_sets[st.session_state.selected_workout_set]
        exercises_df = pd.DataFrame(exercises)
        edited_exercises_df = st.data_editor(exercises_df, key=f"editor_{st.session_state.selected_workout_set}")

        # Кнопка "Сохранить изменения" для сохранения изменений в наборе упражнений
        if st.form_submit_button("Сохранить изменения"):
            # Обновляем набор упражнений
            updated_exercises = edited_exercises_df.to_dict("records")
            workout_sets[st.session_state.selected_workout_set] = updated_exercises
            # Обновляем данные в st.session_state.exercise_sets
            updated_data = pd.DataFrame(
                [(st.session_state.selected_workout_set, exercise["Упражнение"], exercise["Повторения"], exercise["Вес (кг)"], exercise["Подходы"])
                 for exercise in updated_exercises],
                columns=["Набор", "Упражнение", "Повторения", "Вес (кг)", "Подходы"],
            )
            st.session_state.exercise_sets = pd.concat(
                [st.session_state.exercise_sets[st.session_state.exercise_sets["Набор"] != st.session_state.selected_workout_set], updated_data]
            )
            save_exercise_sets(st.session_state.exercise_sets)  # Сохраняем изменения в файл
            st.success("Изменения в наборе упражнений сохранены!")

    submitted = st.form_submit_button("Завершить тренировку")

    if submitted and "selected_workout_set" in st.session_state:
        # Сохраняем тренировку
        new_workout = pd.DataFrame(
            [[st.session_state.workout_counter, workout_date, st.session_state.selected_workout_set]],
            columns=["Номер тренировки", "Дата", "Набор упражнений"],
        )
        st.session_state.workouts = pd.concat([st.session_state.workouts, new_workout], ignore_index=True)
        st.session_state.workout_counter += 1  # Увеличиваем счетчик тренировок
        save_workouts(st.session_state.workouts)  # Сохраняем данные в файл
        st.success("Тренировка сохранена!")
        del st.session_state.selected_workout_set  # Очищаем выбранный набор после сохранения

# Отображение всех тренировок в виде таблицы
st.write("Сохраненные тренировки:")
if not st.session_state.workouts.empty:
    st.dataframe(st.session_state.workouts)
else:
    st.write("Пока нет сохраненных тренировок.")