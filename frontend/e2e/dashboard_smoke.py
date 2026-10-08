"""Smoke-test the dashboard's critical loading, success, and error states."""

from playwright.sync_api import Page, sync_playwright


VALID_METRICS = [
    {
        "create_date": "2024-01-10",
        "amount": 1000,
        "operation_type": "income",
        "category": "sales",
        "business_type": "B2B",
    },
    {
        "create_date": "2024-01-15",
        "amount": 250,
        "operation_type": "outcome",
        "category": "suppliers",
        "business_type": "B2B",
    },
    {
        "create_date": "2024-02-01",
        "amount": 500,
        "operation_type": "income",
        "category": "sales",
        "business_type": "B2C",
    },
]


def fulfill_metrics(page: Page) -> None:
    page.route("**/api/metrics", lambda route: route.fulfill(json=VALID_METRICS))


def test_dashboard_success(page: Page) -> None:
    """The dashboard renders KPIs and both charts after a successful API call."""
    fulfill_metrics(page)
    page.goto("http://localhost:5173")
    page.wait_for_load_state("networkidle")

    page.get_by_role("heading", name="Financial Overview").wait_for()
    page.get_by_text("Total Income").wait_for()
    page.get_by_text("$1,500").wait_for()
    page.get_by_role("figure", name="Income vs. Outcome").wait_for()
    page.get_by_role("figure", name="Profit Margin %").wait_for()

    assert page.get_by_role("status").count() == 0
    assert page.get_by_role("alert").count() == 0


def test_dashboard_error_state(page: Page) -> None:
    """A failed metrics request exposes the error message accessibly."""
    page.route(
        "**/api/metrics",
        lambda route: route.fulfill(status=503, body="Service unavailable"),
    )
    page.goto("http://localhost:5173")
    page.wait_for_load_state("networkidle")

    alert = page.get_by_role("alert")
    alert.wait_for()
    assert "No se pudo cargar" in alert.inner_text()
    assert page.get_by_role("status").count() == 0


def main() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_dashboard_success(page)
            page = browser.new_page()
            test_dashboard_error_state(page)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
    print("Dashboard smoke tests passed")
