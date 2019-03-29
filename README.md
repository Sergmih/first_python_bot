<h2>Валютный бот</h2>

Простенький бот написанный на питоне, который умеет выдавать курс валюты и строить график изменения курса в течении указанного периода.

<h2>Команды:</h2><br>
<b>/get</b> - Выведет список доступных валют, количество единиц, в котором они измеряются и полное название на русском языке<br>
<b>/get currency</b> - выведет текущий курс валюты "curency" (Например <b>/get usd</b>)<br>
<b>/statistic currency</b> <b><i>(from YYYY.MM.DD)</i></b> <b><i>(to YYYY.MM.DD)</i></b> - Построит график указанной валюты начиная с from и заканчивая to датами. Даты from и to являются необязательными аргументами. В случае отсутствия даты from будет использоваться дата по умочанию 2018.01.01. В случае отсутствия даты to будет использоваться сегодняшняя дата. В случае некорректных дат - поведение неопределно и возможны ошибки. 

***
Опробовать бота можно, найдя его по имени: <b>@mikser-test-bot</b><br>
Но его работоспособность не гарантируется из-за использования беслатного сервера, который может быть нестабильным.
