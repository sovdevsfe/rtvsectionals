import streamlit as st
import os
import pandas as pd

# Mito will automatically read this file into a dataframe
# and display it as a sheet tab
# dfs, _ = spreadsheet("Huntingdon_20231114_12-20.csv")
# use this to allow https://mito-for-st-demo.streamlit.app/

# https://www.trymito.io/plans

import streamlit as st

# Define the URL of your Buy Me a Coffee page
# buy_me_a_coffee_url = "https://www.buymeacoffee.com/sovdevs"

# # Define the HTML code to display the icon and link
# html_code = f'<a href="{buy_me_a_coffee_url}" target="_blank"><img src="BuymeACoffee15x15.jpg" alt="Buy Me a Coffee"></a>'

# # Display the HTML code in Streamlit
# st.markdown(html_code, unsafe_allow_html=True)


# Function to read and filter CSV files by horse name
def search_csvs_by_horse(csv_directory, horse_name):
    matching_records = []

    # Loop through the CSV files in the directory
    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(csv_directory, filename)

            # Read the current CSV file into a DataFrame
            current_df = pd.read_csv(file_path)

            # Filter records by horse name
            horse_records = current_df[
                current_df["Runner"].str.contains(horse_name, case=False, na=False)
            ]

            # Drop rows with empty values and reorder columns alphabetically
            horse_records = horse_records.dropna(axis=0, how="all")
            horse_records = horse_records.reindex(sorted(horse_records.columns), axis=1)

            fixed_columns = ["Runner", "Pos", "Total", "Last 4 F times", "Last 4F%"]
            variable_columns = [
                col for col in horse_records.columns if col not in fixed_columns
            ]
            variable_columns.sort()  # Sort variable columns alphabetically
            desired_column_order = fixed_columns + variable_columns
            horse_records = horse_records[desired_column_order]

            # Sort the columns alphabetically
            # horse_records = horse_records.sort_index(axis=1)

            # Remove columns with all None (NaN) values
            horse_records = horse_records.dropna(axis=1, how="all")

            # Append matching records to the result
            if not horse_records.empty:
                matching_records.append(horse_records)

    return pd.concat(matching_records, ignore_index=True)


# Function to get a list of available filenames
def get_available_filenames(csv_directory):
    filenames = []

    # Loop through the CSV files in the directory
    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            filenames.append(filename)

    return filenames


# Streamlit app
def main():
    st.title("SUPER SECTIONALS - UK Horse Racing Data Search")

    # Specify the directory containing your CSV files
    csv_directory = "csvs"

    # Create a search form for horse name
    horse_name = st.text_input("Enter horse name:")

    if st.button("Search by Horse"):
        if horse_name:
            # Perform the search and display results
            st.subheader(f"Search Results for '{horse_name}':")
            matching_records = search_csvs_by_horse(csv_directory, horse_name)
            if not matching_records.empty:
                st.write(matching_records)
            else:
                st.write("No matching records found.")
                st.rerun()

    # Create a dropdown for selecting a filename
    available_filenames = get_available_filenames(csv_directory)
    selected_filename = st.selectbox("Select a filename:", available_filenames)

    if st.button("Search by Racecourse or Date"):
        if selected_filename:
            # Read the selected CSV file into a DataFrame
            file_path = os.path.join(csv_directory, selected_filename)
            selected_df = pd.read_csv(file_path)
            selected_df = selected_df.sort_values(by="Pos", ascending=True)

            # Display the records from the selected file
            st.subheader(f"Records from '{selected_filename}':")
            # st.write(selected_df)
            st.dataframe(data=selected_df.reset_index(drop=True))


if __name__ == "__main__":
    main()
