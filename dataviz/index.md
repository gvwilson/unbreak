# Data Visualization

## Truncated Y-Axis {: #dataviz-truncated}

Open `truncated_axis.html`. Compare the visual height of candidate A's bar to
candidate D's bar. How much larger does D appear? Now look at the actual numbers.
How large is the real difference?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The Y-axis starts at 85 instead of 0. Candidate D's approval (93%) is only 6
percentage points above candidate A's (87%), but the bars make it look roughly
three times taller. Any bar chart where the Y-axis does not start at zero
exaggerates relative differences. The effect is proportional to how far the
baseline is raised: the higher the floor, the more dramatic the distortion.

</details>

## Cherry-Picked Time Window {: #dataviz-cherry}

Open `cherry_pick.html`. The chart shows a clear upward trend over 8 months.
What conclusion might you draw about this product's long-term trajectory?
What information would you need to know whether this is reliable?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The 8 months shown are a recovery from a multi-year decline. The full 5-year series
falls from 100 to roughly 52 before the recent uptick. Choosing a start date at the
bottom of a trough guarantees an upward slope. This pattern is common in financial
and performance reporting: selecting the window that flatters the story while
omitting the longer context that contradicts it.

</details>

## Dual Y-Axis With Independent Scales {: #dataviz-dualaxis}

Open `dual_axis.html`. The two lines appear to move together through the year.
What conclusion might a reader draw? Now read the two Y-axis labels and their ranges.
Is the visual similarity meaningful?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Rainfall and bug reports have no causal connection, but they appear correlated because
the two Y-axes were independently scaled so that both lines fit neatly in the same
chart area. Any two time series can be made to look correlated this way by adjusting
the scales. A reader who does not notice the dual axes and different units will
conclude the variables are related when they are not.

</details>

## Simpson's Paradox {: #dataviz-simpsons}

Open `simpsons_paradox.html`. The trend line shows that students who study more
tend to score lower. Does that mean studying is counterproductive? What might explain
the pattern?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Students in harder courses study more hours but earn lower scores because the courses
are harder, not because studying hurts performance. Within each difficulty level the
relationship is positive: more study leads to higher scores. The aggregate trend
reverses because a third variable — course difficulty — drives both the study hours
and the scores. Adding a color encoding for difficulty would reveal three upward
slopes instead of one downward one. This is Simpson's Paradox: an aggregate trend
that disappears or reverses when a confounding variable is introduced.

</details>

## Mean Conceals a Bimodal Distribution {: #dataviz-meanconceals}

Open `mean_hides_distribution.html`. Both groups have nearly the same average score.
Would you conclude they are performing similarly? What other chart type would you
choose before drawing that conclusion?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Group A is roughly normally distributed around 62. Group B is bimodal: half the
students score near 25 and half score near 90. Both groups have the same mean, but
their situations are completely different — Group B has two distinct subpopulations
that the mean obscures entirely. A strip plot, histogram, or violin chart would make
the bimodal structure immediately visible. Reporting only the mean discards the
information most relevant to understanding Group B.

</details>

## Absolute Counts Instead of Rates {: #dataviz-absolute}

Open `absolute_vs_rate.html`. Which city appears to have the most serious traffic
safety problem? Now calculate accidents per 100,000 residents for each city using
the figures below. Does the ranking change?

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

</details>

## Cumulative Chart Hides a Slowdown {: #dataviz-cumulative}

Open `cumulative_hides_slowdown.html`. The total user count is rising steadily.
Would you describe the product as growing? Now think about what the weekly rate of
new signups looks like in the second half of the year compared to the first.

<details class="explanation" markdown="1"><summary>Show explanation</summary>

A cumulative chart can only go up or stay flat — it can never show a decline even if
new additions stop entirely. Weeks 1–26 add 400–600 users each; weeks 27–52 add
10–30. The product's growth has effectively stopped, but the cumulative line looks
like a healthy upward trend throughout. Plotting the weekly rate instead reveals the
collapse in new signups. Cumulative charts are useful for showing totals but
systematically hide any information about acceleration, deceleration, or stagnation.

</details>

## Overplotting Hides Density {: #dataviz-overplot}

Open `overplotting.html`. The 2,000 points appear to be distributed fairly evenly
across the chart. Where are most of them actually located? What would you change
about the chart to reveal the true distribution?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Eighty percent of the points are tightly clustered near (1, 1) in the lower-left
corner, but opaque markers stack on top of each other and become indistinguishable
from a single point. The remaining 20% scattered across the full range give the
misleading impression of uniform coverage. Reducing opacity to around 0.05, using a
2D density contour, or adding a hex-bin aggregation would make the cluster visible.
Overplotting is common whenever a scatter plot contains more than a few hundred
observations.

</details>

## Pie Chart Obscures Ranking {: #dataviz-pie}

Open `pie_chart.html`. Without reading the tooltip, rank the seven categories from
largest to smallest share. How confident are you in your ranking? Which pairs of
adjacent categories are hardest to distinguish?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

Human perception of angles and arc lengths is unreliable, especially when slices are
similar in size. The shares range from 18.4% down to 8.6% — a meaningful spread —
but most readers cannot reliably rank the middle five categories without reading the
labels. A horizontal bar chart sorted by value requires only length perception, which
humans perform much more accurately. Pie charts are defensible only when there are
two or three slices with clearly different sizes.

</details>

## Ecological Fallacy {: #dataviz-ecological}

Open `ecological_fallacy.html`. The trend line shows that regions with higher average
income give Party A a larger vote share. Does this mean wealthier individuals are
more likely to vote for Party A? What kind of data would you need to test that claim?

<details class="explanation" markdown="1"><summary>Show explanation</summary>

The chart shows regional aggregates, not individual votes. The correlation at the
regional level does not imply that within any region the higher-income residents are
the ones voting for Party A — they may not be. Attributing a group-level pattern to
the individuals within the group is the ecological fallacy. The individual-level data
used to construct this chart has no correlation between income and vote choice; the
regional pattern emerges from geographic sorting and other confounders. Confirming
any claim about individual behavior requires individual-level data.

</details>
