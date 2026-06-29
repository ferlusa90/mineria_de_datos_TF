import html
import base64
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
HERO_IMAGE = ROOT / "app" / "assets" / "streaming-data-mining-hero.png"


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --tf-bg: #f6f8fb;
            --tf-surface: #ffffff;
            --tf-surface-strong: #eef4f7;
            --tf-ink: #15202b;
            --tf-muted: #5d6b78;
            --tf-border: #dce5eb;
            --tf-teal: #0f766e;
            --tf-coral: #e56b55;
            --tf-gold: #b5812a;
        }

        .stApp {
            background: var(--tf-bg);
        }

        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 3.2rem;
            max-width: 1180px;
        }

        h1, h2, h3 {
            color: var(--tf-ink);
            letter-spacing: 0;
        }

        p, li, .stMarkdown {
            color: var(--tf-muted);
        }

        div[data-testid="stMetric"] {
            background: var(--tf-surface);
            border: 1px solid var(--tf-border);
            border-radius: 8px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 26px rgba(21, 32, 43, 0.06);
        }

        div[data-testid="stMetricLabel"] p {
            color: var(--tf-muted);
            font-size: 0.86rem;
        }

        div[data-testid="stMetricValue"] {
            color: var(--tf-ink);
        }

        .tf-hero {
            background: var(--tf-surface);
            border: 1px solid var(--tf-border);
            border-radius: 8px;
            padding: 1.15rem;
            box-shadow: 0 18px 40px rgba(21, 32, 43, 0.08);
        }

        .tf-hero img {
            width: 100%;
            max-height: 430px;
            object-fit: cover;
            border-radius: 7px;
            display: block;
        }

        .tf-card {
            background: var(--tf-surface);
            border: 1px solid var(--tf-border);
            border-radius: 8px;
            padding: 1.1rem 1.15rem;
            height: 100%;
            box-shadow: 0 10px 26px rgba(21, 32, 43, 0.06);
        }

        .tf-card--soft {
            background: linear-gradient(180deg, #ffffff 0%, var(--tf-surface-strong) 100%);
        }

        .tf-kicker {
            color: var(--tf-teal);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            margin-bottom: 0.45rem;
            text-transform: uppercase;
        }

        .tf-card h3 {
            color: var(--tf-ink);
            font-size: 1.05rem;
            line-height: 1.25;
            margin: 0 0 0.5rem;
        }

        .tf-card p {
            color: var(--tf-muted);
            font-size: 0.96rem;
            line-height: 1.58;
            margin: 0;
        }

        .tf-badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.9rem;
        }

        .tf-badge {
            background: #eef7f6;
            border: 1px solid #cfe5e2;
            border-radius: 999px;
            color: #145f59;
            font-size: 0.82rem;
            font-weight: 700;
            padding: 0.28rem 0.65rem;
        }

        .tf-accent {
            border-left: 4px solid var(--tf-coral);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--tf-surface);
            border-color: var(--tf-border);
            box-shadow: 0 10px 24px rgba(21, 32, 43, 0.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str, kicker: str | None = None, soft: bool = False) -> None:
    classes = "tf-card tf-card--soft" if soft else "tf-card"
    kicker_html = f'<div class="tf-kicker">{html.escape(kicker)}</div>' if kicker else ""
    st.markdown(
        f"""
        <div class="{classes}">
            {kicker_html}
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def callout(title: str, body: str, kicker: str | None = None) -> None:
    kicker_html = f'<div class="tf-kicker">{html.escape(kicker)}</div>' if kicker else ""
    st.markdown(
        f"""
        <div class="tf-card tf-card--soft tf-accent">
            {kicker_html}
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badges(items: list[str]) -> None:
    badges_html = "".join(f'<span class="tf-badge">{html.escape(item)}</span>' for item in items)
    st.markdown(f'<div class="tf-badge-row">{badges_html}</div>', unsafe_allow_html=True)


def hero_image(path: Path = HERO_IMAGE, alt: str = "Panel de mineria de datos") -> None:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    st.markdown(
        f"""
        <div class="tf-hero">
            <img src="data:image/png;base64,{encoded}" alt="{html.escape(alt)}" />
        </div>
        """,
        unsafe_allow_html=True,
    )
