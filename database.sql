create table users
(
    id        bigint generated always as identity
        primary key,
    username  varchar(255)
        unique,
    password  varchar(255),
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
    secret  varchar(255)
        unique
);
