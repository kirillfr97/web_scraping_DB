from typing import Dict, List

from pandas import DataFrame

from web_scraping.utils import DataFields


def create_message(data: DataFrame) -> str:
    """Creates message containing information about documents in the table."""
    return ''.join(f'\"{row[DataFields.Title]}\": {row[DataFields.Link]}\n' for _, row in data.iterrows())


def create_summary(summary: Dict[str, List[int]]) -> str:
    """Creates summary-message containing information about totals and quantity of scraped webpages."""
    # Count totals
    total_new = str(sum([val[0] for val in summary.values()]))
    total_parsed = str(sum([val[1] for val in summary.values()]))
    total_time = sum([val[2] for val in summary.values()])

    # Construct messages
    article_totals = ''.join(
        [f'{"- `" + name + "`":<30} {str(val[0]) + " / " + str(val[1]):<15} {val[2]:.1f}\n' for name, val in summary.items()]
    )

    return f'{"Total":<30} {total_new + " / " + total_parsed:<15} {total_time:.1f}\n{article_totals}'
