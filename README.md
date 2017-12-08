<center>
# Sberbank Data Science Contest 2017: Problem A
<img src="img/task_a.png" width=400px; height=400px>
</center>
<h4 align='right'>
Автор решения: Александр Желубенков (topspin26), 1 место.
</h4>

## Данные:

Специально для данного соревнования был собран первый в своем роде набор данных для вопрос-ответных систем на русском языке. Данные были собраны из русскоязычных статей, лежащих в открытом доступе. Совместными усилиями более тысячи человек удалось собрать 100 543 пары вопросов и ответов по 18 334 уникальным параграфам.

В двух представленных нами задачах мы предоставим участникам 50 365 пар вопросов и ответов с их параграфами для анализа и построения моделей. Оставшиеся пары вопросов и ответов будут скрыты и использоваться в качестве тестовых множеств двух задач.

## Задача А: определение релевантности вопроса

Необходимо построить алгоритм, определяющий релевантность поставленных вопросов к параграфу текста. Для решения этой задачи требуется не только понимать, относится ли вопрос к параграфу, но и насколько корректно он поставлен.

Это задача бинарной классификации, в которой целевая переменная target принимает два значения: 0 и 1.<br> Класс 1 - релевантные вопросы, заданные к параграфу человеком.<br> Класс 0 - вопросы, либо заданные человеком к другим параграфам, либо были составлены компьютером.

#### Метрика: ROC-AUC

#### Данные для задачи A:

Тренировочные: 119 399 пар вопросов и параграфов train_taskA.csv, имеющие вид: paragraph_id, question_id, paragraph, question, target.<br>Тестовые:  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 74 295 пар вопросов и параграфов &nbsp;test_taskA.csv, имеющие вид: paragraph_id, question_id, paragraph, question.

В предоставленных тренировочных и тестовых данных релевантные вопросы класса 1 были случайно выбраны из собранных вопросов и ответов. Нерелевантные примеры класса 0, составленные человеком, были получены случайным выбором вопроса к другому параграфу по той же теме. Нерелевантные вопросы класса 0, заданные компьютером, в тренировочных данных отсутствуют.

## Краткое описание решения

Обучение - две модели(xgb):
1. для отделения единичек (положительных примеров из train выборки) от всего остального (т.е. нулей из train и всей test выборки),<br> **цель - научиться отделять релевантные пары (параграф, вопрос) от нерелевантных пар и пар с синтетическими вопросами**;
2. для отделения train выборки от всей test выборки,<br> **цель - научиться отделять нормальные пары(с человеческими вопросами) от пар с синтетическими вопросами**;

Т.е. обучаем обе модели на зашумленной разметке, т.к. пары из тестовой выборки при обучении используются в качестве негативных примеров. <br>
Для получения предсказаний обеих моделей на test выборке делаем это с разбиением test-а на 5 фолдов (при этом обучаем модели 1) и 2) без того фолда, на котором хотим получить предсказания).<br>
**Финальное предсказание - произведение выходов из моделей 1) и 2).**

Факторы (~1800 начальных факторов и ~350 факторов, использующихся в итоговой модели):
- NLP-факторы для вопроса, для пары (параграф, вопрос);
- Ранг _(по всем возможным парам вопрос-параграф)_ вопроса для параграфа по "схожести вопроса параграфу" (это один из факторов для пары (параграф, вопрос)), max-значение "схожести" вопроса по всем параграфам;
- Особенности синтетических вопросов: 
  - не встречаются более одного раза;
  - в них очень редко встречаются слова с большой буквы(они могут стоять только в начале вопроса);
  - в них часто встречаются повторы (слов, словосочетаний);
  - в них могут повторяться одинаковые достаточно длинные куски нормальных вопросов;
  - в них часто присутствуют слова из слабо-связанных тем;
  - в них часто присутствуют грамматические ошибки.

**Итоговая модель** - усреднение рангов финальных предсказаний 5 моделей по различным разбиениям test-а на фолды.

### Этапы

* Этап 0. Чтение и подготовка данных
* Этап 1. Построение факторов для вопроса
* Этап 2. Исправление опечаток в вопросе
* Этап 3. Построение факторов для пары параграф-вопрос
* Этап 4. Построение факторов для параграфа
* Этап 5. Обучение моделей
* Этап 6. Анализ предсказаний

Этапы 0-4 здесь: [a_winner_feature_engineering.ipynb](a_winner_feature_engineering.ipynb)<br>
Этапы 5-6 здесь: [a_winner_models.ipynb](a_winner_models.ipynb)

### Технические детали

Основные используемые библиотеки:
* pymystem3
* pandas
* numpy
* scipy
* sklearn
* xgboost

Дополнительные библиотеки:
* [LanguageTool](http://wiki.languagetool.org/)

Внешние данные:

* [CoNLL Embeddings](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-1989)

Железо: 
* Intel "Core-i7-7700K", 32GB RAM


