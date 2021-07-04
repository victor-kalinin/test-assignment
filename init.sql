create table devices
(
    id          bigserial not null
                constraint devices_pk
                primary key,
    dev_id      varchar(200) not null,
    dev_type    varchar(120) not null
);

alter table devices
    owner to postgres;

create index devices_dev_id_dev_type_index
    on devices (dev_id, dev_type);

create table endpoints
(
    id          bigserial not null
                constraint endpoints_pk
                primary key,
    device_id   integer
                constraint endpoints_devices_id_fk
                references devices
                on update cascade on delete cascade,
    comment     text
);

alter table endpoints
    owner to postgres;