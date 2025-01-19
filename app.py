import streamlit as st


st.title('Deploy App')

st.write('My First Deploy App')


import os
key=os.environ.get('My_secret', 'Not set yet')
st.write(f'sever key : {key}')

