for the db, you need a posts table with id integer, title character varying(255), link character varying(255), shortcake character varying(6), length integer, md5 character varying(32), key character varying(64), auto_approach character varying(255), auto_solution text

config.py needs pgsql={"string": "postgresql://user:password@server:port/database"} keylist=[b'A858DE45F56D9BC9'] ivlist=[b'\0\0\0\0\0\0\0\0'] bf=False

after the initial dataset load of title and content, you need to populate_shortcodes() populate_lengths() populate_md5() populate_solutions() (the last one takes a while)