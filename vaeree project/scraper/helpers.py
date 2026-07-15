from playwright.sync_api import Page


def safe_text(locator):
    """
    Safely get text from a locator.
    Returns an empty string if not found.
    """

    try:
        if locator.count() > 0:
            return locator.first.inner_text().strip()
    except:
        pass

    return ""


def get_detail(page: Page, label: str):
    """
    Reads details like:
    Material -> Metal
    Color -> Black
    Space -> Bathroom
    """

    try:

        labels = page.locator("p")

        for i in range(labels.count()):

            if labels.nth(i).inner_text().strip() == label:

                return labels.nth(i).locator(
                    "xpath=following-sibling::span[1]"
                ).inner_text().strip()

    except:
        pass

    return ""


def get_seller(page: Page):

    try:

        labels = page.locator("p")

        for i in range(labels.count()):

            if labels.nth(i).inner_text().strip() == "Seller Name":

                return labels.nth(i).locator(
                    "xpath=following-sibling::p[1]"
                ).inner_text().strip()

    except:
        pass

    return ""