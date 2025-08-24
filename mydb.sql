--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-08-23 01:14:55

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 32782)
-- Name: sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales (
    id integer NOT NULL,
    unit_sales integer NOT NULL,
    date date NOT NULL
);


ALTER TABLE public.sales OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 32781)
-- Name: sales_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sales_id_seq OWNER TO postgres;

--
-- TOC entry 4809 (class 0 OID 0)
-- Dependencies: 217
-- Name: sales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sales_id_seq OWNED BY public.sales.id;


--
-- TOC entry 220 (class 1259 OID 32789)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 32788)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4810 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4646 (class 2604 OID 32785)
-- Name: sales id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales ALTER COLUMN id SET DEFAULT nextval('public.sales_id_seq'::regclass);


--
-- TOC entry 4647 (class 2604 OID 32792)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4801 (class 0 OID 32782)
-- Dependencies: 218
-- Data for Name: sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sales (id, unit_sales, date) FROM stdin;
1	644	2017-07-16
2	544	2017-07-17
3	795	2017-07-18
4	506	2017-07-19
5	486	2017-07-20
6	576	2017-07-21
7	567	2017-07-22
8	511	2017-07-23
9	676	2017-07-24
10	730	2017-07-25
11	617	2017-07-26
12	574	2017-07-27
13	477	2017-07-28
14	676	2017-07-29
15	689	2017-07-30
16	508	2017-07-31
17	632	2017-08-01
18	652	2017-08-02
19	606	2017-08-03
20	778	2017-08-04
21	774	2017-08-05
22	794	2017-08-06
23	504	2017-08-07
24	700	2017-08-08
25	508	2017-08-09
26	489	2017-08-10
27	764	2017-08-11
28	743	2017-08-12
29	554	2017-08-13
30	550	2017-08-14
31	571	2017-08-15
32	582	2017-08-16
33	599	2017-08-17
34	518	2017-08-18
35	723	2017-08-19
36	572	2017-08-20
\.


--
-- TOC entry 4803 (class 0 OID 32789)
-- Dependencies: 220
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, created_at) FROM stdin;
1	admin	scrypt:32768:8:1$r5Bgd40tKzSHzytS$0549e350b388090968eaa796bd6ab92f9ce44317576d0243ed8e2eeacc98b2abe1ef257d1bc9413dcc342716e9027046a6d22166c76e7578e775ed79f4ea18e7	2025-08-22 21:36:09.839851
\.


--
-- TOC entry 4811 (class 0 OID 0)
-- Dependencies: 217
-- Name: sales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sales_id_seq', 36, true);


--
-- TOC entry 4812 (class 0 OID 0)
-- Dependencies: 219
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- TOC entry 4650 (class 2606 OID 32787)
-- Name: sales sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);


--
-- TOC entry 4652 (class 2606 OID 32797)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4654 (class 2606 OID 32799)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


-- Completed on 2025-08-23 01:14:55

--
-- PostgreSQL database dump complete
--

