"""
The Loss function of the assessment
Over 43,329 examples
the mean loss is
"""
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from data_exploration.utils import load_pervo_data, \
    sample_paper_by_devices, sample_disjoint_devices, filter_by_kpi
import pandas as pd

w = {

}


# todo (0): all should be changed to vector multiplication if we change to
#  training a model with that
# todo: test the statistics functions and plots with small
#  subset of the data
# todo: improve the loss from 37~ when not relevant and 9~ when relevant more
#  to ~95 when not relevant and ~5 when relevant
# todo: Analyze fields statistics for the weight function
#  - boolean fields - chose a threshold that above it the field is almost
#  always the same answer it is not relevant for the error
#  - string fields - chose a threshold that above it the field is almost not
#  relevant for the error maybe use string comparisons methods


def field_error(field_name) -> float:
    pass


def compute_error(y_pred, y_true, float_tolerance=1e-3) -> float:
    """
    Compute the error between the model output and the expected output.
    #
    y_pred (list of tuples): The output from the ML model
    y_true (list of tuples): The expected output
    float_tolerance (float): The tolerance for float comparisons
    """
    if len(y_pred) != len(y_true):
        raise ValueError(
            "The length of model output and expected output must be equal\n"
            f"length of model output: {len(y_pred)}\n"
            f"length of expected output: {len(y_true)}")
    n = 0
    incorrect = 0
    for i, (model_val, expected_val) in enumerate(zip(y_pred,
                                                      y_true)):
        if model_val != model_val and expected_val != expected_val:
            continue
        try:
            model_val = model_val.item()
        except AttributeError:
            pass
        try:
            expected_val = expected_val.item()
        except AttributeError:
            pass
        if type(model_val) != type(expected_val):
            incorrect += 1
        elif isinstance(model_val, float):
            if not np.isclose(model_val, expected_val, atol=float_tolerance):
                incorrect += 1
        else:
            if model_val != expected_val:
                incorrect += 1
        n += 1
    error_rate = (incorrect / n) * 100
    return error_rate


def calc_random_error_stats(df, n=100):
    papers = sample_disjoint_devices(df, n)
    stats = dict(mean=[], sd=[], max=[], min=[])
    for i in range(len(papers)):
        paper_df = papers.copy()
        paper_df['error_rate'] = paper_df.apply(
            lambda y_pred: compute_error(y_pred, paper_df.iloc[:i]),
            axis=1)
        stats['mean'].append(df['error_rate'].mean())
        stats['sd'].append(df['error_rate'].std())
        stats['max'].append(df['error_rate'].max())
        stats['min'].append(df['error_rate'].min())
    return stats


def plot_stats(stats: dict):
    """plot the max, min mean and sd from the stats dictionary using plotly"""
    n = len(stats['mean'])
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=("Mean", "SD", "Max", "Min"))
    fig.add_trace(go.Scatter(x=list(range(n)), y=stats['mean'],
                             mode='lines+markers',
                             name='Mean'), row=1, col=1)
    fig.add_trace(go.Scatter(x=list(range(n)), y=stats['sd'],
                             mode='lines+markers',
                             name='SD'), row=1, col=2)
    fig.add_trace(go.Scatter(x=list(range(n)), y=stats['max'],
                             mode='lines+markers',
                             name='Max'), row=2, col=1)
    fig.add_trace(go.Scatter(x=list(range(n)), y=stats['min'],
                             mode='lines+markers',
                             name='Min'), row=2, col=2)
    fig.update_layout(height=600, width=800,
                      title_text="Error rate statistics")
    fig.show()


def calc_eval_metric_kpi_stats(stats: dict) -> dict:
    return {
        'mean': dict(mean=np.mean(stats['mean']), sd=np.std(stats['mean'])),
        'sd': dict(mean=np.mean(stats['sd']), sd=np.std(stats['sd'])),
        'max': dict(mean=np.mean(stats['max']), sd=np.std(stats['max'])),
        'min': dict(mean=np.mean(stats['min']), sd=np.std(stats['min'])),
    }


def eval_random_error(n=100):
    stats = calc_random_error_stats(load_pervo_data(), n)
    plot_stats(stats)

def compare_results_from_db():
    results_path = "dataset/papers/downloads/10.1002_adem.201900288_api_results.csv"
    ai_res = pd.read_csv(results_path).iloc[1]
    pervo_data = load_pervo_data()
    doi_number = '10.1002/adem.201900288'
    true_res = pervo_data[pervo_data['Ref_DOI_number'] == doi_number]
    filter_by_kpi(true_res)
    for i, y_pred in true_res.iterrows():
        error_rate = compute_error(ai_res, y_pred)
        print(f"Error rate: {round(error_rate, 3)}%")
    print(true_res)

if __name__ == '__main__':
    np.random.seed(42)
    # eval_random_error(n=100)
    compare_results_from_db()
    # df = load_pervo_data()
    # y_true_all = sample_paper_by_devices(df, 5, 5)
    # y_true = y_true_all.iloc[0]
    # y_preds = sample_paper_by_devices(df, 4, 4)
    # # y_preds = y_true_all
    # # y_preds = df
    # for i, y_pred in y_preds.iterrows():
    #     error_rate = compute_error(y_true, y_pred)
    #     print(f"Error rate: {round(error_rate, 3)}%")
    # # df['error_rate'] = df.apply(lambda y_pred: compute_error(y_pred, y_true),
    # #                             axis=1)
    # a = 3
    # print("done")
