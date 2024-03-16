CREATE TABLE Households(
    hID             INTEGER PRIMARY KEY,
    netWorth        INTEGER,
    ChildrenNum     INTEGER
);


CREATE TABLE Programs(
    title       VARCHAR(45) PRIMARY KEY,
    genre       VARCHAR(25),
    duration    INTEGER
);


CREATE TABLE RecordOrders(
    title       VARCHAR(45),
    hID         INTEGER,
    PRIMARY KEY (title, hID),
    FOREIGN KEY (title) REFERENCES Programs
        ON DELETE CASCADE,
    FOREIGN KEY (hID) REFERENCES Households
        ON DELETE CASCADE,
);

CREATE TABLE RecordReturns(
    title       VARCHAR(45),
    hID         INTEGER,
    PRIMARY KEY (title, hID),
    FOREIGN KEY (title) REFERENCES Programs
        ON DELETE CASCADE,
    FOREIGN KEY (hID) REFERENCES Households
        ON DELETE CASCADE,
);

CREATE TABLE ProgramRanks(
    title       VARCHAR(45),
    hID         INTEGER,
    rank        INTEGER,
    PRIMARY KEY (title, hID),
    FOREIGN KEY (title) REFERENCES Programs
        ON DELETE CASCADE,
    FOREIGN KEY (hID) REFERENCES Households
        ON DELETE CASCADE,
    CHECK(1<=rank AND rank<=5)
);


-----------------A
create view A_Programs
as
select  distinct(RR.title) as title ,P.genre  as genre ,p.duration as duration
from RecordReturns RR left join Programs P on P.title = RR.title left join  HouseHolds H on RR.hID = H.hID
where ChildrenNum=0 and genre like 'A%'
 drop view A_Programs


create view  max_len_A_programs
as
select A_Programs.genre, title, A_Programs.duration as duration
from A_Programs  join (
select genre, max(duration) as maxLength
from A_Programs group by genre)maxLen on A_Programs.genre=maxLen.genre And  A_Programs.duration=maxLen.maxLength

drop view max_len_A_programs

----the queryA
select genre, min(title) as title, duration
from  max_len_A_programs
group by genre, duration
order by genre


-------------------------------------B
create view orderFamlies as
select  (count(distinct RO.hID)) as femaliesO, PR.title
    from ProgramRanks PR
       left JOIN RecordOrders RO on RO.hID = PR.hID and RO.title=pr.title
group by PR.title


drop view orderFamlies
drop view returnFamlies


create view returnFamlies as
select  (count(distinct RR.hID)) as femaliesR, PR.title
    from ProgramRanks PR
        JOIN RecordReturns RR on RR.hID = PR.hID and  RR.title=pr.title
group by PR.title


drop view returnFamlies



create view CosherSum as
select  ProgramRanks.title, (isnull(femaliesO,0) + isnull(femaliesR,0)) as cosher, femaliesO, femaliesR
    from ProgramRanks left join  orderFamlies on ProgramRanks.title= orderFamlies.title
   left join returnFamlies on ProgramRanks.title=returnFamlies.title
group by ProgramRanks.title, femaliesO, femaliesR

drop view cosherSum


create view totalRate as
select format((avg(cast(ProgramRanks.rank as decimal(10,2)))),'N2') as rate, title
    from ProgramRanks
group by title




------the queryB
select totalRate.title as title,totalRate.rate as AverageRank
    from totalRate join CosherSum CS on totalRate.title = CS.title where CS.cosher>=3
ORDER BY rate desc , title


-------tests
select rank,title,hID
    from ProgramRanks where title='Mona Lisa Smile'
and rank is not null


select sum (rank),count(title)
    from ProgramRanks where title='Beautiful Creatures'

---------------------------------------


--------------------------------------------C
create view  famaliesReturnCount as
select distinct title,count(distinct hid) famlies
    from RecordReturns
group by title



create view netWorthFamlies as
select distinct title,count(distinct Households.hID) famlies
    from Households join RecordReturns on  Households.hID=RecordReturns.hID
    where Households.netWorth>=8
group by title

create view prestigiousShow as
select netWorthFamlies.title as title
    from famaliesReturnCount , netWorthFamlies where netWorthFamlies.famlies*2>famaliesReturnCount.famlies
       and famaliesReturnCount.famlies>=10 and netWorthFamlies.title=famaliesReturnCount.title

drop view prestigiousShow


select  prestigiousShow.title as title
from prestigiousShow
except
(select prestigiousShow.title
 from prestigiousShow
          join ProgramRanks on prestigiousShow.title = ProgramRanks.title and ProgramRanks.rank < 2)
order by title




----------------------------------------PART 3 QUERY

select hid
    from Households
where hID=28

select title
    from programs

create view poses3 as
 select hid,titles
     from
(select  hid, count(distinct(title)) as titles
    from RecordOrders
group by hid)T



 select hid, ChildrenNum
                                            from Households
                                            where ChildrenNum>0 and hid=%s
select title
    from Programs
where genre ='Adults only' or genre ='Reality'


select  *

    from RecordReturns
where title=%s and hID=%s

select *
  from RecordOrders
where title=%s and hID!=%s

select hID,
CASE
    when hid>200 THEN 'no'
    else 'yes'
end as A
from RecordOrders;

select *
    from RecordOrders
where title=%s and hID=%s


select titles,
CASE
    when titles>=3 THEN 'error A'
    else 'yes'
end as A
from (select  hid, count(distinct(title)) titles
    from RecordOrders
    where hid=1
group by hid) T;


select top 3 hID as hID,count(distinct title) as TotalOrders
from
(select*
    from RecordOrders union
select *from RecordReturns)T
group by hID
order by TotalOrders desc , hID


 SELECT  T.genre as genre
     from
(select  count(distinct title) as  titleNum, genre
    from programs
group by genre)T
     where titleNum>=5
order by titleNum desc


select top 5 T.title as title,T.r as rank
from
(select *,
    case
        when rank >= 4 then rank
        else '0'
    end as r
    from ProgramRanks)T
left join Programs on T.title=Programs.title where genre='Horror'
order by r desc, title




 select top 5 T.title as title ,T.r as rank
                                     from
                                     (select *,
                                         case
                                             when rank >=4 then rank
                                             else '0'
                                         end as r
                                         from ProgramRanks)T
                                     left join Programs on T.title=Programs.title where genre='Horror'
                                     order by T.r desc, T.title






select *
    from ProgramRanks
where hid=%s and title=%s





select top 3 B.hID as NEWhID, count(distinct B.title) as NEWTotalOrders
                    from
                    (select*
                        from RecordOrders union
                    select *from RecordReturns)B
                    group by B.hID
                    order by NEWTotalOrders desc , B.hID


   select top 3 hID as hID,count(distinct title) as TotalOrders
                    from RecordReturns
                    group by hID
                    order by TotalOrders desc , hID














    select top 5 N.title as title ,N.r as rank
                                     from
                                     (select *,
                                         case
                                             when rank >=4 then rank
                                             else '0'
                                         end as r
                                         from ProgramRanks)N
                                     left join Programs on N.title=Programs.title where Programs.genre='Horror'
                                     order by N.r desc, N.title




create view titleRank as
SELECT Programs.title, count(ProgramRanks.rank) as Countrank,avg(ProgramRanks.rank) avgRank
    FROM ProgramRanks join Programs on Programs.title=ProgramRanks.title
where genre='Comedy'
group by Programs.title



select C.title as title, c.Avgrank as Avgrank
    from
(select B.title as title, isnull(A.avgRank,0) as Avgrank
    from
(select Countrank,title
 from( SELECT Programs.title, count(ProgramRanks.rank) as Countrank
    FROM ProgramRanks join Programs on Programs.title=ProgramRanks.title

group by Programs.title)TitleRank)B

left join



(select *
    from( SELECT Programs.title, count(ProgramRanks.rank) as Countrank ,cast(avg(cast(ProgramRanks.rank as decimal(10,2))) as decimal(10,2)) as avgRank
    FROM ProgramRanks join Programs on Programs.title=ProgramRanks.title

group by Programs.title)TitleRanks

where Countrank>=3)A
 ON A.title=B.title)
C inner join Programs on Programs.title=C.title where genre='Comedy'
order by Avgrank DESC, C.title








  select hid, ChildrenNum
     from Households
      where ChildrenNum>0 and hid=28


  (select title
            from programs
              where title='Zoey 101'









