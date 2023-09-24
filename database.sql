create table users
(
    id        bigint generated always as identity
        primary key,
    username  varchar(255)
        unique,
    password  varchar(255),
    salt varchar(255),
    create_at date
);
create table users_additionally
(
    id      bigint generated always as identity
        primary key,
    user_id bigint
        references users,
    gender  varchar(10),
    years   integer,
    country varchar(255)
);
create table users_secrets
(
    id      bigint generated always as identity
        primary key,
    user_id bigint
        references users,
    secret  varchar(2500)
        unique,
    telegram_id bigint
        unique
);
create table posts
(
    id      bigint generated always as identity
        primary key,
    user_id bigint references users(id),
    user_name varchar(255),
    name    varchar(255),
    content text
);

INSERT INTO posts (name, content) VALUES ('ZXC???', '100-7???????');
INSERT INTO posts (name, content) VALUES ('ЧвК Редан?О_О ryodan??', e'Название: Геней Рёдан/Призрачная Труппа「幻影旅団], также известная как "Труппа" и "Паук"
Функции/цели:

Заработок денег (преимущественно незаконным путём)
Местоположение: Как таковой не существует, однако многие выходцы из города Падающей Звезды

Численность: Единовременно 13 членов
Внутреннее устройство: Все члены банды подчиняются боссу. Когда дело окончено, участники вольны делать, что захотят, пока их снова не созовёт лидер

Умения, силы и способности: Сверхчеловеческие физические характеристики, гениальный интеллект (тактический, стратегический, преступный), владение оружием, ловкость, манипуляции энергией

Слабые стороны:

Производственный потенциал: Как таковой отсутствует

Показатели основных боевых характеристик:

Разрушительный потенциал: От уровня строения до уровня большого здания+
Прочность/защита: От уровня строения до уровня большого здания+
Скорость: От сверхзвуковой+ до гиперзвуковой для скорости боя
Союзники: Отсутствуют
Противники:

Курапика
Хисока
');
create table comments
(
    id       bigint generated always as identity
        primary key,
    post_id  bigint
        references posts,
    user_id bigint references users(id),
    username varchar(255),
    content  text
);
