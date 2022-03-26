create table if not exists login (username text, salt text, hash text);

drop table if exists role;
create table role(username text, relationship text, other text);
insert into role (username, relationship, other)
values
  ("arthur", "", "ics_user"),
  ("justo", "", "ics_user"),
  ("edmundo", "", "ics_user"),
  ("alicia", "", "ics_user");

drop table if exists answers;
create table answers (
  username text,
  ts integer,
  question text,
  question_only text,
  answer text);

drop table if exists questions;
create table questions (
  question_id integer primary key,
  username text,
  question text,
  correct_answer text,
  wrong_answers text); -- wrong_answers is a json list.
