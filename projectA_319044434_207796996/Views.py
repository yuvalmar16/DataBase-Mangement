VIEWS_DICT = {
    "Q3":
        [
"""create view [bigRichFamily] as
select  *
from Households  where size>=3 and netWorth>5""",
            """create view [familyWithClass] as (
select distinct (bigRichFamily.hID)
from bigRichFamily
except
(select distinct(bigRichFamily.hID)
from bigRichFamily inner join Devices D on bigRichFamily.hID=D.hID
inner join Viewing V on D.dID = V.dID inner join Programs P on P.pCode=V.pCode
where p.genre ='Reality'))"""
        ]
    ,
    "Q4":
        [
            """create view LongestPrograms as
select Programs.pCode
from Programs where Programs.genre is not null
except (select p1.pCode
from Programs P1 ,Programs P2
where p1.genre=P2.genre and P1.genre is not null
and p1.pCode != P2.pCode and P1.duration<=P2.duration);
""",
            """create view PopularShow as
select DISTINCT V.pCode
from Devices d INNER JOIN  Viewing V on d.dID = V.dID
INNER JOIN LongestPrograms LP on V.pCode = LP.pCode
GROUP BY V.pCode HAVING COUNT(distinct D.hID)>=3;
""",
            """CREATE  VIEW modernFamily AS
select   distinct PopularShow.pCode ,D.hID
from LongestPrograms inner join PopularShow on LongestPrograms.pCode=LongestPrograms.pCode inner join Viewing
on PopularShow.pCode=Viewing.pCode inner join Devices D on D.dID = Viewing.dID
"""
            ,
"""create view longAndPopular as (select LongestPrograms.pCode, D.hID, v.eTime, p.title from PopularShow
    inner join  LongestPrograms on PopularShow.pCode = LongestPrograms.pCode
    inner join Viewing v on v.pCode=PopularShow.pCode
    inner join Devices D on D.dID = v.dID
    inner join Programs P ON v.pCode = P.pCode)""",
            
            """create  view firstShowsWatched as
(select longAndPopular.eTime, longAndPopular.title, longAndPopular.hID
from longAndPopular
except
(select  l1.eTime, l1.title,l1.hID
    from longAndPopular l1,longAndPopular l2 where l1.hid=l2.hid and l1.eTime>l2.eTime));"""
            ,
        ]
}

