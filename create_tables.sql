CREATE DATABASE DBMS_PROJECT;
USE DBMS_PROJECT;

CREATE TABLE login(
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);

INSERT INTO login VALUES ('admin','admin');

CREATE TABLE Branch(
  Branch_ID varchar(6) NOT NULL check(length(Branch_ID) >= 6),
  Branch_name varchar(20) NOT NULL,
  Phone_no bigint NOT NULL check(Phone_no between  6000000000 and 9999999999),
  -- Phone_no bigint NOT NULL ,

  Address varchar(250),
  Date_of_est date NOT NULL,
  PRIMARY KEY(Branch_ID)
);
-- insert into branch values ();
insert into branch values ('br1234', 'ganesh', '6304772654', 'near rr layout', '2001-01-31');

#table 1
CREATE TABLE donation_Camp(
    DC_ID varchar(6) NOT NULL check(length(DC_ID) >= 6),
    Date_of_Conduction date NOT NULL,
    -- No_of_Days int,
    Branch_ID varchar(6) NOT NULL  check(length(Branch_ID) >= 6),
    Amount_Collected int,
    Street varchar(20),
    City varchar(20),
    State varchar(20),
    FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON DELETE CASCADE,
    PRIMARY KEY(DC_ID)
);

CREATE TABLE orphanage(
    Orphanage_ID varchar(6) NOT NULL  check(length(Orphanage_ID) >= 6),
    Orphanage_Name varchar(20) NOT NULL,
    Branch_ID varchar(6) NOT NULL  check(length(Branch_ID) >= 6),
    No_Boys int,
    No_Girls int,
    Orphanage_Address varchar(250),
    -- Orpahanage_Pno varchar(10),
    Orphanage_Pno bigint NOT NULL check(Orphanage_Pno between  6000000000 and 9999999999),
    
    FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) on DELETE CASCADE,
    PRIMARY KEY(Orphanage_ID)
);

CREATE TABLE orphanage_stats(
  Orphanage_ID  varchar(6) NOT NULL  check(length(Orphanage_ID) >= 6),
  Date_stat date NOT NULL,
  Amount_Donated int NOT NULL,
  -- Date_of_transvaraction date NOT NULL,
  FOREIGN KEY(Orphanage_ID) REFERENCES orphanage(Orphanage_ID) ON DELETE CASCADE,
  PRIMARY KEY(Orphanage_ID,Date_stat)

);

#table 6
CREATE TABLE donor(
  Donor_ID varchar(6) NOT NULL  check(length(Donor_ID) >= 6),
  Donor_Name varchar(32),
  -- Donor_Phno varchar(10),   
  Donor_Phno bigint NOT NULL check(Donor_Phno between  6000000000 and 9999999999),
  Date_of_Donation date NOT NULL,
  Amount_donated int,
  Items_donated varchar(100),
  DC_ID varchar(6) NOT NULL  check(length(DC_ID) >= 6),
  FOREIGN KEY(DC_ID) REFERENCES Donation_Camp(DC_ID) ON DELETE CASCADE,
  -- FOREIGN KEY(Date_of_Donation) REFERENCES Donation_Camp(Date_of_Conduction) ON DELETE CASCADE,
  PRIMARY KEY(Donor_ID)
);

#table 7
CREATE TABLE Stock(
  Date_Stock date NOT NULL,
  Branch_ID varchar(6) NOT NULL  check(length(Branch_ID) >= 6),
  Amount_Left int,
  Pens_Left int,
  Books_Left int,
  Clothes_Left int,
  Bags_Left int,
  Blanket_Left int,
  FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON DELETE CASCADE,
  PRIMARY KEY(Date_Stock)
);

#table 8
CREATE TABLE  Daily_Stats(
  DC_ID varchar(6) NOT NULL  check(length(DC_ID) >= 6),
  Date_stats date NOT NULL,
  Amount_Collect int,
  Date_of_transaction date NOT NULL,
  FOREIGN KEY(DC_ID) REFERENCES Donation_Camps(DC_ID) ON DELETE CASCADE,
  PRIMARY KEY(DC_ID,Date_stats)
);

#table 9
CREATE TABLE Item(
  ITEM_ID varchar(6) NOT NULL  check(length(ITEM_ID) >= 6),
  ITEM_NAME varchar(20) NOT NULL,
  ITEM_COUNT int NOT NULL,
  PRIMARY KEY(ITEM_ID)
);

insert into Item values("it0001", "blanket", "0");
insert into Item values("it0002", "pen", "0");
insert into Item values("it0003", "pencil", "0");

insert into Item values("it0004", "notebook", "0");
insert into Item values("it0005", "chair", "0");
insert into Item values("it0006", "table", "0");
insert into Item values("it0007", "cloth", "0");
insert into Item values("it0008", "bag", "0");
insert into Item values("it0009", "toy", "0");
insert into Item values("it0010", "electronic devices", "0");


#table 10
CREATE TABLE Branch_phone_no(
  Branch_ID varchar(6) NOT NULL  check(length(Branch_ID) >= 6),
  Phone_no bigint NOT NULL check(Phone_no between  6000000000 and 9999999999),
  FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON DELETE CASCADE
);

-- #table 10
-- CREATE TABLE Doctor_phone_no(
--   Doctor_ID int NOT NULL,
--   Phone_no varchar(15),
--   FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID) ON DELETE CASCADE
-- );


--
-- delimiter //
-- create trigger ADD_DONOR
-- after insert
-- on Donor
-- for each row
-- begin
-- insert into Organ_available(Organ_name, Donor_ID)
-- values (new.organ_donated, new.Donor_ID);
-- end//
-- delimiter ;
--
-- delimiter //
-- create trigger REMOVE_ORGAN
-- after insert
-- on Transaction
-- for each row
-- begin
-- delete from Organ_available
-- where Organ_ID = new.Organ_ID;
-- end//
-- delimiter ;

create table log (
  querytime datetime,
  comment varchar(255)
);

delimiter //
create trigger ADD_DONOR_LOG
after insert
on Donor
for each row
begin
insert into log values
(now(), concat("Inserted new Donor", cast(new.Donor_Id as char)));
end //

create trigger UPD_DONOR_LOG
after update
on Donor
for each row
begin
insert into log values
(now(), concat("Updated Donor Details", cast(new.Donor_Id as char)));
end //

delimiter //
create trigger DEL_DONOR_LOG
after delete
on Donor
for each row
begin
insert into log values
(now(), concat("Deleted Donor ", cast(old.Donor_Id as char)));
end //

create trigger ADD_PATIENT_LOG
after insert
on Patient
for each row
begin
insert into log values
(now(), concat("Inserted new Patient ", cast(new.Patient_Id as char)));
end //

create trigger UPD_PATIENT_LOG
after update
on Patient
for each row
begin
insert into log values
(now(), concat("Updated Patient Details ", cast(new.Patient_Id as char)));
end //

create trigger DEL_PATIENT_LOG
after delete
on Donor
for each row
begin
insert into log values
(now(), concat("Deleted Patient ", cast(old.Donor_Id as char)));
end //

create trigger ADD_TRASACTION_LOG
after insert
on Transaction
for each row
begin
insert into log values
(now(), concat("Added Transaction :: Patient ID : ", cast(new.Patient_ID as char), "; Donor ID : " ,cast(new.Donor_ID as char)));
end //

-- INSERT INTO User VALUES(10,'Random1','2000-01-01',1,NULL,'Street 1','City 1','State 1');
-- INSERT INTO User VALUES(20,'Random2','2000-01-02',1,NULL,'Street 2','City 2','State 2');
-- insert into orphanage values("or3", "ramesh", "br5", "20", "15",  "majestic", "9998887776"
