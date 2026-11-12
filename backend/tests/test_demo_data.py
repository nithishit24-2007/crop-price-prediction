from io import StringIO

import pytest
from django.core.management import call_command

from apps.agriculture.models import Crop, HistoricalMarketPrice, Market


@pytest.mark.django_db
def test_demo_loader_populates_every_crop_market_pair_with_ascii_output():
    output = StringIO()
    call_command('load_demo_data', days=1, stdout=output)

    assert Crop.objects.count() == 10
    assert Market.objects.count() == 8
    assert HistoricalMarketPrice.objects.filter(is_demo_data=True).count() == 80
    assert (
        HistoricalMarketPrice.objects.filter(is_demo_data=True)
        .values('crop_id', 'market_id')
        .distinct()
        .count()
        == 80
    )
    assert output.getvalue().isascii()
