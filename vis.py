import plotly.express as px

def salary_histogram(df, binsize, **kwargs):
    width = kwargs.get('width', 800)
    height = kwargs.get('height', 600)
    fig = px.histogram(
        df,
        x="salary_in_usd",
        nbins=binsize,
        title="Salary Distribution (USD)"
    )
    fig.update_layout(
        autosize=False,
        width=width,
        height=height)
    return fig