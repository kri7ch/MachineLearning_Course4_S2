import pandas as pd
import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"


def request_api(path: str, method: str = "GET", data: dict | None = None):
    url = f"{API_BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Ошибка API: {e}")
        return None


def page_comments():
    st.header("Комментарии из базы данных")
    with st.spinner("Загрузка комментариев..."):
        data = request_api("/comments")
        if data and "text" in data:
            df = pd.DataFrame(data)

            col_search, col_filter = st.columns([0.7, 0.3])
            
            with col_search:
                search_query = st.text_input("🔍 Поиск по тексту", placeholder="Введите слово для поиска...")
            
            with col_filter:
                filter_status = st.selectbox("📌 Фильтр по статусу", ["Все", "Нормальный", "Токсичный"])

            if search_query:
                df = df[df["text"].str.contains(search_query, case=False, na=False)]
            
            if filter_status == "Нормальный":
                df = df[df["is_toxic"] == 0]
            elif filter_status == "Токсичный":
                df = df[df["is_toxic"] == 1]

            if df.empty:
                st.info("Комментарии не найдены.")
            else:
                for index, row in df.iterrows():
                    text = row["text"]
                    label = row["is_toxic"]
                    date_str = row["created_at"] if row["created_at"] else "Неизвестно"
                    comment_id = row["id"]

                    if label == 1:
                        icon = "❌"
                        status = "Токсичный"
                    else:
                        icon = "✅"
                        status = "Нормальный"

                    with st.container(border=True):
                        col1, col2 = st.columns([0.1, 0.9])
                        with col1:
                            st.write(f"## {icon}")
                        with col2:
                            st.caption(f"ID: {comment_id} • {date_str}")
                            st.markdown(f"**Статус:** {status}")
                            st.text_area("Текст", value=text, disabled=True, height=68, key=f"txt_{comment_id}")


def page_add_comment():
    st.header("Проверка тональности комментария")
    text = st.text_area("Введите комментарий", max_chars=1000)

    if st.button("Определить тональность и сохранить"):
        if not text.strip():
            st.warning("Введите текст комментария")
            return

        with st.spinner("Отправка в API..."):
            result = request_api("/comments", method="POST", data={"text": text})

        if result:
            label = result.get("is_toxic", 0)
            if label == 1:
                st.error("Комментарий определён как токсичный")
            else:
                st.success("Комментарий определён как нормальный")


def page_info():
    st.header("О проекте")
    st.write(
        "Приложение использует обученную LSTM‑модель для определения токсичности "
        "русскоязычных комментариев. Комментарии хранятся в базе данных MySQL."
    )


def main():
    st.set_page_config(page_title="Тональность комментариев", layout="wide")
    st.title("Определение тональности комментариев")

    page = st.sidebar.radio(
        "Навигация",
        ["Комментарии из БД", "Проверка комментария", "О проекте"],
    )

    if page == "Комментарии из БД":
        page_comments()
    elif page == "Проверка комментария":
        page_add_comment()
    else:
        page_info()


if __name__ == "__main__":
    main()
