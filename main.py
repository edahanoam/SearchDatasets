import streamlit as st
import pandas as pd
from ast import literal_eval

def display_with_links(df, url_column):
    # Display the dataframe without the URL column
    st.dataframe(df.drop(columns=[url_column]))

    # Create clickable links and display them separately
    if not df.empty:
        st.write("Clickable Links:")
        for idx, row in df.iterrows():
            url = row[url_column]
            st.markdown(f"[{url}]({url})", unsafe_allow_html=True)




def page_set():
    st.set_page_config(page_title="Dataset Search", layout="wide")
    #st.set_page_config(page_title="Dataset Search", page_icon="🐍", layout="wide")
    st.title("Summarization Datasets Search Engine")


def connect_to_doc(local=False):
    if not local:
        # Connect to the Google Sheet
        url = "https://docs.google.com/spreadsheets/d/1uJqKosaAD0paPTJHT7-g0Ssw_P-X1Mp7aOchFFKGN4M/edit?usp=sharing"
        df = pd.read_csv(url, dtype=str).fillna("")
        st.write(df)
    else:
        df = pd.read_csv("after_unifying.csv", dtype=str).fillna("")
        #st.write(df)
        return df


def clean_domain(df):
    # Remove columns that start with "Unn"
    df = df.loc[:, ~df.columns.str.startswith('Unn')]
    # List of columns to remove
    to_remove = ['paper name ','fine_domain ', 'how was it collected ', 'collection category', 'Where', 'packages', 'comments']

    # Remove the columns in the list
    df.drop(columns=to_remove, inplace=True)

    # Rename 'city' to 'City Name'
    df.rename(columns={'how many samples':'#Samples','where': 'Venue','Languages choice ': 'Language Modality','Types':'Length','workload':'Annotation Efforts','Formation':'Sources for Supervision' }, inplace=True)

    # Capitalize
    df.columns = [col.title() for col in df.columns]
    df['Language Modality'] = df['Language Modality'].str.title()


    return df



def set_search(df):
    text_search = st.text_input("Search datasets by languages", value="")
    # Filter the dataframe using masks
    m1 = df["languages "].apply(lambda x: text_search in x)
    filtered_df = df[m1]

    if text_search:
        st.write(filtered_df)


def set_search2(df):

    combined_mask = pd.Series([True] * len(df))

    #languages
    df['Languages '] = df['Languages '].apply(literal_eval)
    unique_languages = set(lang for lang_list in df['Languages '].dropna() for lang in lang_list)
    selected_languages = st.multiselect("Languages", options=sorted(unique_languages))

    #language modality
    unique_modalities = set(df['Language Modality'].dropna().unique())
    selected_modality = st.multiselect("Language Modality", options=sorted(unique_modalities))

    #Domain
    unique_domains = set(df['Domain '].dropna().unique())
    selected_domain= st.multiselect("Domain", options=sorted(unique_domains))


    #Length
    unique_Length = set(df['Length'].dropna().unique())
    selected_Length= st.multiselect("Length", options=sorted(unique_Length))


    #Annotation Efforts
    unique_Annotation_Efforts = set(df['Annotation Efforts'].dropna().unique())
    selected_Annotation_Efforts= st.multiselect("Annotation Efforts", options=sorted(unique_Annotation_Efforts))

    ##Source of Supervision
    unique_Supervision = set(df['Sources For Supervision'].dropna().unique())
    selected_Supervision= st.multiselect("Sources For Supervision", options=sorted(unique_Supervision))

    #
    if selected_languages or selected_modality or selected_domain or selected_Length or selected_Length or selected_Annotation_Efforts or selected_Supervision:

        if selected_languages:
            # This mask checks if the list of selected languages are subset of 'languages' array in each row
            mask1 = df['Languages '].apply(lambda x: set(selected_languages).issubset(x))
            combined_mask &= mask1  # Combine with the main mask using logical AND

        if selected_modality:
            mask2 = df['Language Modality'].isin(selected_modality)
            combined_mask &= mask2

        if selected_domain:
            mask3 = df['Domain '].isin(selected_domain)
            combined_mask &= mask3

        if selected_Length:
            mask4 = df['Length'].isin(selected_Length)
            combined_mask &= mask4

        if selected_Annotation_Efforts:
            mask5 = df['Annotation Efforts'].isin(selected_Annotation_Efforts)
            combined_mask &= mask5

        if selected_Supervision:
            mask6 = df['Sources For Supervision'].isin(selected_Supervision)
            combined_mask &= mask6




        # Apply the combined mask to filter the DataFrame
        filtered_df = df[combined_mask]
        if not filtered_df.empty:
            #st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)

            #change to links
            st.data_editor(
                filtered_df,
                column_config={
                    "Paper Link": st.column_config.LinkColumn(
                        "Paper Link",
                        validate=r"^https://[a-z]+\.streamlit\.app$",
                        max_chars=100,
                        display_text=r"https://(.*?)\.streamlit\.app"
                    )
                },
                hide_index=True,
            )

            #st.write(filtered_df)
        else:
            st.write("No results match your criteria.")


if __name__ == '__main__':
    page_set()
    df= connect_to_doc(True)
    df = clean_domain(df)
    set_search2(df)



