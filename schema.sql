
create table if not exists login (username text, salt text, hash text);

create table if not exists role (username, child);

