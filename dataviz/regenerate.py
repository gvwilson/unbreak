"""Generate HTML charts for the data visualization lesson."""

import pathlib
import random

import altair as alt
import polars as pl

HERE = pathlib.Path(__file__).parent
SEED = 20240101


def save(filename, chart):
    html = chart.to_html(inline=False)
    with open(HERE / filename, "w") as writer:
        writer.write(html)


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
            color=alt.Color("candidate:N", legend=None),
        )
        .properties(title="Candidate Approval Ratings", width=300, height=300)
    )
    save("truncated_axis.html", chart)
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
    save("truncated_axis_fixed.html", fixed)


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
    save("cherry_pick.html", chart)
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
    save("cherry_pick_fixed.html", fixed)


def dual_axis():
    """Two unrelated metrics on the same chart with independently scaled Y-axes."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rainfall_mm = [52, 41, 63, 78, 95, 88, 72, 61, 83, 54, 44, 58]
    bug_reports = [124, 93, 201, 185, 88, 162, 215, 97, 178, 133, 104, 142]
    df = pl.DataFrame({
        "month": months,
        "rainfall": rainfall_mm,
        "bugs": bug_reports,
    })
    base = alt.Chart(df).encode(x=alt.X("month:O", sort=None, title="Month"))
    rain_line = base.mark_line(color="steelblue", strokeWidth=2).encode(
        y=alt.Y(
            "rainfall:Q",
            axis=alt.Axis(title="Rainfall (mm)", titleColor="steelblue"),
        )
    )
    bug_line = base.mark_line(color="orange", strokeWidth=2).encode(
        y=alt.Y(
            "bugs:Q",
            axis=alt.Axis(title="Bug Reports", titleColor="orange"),
        )
    )
    chart = (
        alt.layer(rain_line, bug_line)
        .resolve_scale(y="independent")
        .properties(title="Monthly Rainfall vs Bug Reports", width=450, height=300)
    )
    save("dual_axis.html", chart)
    rain_chart = base.mark_line(color="steelblue", strokeWidth=2).encode(
        y=alt.Y("rainfall:Q", title="Rainfall (mm)")
    ).properties(title="Monthly Rainfall", width=450, height=150)
    bug_chart = base.mark_line(color="orange", strokeWidth=2).encode(
        y=alt.Y("bugs:Q", title="Bug Reports")
    ).properties(title="Monthly Bug Reports", width=450, height=150)
    fixed = alt.vconcat(rain_chart, bug_chart)
    save("dual_axis_fixed.html", fixed)


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
    save("simpsons_paradox.html", chart)
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
    save("simpsons_paradox_fixed.html", fixed)


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
    save("mean_hides_distribution.html", chart)
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
    save("mean_hides_distribution_fixed.html", fixed)


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
    save("absolute_vs_rate.html", chart)
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
    save("absolute_vs_rate_fixed.html", fixed)


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
    save("cumulative_hides_slowdown.html", chart)
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
    save("cumulative_hides_slowdown_fixed.html", fixed)


def overplotting():
    """Opaque markers make 2000 points look uniformly spread; 80% cluster in one corner."""
    random.seed(SEED)
    cluster = [{"x": random.gauss(1, 0.3), "y": random.gauss(1, 0.3)} for _ in range(1600)]
    spread = [{"x": random.uniform(0, 10), "y": random.uniform(0, 10)} for _ in range(400)]
    df = pl.DataFrame(cluster + spread)
    chart = (
        alt.Chart(df)
        .mark_circle(size=8, color="steelblue")
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[0, 10]), title="Variable X"),
            y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 10]), title="Variable Y"),
        )
        .properties(title="Distribution of Observations (n=2000)", width=350, height=350)
    )
    save("overplotting.html", chart)
    fixed = (
        alt.Chart(df)
        .mark_circle(size=8, opacity=0.05, color="steelblue")
        .encode(
            x=alt.X("x:Q", scale=alt.Scale(domain=[0, 10]), title="Variable X"),
            y=alt.Y("y:Q", scale=alt.Scale(domain=[0, 10]), title="Variable Y"),
        )
        .properties(title="Distribution of Observations — Low Opacity (n=2000)", width=350, height=350)
    )
    save("overplotting_fixed.html", fixed)


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
    save("pie_chart.html", chart)
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
    save("pie_chart_fixed.html", fixed)


def ecological_fallacy():
    """Regional aggregate shows income predicts Party A support; individual data shows no relationship."""
    random.seed(SEED)
    # 500 individuals with income; vote choice is independent of income
    income = [random.gauss(50, 15) for _ in range(500)]
    # Assign to 20 regions of 25 people each
    # Wealthy regions happen (by construction) to have higher Party A vote shares,
    # but this is driven by region identity, not individual income
    regions = []
    for r in range(20):
        members = slice(r * 25, (r + 1) * 25)
        avg_income = round(sum(income[members]) / 25, 1)
        # Party A share correlates with avg_income at the regional level
        party_a_pct = round(min(90, max(10, 30 + avg_income * 0.55 + random.gauss(0, 4))), 1)
        regions.append({
            "region": f"R{r + 1:02d}",
            "avg_income": avg_income,
            "party_a_pct": party_a_pct,
        })
    df = pl.DataFrame(regions)
    points = (
        alt.Chart(df)
        .mark_circle(size=80, opacity=0.8)
        .encode(
            x=alt.X("avg_income:Q", title="Region Average Income ($k)"),
            y=alt.Y(
                "party_a_pct:Q",
                title="Party A Vote Share (%)",
                scale=alt.Scale(domain=[0, 100]),
            ),
        )
    )
    trend = (
        alt.Chart(df)
        .transform_regression("avg_income", "party_a_pct")
        .mark_line(color="red", strokeWidth=2)
        .encode(x="avg_income:Q", y="party_a_pct:Q")
    )
    chart = (points + trend).properties(
        title="Income vs Party A Support (by Region)", width=400, height=300
    )
    save("ecological_fallacy.html", chart)
    # Individual-level data: vote choice is independent of income
    random.seed(SEED)
    income_ind = [random.gauss(50, 15) for _ in range(500)]
    # 45% base rate for Party A; no relationship with income
    votes = [1 if random.random() < 0.45 else 0 for _ in range(500)]
    df_ind = pl.DataFrame({
        "income": [round(x, 1) for x in income_ind],
        "party_a_vote": votes,
    })
    ind_points = (
        alt.Chart(df_ind)
        .mark_circle(size=20, opacity=0.3)
        .encode(
            x=alt.X("income:Q", title="Individual Income ($k)"),
            y=alt.Y(
                "party_a_vote:Q",
                title="Voted Party A (1=Yes, 0=No)",
                scale=alt.Scale(domain=[-0.2, 1.2]),
            ),
        )
    )
    ind_trend = (
        alt.Chart(df_ind)
        .transform_regression("income", "party_a_vote")
        .mark_line(color="red", strokeWidth=2)
        .encode(x="income:Q", y="party_a_vote:Q")
    )
    fixed = (ind_points + ind_trend).properties(
        title="Income vs Party A Vote — Individual Level", width=400, height=300
    )
    save("ecological_fallacy_fixed.html", fixed)


def main():
    alt.data_transformers.disable_max_rows()
    truncated_axis()
    cherry_pick()
    dual_axis()
    simpsons_paradox()
    mean_hides_distribution()
    absolute_vs_rate()
    cumulative_hides_slowdown()
    overplotting()
    pie_chart()
    ecological_fallacy()


if __name__ == "__main__":
    main()
