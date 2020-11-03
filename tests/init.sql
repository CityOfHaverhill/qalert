CREATE TABLE public.qalert_requests
(
    id integer NOT NULL,
    status integer,
    create_date date,
    create_date_unix integer,
    last_action date,
    last_action_unix integer,
    type_id integer,
    type_name text COLLATE pg_catalog."default",
    comments text COLLATE pg_catalog."default",
    street_num text COLLATE pg_catalog."default",
    street_name text COLLATE pg_catalog."default",
    cross_name text COLLATE pg_catalog."default",
    city_name text COLLATE pg_catalog."default",
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