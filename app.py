#loading librabries
import pandas as pd
import streamlit as st 
import numpy as np
import re
from PIL import Image
from io import BytesIO


#####################################################



def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path=r"C:\Users\athanneru\OneDrive - hsconline\Desktop\Data science projetcs- AP _2023\Ap data analytics\MicrosoftTeams-image.png", 
                   width=350, height=120)
st.sidebar.image(my_logo)

st.sidebar.write("""## Project Objectives
a) **Duplicates**:    
This project is related to AP DATA ANALYTICS, where this app finds duplicates based on ***certain criteria***. It will help us to improve quality of data.

**Note**: Duplicate data occurs when storing the same data entries in the same data storage system, or across multiple systems. 

b) **Outliers**    
Furthermore, this app displays the outliers in the data on given thresholds and display them.

**Note**: An outlier is an observation that lies an abnormal distance from other values in a random sample from a population.

""")


######################################################
 

def main():
    #st.title("AP Data Analytics")
    #st.title("Excel/CSV File Uploader")
    st.markdown("<h1 style='text-align: center; color: black;'>AP Data Analytics</h1>", unsafe_allow_html=True)


    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

    

    if uploaded_file is not None:

        try:

            if uploaded_file.type == 'xls' or 'xlsx':  # Excel file

                df = pd.read_excel(uploaded_file)

            elif uploaded_file.type == 'text/csv':  # CSV file

                df = pd.read_csv(uploaded_file)

            else:

                st.error("Unsupported file format. Please upload a CSV or Excel file.")

                return
        except Exception as e:

            st.error(f"Error reading the file: {e}")
            
          
        
        di =len(df.columns)
        
            
        if di == 37:
        # Display sample and shape of the dataset
             a = df.head()
             b = df.shape
             st.write('Sample size of the dataset', a)
             st.write('**Shape of the dataset** ', b)
        
            # Function to convert DataFrame to CSV
             def convert_df(dataframe):
                return dataframe.to_csv().encode('utf-8')
        
            # Find duplicates based on specific columns
             duplicates = df[df.duplicated(subset=['Supplier Name', 'Invoice Number'], keep=False)]
        
            # Check if duplicates DataFrame is empty
             # Display the duplicates if any
             if not duplicates.empty:
                    st.subheader('**No. of duplicates found in the data set** ')
                    st.write(duplicates)
            
                    # Create a download button for the duplicates
                    csv = duplicates.to_csv(index=False)
                    st.download_button(
                        label="Download Duplicates",
                        data=csv,
                        file_name='duplicates.csv',
                        mime='text/csv'
                    )
             else:
                st.markdown("<h1 style='text-align: left; color: green;'>The data frame has no duplicates</h1>", 
                              unsafe_allow_html=True)
            
        
            # Function to check spaces before and after the invoice number
             def check_spaces(invoice):
                if isinstance(invoice, str):
                    before_space = invoice.startswith(' ')
                    after_space = invoice.endswith(' ')
                    if before_space and after_space:
                        return 'space before and after'
                    elif before_space:
                        return 'space before'
                    elif after_space:
                        return 'space after'
                    elif '\t' in invoice:
                        return 'tab character present'
                return 'no space'
        
            # Create a new column 'Spaces in invoices'
             df['Spaces in invoices'] = df['Invoice Number'].apply(check_spaces)
        
            # Ensure 'Invoice Number' is treated as a string
             df['Invoice Number'] = df['Invoice Number'].apply(str)
        
            # Function to extract alphabets from a string
             def extract_alphabets(text):
                return ''.join(re.findall(r'[a-zA-Z]', text))
        
            # Function to extract special characters from a string
             def extract_special_chars(text):
                special_chars = re.sub(r'[a-zA-Z0-9]', '', text)  # Extract special characters
                return special_chars
        
            # Extract suffix (alphabets or special characters) from the 'Invoice Number' column
             df['Suffix'] = df['Invoice Number'].str.extract(r'([^\d]+)$')

            # Uncomment below to use these functions if needed
             df['Extracted_Alphabets'] = duplicates['Invoice Number'].apply(extract_alphabets)
             df['Extracted_Special_Chars'] = duplicates['Invoice Number'].apply(extract_special_chars)

            
            
            
            
            
           
            
            
            
          
             def  find_outliers(group):
                 q1 = group['Invoice Amount'].quantile(0.25)
                 q3 = group['Invoice Amount'].quantile(0.75)
                 iqr = q3 - q1
                 lower_bound = q1 - 1.5 * iqr
                 upper_bound = q3 + 1.5 * iqr
                 return group[(group['Invoice Amount'] < lower_bound) | (group['Invoice Amount'] > upper_bound)]

 # Group by 'product_supplier' and apply the outlier detection function
             outliers = df.groupby('Supplier Name').apply(find_outliers).reset_index(drop=True)
                
            
                 
            
            
            
              
            
             st.write('## Finding **Outliers** in Invoices')
            
            #outliers = detect_outliers_with_invoice_numbers(df, 'Invoice Amount')
             final_list = outliers
            # o = final_list.head(5)
             s = final_list.shape
             st.write('**Size of the outliers found in the data set**', s)
            # st.write('Sample of the outliers found in the data set', o)
             st.write('Outliers sample size ', final_list)
            
            
             df4 = outliers
                        # Function to create a dictionary of DataFrames
             def create_excel_dict(df4, selected_column, max_rows_per_sheet):
                excel_dict = {}
                unique_countries = df4[selected_column].unique()
            
                for country in unique_countries:
                    country_df = df4[df4[selected_column] == country]
            
                    # Split the country_df into chunks of max_rows_per_sheet
                    chunks = [country_df.iloc[i:i + max_rows_per_sheet] for i in range(0, len(country_df), max_rows_per_sheet)]
            
                    # Store each chunk in the dictionary
                    sheets_dict = {f'Sheet_{i + 1}': chunk for i, chunk in enumerate(chunks)}
                    excel_dict[country] = sheets_dict
            
                return excel_dict
            
            # Streamlit App
             st.write('## Download Country wise segregation')
            
            # Specify the column containing country names
             selected_column = 'Supplier Country'
            
            # Set the maximum rows per sheet
             max_rows_per_sheet = 25
            
            # Create a dictionary of DataFrames
             excel_sheets_dict = create_excel_dict(df4, selected_column, max_rows_per_sheet)
            
            # Download button for the generated Excel workbook
            #if st.button("Download Excel Workbook"):
             output_buffer = BytesIO()
        
             with pd.ExcelWriter(output_buffer, engine="xlsxwriter") as writer:
                for country, sheets_dict in excel_sheets_dict.items():
                    for sheet_name, sheet_df in sheets_dict.items():
                        sheet_df.to_excel(writer, sheet_name=f"{country}_{sheet_name}", index=False)
        
             output_buffer.seek(0)
             st.download_button(label="Download Excel Workbook", data=output_buffer, file_name="output_workbook.xlsx", key="download_btn")

            
                            
                
                
                
            
        elif di==48:
            a = df.head()
            b = df.shape
            st.write('Sample size of the dataset', a)
            st.write('**Shape of the dataset** ', b)
            
            duplicates = df[df.duplicated(subset=['Alpha Name --------------------','Invoice Number --------------------'],keep=False)] # Specify the column(s) to check for duplicates
            
            
            #duplicates1 = len(duplicates)
            # Function to check spaces before and after the invoice number
            def check_spaces(invoice):
                if isinstance(invoice, str):
                    before_space = invoice.startswith(' ')
                    after_space = invoice.endswith(' ')
                    if before_space and after_space:
                        return 'space before and after'
                    elif before_space:
                        return 'space before'
                    elif after_space:
                        return 'space after'
                    elif '\t' in invoice:
                        return 'tab character present'
                return 'no space'
            
            # Create a new column 'Space in invoice' to indicate the presence and location of spaces or tabs
            df['Spaces in invoices'] = df['Invoice Number --------------------'].apply(check_spaces)
            
            df['Invoice Number --------------------'] = df['Invoice Number --------------------'].apply(str)
            
            def extract_alphabets(text):
                return ''.join(re.findall(r'[a-zA-Z]', text))
            # Apply the function to the DataFrame column
            df['Extracted_Alphabets'] = df['Invoice Number --------------------'].apply(extract_alphabets)
            
            # Function to extract special characters from a string
            def extract_special_chars(text):
                special_chars = re.sub(r'[a-zA-Z0-9]', '', text)  # Extract special characters
                return special_chars
            
            # Apply the function to the DataFrame column
            df['Extracted_Special_Chars'] = df['Invoice Number --------------------'].apply(extract_special_chars)
            # Display the resulting DataFrame
            
            
            # Extract the suffix (alphabets or special characters) from the 'invoices' column
            df['Suffix'] = df['Invoice Number --------------------'].str.extract(r'([^\d]+)$')
            # Extract the suffix (alphabets or special characters) from the 'invoices' column
            df['Suffix'] = df['Invoice Number --------------------'].str.extract(r'([^\d]+)$')
            
            if not duplicates.empty:
                   st.subheader('**No. of duplicates found in the data set** ')
                   st.write(duplicates)
           
                   # Create a download button for the duplicates
                   csv = duplicates.to_csv(index=False)
                   st.download_button(
                       label="Download Duplicates",
                       data=csv,
                       file_name='duplicates.csv',
                       mime='text/csv'
                   )
            else:
               st.markdown("<h1 style='text-align: left; color: green;'>The data frame has no duplicates</h1>", 
                             unsafe_allow_html=True)
            
            
            
                    
            
            
            
            
            
           
            
            
            
            def find_outliers(group):
                 q1 = group['Gross Amount --------------------'].quantile(0.25)
                 q3 = group['Gross Amount --------------------'].quantile(0.75)
                 iqr = q3 - q1
                 lower_bound = q1 - 1.5 * iqr
                 upper_bound = q3 + 1.5 * iqr
                 return group[(group['Gross Amount --------------------'] < lower_bound) | (group['Gross Amount --------------------'] > upper_bound)]

 # Group by 'product_supplier' and apply the outlier detection function
            outliers = df.groupby('Alpha Name --------------------').apply(find_outliers).reset_index(drop=True)
                
            
            
            
            
            def convert_df(df):
                return df.to_csv().encode('utf-8')
            
              
            
            st.write('## Finding **Outliers** in Invoices')
            
            #outliers = detect_outliers_with_invoice_numbers(df, 'Gross Amount --------------------')
            final_list = outliers

            # o = final_list.head(5)
            s = final_list.shape
            st.write('**Size of the outliers found in the data set**', s)
            # st.write('Sample of the outliers found in the data set', o)
            st.write('Outliers sample size ', final_list)
            df4 = outliers
                        # Function to create a dictionary of DataFrames
            def create_excel_dict(df4, selected_column, max_rows_per_sheet):
                excel_dict = {}
                unique_countries = df4[selected_column].unique()
            
                for country in unique_countries:
                    country_df = df4[df4[selected_column] == country]
            
                    # Split the country_df into chunks of max_rows_per_sheet
                    chunks = [country_df.iloc[i:i + max_rows_per_sheet] for i in range(0, len(country_df), max_rows_per_sheet)]
            
                    # Store each chunk in the dictionary
                    sheets_dict = {f'Sheet_{i + 1}': chunk for i, chunk in enumerate(chunks)}
                    excel_dict[country] = sheets_dict
            
                return excel_dict
            
            # Streamlit App
            st.write('## Download Country wise segregation')
            
            # Specify the column containing country names
            selected_column = 'Country'
            
            # Set the maximum rows per sheet
            max_rows_per_sheet = 25
            
            # Create a dictionary of DataFrames
            excel_sheets_dict = create_excel_dict(df4, selected_column, max_rows_per_sheet)
            
            # Download button for the generated Excel workbook
            #if st.button("Download Excel Workbook"):
            output_buffer = BytesIO()
        
            with pd.ExcelWriter(output_buffer, engine="xlsxwriter") as writer:
                for country, sheets_dict in excel_sheets_dict.items():
                    for sheet_name, sheet_df in sheets_dict.items():
                        sheet_df.to_excel(writer, sheet_name=f"{country}_{sheet_name}", index=False)
        
            output_buffer.seek(0)
            st.download_button(label="Download Excel Workbook", data=output_buffer, file_name="output_workbook.xlsx", key="download_btn")
            
            
            
            
            
            
        elif  di==15:
            
            a = df.head()
            b = df.shape
            st.write('Sample size of the dataset', a)
            st.write('**Shape of the dataset** ', b)
            duplicates = df[df.duplicated(subset=['Supplier Name', 'Invoice Number'], keep=False)]  # Specify the column(s) to check for duplicates
            #duplicates = df[df.duplicated()]
            #dublicates1 = len(duplicates)
            if not duplicates.empty:
                   st.subheader('**No. of duplicates found in the data set** ')
                   st.write(duplicates)
           
                   # Create a download button for the duplicates
                   csv = duplicates.to_csv(index=False)
                   st.download_button(
                       label="Download Duplicates",
                       data=csv,
                       file_name='duplicates.csv',
                       mime='text/csv'
                   )
            else:
               st.markdown("<h1 style='text-align: left; color: green;'>The data frame has no duplicates</h1>", 
                             unsafe_allow_html=True)
            
            # Function to check spaces before and after the invoice number
            def check_spaces(invoice):
                if isinstance(invoice, str):
                    before_space = invoice.startswith(' ')
                    after_space = invoice.endswith(' ')
                    if before_space and after_space:
                        return 'space before and after'
                    elif before_space:
                        return 'space before'
                    elif after_space:
                        return 'space after'
                    elif '\t' in invoice:
                        return 'tab character present'
                return 'no space'
            
            # Create a new column 'Space in invoice' to indicate the presence and location of spaces or tabs
            df['Spaces in invoices'] = df['Invoice Number'].apply(check_spaces)
            
            df['Invoice Number'] = df['Invoice Number'].apply(str)
            
            def extract_alphabets(text):
                return ''.join(re.findall(r'[a-zA-Z]', text))
            
            # Apply the function to the DataFrame column
            df['Extracted_Alphabets'] = duplicates['Invoice Number'].apply(extract_alphabets)
            
            # Function to extract special characters from a string
            def extract_special_chars(text):
                special_chars = re.sub(r'[a-zA-Z0-9]', '', text)  # Extract special characters
                return special_chars
            # Apply the function to the DataFrame column
            df['Extracted_Special_Chars'] = duplicates['Invoice Number'].apply(extract_special_chars)
            # Display the resulting DataFrame
            
            #final_df= df[['Supplier Name','Supplier Site','Invoice Number','Invoice Date', 'Invoice Amount','Extracted_Alphabets','Extracted_Special_Chars']]
            
            # Extract the suffix (alphabets or special characters) from the 'invoices' column
            df['Suffix'] = df['Invoice Number'].str.extract(r'([^\d]+)$')
            
            def convert_df(df):
                return df.to_csv().encode('utf-8')
            
            
            
            
           
            
            
            
            def find_outliers(group):
                q1 = group['Invoice Amount'].quantile(0.25)
                q3 = group['Invoice Amount'].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                return group[(group['Invoice Amount'] < lower_bound) | (group['Invoice Amount'] > upper_bound)]

# Group by 'product_supplier' and apply the outlier detection function
            outliers = df.groupby('Supplier Name').apply(find_outliers).reset_index(drop=True)
                
            
            
            
            
            
            
              
            
            st.write('## Finding **Outliers** in Invoices')
            
            #outliers = detect_outliers_with_invoice_numbers(df, 'Invoice Amount')
            final_list = outliers

            # o = final_list.head(5)
            s = final_list.shape
            st.write('**Size of the outliers found in the data set**', s)
            # st.write('Sample of the outliers found in the data set', o)
            st.write('Outliers sample size ', final_list)
            
            
            
            df4 = outliers
                        # Function to create a dictionary of DataFrames
            def create_excel_dict(df4, selected_column, max_rows_per_sheet):
                excel_dict = {}
                unique_countries = df4[selected_column].unique()
            
                for country in unique_countries:
                    country_df = df4[df4[selected_column] == country]
            
                    # Split the country_df into chunks of max_rows_per_sheet
                    chunks = [country_df.iloc[i:i + max_rows_per_sheet] for i in range(0, len(country_df), max_rows_per_sheet)]
            
                    # Store each chunk in the dictionary
                    sheets_dict = {f'Sheet_{i + 1}': chunk for i, chunk in enumerate(chunks)}
                    excel_dict[country] = sheets_dict
            
                return excel_dict
            
            # Streamlit App
            st.write('## Download Country wise segregation')
            
            # Specify the column containing country names
            selected_column = 'Country'
            
            # Set the maximum rows per sheet
            max_rows_per_sheet = 25
            
            # Create a dictionary of DataFrames
            excel_sheets_dict = create_excel_dict(df4, selected_column, max_rows_per_sheet)
            
            # Download button for the generated Excel workbook
            #if st.button("Download Excel Workbook"):
            output_buffer = BytesIO()
        
            with pd.ExcelWriter(output_buffer, engine="xlsxwriter") as writer:
                for country, sheets_dict in excel_sheets_dict.items():
                    for sheet_name, sheet_df in sheets_dict.items():
                        sheet_df.to_excel(writer, sheet_name=f"{country}_{sheet_name}", index=False)
        
            output_buffer.seek(0)
            st.download_button(label="Download Excel Workbook", data=output_buffer, file_name="output_workbook.xlsx", key="download_btn")
            
                          
            
                    
                       
                   
           
                     
                     
            
            
            
            
           
            
            
            
            
            
            
            
        else:
           st.write('# Please input a valid file format #')
            
            
        
            
        
        
        
         
if __name__=='__main__':
    main()          
        
            
            
            
