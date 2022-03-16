create table if not exists login (username text, salt text, hash text);

drop table if exists role;
create table role(username text, relationship text, other text);

insert into role (username, relationship, other)
values
  ("arthur", "", "ics_user"),
  ("justo", "", "ics_user"),
  ("edmundo", "", "ics_user");

drop table if exists questions;
create table questions (username text, question text, ts integer);

drop table if exists answers;
create table answers (username text, question text, answer text, ts integer);

