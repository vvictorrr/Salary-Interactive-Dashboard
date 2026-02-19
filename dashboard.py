import panel as pn
import salary_api
import vis

# DIMENSIONS
CARD_WIDTH = 320

api = salary_api.SalaryAPI(salary_api.DATA_FILE_PATH)

def get_dataset(position, year_slider, min_salary, remote, min_samples):
    global api
    df = api.get_filtered_data(position, year_slider, min_salary, remote, min_samples)
    return df

def get_plot(df, binsize, width, height):
    return vis.salary_histogram(df, binsize,  width=width, height=height)

def get_valid_positions(year_slider, min_salary, remote, min_samples):
    '''
    need to have the positions reactive to the valid positions and not display empty tables
    '''
    df = api.get_filtered_data(
        "All Positions",
        year_slider,
        min_salary,
        remote,
        min_samples
    )
    return ["All Positions"] + sorted(df["job_title"].unique())

def main():
    # Loads javascript dependencies and configures Panel (required)
    pn.extension()

    global api

    position = pn.widgets.Select(name="Job Title")


    remote = pn.widgets.Select(name="Remote Ratio", options=api.get_remote_ratio())
    
    bins_sldr = pn.widgets.IntSlider(name="Bins", start=5, end=60, step=1, value=40)
    width_sldr = pn.widgets.IntSlider(name="Width", start=800, end=5000, step=100, value=800)
    height_sldr = pn.widgets.IntSlider(name="Height", start=600, end=5000, step=100, value=600)

    min_samples = pn.widgets.IntSlider(name="Minimum Sample Size", start=1, end=100, step=1, value=20)


    year_range = api.get_year_range()
    year_slider = pn.widgets.RangeSlider(name="Work Year",start=year_range[0], end=year_range[1], value=(year_range[0], year_range[1]))

    min_salary = pn.widgets.IntSlider(name="Minimum Salary",start=0, end=300000, step=5000, value=0)


    dataset = pn.bind(
        get_dataset,
        position,
        year_slider,
        min_salary,
        remote,
        min_samples
    )

    plot = pn.bind(
        get_plot,
        dataset,
        bins_sldr,
        width_sldr,
        height_sldr
    )

    position.options = ["All Positions"]
    position.value = "All Positions"

    valid_positions = pn.bind(
        get_valid_positions,
        year_slider,
        min_salary,
        remote,
        min_samples
    )
    position.options = valid_positions

    search_card = pn.Card(
        pn.Column(
            position,
            remote,
            year_slider,
            min_salary,
            min_samples

        ),
        title="Search", width=CARD_WIDTH, collapsed=False
    )
    plot_card = pn.Card(
        pn.Column(
            bins_sldr,
            width_sldr,
            height_sldr
        ),

        title="Plot", width=CARD_WIDTH, collapsed=True
    )

    layout = pn.template.FastListTemplate(
        title="Data Science Salary Explorer",
        sidebar=[
            search_card,
            plot_card,
        ],
        theme_toggle=False,
        main=[
            pn.Tabs(
                ("Plot", plot),  
                ("Table", dataset),  
                active=0  # Which tab is active by default?
            )
        ],
        header_background='#2E6F40'

    ).servable()

    layout.show()

if __name__ == "__main__":
    main()



