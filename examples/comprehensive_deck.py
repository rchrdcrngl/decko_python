"""comprehensive_deck.py — All 23 built-in templates + 2 custom templates.

Output: comprehensive_deck.html
"""

from typing import Literal, Union

from decko_py import (
    AgendaSlide,
    ArchitectureDiagramSlide,
    BigMetricSlide,
    BulletsMediaSlide,
    CalloutBlock,
    ChartBlock,
    ChartCalloutSlide,
    ChartData,
    ChartDataset,
    ClosingSlide,
    CodeBlock,
    CodeWalkthroughSlide,
    ComparisonSlide,
    DeckBuilder,
    FullBleedMediaSlide,
    HeaderBodySlide,
    ImageGridSlide,
    KineticCanvasSlide,
    KineticHeroSlide,
    ListBlock,
    MediaBlock,
    MediaCaptionSlide,
    MetricBlock,
    MetricTrioSlide,
    QuoteSlide,
    SectionBreakSlide,
    SingleColumnSlide,
    TableBlock,
    TableSlide,
    TemplateRegistry,
    TerminalSlide,
    TextBlock,
    ThreeUpSlide,
    TitleSlide,
    TwoColumnSlide,
    register_defaults,
)
from decko_py.models.blocks import Block, KineticTextBlock
from decko_py.models.rich_text import ListItem
from decko_py.models.slide import (
    ColorBackground,
    GradientBackground,
    SlideAmbient,
    SlotStyle,
)
from decko_py.models.template import (
    AiHints,
    BaseTemplate,
    ContentBudget,
    LayoutMode,
    TemplateCategory,
    TemplateSlot,
)
from decko_py.models.transition import FadeTransition, PanTransition
from decko_py.models.typed_slides import TextSlot, TypedSlide

# ── Custom templates ──────────────────────────────────────────────────────────


class TestimonialGridTemplate(BaseTemplate):
    id: str = "testimonial-grid"
    name: str = "Testimonial Grid"
    category: TemplateCategory = "narrative"
    description: str = "Three customer testimonials arranged in a grid."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="testimonial-1",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="testimonial-2",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="testimonial-3",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=False,
            content_budget=ContentBudget(max_chars=80),
        ),
    ]
    layout_modes: list[LayoutMode] = ["auto", "centered"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show three customer or user testimonials side by side.",
        good_for=["social proof", "customer success", "reviews"],
        avoid=["more than 3 testimonials", "long quotes over 40 words"],
        suggested_follow_up=["closing", "header-body"],
    )


class TimelineTemplate(BaseTemplate):
    id: str = "timeline"
    name: str = "Timeline"
    category: TemplateCategory = "content"
    description: str = "Step-by-step timeline with 2–4 steps and a title."
    slots: list[TemplateSlot] = [
        TemplateSlot(
            id="title",
            accepts=["text"],
            required=True,
            content_budget=ContentBudget(max_chars=80),
        ),
        TemplateSlot(
            id="step-1",
            accepts=["text", "callout"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="step-2",
            accepts=["text", "callout"],
            required=True,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="step-3",
            accepts=["text", "callout"],
            required=False,
            content_budget=ContentBudget(max_chars=200),
        ),
        TemplateSlot(
            id="step-4",
            accepts=["text", "callout"],
            required=False,
            content_budget=ContentBudget(max_chars=200),
        ),
    ]
    layout_modes: list[LayoutMode] = ["auto", "top-heavy"]
    ai_hints: AiHints = AiHints(
        when_to_use="Show a sequential process, roadmap, or how-it-works flow.",
        good_for=["onboarding flows", "product roadmaps", "step-by-step guides"],
        avoid=["more than 4 steps", "non-sequential content"],
        suggested_follow_up=["header-body", "code-walkthrough"],
    )


# ── Custom typed slides ────────────────────────────────────────────────────────


class TestimonialGridSlide(TypedSlide):
    template_id: Literal["testimonial-grid"] = "testimonial-grid"
    testimonial_1: TextSlot
    testimonial_2: TextSlot
    testimonial_3: TextSlot
    title: Union[TextSlot, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "testimonial-1": self.testimonial_1,
            "testimonial-2": self.testimonial_2,
            "testimonial-3": self.testimonial_3,
        }
        if self.title is not None:
            s["title"] = self.title
        return s


class TimelineSlide(TypedSlide):
    template_id: Literal["timeline"] = "timeline"
    title: TextSlot
    step_1: Union[TextBlock, CalloutBlock]
    step_2: Union[TextBlock, CalloutBlock]
    step_3: Union[TextBlock, CalloutBlock, None] = None
    step_4: Union[TextBlock, CalloutBlock, None] = None

    def _build_slots(self) -> dict[str, Union[Block, list[Block]]]:
        s: dict[str, Union[Block, list[Block]]] = {
            "title": self.title,
            "step-1": self.step_1,
            "step-2": self.step_2,
        }
        if self.step_3 is not None:
            s["step-3"] = self.step_3
        if self.step_4 is not None:
            s["step-4"] = self.step_4
        return s


# ── Registry ──────────────────────────────────────────────────────────────────

registry = TemplateRegistry()
register_defaults(registry)
registry.register(TestimonialGridTemplate())
registry.register(TimelineTemplate())

# ── Shared assets (placeholder URLs for demo) ─────────────────────────────────

IMG = "https://placehold.co/1280x720/1a1a2e/ffffff"
IMG_SQUARE = "https://placehold.co/600x600/1a1a2e/ffffff"
IMG_DIAGRAM = "https://placehold.co/1200x800/0f3460/ffffff"

# ── Deck ──────────────────────────────────────────────────────────────────────

deck_html = (
    DeckBuilder()
    .meta(
        title="Decko Platform: All Templates",
        author="Decko Team",
        date="2026-06-11",
        org="Decko",
    )
    .theme(
        "midnight",
        tokens={
            "colorAccent": "#7c3aed",
            "motionIntensity": "expressive",
        },
    )
    # ── 1. TITLE SLIDE ──────────────────────────────────────────────────────────
    .slide(
        TitleSlide(
            headline=TextBlock(display="hero", content="Build. Present. Ship."),
            subtitle="A complete tour of all 23 Decko templates",
            eyebrow="Decko Platform · 2026",
            ambient=SlideAmbient(type="particles", intensity="medium"),
            transition=FadeTransition(duration=0.6),
            notes="Welcome slide. Walk through the full template catalog.",
        )
    )
    # ── 2. AGENDA ───────────────────────────────────────────────────────────────
    .slide(
        AgendaSlide(
            title="What we're covering",
            items=ListBlock(
                display="numbered",
                items=[
                    ListItem(text="Narrative — title, section breaks, agenda, quotes, closing"),
                    ListItem(text="Content — headers, columns, bullets, three-up"),
                    ListItem(text="Data — metrics, charts, tables"),
                    ListItem(text="Visual — media, kinetic typography"),
                    ListItem(text="Technical — code, architecture, terminal"),
                    ListItem(text="Custom templates"),
                ],
            ),
        )
    )
    # ── 3. SECTION BREAK — Narrative ────────────────────────────────────────────
    .slide(
        SectionBreakSlide(
            title="Narrative Templates",
            label="Part I",
            description="Set the stage, open sections, close with impact.",
            background=ColorBackground(value="#0f0f1a"),
            transition=PanTransition(direction="right"),
        )
    )
    # ── 4. HEADER + BODY ────────────────────────────────────────────────────────
    .slide(
        HeaderBodySlide(
            title="Why presentations still matter",
            subtitle="The case for structured, code-driven decks",
            body=ListBlock(
                display="bullets",
                items=[
                    ListItem(text="Decks are the universal format for alignment"),
                    ListItem(text="Manual slide tools don't scale with data or code"),
                    ListItem(text="Decko bridges Python pipelines and polished output"),
                    ListItem(text="Fully typed, validated, version-controlled"),
                ],
            ),
        )
    )
    # ── 5. QUOTE ────────────────────────────────────────────────────────────────
    .slide(
        QuoteSlide(
            quote="We replaced three days of slide work with a 40-line Python script.",
            attribution="— Engineering Lead, Series B startup",
            ambient=SlideAmbient(type="aurora", intensity="low"),
        )
    )
    # ── 6. SECTION BREAK — Content ──────────────────────────────────────────────
    .slide(
        SectionBreakSlide(
            title="Content Templates",
            label="Part II",
            background=ColorBackground(value="#0d1117"),
        )
    )
    # ── 7. SINGLE COLUMN ────────────────────────────────────────────────────────
    .slide(
        SingleColumnSlide(
            title="One idea at a time",
            body=TextBlock(
                display="body",
                content="The single-column layout keeps focus on a single, clear idea. "
                "No sidebars, no distractions — just the message and the reader.",
            ),
        )
    )
    # ── 8. TWO COLUMN ───────────────────────────────────────────────────────────
    .slide(
        TwoColumnSlide(
            title="Manual slides vs Decko",
            left_label="Manual tools",
            right_label="Decko",
            left=ListBlock(
                display="bullets",
                items=[
                    ListItem(text="Click-drag layout"),
                    ListItem(text="No version control"),
                    ListItem(text="Data copy-paste"),
                    ListItem(text="Hard to review"),
                ],
            ),
            right=ListBlock(
                display="bullets",
                items=[
                    ListItem(text="Code-first layout"),
                    ListItem(text="Full git history"),
                    ListItem(text="Live data binding"),
                    ListItem(text="PR reviewable"),
                ],
            ),
        )
    )
    # ── 9. BULLETS + MEDIA ──────────────────────────────────────────────────────
    .slide(
        BulletsMediaSlide(
            title="Template-driven slides",
            bullets=ListBlock(
                display="bullets",
                items=[
                    ListItem(text="23 built-in templates across 5 categories"),
                    ListItem(text="Typed slot fields — no raw dict required"),
                    ListItem(text="String coercion: headline='Hello' just works"),
                    ListItem(text="Catalog-aware validation at build time"),
                ],
            ),
            media=MediaBlock(src=IMG, alt="Decko template picker screenshot"),
            caption="Template catalog in the Decko editor",
        )
    )
    # ── 10. THREE UP ────────────────────────────────────────────────────────────
    .slide(
        ThreeUpSlide(
            title="Three pillars of Decko",
            col_1_label="Type-safe",
            col_2_label="Validated",
            col_3_label="Renderable",
            col_1=TextBlock(
                display="body",
                content="Pydantic v2 models. Every field is typed. "
                "Catch errors before the deck renders.",
            ),
            col_2=TextBlock(
                display="body",
                content="Content budgets enforced at build time. "
                "No more overflowing text at runtime.",
            ),
            col_3=TextBlock(
                display="body",
                content="Outputs static HTML with a CDN runtime. "
                "Deploy anywhere, no server needed.",
            ),
        )
    )
    # ── 11. SECTION BREAK — Data ────────────────────────────────────────────────
    .slide(
        SectionBreakSlide(
            title="Data Templates",
            label="Part III",
            background=GradientBackground(
                value="linear-gradient(135deg, #0f0f1a 0%, #1a0a2e 100%)"
            ),
        )
    )
    # ── 12. BIG METRIC ──────────────────────────────────────────────────────────
    .slide(
        BigMetricSlide(
            metric=MetricBlock(
                value="23",
                label="Built-in templates",
                delta="+18 since v1",
                trend="up",
            ),
            eyebrow="Template catalog",
            context="Covering narrative, content, data, visual, and technical categories.",
            ambient=SlideAmbient(type="ripple", intensity="low"),
        )
    )
    # ── 13. METRIC TRIO ─────────────────────────────────────────────────────────
    .slide(
        MetricTrioSlide(
            title="Decko by the numbers",
            metric_1=MetricBlock(
                value="23",
                label="Templates",
                trend="up",
            ),
            metric_2=MetricBlock(
                value="14",
                label="Block types",
                trend="up",
            ),
            metric_3=MetricBlock(
                value="85%",
                label="Test coverage",
                trend="neutral",
            ),
        )
    )
    # ── 14. CHART + CALLOUT ─────────────────────────────────────────────────────
    .slide(
        ChartCalloutSlide(
            title="Template adoption by category",
            chart=ChartBlock(
                chart_type="bar",
                data=ChartData(
                    labels=["narrative", "content", "data", "visual", "technical"],
                    datasets=[
                        ChartDataset(
                            label="Templates",
                            values=[5, 5, 4, 6, 3],
                        )
                    ],
                ),
            ),
            callout=CalloutBlock(
                display="info",
                title="Most popular",
                body="Visual templates see 2× more use in marketing decks.",
            ),
        )
    )
    # ── 15. TABLE SLIDE ─────────────────────────────────────────────────────────
    .slide(
        TableSlide(
            title="Template categories at a glance",
            table=TableBlock(
                headers=["Category", "Templates", "Best for"],
                rows=[
                    ["narrative", "5", "Intros, sections, quotes, closing"],
                    ["content", "5", "Bullets, columns, headers, media"],
                    ["data", "4", "Metrics, charts, tables"],
                    ["visual", "6", "Media, kinetic, comparison"],
                    ["technical", "3", "Code, diagrams, terminal"],
                ],
            ),
            footnote="All templates support ambient effects and custom backgrounds.",
        )
    )
    # ── 16. SECTION BREAK — Visual ──────────────────────────────────────────────
    .slide(
        SectionBreakSlide(
            title="Visual Templates",
            label="Part IV",
            background=ColorBackground(value="#0a0a14"),
        )
    )
    # ── 17. FULL BLEED MEDIA ────────────────────────────────────────────────────
    .slide(
        FullBleedMediaSlide(
            media=MediaBlock(src=IMG, alt="Decko full-screen render"),
            overlay_text="See it. Feel it. Ship it.",
            caption="Full-bleed media with overlay text",
            ambient=SlideAmbient(type="gradient-shift", intensity="medium"),
        )
    )
    # ── 18. MEDIA + CAPTION ─────────────────────────────────────────────────────
    .slide(
        MediaCaptionSlide(
            media=MediaBlock(src=IMG, alt="Architecture overview"),
            title="System overview",
            caption="Decko renders a Pydantic deck model into static HTML "
            "consumed by the CDN runtime.",
        )
    )
    # ── 19. IMAGE GRID ──────────────────────────────────────────────────────────
    .slide(
        ImageGridSlide(
            title="Template previews",
            image_1=MediaBlock(src=IMG_SQUARE, alt="Title slide preview"),
            image_2=MediaBlock(src=IMG_SQUARE, alt="Chart slide preview"),
            image_3=MediaBlock(src=IMG_SQUARE, alt="Metric slide preview"),
            image_4=MediaBlock(src=IMG_SQUARE, alt="Code slide preview"),
        )
    )
    # ── 20. COMPARISON ──────────────────────────────────────────────────────────
    .slide(
        ComparisonSlide(
            title="Before and after",
            left_label="Raw Slide dict",
            right_label="TypedSlide class",
            before=TextBlock(
                display="body",
                content='Slide(template_id="title-slide", '
                'slots={"headline": TextBlock(content="Hello")})',
            ),
            after=TextBlock(
                display="body",
                content='TitleSlide(headline="Hello")',
            ),
        )
    )
    # ── 21. KINETIC CANVAS ──────────────────────────────────────────────────────
    .slide(
        KineticCanvasSlide(
            word_1=KineticTextBlock(content="Build", font_size="9rem", color="#7c3aed"),
            word_2=KineticTextBlock(content="Present", font_size="6rem", color="#a78bfa"),
            word_3=KineticTextBlock(content="Ship", font_size="4rem", color="#c4b5fd"),
            caption="The Decko workflow",
            ambient=SlideAmbient(type="orbs", intensity="medium"),
            slot_styles={
                "word-1": SlotStyle(position="absolute", top="15%", left="8%"),
                "word-2": SlotStyle(position="absolute", top="42%", right="10%"),
                "word-3": SlotStyle(position="absolute", bottom="18%", left="30%"),
                "caption": SlotStyle(position="absolute", bottom="6%", right="6%"),
            },
        )
    )
    # ── 22. KINETIC HERO ────────────────────────────────────────────────────────
    .slide(
        KineticHeroSlide(
            word_top=KineticTextBlock(content="CODE", font_size="12rem", color="#7c3aed"),
            word_mid=KineticTextBlock(content="DECK", font_size="12rem", color="#ffffff"),
            word_bottom=KineticTextBlock(content="SHIP", font_size="12rem", color="#a78bfa"),
            ghost_bg=KineticTextBlock(content="DECKO", ghost=True, color="#ffffff"),
            tagline="From Python to polished — in seconds.",
            ambient=SlideAmbient(type="constellation", intensity="high"),
            slot_styles={
                "ghost-bg": SlotStyle(position="absolute", top="50%", left="50%"),
                "word-top": SlotStyle(position="absolute", top="8%", left="5%"),
                "word-mid": SlotStyle(position="absolute", top="38%", right="5%"),
                "word-bottom": SlotStyle(position="absolute", bottom="8%", left="15%"),
                "tagline": SlotStyle(position="absolute", bottom="4%", right="4%"),
            },
        )
    )
    # ── 23. SECTION BREAK — Technical ───────────────────────────────────────────
    .slide(
        SectionBreakSlide(
            title="Technical Templates",
            label="Part V",
            background=ColorBackground(value="#0d1117"),
        )
    )
    # ── 24. CODE WALKTHROUGH ────────────────────────────────────────────────────
    .slide(
        CodeWalkthroughSlide(
            title="Five lines to a deck",
            code=CodeBlock(
                language="python",
                filename="quickstart.py",
                highlight=[3, 4, 5],
                code=(
                    "from decko_py import DeckBuilder, TitleSlide\n"
                    "\n"
                    "html = (\n"
                    '    DeckBuilder().meta("Launch Deck")\n'
                    '    .theme("midnight")\n'
                    '    .slide(TitleSlide(headline="Hello, World!"))\n'
                    "    .render_html()\n"
                    ")"
                ),
            ),
            annotation=CalloutBlock(
                display="success",
                title="String coercion",
                body='headline="Hello, World!" auto-wraps to TextBlock.',
            ),
        )
    )
    # ── 25. ARCHITECTURE DIAGRAM ────────────────────────────────────────────────
    .slide(
        ArchitectureDiagramSlide(
            title="Decko rendering pipeline",
            diagram=MediaBlock(src=IMG_DIAGRAM, alt="Rendering pipeline diagram"),
            diagram_notes=ListBlock(
                display="bullets",
                items=[
                    ListItem(text="Pydantic models → JSON deck payload"),
                    ListItem(text="HtmlRenderer injects payload into HTML shell"),
                    ListItem(text="CDN runtime hydrates slides client-side"),
                ],
            ),
        )
    )
    # ── 26. TERMINAL ────────────────────────────────────────────────────────────
    .slide(
        TerminalSlide(
            title="Install and run",
            code=CodeBlock(
                display="block",
                language="bash",
                code=(
                    "$ pip install decko-py\n"
                    "$ python examples/comprehensive_deck.py\n"
                    "Saved → comprehensive_deck.html\n"
                    "\n"
                    "$ open comprehensive_deck.html"
                ),
            ),
        )
    )
    # ── 27. CUSTOM: TESTIMONIAL GRID ────────────────────────────────────────────
    .slide(
        TestimonialGridSlide(
            title="What teams are saying",
            testimonial_1="Replaced our entire slide pipeline. "
            "Decks now ship with the weekly report. — Data team, fintech",
            testimonial_2="The typed API caught a layout bug before the demo. "
            "Saved us. — Engineer, startup",
            testimonial_3="Our AI agent generates full decks from meeting notes. "
            "Decko made it trivial. — Product team",
        )
    )
    # ── 28. CUSTOM: TIMELINE ────────────────────────────────────────────────────
    .slide(
        TimelineSlide(
            title="Getting started in 4 steps",
            step_1=CalloutBlock(
                display="info",
                title="1. Install",
                body="pip install decko-py",
            ),
            step_2=CalloutBlock(
                display="info",
                title="2. Build",
                body="DeckBuilder().slide(TitleSlide(headline='Hi')).build()",
            ),
            step_3=CalloutBlock(
                display="success",
                title="3. Render",
                body=".render_html() or .save('deck.html')",
            ),
            step_4=CalloutBlock(
                display="warning",
                title="4. Validate",
                body="Content budgets enforced automatically on build()",
            ),
        )
    )
    # ── 29. CLOSING ─────────────────────────────────────────────────────────────
    .slide(
        ClosingSlide(
            headline="Start building with Decko",
            cta="pip install decko-py",
            contact=ListBlock(
                display="bullets",
                items=[
                    ListItem(text="github.com/rchrdcrngl/decko_python"),
                    ListItem(text="PyPI: decko-py"),
                ],
            ),
            ambient=SlideAmbient(type="particles", intensity="low"),
            transition=FadeTransition(duration=0.8),
            notes="End on a clear CTA. Leave PyPI install command visible.",
        )
    )
    .render_html(registry=registry)
)

CUSTOM_CSS = """
  <style>
    /* testimonial-grid: three-column testimonial layout */
    [data-template="testimonial-grid"] [data-slot] {
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 2rem;
    }
    [data-template="testimonial-grid"] [data-slot="testimonial-1"],
    [data-template="testimonial-grid"] [data-slot="testimonial-2"],
    [data-template="testimonial-grid"] [data-slot="testimonial-3"] {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 0.75rem;
      padding: 1.5rem;
      font-style: italic;
    }

    /* timeline: horizontal stepped layout */
    [data-template="timeline"] [data-slot^="step-"] {
      display: flex;
      flex-direction: row;
      align-items: flex-start;
      gap: 0.75rem;
    }
    [data-template="timeline"] {
      display: grid;
      grid-template-rows: auto 1fr;
      gap: 2rem;
    }
  </style>"""

deck_html = deck_html.replace("</head>", CUSTOM_CSS + "\n</head>", 1)

output = "comprehensive_deck.html"
with open(output, "w", encoding="utf-8") as f:
    f.write(deck_html)

print(f"Saved → {output}")
print("Slides: 29 (23 built-in templates + 2 custom + section breaks)")
