--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-07-22 17:12:56

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
-- TOC entry 222 (class 1259 OID 16697)
-- Name: menus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menus (
    menu_id integer NOT NULL,
    menu_name character varying(100) NOT NULL,
    route character varying(150),
    parent_menu_id integer,
    icon character varying(100),
    order_no integer DEFAULT 0,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    created_by integer,
    updated_by integer
);


ALTER TABLE public.menus OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16696)
-- Name: menus_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.menus_menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.menus_menu_id_seq OWNER TO postgres;

--
-- TOC entry 4967 (class 0 OID 0)
-- Dependencies: 221
-- Name: menus_menu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.menus_menu_id_seq OWNED BY public.menus.menu_id;


--
-- TOC entry 223 (class 1259 OID 16721)
-- Name: role_menu_access; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_menu_access (
    role_id integer NOT NULL,
    menu_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    created_by integer,
    updated_by integer
);


ALTER TABLE public.role_menu_access OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16662)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    created_by integer,
    updated_by integer
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16661)
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_role_id_seq OWNER TO postgres;

--
-- TOC entry 4968 (class 0 OID 0)
-- Dependencies: 219
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;


--
-- TOC entry 225 (class 1259 OID 16748)
-- Name: user_action_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_action_logs (
    log_id integer NOT NULL,
    user_id integer,
    menu_id integer,
    terminal_name character varying(50),
    action character varying(50),
    target_id integer,
    description text,
    ip_address character varying(45),
    device_info text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_action_logs OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16747)
-- Name: user_action_logs_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_action_logs_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_action_logs_log_id_seq OWNER TO postgres;

--
-- TOC entry 4969 (class 0 OID 0)
-- Dependencies: 224
-- Name: user_action_logs_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_action_logs_log_id_seq OWNED BY public.user_action_logs.log_id;


--
-- TOC entry 218 (class 1259 OID 16646)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password text NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying,
    role_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    created_by integer,
    updated_by integer,
    CONSTRAINT users_status_check CHECK (((status)::text = ANY ((ARRAY['active'::character varying, 'inactive'::character varying, 'suspended'::character varying, 'pending'::character varying, 'terminated'::character varying, 'on_leave'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16645)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- TOC entry 4970 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 4766 (class 2604 OID 16700)
-- Name: menus menu_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus ALTER COLUMN menu_id SET DEFAULT nextval('public.menus_menu_id_seq'::regclass);


--
-- TOC entry 4764 (class 2604 OID 16665)
-- Name: roles role_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);


--
-- TOC entry 4771 (class 2604 OID 16751)
-- Name: user_action_logs log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_action_logs ALTER COLUMN log_id SET DEFAULT nextval('public.user_action_logs_log_id_seq'::regclass);


--
-- TOC entry 4761 (class 2604 OID 16649)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 4958 (class 0 OID 16697)
-- Dependencies: 222
-- Data for Name: menus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menus (menu_id, menu_name, route, parent_menu_id, icon, order_no, is_active, created_at, updated_at, created_by, updated_by) FROM stdin;
1	Dashboard	/dashboard	\N	fa fa-home	1	t	2025-07-21 14:52:47.226979	\N	1	\N
2	Manajemen Karyawan	/karyawan	\N	fa fa-users	2	t	2025-07-21 14:52:47.226979	\N	1	\N
3	Manajemen Absensi	/absensi	\N	fa fa-calendar-check	3	t	2025-07-21 14:52:47.226979	\N	1	\N
4	Pengajuan Izin & Cuti	/izin	\N	fa fa-envelope-open-text	4	t	2025-07-21 14:52:47.226979	\N	1	\N
5	Penggajian	/penggajian	\N	fa fa-money-bill	5	t	2025-07-21 14:52:47.226979	\N	1	\N
6	Slip Gaji	/slip-gaji	\N	fa fa-file-invoice-dollar	6	t	2025-07-21 14:52:47.226979	\N	1	\N
7	Laporan	/laporan	\N	fa fa-chart-line	7	t	2025-07-21 14:52:47.226979	\N	1	\N
8	Manajemen User	/user-management	\N	fa fa-user-shield	8	t	2025-07-21 14:52:47.226979	\N	1	\N
9	Log Aktivitas	/logs	\N	fa fa-history	9	t	2025-07-21 14:52:47.226979	\N	1	\N
10	Pengaturan	/pengaturan	\N	fa fa-cogs	10	t	2025-07-21 14:52:47.226979	\N	1	\N
11	Data Karyawan	/karyawan/data	2	fa fa-id-card	1	t	2025-07-21 14:53:08.457866	\N	1	\N
12	Tambah Karyawan	/karyawan/tambah	2	fa fa-user-plus	2	t	2025-07-21 14:53:08.457866	\N	1	\N
13	Rekap Absensi	/absensi/rekap	3	fa fa-clipboard-list	1	t	2025-07-21 14:53:08.457866	\N	1	\N
14	Input Manual Absensi	/absensi/input	3	fa fa-pen	2	t	2025-07-21 14:53:08.457866	\N	1	\N
15	Form Cuti	/izin/cuti	4	fa fa-suitcase-rolling	1	t	2025-07-21 14:53:08.457866	\N	1	\N
16	Form Sakit	/izin/sakit	4	fa fa-thermometer-half	2	t	2025-07-21 14:53:08.457866	\N	1	\N
17	Gaji Bulanan	/penggajian/bulanan	5	fa fa-calendar-dollar	1	t	2025-07-21 14:53:08.457866	\N	1	\N
18	Komponen Gaji	/penggajian/komponen	5	fa fa-cubes	2	t	2025-07-21 14:53:08.457866	\N	1	\N
19	Laporan Absensi	/laporan/absensi	7	fa fa-book-open	1	t	2025-07-21 14:53:08.457866	\N	1	\N
20	Laporan Gaji	/laporan/gaji	7	fa fa-file-invoice	2	t	2025-07-21 14:53:08.457866	\N	1	\N
21	Daftar User	/user-management/list	8	fa fa-users-cog	1	t	2025-07-21 14:53:08.457866	\N	1	\N
22	Role Akses	/user-management/roles	8	fa fa-shield-alt	2	t	2025-07-21 14:53:08.457866	\N	1	\N
\.


--
-- TOC entry 4959 (class 0 OID 16721)
-- Dependencies: 223
-- Data for Name: role_menu_access; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role_menu_access (role_id, menu_id, created_at, updated_at, created_by, updated_by) FROM stdin;
1	1	2025-07-21 14:53:40.489486	\N	1	\N
1	2	2025-07-21 14:53:40.489486	\N	1	\N
1	3	2025-07-21 14:53:40.489486	\N	1	\N
1	4	2025-07-21 14:53:40.489486	\N	1	\N
1	5	2025-07-21 14:53:40.489486	\N	1	\N
1	6	2025-07-21 14:53:40.489486	\N	1	\N
1	7	2025-07-21 14:53:40.489486	\N	1	\N
1	8	2025-07-21 14:53:40.489486	\N	1	\N
1	9	2025-07-21 14:53:40.489486	\N	1	\N
1	10	2025-07-21 14:53:40.489486	\N	1	\N
1	11	2025-07-21 14:53:40.489486	\N	1	\N
1	12	2025-07-21 14:53:40.489486	\N	1	\N
1	13	2025-07-21 14:53:40.489486	\N	1	\N
1	14	2025-07-21 14:53:40.489486	\N	1	\N
1	15	2025-07-21 14:53:40.489486	\N	1	\N
1	16	2025-07-21 14:53:40.489486	\N	1	\N
1	17	2025-07-21 14:53:40.489486	\N	1	\N
1	18	2025-07-21 14:53:40.489486	\N	1	\N
1	19	2025-07-21 14:53:40.489486	\N	1	\N
1	20	2025-07-21 14:53:40.489486	\N	1	\N
1	21	2025-07-21 14:53:40.489486	\N	1	\N
1	22	2025-07-21 14:53:40.489486	\N	1	\N
\.


--
-- TOC entry 4956 (class 0 OID 16662)
-- Dependencies: 220
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (role_id, role_name, created_at, updated_at, created_by, updated_by) FROM stdin;
1	Super Admin	2025-07-21 14:21:14.809565	\N	\N	\N
\.


--
-- TOC entry 4961 (class 0 OID 16748)
-- Dependencies: 225
-- Data for Name: user_action_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_action_logs (log_id, user_id, menu_id, terminal_name, action, target_id, description, ip_address, device_info, created_at) FROM stdin;
\.


--
-- TOC entry 4954 (class 0 OID 16646)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, email, password, status, role_id, created_at, updated_at, created_by, updated_by) FROM stdin;
1	superadmin	superadmin@gmail.com	$2b$12$76Z2CZVYRVbrhOJ0H0BMmefIRfiCHWYXAyfWXHwXBFWpQStCx1k82	active	1	2025-07-21 14:34:22.788544	\N	\N	\N
\.


--
-- TOC entry 4971 (class 0 OID 0)
-- Dependencies: 221
-- Name: menus_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menus_menu_id_seq', 22, true);


--
-- TOC entry 4972 (class 0 OID 0)
-- Dependencies: 219
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 1, true);


--
-- TOC entry 4973 (class 0 OID 0)
-- Dependencies: 224
-- Name: user_action_logs_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_action_logs_log_id_seq', 1, false);


--
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- TOC entry 4787 (class 2606 OID 16705)
-- Name: menus menus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_pkey PRIMARY KEY (menu_id);


--
-- TOC entry 4789 (class 2606 OID 16726)
-- Name: role_menu_access role_menu_access_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_menu_access
    ADD CONSTRAINT role_menu_access_pkey PRIMARY KEY (role_id, menu_id);


--
-- TOC entry 4782 (class 2606 OID 16668)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- TOC entry 4784 (class 2606 OID 16670)
-- Name: roles roles_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);


--
-- TOC entry 4793 (class 2606 OID 16756)
-- Name: user_action_logs user_action_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_action_logs
    ADD CONSTRAINT user_action_logs_pkey PRIMARY KEY (log_id);


--
-- TOC entry 4776 (class 2606 OID 16660)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4778 (class 2606 OID 16656)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 4780 (class 2606 OID 16658)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4790 (class 1259 OID 16770)
-- Name: idx_logs_menu; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_logs_menu ON public.user_action_logs USING btree (menu_id);


--
-- TOC entry 4791 (class 1259 OID 16769)
-- Name: idx_logs_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_logs_user ON public.user_action_logs USING btree (user_id);


--
-- TOC entry 4785 (class 1259 OID 16768)
-- Name: idx_menus_parent; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_menus_parent ON public.menus USING btree (parent_menu_id);


--
-- TOC entry 4774 (class 1259 OID 16767)
-- Name: idx_users_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_role_id ON public.users USING btree (role_id);


--
-- TOC entry 4797 (class 2606 OID 16686)
-- Name: roles fk_roles_created_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT fk_roles_created_by FOREIGN KEY (created_by) REFERENCES public.users(user_id);


--
-- TOC entry 4798 (class 2606 OID 16691)
-- Name: roles fk_roles_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT fk_roles_updated_by FOREIGN KEY (updated_by) REFERENCES public.users(user_id);


--
-- TOC entry 4794 (class 2606 OID 16676)
-- Name: users fk_users_created_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_created_by FOREIGN KEY (created_by) REFERENCES public.users(user_id);


--
-- TOC entry 4795 (class 2606 OID 16671)
-- Name: users fk_users_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES public.roles(role_id) ON DELETE SET NULL;


--
-- TOC entry 4796 (class 2606 OID 16681)
-- Name: users fk_users_updated_by; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_users_updated_by FOREIGN KEY (updated_by) REFERENCES public.users(user_id);


--
-- TOC entry 4799 (class 2606 OID 16711)
-- Name: menus menus_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id);


--
-- TOC entry 4800 (class 2606 OID 16706)
-- Name: menus menus_parent_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_parent_menu_id_fkey FOREIGN KEY (parent_menu_id) REFERENCES public.menus(menu_id) ON DELETE CASCADE;


--
-- TOC entry 4801 (class 2606 OID 16716)
-- Name: menus menus_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.menus
    ADD CONSTRAINT menus_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(user_id);


--
-- TOC entry 4802 (class 2606 OID 16737)
-- Name: role_menu_access role_menu_access_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_menu_access
    ADD CONSTRAINT role_menu_access_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id);


--
-- TOC entry 4803 (class 2606 OID 16732)
-- Name: role_menu_access role_menu_access_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_menu_access
    ADD CONSTRAINT role_menu_access_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.menus(menu_id) ON DELETE CASCADE;


--
-- TOC entry 4804 (class 2606 OID 16727)
-- Name: role_menu_access role_menu_access_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_menu_access
    ADD CONSTRAINT role_menu_access_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id) ON DELETE CASCADE;


--
-- TOC entry 4805 (class 2606 OID 16742)
-- Name: role_menu_access role_menu_access_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_menu_access
    ADD CONSTRAINT role_menu_access_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.users(user_id);


--
-- TOC entry 4806 (class 2606 OID 16762)
-- Name: user_action_logs user_action_logs_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_action_logs
    ADD CONSTRAINT user_action_logs_menu_id_fkey FOREIGN KEY (menu_id) REFERENCES public.menus(menu_id) ON DELETE SET NULL;


--
-- TOC entry 4807 (class 2606 OID 16757)
-- Name: user_action_logs user_action_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_action_logs
    ADD CONSTRAINT user_action_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


-- Completed on 2025-07-22 17:12:56

--
-- PostgreSQL database dump complete
--

