from data_exploration.utils import load_data
import plotly.express as px

def plot_devices_per_paper():
    df = load_data(r"..\data\Perovskite_database_content_all_data.csv")
    df = df.groupby("Ref_DOI_number")['Ref_ID'].count()
    px.histogram(df, x="Ref_ID", nbins=100,
                 labels={"Ref_ID" : 'Devices per Article'}).show()

if __name__ == '__main__':
    plot_devices_per_paper()