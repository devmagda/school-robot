create table tbl_faces (
    id serial primary key,
    base bytea,
    age varchar(255) not null,
    race varchar(255),
    gender varchar(255),
    emotion varchar(255)
);