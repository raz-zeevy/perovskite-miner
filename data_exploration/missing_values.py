import numpy as np
import pandas as pd
from data_exploration.utils import *

def plot_fields(sorted_df,max_length=10, percentile = 0.05):
    """
    Parameters:
    - most_important_df: *Sorted* DataFrame to plot.
    - max_length: Maximum length for x-axis labels. Default is 10.
    - percentile: The percentile to use to divide to two groups
    """
    import plotly.express as px
    import plotly.graph_objects as go
    # Truncate and index labels to handle duplicates
    counter = {}
    def truncate_and_index(label):
        truncated = label[:max_length] + "..." if len(
            label) > max_length else label
        if truncated in counter:
            counter[truncated] += 1
            truncated += f"({counter[truncated]})"
        else:
            counter[truncated] = 1
        return truncated
    truncated_labels_with_index = [truncate_and_index(label) for label in
                                   sorted_df.index]
    # Plot
    # Find the position (index) where y values go below 0.05
    position = len(sorted_df[sorted_df.values < percentile])
    # Count the number of rows in each group
    count_above_t = position
    count_below_t = len(sorted_df) - count_above_t

    # Plot the bar chart
    fig = px.bar(sorted_df,
                 x=truncated_labels_with_index,
                 y=sorted_df.values,
                 title="Missing values in the database per field",
                 labels={"x": "Field", "y": "% of missing values"})

    # Add a vertical line
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=position,
            x1=position,
            y0=0,
            y1=max(sorted_df.values),
            line=dict(color="Red", width=2)
        )
    )
    font = dict(family="Arial", size=14, color="black")
    per = str(round(percentile * 100,1))+"%"
    # Add annotations for the number of rows in each group
    fig.add_annotation(
        x=position / 2,  # roughly in the middle of the first group
        y=max(sorted_df.values) * 0.9,
        # 90% of the max y value for visibility
        text=f"<b>Fields below {per} missing:\n{count_above_t}</b>",
        font=font,
        showarrow=False
    )

    fig.add_annotation(
        x=(position + len(sorted_df)) / 2,
        # roughly in the middle of the second group
        y=max(sorted_df.values) * 0.9,
        text=f"<b>Fields above {per} missing:\n{count_below_t}</b>",
        font=font,
        showarrow=False
    )
    # Display the plot
    fig.show()  # Commented out for execution purposes

def get_best_5p_fields():
    return fields_by_frequency[fields_by_frequency < 0.05].index

if __name__ == '__main__':
    db_path = "../data/Perovskite_database_content_all_data.csv"
    df = load_data(db_path)
    # Get the percentage of missing values per field
    fields_by_frequency = (df.isna().sum() / len(df)).sort_values()
    plot_fields(fields_by_frequency, max_length=15)
    best_5p_fields = get_best_5p_fields()