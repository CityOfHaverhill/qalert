CREATE TABLE public.qalert_requests
(
    id integer NOT NULL,
    status integer,
    create_date date,
    create_date_unix integer,
    last_action date,
    last_action_unix integer,
    type_id integer,
    type_name varchar(200) COLLATE pg_catalog."default",
    comments varchar(5000) COLLATE pg_catalog."default",
    street_num varchar(100) COLLATE pg_catalog."default",
    street_name varchar(100) COLLATE pg_catalog."default",
    cross_name varchar(100) COLLATE pg_catalog."default",
    city_name varchar(100) COLLATE pg_catalog."default",
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    point geometry(Point,4269) NOT NULL,
    CONSTRAINT qalert_requests_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.qalert_requests
    OWNER to docker;

CREATE TABLE public.qalert_audits
(
    id SERIAL NOT NULL,
    create_date text 
)

WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.qalert_audits
    OWNER to docker;