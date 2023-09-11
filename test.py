import pytest

import tracker


@pytest.mark.parametrize(
    'input_data, expected',
    [
        (
            ['SWM', [720, 1, 80, 25, 40]],
            (
                'Тип тренировки: Swimming; '
                'Длительность: 1.000 ч.; '
                'Дистанция: 0.994 км; '
                'Ср. скорость: 1.000 км/ч; '
                'Потрачено ккал: 336.000.'
            ),
        ),
        (
            ['RUN', [1206, 12, 6]],
            (
                'Тип тренировки: Running; '
                'Длительность: 12.000 ч.; '
                'Дистанция: 0.784 км; '
                'Ср. скорость: 0.065 км/ч; '
                'Потрачено ккал: 12.812.'
            ),
        ),
        (
            ['WLK', [9000, 1, 75, 180]],
            (
                'Тип тренировки: SportsWalking; '
                'Длительность: 1.000 ч.; '
                'Дистанция: 5.850 км; '
                'Ср. скорость: 5.850 км/ч; '
                'Потрачено ккал: 349.252.'
            ),
        ),
    ],
)
def test_read_package(input_data, expected):
    assert (
        tracker.read_package(*input_data).show_training_info().get_message()
        == expected
    )
