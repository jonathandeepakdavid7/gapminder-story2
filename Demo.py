# CS 7510 - Streamlit Workshop
# All 6 Checkpoints and Demonstrations

import streamlit as st
import plotly.express as px
import time

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Global Development Explorer",
    layout="wide"
)

# SIDEBAR NAVIGATION
st.sidebar.title("Streamlit Workshop")
section = st.sidebar.selectbox(
    "Choose an example",
    [
        "Checkpoint 1 - Hello Streamlit",
        "Checkpoint 2 - Plotly Chart",
        "Checkpoint 3 - Widgets",
        "Demo - Rerun Model",
        "Checkpoint 4 - Layout and Metrics",
        "Demo - Caching",
        "Checkpoints 5 and 6 - Final App",
        "Task A - Health NGO Board"
    ]
)



# CHECKPOINT 1: HELLO STREAMLIT
if section == "Checkpoint 1 - Hello Streamlit":

    st.title("Global Development Explorer")
    st.write(
        "Life expectancy and income for 142 countries, 1952–2007."
    )

    df = px.data.gapminder()

    st.dataframe(df)


# CHECKPOINT 2: PLOTLY CHART
elif section == "Checkpoint 2 - Plotly Chart":

    st.title("Global Development Explorer")
    st.write(
        "Life expectancy and income for 142 countries, 1952–2007."
    )

    df = px.data.gapminder()
    df_2007 = df[df["year"] == 2007]

    fig = px.scatter(
        df_2007,
        x="gdpPercap",
        y="lifeExp",
        hover_name="country",
        color="continent",
        size="pop",
        log_x=True
    )

    st.plotly_chart(fig)


# CHECKPOINT 3: INTERACTIVE WIDGETS
elif section == "Checkpoint 3 - Widgets":

    st.title("Global Development Explorer")

    df = px.data.gapminder()

    continent = st.selectbox(
        "Continent",
        ["All"] + sorted(df["continent"].unique())
    )

    year = st.slider(
        "Year",
        1952,
        2007,
        2007,
        step=5
    )

    filtered = df[df["year"] == year]

    if continent != "All":
        filtered = filtered[
            filtered["continent"] == continent
        ]

    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        hover_name="country",
        color="continent",
        size="pop",
        log_x=True,
        size_max=50,
        range_y=[25, 90]
    )

    st.plotly_chart(fig)


# DEMONSTRATION: STREAMLIT RERUN MODEL
elif section == "Demo - Rerun Model":

    st.title("Streamlit Rerun Demonstration")

    st.write(
        "Script ran at",
        time.strftime("%H:%M:%S")
    )

    name = st.text_input("Your name")

    st.slider("Move me", 0, 10)

    # Ordinary variable resets on every rerun
    counter = 0
    counter += 1

    st.write("Plain counter:", counter)

    # Session state remembers across reruns
    if "clicks" not in st.session_state:
        st.session_state.clicks = 0

    if st.button("Click me"):
        st.session_state.clicks += 1

    st.write(
        "Session-state clicks:",
        st.session_state.clicks
    )


# CHECKPOINT 4: SIDEBAR AND KPI METRICS
elif section == "Checkpoint 4 - Layout and Metrics":

    st.title("Global Development Explorer")

    df = px.data.gapminder()

    continent = st.sidebar.selectbox(
        "Continent",
        ["All"] + sorted(df["continent"].unique())
    )

    year = st.sidebar.slider(
        "Year",
        1952,
        2007,
        2007,
        step=5
    )

    filtered = df[df["year"] == year]

    if continent != "All":
        filtered = filtered[
            filtered["continent"] == continent
        ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Countries",
        len(filtered)
    )

    col2.metric(
        "Avg life expectancy",
        f"{filtered['lifeExp'].mean():.1f} yrs"
    )

    col3.metric(
        "Median GDP per capita",
        f"${filtered['gdpPercap'].median():,.0f}"
    )

    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        hover_name="country",
        color="continent",
        size="pop",
        log_x=True,
        size_max=50,
        range_y=[25, 90]
    )

    st.plotly_chart(fig)


# DEMONSTRATION: CACHING
elif section == "Demo - Caching":

    st.title("Streamlit Caching Demonstration")

    @st.cache_data
    def load_cache_demo():
        time.sleep(3)
        return px.data.gapminder()

    df = load_cache_demo()

    year = st.slider(
        "Year",
        1952,
        2007,
        2007,
        step=5
    )

    st.write(
        f"{len(df[df['year'] == year])} countries in {year}"
    )

    st.write(
        "Caching prevents unnecessary repeated data loading."
    )


# CHECKPOINTS 5 AND 6: COMPLETE DATA STORY APP
elif section == "Checkpoints 5 and 6 - Final App":

    @st.cache_data
    def load_data():
        return px.data.gapminder()

    df = load_data()

    st.title(
        "Asia gained 24 years of life expectancy since 1952"
    )

    story, explore = st.tabs(
        ["The story", "Explore it yourself"]
    )

    # CHECKPOINT 5 - PART 1: STORY TAB
    with story:

        by_continent = df.groupby(
            ["continent", "year"],
            as_index=False
        )["lifeExp"].mean()

        fig = px.line(
            by_continent,
            x="year",
            y="lifeExp",
            color="continent",
            labels={
                "lifeExp": "Average life expectancy (years)",
                "year": ""
            }
        )

        st.plotly_chart(fig)

        st.markdown(
            "Every continent improved, but **Asia** rose fastest: "
            "from **46.3** years in 1952 to **70.7** in 2007."
        )

        st.caption(
            "Source: Gapminder, via plotly.express. "
            "Unweighted country averages."
        )

    # CHECKPOINT 5 - PART 2: EXPLORE TAB
    with explore:

        left, right = st.columns([1, 3])

        continent = left.selectbox(
            "Continent",
            ["All"] + sorted(df["continent"].unique())
        )

        year = left.slider(
            "Year",
            1952,
            2007,
            2007,
            step=5
        )

        filtered = df[df["year"] == year]

        if continent != "All":
            filtered = filtered[
                filtered["continent"] == continent
            ]

        place = (
            "the world"
            if continent == "All"
            else continent
        )

        left.metric(
            "Avg life expectancy",
            f"{filtered['lifeExp'].mean():.1f} yrs"
        )

        right.markdown(
            f"In **{year}**, the **{len(filtered)}** countries "
            f"in **{place}** had an average life expectancy "
            f"of **{filtered['lifeExp'].mean():.1f} years**."
        )

        fig = px.scatter(
            filtered,
            x="gdpPercap",
            y="lifeExp",
            hover_name="country",
            color="continent",
            size="pop",
            log_x=True,
            size_max=50,
            range_y=[25, 90]
        )

        right.plotly_chart(fig)

        # CHECKPOINT 6: VIEW AND DOWNLOAD DATA
        with st.expander(
            "See the data behind this chart"
        ):

            st.dataframe(
                filtered,
                hide_index=True
            )

            st.download_button(
                "Download as CSV",
                data=filtered.to_csv(index=False),
                file_name=f"gapminder_{place}_{year}.csv",
                mime="text/csv"
            )

# TASK A: HEALTH NGO BOARD

elif section == "Task A - Health NGO Board":

    df = px.data.gapminder()

    st.title("Health NGO: Global Life Expectancy")

    story, explore = st.tabs([
        "The story",
        "Explore it yourself"
    ])

    with story:
        st.write("Our data story will go here.")

    with explore:
        st.write("Our interactive explorer will go here.")
