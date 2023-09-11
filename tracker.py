from dataclasses import dataclass
from typing import Sequence


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить информационное сообщение.

        Возвращает:
            Данные о типе тренировки, ее продолжительности, пройденном
            расстоянии, средней скорости и сожженных калориях.
        """
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class InvalidTrainingDataError(Exception):
    """Кастомный обработчик ошибок функции read_package."""

    def __init__(self, error, workout_type: str) -> None:
        if isinstance(error, TypeError):
            self.message = (
                f'Неверное кол-во аргументов для тренировки: {workout_type}'
            )
        else:
            self.message = f'Невалидный код тренировки: {workout_type}'
        super().__init__(self.message)


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # Длина шага по умолчанию.
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить пройденную дистанцию в км.

        Возвращает:
            Пройденная дистанция в км.
        """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость в км/ч.

        Возвращает:
            Средняя скорость км/ч.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество сожженных калорий за тренировку.

        Поднимает:
            NotImplementedError: вызывает исключение, если данный метод
                вызывается из базового класса Training.
        """
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Получить информацию о тренировке.

        Возвращает:
            Объект класса InfoMessage.
        """
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тип тренировки: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество сожженных калорий за пробежку.

        Возвращает:
            Количество сожженных калорий.
        """
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тип тренировки: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278  # км/ч в м/с.
    CM_IN_M = 100  # кол-во сантиметров в метре.

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество сожженных калорий за сессию спортивной ходьбы.

        Returns:
            Количество сожженных калорий.
        """
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    """Тип тренировки: плаванье."""

    LEN_STEP = 1.38  # Длина гребка.
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость за заплыв в км/ч.

        Возвращает:
            Средняя скорость.
        """
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество сожженных калорий за заплыв.

        Возвращает:
            Количество сожженных калорий.
        """
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight
            * self.duration
        )


WORKOUTS = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: Sequence[float]) -> Training:
    """Получить данные с датчиков.

    Аргументы:
        workout_type (str): Кодовое имя тренировки.
        data (list): Цифровые показатели датчиков.

    Возвращает:
        Объект класса Training.

    Поднимает:
        TypeError: вызывает исключение, если код. имя тренировки некорректно.
        KeyError: вызывает исключение, количество указанных аргументов не
            соответствует типу тренировки.
    """
    try:
        return WORKOUTS[workout_type](*data)
    except (TypeError, KeyError) as err:
        raise InvalidTrainingDataError(err, workout_type)


def main(training: Training) -> None:
    """Главная функция.

    Аргументы:
        training (Training): Объект класса Training.
    """
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
