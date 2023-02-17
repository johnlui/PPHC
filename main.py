import streamlit as st
import os
import re

regex = re.compile('\!\[\]\((\S+)\)')
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 400


@st.cache_resource
def load_base_dirs():
    dirs = sort(os.listdir('.'))
    tmp_dir = []
    for path_name in dirs:
        if path_name.startswith('0'):
            tmp_dir.append(path_name)
    return tmp_dir


base_dirs = load_base_dirs()

select_name = st.sidebar.selectbox('Pages', options=base_dirs, index=0)
if select_name:
    with open('%s/%s' % (select_name, 'README.md'), 'r', encoding='utf-8') as fp:
        content = fp.read()
        args = regex.findall(content)
        for i in args:
            content = content.replace("![](%s)" % i, '<img src="%s" width = "%d" height = "%d" />' % (i, IMAGE_WIDTH, IMAGE_HEIGHT))
        content += """\n<img src="https://lvwenhan.com/content/uploadfile/202301/79c41673579170.jpg" width="800" height="400"/>"""
        st.markdown(content, unsafe_allow_html=True)
else:
    st.markdown("no things here")


st.sidebar.markdown("""
### 作者信息：

1. 姓名：吕文翰
2. GitHub：[johnlui](https://github.com/johnlui)
3. 职位：住范儿 CTO

streamlit app by [sherry0429](https://github.com/sherry0429)
""", unsafe_allow_html=True)
