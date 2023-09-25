create table users
(
    id        bigint generated always as identity
        primary key,
    username  varchar(255)
        unique,
    password  varchar(255),
    salt      varchar(255),
    create_at date
);

alter table users
    owner to katana;

INSERT INTO public.users (username, password, salt, create_at) VALUES ('katana', 'ca54472303cbff762171e34851026e6ae09cecc18bf9872095cd6d294ea97a97', '2432622431322471323656737150683737795170626d594d364a436c65', '2023-09-24');
INSERT INTO public.users (username, password, salt, create_at) VALUES ('rukati', '2af178b50bc39a709827a79a86bd7d9c1f7b152b1b9434c2aa638927623dd966', '24326224313224694a304472486854707735514b5673364e336c754865', '2023-09-24');
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

alter table users_additionally
    owner to katana;

INSERT INTO public.users_additionally (user_id, gender, years, country) VALUES (1, 'female', 20, '20');
INSERT INTO public.users_additionally (user_id, gender, years, country) VALUES (2, 'other', 20, 'STARAIII');
create table users_secrets
(
    id          bigint generated always as identity
        primary key,
    user_id     bigint
        references users,
    secret      varchar(2500)
        unique,
    telegram_id bigint
        unique
);

alter table users_secrets
    owner to katana;

INSERT INTO public.users_secrets (user_id, secret, telegram_id) VALUES (1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NTU4NTg3MCwianRpIjoiOGE1NTUwYjMtN2E2OS00MTk2LThmZTktZmMxNDU2MDUyMGFkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImthdGFuYSIsIm5iZiI6MTY5NTU4NTg3MCwiZXhwIjoxNjk1NTg2NzcwfQ.FuJHvDAy_V5cCAUpmmNh1IxhX-l17hLXDTlrcus3eLA', null);
INSERT INTO public.users_secrets (user_id, secret, telegram_id) VALUES (2, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NTU4NTkxOCwianRpIjoiOTdiY2Q2NTctOTVlZi00NWM5LWFjYzUtMjMxNmE1ZjkwODA3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InJ1a2F0aSIsIm5iZiI6MTY5NTU4NTkxOCwiZXhwIjoxNjk1NTg2ODE4fQ.CSt4DYGbWkgY_vPCY10otV-OvPQmRbaRRwzNPMGVw7U', null);
create table posts
(
    id        bigint generated always as identity
        primary key,
    user_id   bigint
        references users,
    user_name varchar(255),
    name      varchar(255),
    content   text
);

alter table posts
    owner to katana;

INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', 'ЧвК Редан?О_О ryodan??', e'Название: Геней Рёдан/Призрачная Труппа「幻影旅団], также известная как "Труппа" и "Паук"
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
INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', 'ZXC???', 'ЧвК Редан?О_О ryodan??');
INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', 'Премьера когда то в 2025 году.', e'Вышел трейлер Dungeons & Kittens, мультсериала вдохновлённого стилем игры Dungeons & Dragons.

По сюжету группа котят, которых изгнали из кошачьего королевства, отправится на поиски сокровища, которое поможет им вернуться домой.');
INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', 'Мальчик и птица', e'«Мальчик и птица» Миядзаки выйдет в России 7 декабря.

Премьера была запланирована на ноябрь, но немного перенесли.');
INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', '⚡️ Genshin Impact чуть не взорвал iPhone 15 Pro.', e'⚡️ Genshin Impact чуть не взорвал iPhone 15 Pro.

Игру запустили с максимальными настройками графики и смартфон начал сильно лагать и нагреваться.

При этом игры вроде GTA: San Andreas, eFootball PES, PUBG Mobile и Call of Duty Mobile запустились без проблем.');
INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', 'Искусство высшего уровня.', 'Ютубер построил картину Ван Гога «Звёздная ночь» в Майнкрафте.');
INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', 'Продолжение истории с украинской локализацией в Cyberpunk 2077: ', 'СССР заменили на Украину');
INSERT INTO public.posts (user_id, user_name, name, content) VALUES (1, 'katana', 'Ш е д е в р.', 'Энтузиаст создал интро Baldur’s Gate 3 в стиле «Друзей».');
create table comments
(
    id       bigint generated always as identity
        primary key,
    post_id  bigint
        references posts,
    user_id  bigint
        references users,
    username varchar(255),
    content  text
);

alter table comments
    owner to katana;

INSERT INTO public.comments (post_id, user_id, username, content) VALUES (1, 2, 'rukati', 'Очень крутой пост спасибо большое');
INSERT INTO public.comments (post_id, user_id, username, content) VALUES (2, 2, 'rukati', 'Очень интересно, делай побольше таких постов');
