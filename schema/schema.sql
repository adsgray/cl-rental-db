
create table ad(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	time TEXT,
	title TEXT,
	loctext TEXT,
	bedrooms INTEGER,
	squarefeet INTEGER,
	price INTEGER,
	location_id INTEGER,
	loc1 TEXT,
	furnished INTEGER,
	FOREIGN KEY(location_id) REFERENCES location(id)
	UNIQUE (bedrooms, squarefeet, loctext, price)
);

create table location(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT
);
