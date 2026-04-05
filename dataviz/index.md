# Data Visualization

## Truncated Y-Axis {: #dataviz-truncated}

[% figure slug="dataviz-truncated-wrong" img="truncated_axis.svg" alt="Bar chart of candidate approval ratings with Y-axis starting at 85." caption="Candidate approval ratings with a truncated Y-axis." %]

Compare the visual height of candidate A's bar to candidate D's bar. How much larger
does D appear? Now look at the actual numbers. How large is the real difference?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The Y-axis starts at 85 instead of 0. Candidate D's approval (93%) is only 6
percentage points above candidate A's (87%), but the bars make it look roughly
three times taller. Any bar chart where the Y-axis does not start at zero
exaggerates relative differences. The effect is proportional to how far the
baseline is raised: the higher the floor, the more dramatic the distortion.

[% figure slug="dataviz-truncated-fixed" img="truncated_axis_fixed.svg" alt="Bar chart of candidate approval ratings with Y-axis starting at 0." caption="The same data with the Y-axis starting at 0." %]

</details>

## Cherry-Picked Time Window {: #dataviz-cherry}

[% figure slug="dataviz-cherry-wrong" img="cherry_pick.svg" alt="Line chart showing an upward performance trend over 8 months." caption="Performance trend over the last 8 months." %]

The chart shows a clear upward trend over 8 months. What conclusion might you draw
about this product's long-term trajectory? What information would you need to know
whether this is reliable?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The 8 months shown are a recovery from a multi-year decline. The full 5-year series
falls from 100 to roughly 52 before the recent uptick. Choosing a start date at the
bottom of a trough guarantees an upward slope. This pattern is common in financial
and performance reporting: selecting the window that flatters the story while
omitting the longer context that contradicts it.

[% figure slug="dataviz-cherry-fixed" img="cherry_pick_fixed.svg" alt="Line chart showing the full 60-month history with a recent uptick at the end of a long decline." caption="The full 60-month history." %]

</details>

## Spurious Correlation via Shared Trend {: #dataviz-spurious}

[% figure slug="dataviz-spurious-wrong" img="spurious_correlation.svg" alt="Scatter plot of monthly coffee consumption vs code commits with a tight regression line." caption="Coffee consumption vs code commits over 48 months." %]

The scatter plot shows a strong positive relationship between monthly coffee
consumption and code commits, with a tight regression line. What conclusion might
a reader draw? What third factor might explain the pattern?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Both metrics grow because the engineering team grew: more engineers means more commits
and more coffee consumed. Plotting two time-trending variables against each other
removes the time axis entirely and makes a shared common cause look like a direct
relationship between the two variables. Any two series that both trend in the same
direction will produce a scatter that looks correlated, regardless of whether they
have anything to do with each other.

[% figure slug="dataviz-spurious-fixed" img="spurious_correlation_fixed.svg" alt="Scatter plot of coffee vs commits with points colored from dark to light by month, showing temporal ordering." caption="The same scatter with points colored by month. Early months are dark; late months are light." %]

Early months cluster in the lower left and late months in the upper right — the
apparent correlation is entirely temporal ordering.

</details>

## Simpson's Paradox {: #dataviz-simpsons}

[% figure slug="dataviz-simpsons-wrong" img="simpsons_paradox.svg" alt="Scatter plot of study hours vs exam score with a downward-sloping regression line." caption="Study hours vs exam score across all students." %]

The trend line shows that students who study more tend to score lower. Does that
mean studying is counterproductive? What might explain the pattern?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Students in harder courses study more hours but earn lower scores because the courses
are harder, not because studying hurts performance. Within each difficulty level the
relationship is positive: more study leads to higher scores. The aggregate trend
reverses because a third variable — course difficulty — drives both the study hours
and the scores. Adding a color encoding for difficulty would reveal three upward
slopes instead of one downward one. This is Simpson's Paradox: an aggregate trend
that disappears or reverses when a confounding variable is introduced.

[% figure slug="dataviz-simpsons-fixed" img="simpsons_paradox_fixed.svg" alt="Scatter plot colored by course difficulty showing three upward-sloping regression lines." caption="The same data colored by difficulty, with a separate regression line for each group." %]

</details>

## Mean Conceals a Bimodal Distribution {: #dataviz-meanconceals}

[% figure slug="dataviz-mean-wrong" img="mean_hides_distribution.svg" alt="Bar chart showing nearly identical group means for groups A and B." caption="Average score by group." %]

Both groups have nearly the same average score. Would you conclude they are
performing similarly? What other chart type would you choose before drawing that
conclusion?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Group A is roughly normally distributed around 62. Group B is bimodal: half the
students score near 25 and half score near 90. Both groups have the same mean, but
their situations are completely different — Group B has two distinct subpopulations
that the mean obscures entirely. A strip plot, histogram, or violin chart would make
the bimodal structure immediately visible. Reporting only the mean discards the
information most relevant to understanding Group B.

[% figure slug="dataviz-mean-fixed" img="mean_hides_distribution_fixed.svg" alt="Strip plot showing Group A clustered around 62 and Group B split near 25 and 90." caption="Individual scores for each group as a strip plot." %]

</details>

## Absolute Counts Instead of Rates {: #dataviz-absolute}

[% figure slug="dataviz-absolute-wrong" img="absolute_vs_rate.svg" alt="Bar chart of raw traffic accident counts by city, with Metro City tallest." caption="Traffic accidents by city (raw counts)." %]

Which city appears to have the most serious traffic safety problem? Now calculate
accidents per 100,000 residents for each city using the figures below. Does the
ranking change?

Metro City: 820 accidents, population 2,100,000.
River Town: 210 accidents, population 180,000.
Oak Valley: 95 accidents, population 52,000.
Pine Bluff: 430 accidents, population 640,000.

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Metro City's raw count is largest, but its rate is 39 per 100,000 — the lowest of
the four. Oak Valley has only 95 accidents but a rate of 183 per 100,000 — nearly
five times higher. Absolute counts favor larger populations and are only meaningful
when comparing groups of similar size. Any comparison that involves groups of
different sizes requires a denominator: rate, proportion, or per-capita figure.

[% figure slug="dataviz-absolute-fixed" img="absolute_vs_rate_fixed.svg" alt="Bar chart of traffic accidents per 100,000 residents, with Oak Valley now tallest." caption="Traffic accidents per 100,000 residents by city." %]

</details>

## Cumulative Chart Hides a Slowdown {: #dataviz-cumulative}

[% figure slug="dataviz-cumulative-wrong" img="cumulative_hides_slowdown.svg" alt="Line chart of cumulative user signups rising steadily over 52 weeks." caption="Cumulative user signups over 52 weeks." %]

The total user count is rising steadily. Would you describe the product as growing?
Now think about what the weekly rate of new signups looks like in the second half of
the year compared to the first.

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A cumulative chart can only go up or stay flat — it can never show a decline even if
new additions stop entirely. Weeks 1–26 add 400–600 users each; weeks 27–52 add
10–30. The product's growth has effectively stopped, but the cumulative line looks
like a healthy upward trend throughout. Plotting the weekly rate instead reveals the
collapse in new signups. Cumulative charts are useful for showing totals but
systematically hide any information about acceleration, deceleration, or stagnation.

[% figure slug="dataviz-cumulative-fixed" img="cumulative_hides_slowdown_fixed.svg" alt="Line chart of weekly new signups showing a sharp drop to near zero after week 26." caption="Weekly new signups for the same period." %]

</details>

## Discrete Overplotting Hides Density {: #dataviz-overplot}

[% figure slug="dataviz-overplot-wrong" img="discrete_overplot.svg" alt="Grid of uniformly-sized dots showing exam scores vs study hours for 600 students." caption="Exam scores by hours studied (600 students)." %]

How many students appear to have studied for 4 hours and scored 65? How confident
are you that each visible dot represents the same number of students?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Both the exam scores (multiples of 5) and hours studied (integers) are discrete, so
many students share the same coordinates. Opaque markers stack on top of each other
and become indistinguishable from a single point: a position with 40 students on top
of each other looks identical to a position with 1. The chart gives no indication
of how populated each cell is, making the data appear uniformly distributed when 80%
of students cluster at 3–6 hours and scores of 55–75.

[% figure slug="dataviz-overplot-fixed" img="discrete_overplot_fixed.svg" alt="Bubble chart of exam scores vs study hours where bubble size reveals dense clustering at 3-6 hours and scores of 55-75." caption="The same data with bubble area proportional to number of students." %]

</details>

## Pie Chart Obscures Ranking {: #dataviz-pie}

[% figure slug="dataviz-pie-wrong" img="pie_chart.svg" alt="Pie chart with seven similarly-sized slices labeled Alpha through Eta." caption="Market share by category." %]

Without reading the exact percentages, rank the seven categories from largest to
smallest share. How confident are you in your ranking? Which pairs of adjacent
categories are hardest to distinguish?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Human perception of angles and arc lengths is unreliable, especially when slices are
similar in size. The shares range from 18.4% down to 8.6% — a meaningful spread —
but most readers cannot reliably rank the middle five categories without reading the
labels. A horizontal bar chart sorted by value requires only length perception, which
humans perform much more accurately. Pie charts are defensible only when there are
two or three slices with clearly different sizes.

[% figure slug="dataviz-pie-fixed" img="pie_chart_fixed.svg" alt="Horizontal bar chart of the same seven categories sorted by market share." caption="The same data as a sorted horizontal bar chart." %]

</details>

## Group Average Does Not Predict Individuals {: #dataviz-ecological}

[% figure slug="dataviz-ecological-wrong" img="group_vs_individual.svg" alt="Scatter plot of 20 district averages showing a tight positive correlation between household income and test scores." caption="District average income vs average test score (20 districts)." %]

The chart shows that school districts with higher average household income have higher
average test scores, with a tight regression line. Would you expect to be able to
predict an individual student's score from knowing their district's average income?
How accurate do you think that prediction would be?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The district-level chart uses 20 aggregate points, so noise is suppressed and the
trend looks precise. But the district average income is a property of the district,
not the student. Within any district, students from families with very different
incomes sit in the same classrooms and take the same tests, and individual scores
scatter widely around the district mean. A statistic that explains 95% of the
variance across group averages may explain only 25–30% of the variance across
individuals, because most of the individual variance is within-group and invisible
in the aggregate chart. Drawing conclusions about individuals from group-level
correlations is the ecological fallacy.

[% figure slug="dataviz-ecological-fixed" img="group_vs_individual_fixed.svg" alt="Scatter plot of 500 individual students at their district average income showing wide vertical spread around the trend line." caption="Individual student scores plotted at their district's average income level." %]

The upward trend is still present but the scatter is so wide that knowing a student's
district tells you little about that student's score.

</details>
