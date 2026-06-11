"""Data-driven deck: chart + metrics + table → data_deck.html"""

from decko_py import (
    ChartBlock,
    ChartCalloutSlide,
    ChartData,
    ChartDataset,
    DeckBuilder,
    MetricBlock,
    MetricTrioSlide,
    TableBlock,
    TableSlide,
    TemplateRegistry,
    TextBlock,
    TitleSlide,
    register_defaults,
)

registry = TemplateRegistry()
register_defaults(registry)

deck_html = (
    DeckBuilder()
    .meta(title="Q1 Sales Report", author="Bob", date="2024-03-31")
    .theme("nova")
    .slide(
        TitleSlide(
            headline=TextBlock(display="hero", content="Q1 Sales Report"),
            subtitle=TextBlock(display="subheading", content="January – March 2024"),
        )
    )
    .slide(
        MetricTrioSlide(
            title=TextBlock(display="heading", content="Key Numbers"),
            metric_1=MetricBlock(
                display="kpi",
                value="$2.4M",
                label="Total Revenue",
                delta="+18%",
                trend="up",
            ),
            metric_2=MetricBlock(
                display="kpi",
                value="1,240",
                label="New Customers",
                delta="+31%",
                trend="up",
            ),
            metric_3=MetricBlock(
                display="kpi",
                value="94%",
                label="Retention Rate",
                delta="-1%",
                trend="down",
            ),
        )
    )
    .slide(
        ChartCalloutSlide(
            title=TextBlock(display="heading", content="Monthly Revenue"),
            chart=ChartBlock(
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
        )
    )
    .slide(
        TableSlide(
            title=TextBlock(display="heading", content="Top Products"),
            table=TableBlock(
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
            footnote=TextBlock(content="All figures unaudited."),
        )
    )
    .render_html()
)

output = "data_deck.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(deck_html)

print(f"Saved → {output}")
