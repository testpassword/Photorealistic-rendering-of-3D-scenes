# Лабораторная №1: Рендеринг с картами освещённости #

***Исходные материалы и оборудование:***

Компьютер с установленным комплексом программ компьютерной графики и оптического моделирования Lumicept.

***Цель работы:***

Овладеть навыками фотореалистичной визуализации трехмерных сцен с использованием карт освещенности.

***Задачи:***

- Импортировать сцену (Cornel Box).
- Заменить источник света на точечный.
- Выполнить расчет карт освещенности.
- Выполнить рендеринг с учетом рассчитанных карт освещенности.
- Назначить на источник полусферическую диаграмму излучения, направленную вниз и повторить расчет карт освещенности и рендеринг.
- Изменить разбивку геометрии сцены на большее количество треугольников и повторить расчет карт освещенности и рендеринг.
- Сравнить полученные в результате рендеринга изображения (NIT-файлы).
- Назначить в качестве свойств стен узкую ДФО, провести расчет карт освещенности и рендеринг и сравнить с результатом рендеринга методом трассировки пути.
- Сделать выводы о полученных результатах и причинах различия в изображениях.

Отчет представить в электронном виде: Формат MS Word или MS PowerPoint, эскиз схемы с указанием заданных параметров. Для подготовки эскиза можно использовать скриншоты из Lumicept. Записать финальную сцену. К отчету приложить файлы скриптов (`*.py`), (`*.iof`) и результатов визуализации (NIT-файлы).

# Лабораторная №2: Моделирование двумерного распределения яркости на базе прямой трассировки лучей методом Монте-Карло. #

***Исходные данные:***

Компьютер с установленным комплексом программ компьютерной графики и оптического моделирования Lumicept.

***Цель работы:***

Овладеть навыками фотореалистичной визуализации трехмерных сцен с использованием прямой трассировки лучей методом Монте-Карло и моделей плоских фотоприемников на базе комплекса программ Lumicept.

***Задачи:***

- Импортировать сцену (“initial.iof”).
- Настроить параметры камеры.
- Для всех объектов сцены назначить значения яркости, отличные от значений, представленных в примере (“initial.iof”).
- Добавить в сцену модель фотоприемника “plane observer” и настроить ее параметры
- Добавить в сцену модель линзового фотоприемника “lens observer” и настроить ее параметры
- Произвести автоматический расчет двумерного распределения яркости с помощью инструмента “Illumination map calculation”.
- Визуализировать результаты расчета двумерного распределения яркости с помощью LumiVue
- Повторить расчет для модели фотоприемника “plane observer” с увеличенным конусом интегрирования (10, 30, 60 и 90 градусов) и визуализировать результаты с помощью LumiVue.
- Сделать выводы

Отчет представить в электронном виде: Формат MS Word или MS PowerPoint, эскиз схемы с указанием заданных параметров. Для подготовки эскиза можно использовать скриншоты из Lumicept. Записать финальные сцены. К отчету приложить файлы скриптов (`*.py`), сцен (`*.iof`), HDRI (`*.nit`).

# Лабораторная №3, 4, 5: Рендеринг с использованием двунаправленной стохастической трассировки лучей. Трассировка пути без фотонов вторичного освещения. #
Лабораторные работы №3, №4 и №5 имеют общее название "Рендеринг с использованием двунаправленной стохастической трассировки лучей с использованием комплекса программ Lumicept". Существует несколько вариантов такого рендеринга, отличающихся качеством генерируемого изображения, которые объединены в Lumicept под общим названием “Rendering with Path Tracing”. Варианты отличаются глубиной интеграции прямого и каустического освещения на диффузном пути луча, трассируемого из камеры.
Условные названия вариантов: `Path Tracer`, `Low frequency noise`, `High frequency noise`, `Adaptive` и `Multiple`. Лабораторные работы с третьей по пятую связаны с освоением одного или нескольких отдельных вариантов такого типа рендеринга.

***Исходные данные:***

Компьютер с установленным комплексом программ компьютерной графики и оптического моделирования Lumicept.

***Цель работы:***

овладеть навыками фотореалистичной визуализации трехмерных сцен с использованием двунаправленной стохастической трассировки лучей на базе комплекса программ Lumicept в режиме “Path Tracer”, обеспечивающем трассировку пути без фотонов вторичного освещения.

***Задачи:***

- Изучить возможные параметры трассировки лучей в режиме рендеринга с
двунаправленной стохастической трассировкой лучей `Rendering with Path
Tracing`.
- Расширить сцену Cornel Box зеркально отражающими сферами.
- Провести моделирование изображения сцены в режиме `Path Tracer` для
точечного источника света. Исследовать влияние размера диффузного экрана
(сферы) на визуализацию сцены.
- Визуализировать отдельные компоненты глобального освещения (источники, прямое, вторичное и каустическое освещение).
- Провести моделирование изображения сцены в режиме `Path Tracer` для протяженного источника света. Исследовать влияние диаграммы направленности излучения источника на его визуализацию в сцене.
- Модифицировать сцену для прямого освещения объектов дневным светом. Назначить на поверхности сфер отражающие свойства в виде узкой
двунаправленной функции отражения.
- Провести моделирование визуализации сцены с учетом выборки по значимости (`BDF sampling`) двунаправленной функции отражения и без ее учета. Сравнить результаты.
- Модифицировать сцену Cornel Box для освещения солнечным светом через
окно.
- Провести моделирование визуализации сцены для трех возможных вариантов
расчета вторичного освещения (Light optimization): `Off`, `Windows` и
`Automatic`. Сравнить результаты.

Отчет представить в электронном виде: Формат MS Word или MS PowerPoint, эскиз схемы с указанием заданных параметров. Для подготовки эскиза можно
использовать скриншоты из Lumicept. К отчету приложить файлы скриптов (`*.py`), сцен (`*.iof`) и результатов визуализации (NIT-файлы).
