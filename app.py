import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide")
st.title("📊 Excel to Pandas Tutor")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Excel File")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Excel Preview")
        st.dataframe(df)

with col2:
    st.subheader("Excel Formula to Pandas")
    excel_formula = st.text_input("Type Excel formula (e.g., =IF(A2>100,\"High\",\"Low\"))")
    if st.button("Translate"):
        if excel_formula:
            with st.spinner("Translating to Pandas..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that translates Excel formulas to Python pandas code with comments."},
                        {"role": "user", "content": f"Translate this Excel formula to pandas: {excel_formula}"}
                    ]
                )
                st.code(response['choices'][0]['message']['content'], language='python')

st.subheader("Ask a Pandas Question")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a tutor helping accountants learn Pandas by answering questions in clear, non-technical terms."}
    ]

user_question = st.text_input("Ask your question (e.g., how to use pivot tables in pandas)")

if st.button("Ask"):
    if user_question:
        st.session_state.messages.append({"role": "user", "content": user_question})
        with st.spinner("Getting answer..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = response['choices'][0]['message']['content']
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(f"**Answer:**\n\n{reply}")

st.subheader("Run Sample Pandas Code")
sample_data = {
    "A": [120, 80, 95],
    "B": [5, 10, 15]
}
sample_df = pd.DataFrame(sample_data)
st.write("📄 Sample Data")
st.dataframe(sample_df)

user_code = st.text_area("Write your Pandas code here (e.g., df['C'] = df['A'] + df['B'])")

if st.button("Run Code"):
    try:
        df = sample_df.copy()
        exec(user_code)
        st.write("✅ Result:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Error: {e}")
