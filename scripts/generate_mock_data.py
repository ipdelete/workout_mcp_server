#!/usr/bin/env python3
"""Generate mock cycling workout data for development and testing."""

import json
import random
import uuid
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


def calculate_tss(
    duration_minutes: int, avg_power_watts: int, workout_type: str
) -> int:
    """Calculate Training Stress Score based on duration, power, and workout type.

    TSS = (duration * NP * IF) / (FTP * 3600) * 100
    Simplified for mock data generation.
    """
    base_tss = (duration_minutes * avg_power_watts) / 200

    type_multipliers = {
        "recovery": 0.4,
        "endurance": 0.6,
        "tempo": 0.8,
        "threshold": 1.0,
        "interval": 1.2,
        "race": 1.3,
    }

    multiplier = type_multipliers.get(workout_type, 0.6)
    tss = int(base_tss * multiplier)

    return max(20, min(150, tss))


def generate_workout(date: date, workout_pattern: str) -> dict[str, Any]:
    """Generate a single workout entry with realistic values."""
    workout_types = ["recovery", "endurance", "tempo", "threshold", "interval", "race"]

    if workout_pattern == "rest":
        return None

    if workout_pattern == "recovery_week":
        workout_type = random.choice(["recovery", "endurance"])
        duration_range = (30, 90)
        power_range = (100, 180)
    elif workout_pattern == "build":
        workout_type = random.choice(["endurance", "tempo", "threshold"])
        duration_range = (60, 180)
        power_range = (150, 250)
    elif workout_pattern == "intensity":
        workout_type = random.choice(["threshold", "interval", "race"])
        duration_range = (45, 120)
        power_range = (200, 300)
    else:
        workout_type = random.choice(workout_types)
        duration_range = (30, 180)
        power_range = (100, 300)

    duration_minutes = random.randint(*duration_range)
    avg_power_watts = random.randint(*power_range)

    avg_speed_kmh = 20 + (avg_power_watts - 150) / 10 + random.uniform(-3, 3)
    distance_km = round((duration_minutes / 60) * avg_speed_kmh, 1)

    tss = calculate_tss(duration_minutes, avg_power_watts, workout_type)

    return {
        "id": str(uuid.uuid4()),
        "date": date.strftime("%Y-%m-%d"),
        "duration_minutes": duration_minutes,
        "distance_km": distance_km,
        "avg_power_watts": avg_power_watts,
        "tss": tss,
        "workout_type": workout_type,
    }


def generate_training_plan(start_date: date, num_days: int) -> list[str]:
    """Generate a realistic training pattern over the specified period."""
    pattern = []

    for week in range(num_days // 7 + 1):
        week_number = week % 4

        if week_number == 3:
            weekly_pattern = ["recovery_week"] * 4 + ["rest"] * 3
        elif week_number == 2:
            weekly_pattern = [
                "intensity",
                "recovery_week",
                "build",
                "intensity",
                "rest",
                "build",
                "rest",
            ]
        else:
            weekly_pattern = [
                "build",
                "recovery_week",
                "build",
                "intensity",
                "rest",
                "build",
                "recovery_week",
            ]

        pattern.extend(weekly_pattern)

    return pattern[:num_days]


def generate_mock_workouts(num_workouts: int = 50) -> list[dict[str, Any]]:
    """Generate specified number of mock workout entries over ~3 months."""
    random.seed(42)

    days_span = 90
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_span)

    training_pattern = generate_training_plan(start_date, days_span)

    workouts = []
    current_date = start_date
    workout_count = 0
    day_index = 0

    while workout_count < num_workouts and day_index < len(training_pattern):
        pattern = training_pattern[day_index]

        if pattern != "rest" and workout_count < num_workouts:
            workout = generate_workout(current_date, pattern)
            if workout:
                workouts.append(workout)
                workout_count += 1

        current_date += timedelta(days=1)
        day_index += 1

    while workout_count < num_workouts:
        pattern = random.choice(["build", "recovery_week", "intensity"])
        workout = generate_workout(current_date, pattern)
        if workout:
            workouts.append(workout)
            workout_count += 1
        current_date += timedelta(days=1)

    return workouts


def main():
    """Generate mock workout data and save to JSON file."""
    output_dir = Path(__file__).parent.parent / "data_store"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "workouts.json"

    print("Generating 50 mock cycling workouts...")
    workouts = generate_mock_workouts(50)

    with open(output_file, "w") as f:
        json.dump(workouts, f, indent=2)

    print(f"✓ Generated {len(workouts)} workouts")
    print(f"✓ Data saved to {output_file}")

    workout_types = {}
    total_tss = 0
    for workout in workouts:
        workout_type = workout["workout_type"]
        workout_types[workout_type] = workout_types.get(workout_type, 0) + 1
        total_tss += workout["tss"]

    print("\nWorkout type distribution:")
    for wtype, count in sorted(workout_types.items()):
        print(f"  - {wtype}: {count}")

    print(f"\nAverage TSS: {total_tss / len(workouts):.1f}")
    print(f"Date range: {workouts[0]['date']} to {workouts[-1]['date']}")


if __name__ == "__main__":
    main()
