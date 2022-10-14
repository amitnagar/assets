import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import requests
import pandas as pd

def search():
    st.title("CFPB search")

    with st.form("searchform", clear_on_submit=False):
        text_input = st.text_input("Enter search terms")

        #submit form
        submitted = st.form_submit_button("Submit")

        if submitted:
            executeQuery(text_input)

def executeQuery(query):
    SOLR_HOST = "localhost"
    SOLR_PORT = "8983"
    solr_url = f'http://{SOLR_HOST}:{SOLR_PORT}/solr/'
    solr_collections_api = f'{solr_url}admin/collections'
    collection = "complaints"

    request = {
        "query": query,
        "fields": ["Date_received", "Product", "Company", "Consumer_complaint_narrative"],
        # , "score", "[explain style=html]"],
        "params": {
            "qf": ["Consumer_complaint_narrative"],  # specifies which fields in the document to search on
            #     "qf": ["Product","Consumer_complaint_narrative"],              # specifies which fields in the document to search on
            "defType": "edismax",  # edismax is a query parser
            "indent": "true",
            "rows": 100
        }
    }
    from IPython.core.display import display, HTML
    display(HTML(f"<br/><strong>Query: </strong><i>{query}</i><br/><br/><strong>Ranked Docs:</strong>"))
    aresponse = requests.post(f"{solr_url}{collection}/select?", json=request)
    #response = str(requests.post(f"{solr_url}{collection}/select?", json=request) \
    #response = str(aresponse \
    #               .json()["response"]["docs"]).replace('\\n', '').replace(", '", ",<br/>'")

    numFound = aresponse.json().get('response').get('numFound')
    qtime = aresponse.json().get('responseHeader').get('QTime')

    df = pd.DataFrame(requests.post(f"{solr_url}{collection}/select?", json=request).json().get('response').get('docs'))

    # st.dataframe(AgGrid(df))
    st.markdown("""<hr style="height:0.1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    st.text(f"Found {numFound} complaints in {qtime} ms")
    st.markdown("""<hr style="height:0.1px;border:none;color:#333;background-color:#333;" /> """,
                unsafe_allow_html=True)
    for i in range(df.shape[0]):
        st.markdown(str(df.iloc[i]['Consumer_complaint_narrative'][0]))
        st.write(str('Date: ' + df.iloc[i]['Date_received'][0][0:10]), ' | ', str('Company: ' + df.iloc[i]['Company'][0]))
        st.markdown("""<hr style="height:0.5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)