import pandas as pd

import pricing
from pricing.scorer.v0.sample import trip1_dict
from pricing.scorer.v0.trip.constants import (
    ACCELERATION_GFORCE_MIN,
    ACCELERATION_ROLLING,
)


def test_clean_trip():
    # import into df
    df = pd.DataFrame(trip1_dict.get("coordinates"))
    df = pricing.scorer.trip.clean(df)
    assert len(df) >= 200

    # Recompute speed
    speed = pricing.scorer.trip.compute_speed(df)
    assert speed.mean() >= 20.0

    # Get events
    df["acceleration_index"] = pricing.scorer.trip.index_accelerations(
        df.g_force,
        g_force_threshold=ACCELERATION_GFORCE_MIN,
        rolling=ACCELERATION_ROLLING,
    )
    assert df.acceleration_index.max() == 6
    df["deceleration_index"] = pricing.scorer.trip.index_accelerations(
        df.g_force,
        g_force_threshold=ACCELERATION_GFORCE_MIN,
        rolling=ACCELERATION_ROLLING,
        positive=False,
    )
    assert df.deceleration_index.max() == 6

    # Get intensities
    df = pricing.scorer.trip.events.acceleration_intensity(df)
    n_hash_accelerations = (
        df.groupby("acceleration_index").acceleration_intensity.max() > 0.3
    ).sum()
    assert n_hash_accelerations == 1

    df = pricing.scorer.trip.events.deceleration_intensity(df)
    n_soft_decelerations = (
        df.groupby("deceleration_index").deceleration_intensity.max() > -0.3
    ).sum()
    assert n_soft_decelerations == 6
