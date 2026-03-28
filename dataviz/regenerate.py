"""Generate SVG charts for the data visualization lesson."""

import pathlib
import random

import altair as alt
import polars as pl
import vl_convert as vlc

HERE = pathlib.Path(__file__).parent
SEED = 20240101


def save(filename, chart):
    svg = vlc.vegalite_to_svg(chart.to_dict())
    with open(HERE / filename, "w") as writer:
        writer.write(svg)


def truncated_axis():
    """Bar chart with Y-axis starting at 85, making a 6-point spread look enormous."""
    data = pl.DataFrame({
        "candidate": ["A", "B", "C", "D"],
        "approval": [87.0, 89.0, 91.0, 93.0],
    })
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("candidate:N", title="Candidate"),
            y=alt.Y(
                "approval:Q",
                scale=alt.Scale(domain=[85, 95]),
                title="Approval (%)",
            ),
            y2=alt.Y2(datum=85),
            color=alt.Color("candidate:N", legend=None),
        )
        .properties(title="Candidate Approval Ratings", width=300, height=300)
    )
    save("truncated_axis.svg", chart)
    fixed = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("candidate:N", title="Candidate"),
            y=alt.Y(
                "approval:Q",
                scale=alt.Scale(domain=[0, 100]),
                title="Approval (%)",
            ),
            color=alt.Color("candidate:N", legend=None),
        )
        .properties(title="Candidate Approval Ratings (Full Scale)", width=300, height=300)
    )
    save("truncated_axis_fixed.svg", fixed)


def cherry_pick():
    """Line chart of a recent 8-month uptick from a 5-year downward trend."""
    random.seed(SEED)
    n = 60
    all_values = [100.0 - i * 0.8 + random.gauss(0, 2) for i in range(n)]
    # Engineer a clear uptick over the last 8 months
    trough = all_values[51]
    for i in range(8):
        all_values[52 + i] = trough + i * 1.8 + random.gauss(0, 0.5)
    data = pl.DataFrame({
        "month": list(range(1, 9)),
        "value": [round(v, 1) for v in all_values[52:]],
    })
    chart = (
        alt.Chart(data)
        .mark_line(point=True)
        .encode(
            x=alt.X("month:O", title="Month"),
            y=alt.Y(
                "value:Q",
                scale=alt.Scale(zero=False),
                title="Performance Index",
            ),
        )
        .properties(title="Performance Trend — Last 8 Months", width=400, height=300)
    )
    save("cherry_pick.svg", chart)
    full_data = pl.DataFrame({
        "month": list(range(1, 61)),
        "value": [round(v, 1) for v in all_values],
    })
    fixed = (
        alt.Chart(full_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("month:Q", title="Month"),
            y=alt.Y(
                "value:Q",
                scale=alt.Scale(zero=False),
                title="Performance Index",
            ),
        )
        .properties(title="Performance Trend — Full 60-Month History", width=400, height=300)
    )
    save("cherry_pick_fixed.svg", fixed)


def spurious_correlation():
    """Two metrics that both grow with team size appear strongly correlated in a scatter plot."""
    random.seed(SEED)
    n = 48
    commits = [max(50, round(100 + i * 5 + random.gauss(0, 15))) for i in range(n)]
    coffee = [max(10, round(20 + i + random.gauss(0, 3))) for i in range(n)]
    df = pl.DataFrame({
        "month": list(range(1, n + 1)),
        "commits": commits,
        "coffee": coffee,
    })
    points = (
        alt.Chart(df)
        .mark_circle(size=50, color="steelblue", opacity=0.8)
        .encode(
            x=alt.X("coffee:Q", title="Coffee Bags per Month"),
            y=alt.Y("commits:Q", title="Code Commits per Month"),
        )
    )
    trend = (
        alt.Chart(df)
        .transform_regression("coffee", "commits")
        .mark_line(color="red", strokeWidth=2)
        .encode(x="coffee:Q", y="commits:Q")
    )
    chart = (points + trend).properties(
        title="Coffee Consumption vs Code Commits (48 months)", width=380, height=300
    )
    save("spurious_correlation.svg", chart)
    fixed = (
        alt.Chart(df)
        .mark_circle(size=60, opacity=0.85)
        .encode(
            x=alt.X("coffee:Q", title="Coffee Bags per Month"),
            y=alt.Y("commits:Q", title="Code Commits per Month"),
            color=alt.Color(
                "month:Q",
                title="Month",
                scale=alt.Scale(scheme="viridis"),
            ),
        )
        .properties(
            title="Coffee vs Commits — Colored by Month",
            width=380,
            height=300,
        )
    )
    save("spurious_correlation_fixed.svg", fixed)


def simpsons_paradox():
    """Aggregate trend is negative; within each difficulty group the trend is positive."""
    random.seed(SEED)
    records = []
    # Easy: low hours (2-4), high scores (75-95); within-group trend is positive
    for _ in range(40):
        h = random.uniform(2, 4)
        records.append({"hours": round(h, 2),
                        "score": round(75 + (h - 2) * 5 + random.gauss(0, 4), 1),
                        "difficulty": "Easy"})
    # Medium: medium hours (4-6), medium scores (55-75)
    for _ in range(40):
        h = random.uniform(4, 6)
        records.append({"hours": round(h, 2),
                        "score": round(55 + (h - 4) * 5 + random.gauss(0, 4), 1),
                        "difficulty": "Medium"})
    # Hard: high hours (6-8), low scores (35-55)
    for _ in range(40):
        h = random.uniform(6, 8)
        records.append({"hours": round(h, 2),
                        "score": round(35 + (h - 6) * 5 + random.gauss(0, 4), 1),
                        "difficulty": "Hard"})
    df = pl.DataFrame(records)
    points = (
        alt.Chart(df)
        .mark_circle(opacity=0.6, size=40)
        .encode(
            x=alt.X("hours:Q", title="Hours Studied per Week"),
            y=alt.Y("score:Q", title="Exam Score"),
            color=alt.value("steelblue"),
        )
    )
    trend = (
        alt.Chart(df)
        .transform_regression("hours", "score")
        .mark_line(color="red", strokeWidth=2)
        .encode(x="hours:Q", y="score:Q")
    )
    chart = (points + trend).properties(
        title="Study Hours vs Exam Score", width=400, height=300
    )
    save("simpsons_paradox.svg", chart)
    colored_points = (
        alt.Chart(df)
        .mark_circle(opacity=0.6, size=40)
        .encode(
            x=alt.X("hours:Q", title="Hours Studied per Week"),
            y=alt.Y("score:Q", title="Exam Score"),
            color=alt.Color("difficulty:N", title="Difficulty"),
        )
    )
    group_trend = (
        alt.Chart(df)
        .transform_regression("hours", "score", groupby=["difficulty"])
        .mark_line(strokeWidth=2)
        .encode(
            x="hours:Q",
            y="score:Q",
            color=alt.Color("difficulty:N", title="Difficulty"),
        )
    )
    fixed = (colored_points + group_trend).properties(
        title="Study Hours vs Exam Score (Colored by Difficulty)", width=400, height=300
    )
    save("simpsons_paradox_fixed.svg", fixed)


def mean_hides_distribution():
    """Bar chart of group means looks identical; underlying distributions are completely different."""
    random.seed(SEED)
    # Group A: unimodal around 62
    scores_a = [max(0, min(100, random.gauss(62, 8))) for _ in range(80)]
    # Group B: bimodal — half near 25, half near 90
    scores_b = (
        [max(0, min(100, random.gauss(25, 6))) for _ in range(40)] +
        [max(0, min(100, random.gauss(90, 6))) for _ in range(40)]
    )
    df = pl.DataFrame(
        [{"group": "A", "score": round(s, 1)} for s in scores_a] +
        [{"group": "B", "score": round(s, 1)} for s in scores_b]
    )
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("group:N", title="Group"),
            y=alt.Y(
                "mean(score):Q",
                title="Mean Score",
                scale=alt.Scale(domain=[0, 100]),
            ),
            color=alt.Color("group:N", legend=None),
        )
        .properties(title="Average Score by Group", width=250, height=300)
    )
    save("mean_hides_distribution.svg", chart)
    fixed = (
        alt.Chart(df)
        .mark_tick(opacity=0.4, thickness=1)
        .encode(
            x=alt.X("group:N", title="Group"),
            y=alt.Y("score:Q", title="Score", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color("group:N", legend=None),
        )
        .properties(title="Score Distribution by Group (Strip Plot)", width=250, height=300)
    )
    save("mean_hides_distribution_fixed.svg", fixed)


def absolute_vs_rate():
    """Raw accident counts make the large city look most dangerous; per-capita rates reverse the ranking."""
    data = pl.DataFrame({
        "city": ["Metro City", "River Town", "Oak Valley", "Pine Bluff"],
        "accidents": [820, 210, 95, 430],
        "population": [2_100_000, 180_000, 52_000, 640_000],
    })
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("city:N", title="City", sort="-y"),
            y=alt.Y("accidents:Q", title="Traffic Accidents"),
            color=alt.Color("city:N", legend=None),
        )
        .properties(title="Traffic Accidents by City", width=350, height=300)
    )
    save("absolute_vs_rate.svg", chart)
    data_with_rate = data.with_columns(
        (pl.col("accidents") / pl.col("population") * 100_000).alias("rate")
    )
    fixed = (
        alt.Chart(data_with_rate)
        .mark_bar()
        .encode(
            x=alt.X("city:N", title="City", sort="-y"),
            y=alt.Y("rate:Q", title="Accidents per 100,000 Residents"),
            color=alt.Color("city:N", legend=None),
        )
        .properties(title="Traffic Accidents per 100,000 Residents", width=350, height=300)
    )
    save("absolute_vs_rate_fixed.svg", fixed)


def cumulative_hides_slowdown():
    """Cumulative signups always trend up, hiding that weekly new signups dropped to near zero."""
    random.seed(SEED)
    weekly = (
        [random.randint(400, 600) for _ in range(26)] +
        [random.randint(10, 30) for _ in range(26)]
    )
    total = 0
    cumulative = []
    for w in weekly:
        total += w
        cumulative.append(total)
    df = pl.DataFrame({"week": list(range(1, 53)), "total_users": cumulative})
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("week:Q", title="Week"),
            y=alt.Y("total_users:Q", title="Total Signups (cumulative)"),
        )
        .properties(title="User Growth — Cumulative Signups", width=400, height=300)
    )
    save("cumulative_hides_slowdown.svg", chart)
    df_weekly = pl.DataFrame({"week": list(range(1, 53)), "new_users": weekly})
    fixed = (
        alt.Chart(df_weekly)
        .mark_line()
        .encode(
            x=alt.X("week:Q", title="Week"),
            y=alt.Y("new_users:Q", title="New Signups per Week"),
        )
        .properties(title="User Growth — Weekly New Signups", width=400, height=300)
    )
    save("cumulative_hides_slowdown_fixed.svg", fixed)


def discrete_overplot():
    """Opaque markers on an integer grid make all positions look equally populated."""
    random.seed(SEED)
    records = []
    for _ in range(480):
        hours = max(1, min(10, round(random.gauss(4.5, 1.0))))
        score = max(0, min(100, round(random.gauss(65, 8) / 5) * 5))
        records.append({"hours_studied": hours, "exam_score": score})
    for _ in range(120):
        hours = random.randint(1, 10)
        score = random.choice(range(0, 105, 5))
        records.append({"hours_studied": hours, "exam_score": score})
    df = pl.DataFrame(records)
    chart = (
        alt.Chart(df)
        .mark_circle(size=80, color="steelblue", opacity=1.0)
        .encode(
            x=alt.X("hours_studied:O", title="Hours Studied"),
            y=alt.Y("exam_score:O", title="Exam Score"),
        )
        .properties(title="Exam Scores by Study Hours (n=600)", width=320, height=400)
    )
    save("discrete_overplot.svg", chart)
    fixed = (
        alt.Chart(df)
        .mark_circle(color="steelblue", opacity=0.7)
        .encode(
            x=alt.X("hours_studied:O", title="Hours Studied"),
            y=alt.Y("exam_score:O", title="Exam Score"),
            size=alt.Size(
                "count():Q",
                title="Students",
                scale=alt.Scale(range=[20, 600]),
            ),
        )
        .properties(
            title="Exam Scores by Study Hours — Bubble Size Shows Count",
            width=320,
            height=400,
        )
    )
    save("discrete_overplot_fixed.svg", fixed)


def pie_chart():
    """Seven similar-sized slices in a pie chart that cannot be ranked by eye."""
    data = pl.DataFrame({
        "category": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta"],
        "share": [18.4, 16.9, 15.7, 14.8, 13.5, 12.1, 8.6],
    })
    chart = (
        alt.Chart(data)
        .mark_arc()
        .encode(
            theta=alt.Theta("share:Q"),
            color=alt.Color("category:N", legend=alt.Legend(title="Category")),
            tooltip=["category:N", "share:Q"],
        )
        .properties(title="Market Share by Category (%)", width=350, height=350)
    )
    save("pie_chart.svg", chart)
    fixed = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            y=alt.Y("category:N", sort="-x", title="Category"),
            x=alt.X("share:Q", title="Market Share (%)"),
            color=alt.Color("category:N", legend=None),
        )
        .properties(title="Market Share by Category — Sorted Bar Chart", width=350, height=250)
    )
    save("pie_chart_fixed.svg", fixed)


def group_vs_individual():
    """District averages show a tight income-score correlation; individual students vary enormously."""
    random.seed(SEED)
    district_records = []
    student_records = []
    for d in range(20):
        avg_income = 30 + d * 3
        avg_score = round(40 + d * 2.5 + random.gauss(0, 3), 1)
        district_records.append({"avg_income": avg_income, "avg_score": avg_score})
        for _ in range(25):
            score = round(max(0, min(100, random.gauss(avg_score, 22))), 1)
            student_records.append({"avg_income": avg_income, "score": score})
    district_df = pl.DataFrame(district_records)
    student_df = pl.DataFrame(student_records)
    points = (
        alt.Chart(district_df)
        .mark_circle(size=120, color="steelblue", opacity=0.85)
        .encode(
            x=alt.X("avg_income:Q", title="District Average Household Income ($k)"),
            y=alt.Y("avg_score:Q", title="District Average Test Score",
                    scale=alt.Scale(domain=[30, 90])),
        )
    )
    trend = (
        alt.Chart(district_df)
        .transform_regression("avg_income", "avg_score")
        .mark_line(color="red", strokeWidth=2)
        .encode(x="avg_income:Q", y="avg_score:Q")
    )
    chart = (points + trend).properties(
        title="District Income vs Average Test Score (20 districts)", width=400, height=300
    )
    save("group_vs_individual.svg", chart)
    ind_points = (
        alt.Chart(student_df)
        .mark_circle(size=20, opacity=0.3, color="steelblue")
        .encode(
            x=alt.X("avg_income:Q", title="District Average Household Income ($k)"),
            y=alt.Y("score:Q", title="Individual Student Score",
                    scale=alt.Scale(domain=[0, 100])),
        )
    )
    ind_trend = (
        alt.Chart(student_df)
        .transform_regression("avg_income", "score")
        .mark_line(color="red", strokeWidth=2)
        .encode(x="avg_income:Q", y="score:Q")
    )
    fixed = (ind_points + ind_trend).properties(
        title="District Income vs Individual Student Score (500 students)", width=400, height=300
    )
    save("group_vs_individual_fixed.svg", fixed)


def main():
    alt.data_transformers.disable_max_rows()
    truncated_axis()
    cherry_pick()
    spurious_correlation()
    simpsons_paradox()
    mean_hides_distribution()
    absolute_vs_rate()
    cumulative_hides_slowdown()
    discrete_overplot()
    pie_chart()
    group_vs_individual()


if __name__ == "__main__":
    main()
