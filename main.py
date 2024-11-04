import streamlit as st
import pandas as pd


def load_datasets():
    df = pd.read_csv("dataset_list.csv", dtype=str).fillna("")
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'],axis=1)
    df.rename(columns={'Where':'Venue',"Published Year":"Date",'Paper Name ':'Paper'},
                  inplace=True)
    df = df.drop(df.loc[df['Availability'] == 'Unknown'].index)

    return df

def page_set():
    st.set_page_config(page_title="Dataset Search", layout="wide")
    st.title("Summarization Datasets Search Engine")
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False

    url = "https://github.com/edahanoam/Awesome-Summarization-Datasets"
    st.write("For an updated list and to suggest new datasets, please visit our [GitHub page](%s)." % url)



def set_search(df):
    df = df.reset_index(drop=True)

    combined_mask = pd.Series([True] * len(df))

    #languages
    df['Languages '] = df['Languages '].apply(lambda x: x.split(', '))
    #df['Languages '] = df['Languages '].apply(literal_eval)
    unique_languages = set(lang for lang_list in df['Languages '].dropna() for lang in lang_list)
    selected_languages = st.multiselect("Languages", options=sorted(unique_languages))

    #language modality
    unique_modalities = set(df['Language Modality'].dropna().unique())
    selected_modality = st.multiselect("Language Modality", options=sorted(unique_modalities))

    #Domain
    unique_domains = set(df['Domain '].dropna().unique())
    selected_domain= st.multiselect("Domain", options=sorted(unique_domains))


    #Shape
    unique_Length = set(df['Shape'].dropna().unique())
    selected_Length= st.multiselect("Shape", options=sorted(unique_Length))


    #Annotation Efforts
    unique_Annotation_Efforts = set(df['Annotation Efforts'].dropna().unique())
    selected_Annotation_Efforts= st.multiselect("Annotation Efforts", options=sorted(unique_Annotation_Efforts))

    ##Source of Supervision
    unique_Supervision = set(df['Supervision'].dropna().unique())
    selected_Supervision= st.multiselect("Supervision", options=sorted(unique_Supervision))

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
            mask4 = df['Shape'].isin(selected_Length)
            combined_mask &= mask4

        if selected_Supervision:
            mask6 = df['Supervision'].isin(selected_Supervision)
            combined_mask &= mask6

        if selected_Annotation_Efforts:
            mask5 = df['Annotation Efforts'].isin(selected_Annotation_Efforts)
            combined_mask &= mask5

        # Apply the combined mask to filter the DataFrame
        filtered_df = df[combined_mask]
        if not filtered_df.empty:

            # change to links
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

        else:
            st.write("No results match your criteria.")


if __name__ == '__main__':
    page_set()
    df = load_datasets()
    set_search(df)

