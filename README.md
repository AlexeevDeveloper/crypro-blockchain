<p align="center">Open-Source блокчейн на Python</p>
<p align='center'>
	<img src="./extra/cryprocoin.png">
</p>
<br>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/AlexeevDeveloper/crypro-blockchain?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/count/AlexeevDeveloper/crypro-blockchain?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/AlexeevDeveloper/crypro-blockchain?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/AlexeevDeveloper/crypro-blockchain?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/AlexeevDeveloper/crypro-blockchain?style=for-the-badge">
    </br>
</p>

> **CryProN** - это невероятно быстрый, защищенный и простой Open Source блокчейн. 

CryProN (крайпрон) демонстрирует основные концепции технологии блокчейна, такие как транзакции, экономические модели, блоки, кошельки, механизмы консенсуса и многое другое.

> [!CAUTION]
> **CryProN** только начинает развиваться, и в данный момент - это всего лишь простая реализация блокчейна.

> [!CAUTION]
> В данный момент, CryProN находится в активной стадии разработки и крайне **не рекомендуется для использования**. Следите за новостями в [нашем телеграме](https://t.me/crypro_N)!

## Контакты и поддержка
Если у вас остались вопросы по использованию, создайте [issue](https://github.com/AlexeevDeveloper/crypro-blockchain/issues/new) или напишите мне на почту alexeev.dev@main.ru.

Вы также может написать мне в телеграм: [@alexeev_dev](https://t.me/alexeev_dev)

CryProN - это Open Source проект, он живет только благодаря вашей поддержке!

Релизы проекта можно получить по [этой ссылке](https://github.com/AlexeevDeveloper/crypro-blockchain/releases).

## Требования
Для установки вам нужно будет удолетворить следующие требования:

 + Python 3.7 или выше
 + Библиотека ecdsa

## Установка
Если вы хотите установить стабильную версию, то перейдите на [страницу релизов](https://github.com/AlexeevDeveloper/crypro-blockchain/releases). Но если вы хотите установить последнюю версию:

1. Клонирование репозитория

```bash
git clone https://github.com/AlexeevDeveloper/crypro-blockchain.git
cd crypro-blockchain
```

2. Создайте рабочее виртуальное окружение и установите зависимости

> [!NOTE]
> Если ваш shell - fish, вместо `source venv/bin/activate` используйте `source venv/bin/activate.fish`.

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Готово! 💪 🎉  Вы готовы использовать CryProN!

## Функционал
Здесь вы можете увидеть, что уже реализовано, а что только планируется:

 - [x] Кошельки. Генерация и управление кошельками пользователей с парами закрытый/открытый ключ.
 - [x] Транзакции. Создание, подписание и верификация транзакций между кошельками.
 - [x] Блоки. Добыча новых блоков и добавление их в блокчейн.
 - [x] Механизм консенсуса Proof of Work. Это алгоритм, в котором участники сети соревнуются в решении вычислительно-сложной задачи.
 - [x] Использование проверенных криптографических алгоритмов (ECDSA) для обеспечения безопасности
 - [x] Логгирование
 - [x] Простая конфигурация блокчейна
 - [x] Модульная структура, следование принципам SOLID, DRY, KISS и другим.
 - [x] Объектно-ориентированный код
 - [x] Базовый механизм вознаграждения за добычу блоков
 - [x] Базовый механизм рассчета остатка невыпущенных монет в сети
 - [x] Модель комиссии за транзакции
 - [x] Экономическая модель инфляции
 - [x] Установка и управление общим предложением токенов
 - [x] Улучшенная модель динамического управления инфляцией
 - [ ] Механизм консенсуса Proof of Stake (PoS)
 - [ ] Более гибкая система вознаграждения валидаторов
 - [ ] Добавление возможности динамического обновления экономических параметров
 - [ ] Реализация механизмов защиты от DoS атак, атак 51%.
 - [ ] Добавление возможности делегирования стейка (PoS delegated)
 - [ ] Интеграция с внешними сервисами аутенфикации
 - [ ] Повышение масштабируемости
 - [ ] Оптимизация алгоритмов
 - [ ] Использование базы данных или другого распредленного хранилища для данных блокчейна
 - [ ] Улучшение безопасности и отказоустойчивости путем улучшенной обработки исключений
 - [ ] Внедрение модульных и интеграционных тестов
 - [ ] Внедрение дополнительных механизмов безопасности
 - [ ] Добавление поддержки смарт-контрактов
 - [ ] Механизмы консенсуса PBFT, Federated Byzantine Agreement и другие
 - [ ] API для взаимодейтсвия с блокчейном
 - [ ] Интеграция блокчейна в другие сервисы

## Лицензия
Copyright © 2024 Alexeev Bronislav. All rights reversed.

CryPro-N Coin BlockChain
Невероятно быстрый, защищенный и простой Open Source блокчейн. 

CryProN (крайпрон) демонстрирует основные концепции технологии блокчейна, 
такие как транзакции, экономические модели, блоки, кошельки, механизмы
консенсуса и многое другое.

Copyright (C) 2024  Alexeev Bronislav

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
