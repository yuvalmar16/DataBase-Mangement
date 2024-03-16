


create table Employee(
    eID int PRIMARY KEY ,
    DepName varchar(100) not null,
     foreign key (DepName) references Deparment
     on delete cascade ,
    name varchar (100)
)



create table Manager(
    eID int primary key ,
    foreign key (eID) references Employee
     on DELETE cascade ,
    salary int
)


create table Technician(
    eID int primary key ,
    foreign key (eID) references Employee
    on delete cascade ,
    FieldOfExperty varchar (100)
)



create table Deparment
(
    DepName varchar(100) primary key,
    description varchar(100) ,
    ManagerId int,
    foreign key (ManagerId) references Manager (eID)  on delete cascade,
)




create table Family(
    fID int primary key,
    family_name varchar (100),
)

create table Person
(
    first_name varchar(100) not null,
    fID    int not null,
    foreign key (fID) references Family on delete cascade ,
    PRIMARY KEY (first_name, fID),
    birthDate  date,
    phoneNum  varchar(10),
    check ((ISNUMERIC(phoneNum)) > 0)
)




--create table Premium(
  --   fID int primary key,
 --    foreign key (fID) references Family,
  --   wealth int, check  (wealth>=7)

--)



create table premiumFamily(
     fID int primary key,
     foreign key (fID) references Family,
     wealth int, check  (wealth>=7 and wealth<=9),
     TechnianID int not null,
      foreign key (TechnianID)  references Technician (eID) on delete cascade ,

)


create table regularFamily(
     fID int primary key,
     foreign key (fID) references Family  on delete cascade,
     wealth int, check  (wealth<7 and wealth>=1)

)


create table Requested
(
     ManagerId  int not null,
     foreign key (ManagerId) references Manager (eID) on delete cascade ,
    regularFamilyID int not null,
    foreign key (regularFamilyID)  references regularFamily (fID) on delete cascade,
    RequestDate     date not null,
    reason varchar(100) not null,
    finalDecision   varchar(100),
    PRIMARY KEY (ManagerId,regularFamilyID,RequestDate,reason)
)
------אי אפשר לוודא שמעבירים בקשה שכבר אושרה.



create table MoveRequest
(
    --ניסינו לכתוב אחרי שהגדרנו את מנהל פעמיים כמפתח זר On delete cascade אך זה לא התאפשר מבחינת הddl
    SecondManagerId  int not null,
     foreign key (SecondManagerId) references Manager (eID)  ,
    reasonForReplace varchar(100) not null,
    RequestDate     date not null,
    reasonForCancel  varchar(100) not null,
    finalDecision   varchar(100) not null,
    FirstManagerId int not null,
    foreign key (FirstManagerId) references Manager (eID)  ,
    regularFamilyID int not null,
     foreign key (regularFamilyID) references regularFamily (fID),
    foreign key (FirstManagerId,regularFamilyID,RequestDate,reasonForCancel) references Requested
         (ManagerId,regularFamilyID,RequestDate,reason) on delete cascade ,
         unique (FirstManagerId,regularFamilyID,RequestDate,reasonForCancel)


)




create table converterBox
(
    convID     int,
    fid        int foreign key references Family  on delete cascade,
    primary key (convID, fid),
    technitianWhoFixed int,
    foreign key (technitianWhoFixed) references Technician (eID) on delete cascade ,
    priceForFix      int,
    check ((technitianWhoFixed is null and priceForFix is null) or (technitianWhoFixed is not null and priceForFix is not null))
)


create table channel
(
    chanelNum  int primary key,
    chanelName varchar(100)
)




create table channelSwitch
(
    chanelNum int not null,
    foreign key (chanelNum) references channel on delete cascade ,
    convID   int not null,
    fid int not null,
    foreign key (fid) references Family  ,
    foreign key (convID, fid) references converterBox  on delete cascade,
    SwitchTime date,
)









--כאן יש את מועדי הצפייה בכל הערוצים שבאותו ממיר. ההנחה שלנו שישמרו הערוצים שאינם נצפו
-- על ידי הלקוח אך נמצאים בממיר שלו
---והswitchingTime שלהם ישמר כnull

create table tvShow
(
    length   int,
    genere   varchar(100),
    showName varchar(100) primary key
)





create table showSchedule
(

    chanelNum   int foreign key references channel on delete cascade ,
    showName    varchar(100) foreign key references tvShow on delete cascade ,
    showingTime date,

)






insert into  Deparment values ('marketing', 'sell product', 1)
insert into  Deparment values ('purchase', 'purchase product', 2)

select * from Deparment
insert into Employee values (1, 'Marketing', 'moshe')
insert into  Employee values (2, 'purchase', 'omer')

select * from Employee
insert into  Manager values (1, 200)
insert into  Manager values (2, 200)

select * from Manager
insert into  technician values (1, 'data science')
select * from Technician;
insert into Family values (123, 'cohen')
insert into Family values (456, 'levi')
select * from Family
insert into Person values ('adi', 123, '05/04/1995', '0529635252')
insert into Person values ('avi', 123, '05/04/1995', '0529635252')
insert into Person values ('adam', 456, '10/12/2005', '0529635252')
select * from Person
insert into regularFamily values (123, 5)
select * from regularFamily
insert into premiumFamily values (456, 8, 1)
select * from premiumFamily
insert into Requested values (1, 123,'10/12/2022' ,'too expensive', 'move it' )
insert into Requested values (1, 123,'11/12/2022' ,'too expensive', 'move it' )
select * from Requested
insert into MoveRequest values (2, 'hard to decide', '10/12/2022', 'too expensive',  'approve', 1, 123)
select * from MoveRequest
insert into converterBox values (1,456, 1, 500)
insert into converterBox (convID, fid)values (1,123)
select * from converterBox
insert into channel values (12, 'money taxi')
select * from channel;
insert into channelSwitch (chanelNum, convID, fid) values (12, 1, 123)
insert into channelSwitch values (12, 1, 123, '04/04/2022')
insert into channelSwitch values (12, 1, 123, '03/04/2022')
select * from  channelSwitch
insert into tvShow values (60 ,'comedy', 'traffic light');
select * from tvShow
insert into showSchedule values (12 ,'traffic light', '05/12/2012');
select * from showSchedule





