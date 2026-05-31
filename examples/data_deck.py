"""Data-driven deck: chart + metrics + table → data_deck.html"""

from decko_py import (
    DeckBuilder,
    Slide,
    TextBlock,
    MetricBlock,
    ChartBlock,
    ChartData,
    ChartDataset,
    TableBlock,
    GroupBlock,
)

deck_html = (
    DeckBuilder()
    .meta(title="Q1 Sales Report", author="Bob", date="2024-03-31")
    .theme("nova")
    .slide(
        Slide(
            template_id="title",
            slots={
                "headline": TextBlock(display="hero", content="Q1 Sales Report"),
                "subheading": TextBlock(display="subheading", content="January – March 2024"),
            },
        )
    )
    .slide(
        Slide(
            template_id="metrics",
            slots={
                "headline": TextBlock(display="heading", content="Key Numbers"),
                "body": GroupBlock(
                    display="cards",
                    blocks=[
                        MetricBlock(
                            display="kpi",
                            value="$2.4M",
                            label="Total Revenue",
                            delta="+18%",
                            trend="up",
                        ),
                        MetricBlock(
                            display="kpi",
                            value="1,240",
                            label="New Customers",
                            delta="+31%",
                            trend="up",
                        ),
                        MetricBlock(
                            display="kpi",
                            value="94%",
                            label="Retention Rate",
                            delta="-1%",
                            trend="down",
                        ),
                    ],
                ),
            },
        )
    )
    .slide(
        Slide(
            template_id="chart",
            slots={
                "headline": TextBlock(display="heading", content="Monthly Revenue"),
                "body": ChartBlock(
                    display="filled",
                    chart_type="bar",
                    title="Revenue by Month (USD)",
                    data=ChartData(
                        labels=["Jan", "Feb", "Mar"],
                        datasets=[
                            ChartDataset(
                                label="Revenue",
                                values=[720000, 810000, 870000],
                                color="#6366f1",
                            ),
                            ChartDataset(
                                label="Target",
                                values=[700000, 750000, 800000],
                                color="#94a3b8",
                            ),
                        ],
                    ),
                ),
            },
        )
    )
    .slide(
        Slide(
            template_id="data",
            slots={
                "headline": TextBlock(display="heading", content="Top Products"),
                "body": TableBlock(
                    display="striped",
                    headers=["Product", "Units Sold", "Revenue", "Growth"],
                    rows=[
                        ["Widget Pro", "4,200", "$840K", "+22%"],
                        ["Widget Lite", "8,100", "$648K", "+15%"],
                        ["Widget Max", "1,050", "$525K", "+41%"],
                        ["Widget Mini", "12,300", "$369K", "+8%"],
                    ],
                    caption="Q1 2024 — all figures unaudited",
                ),
            },
        )
    )
    .render_html()
)

output = "data_deck.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(deck_html)

print(f"Saved → {output}")
