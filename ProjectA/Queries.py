QUERY_ANSWERS = {
    "Q3":
        """

select familyWithClass.hid, count(D.dID) as DeviceNum
from familyWithClass inner join Devices D on familyWithClass.hID=D.hID
group by familyWithClass.hid;


        """
    ,
    "Q4":
        """


select firstShowsWatched.hID ,firstShowsWatched.title,firstShowsWatched.eTime  as eventTime
    from (SELECT hID from modernFamily group by hID having count(pcode)>=3) modernFamilyMoreThanThree, firstShowsWatched
where firstShowsWatched.hID=modernFamilyMoreThanThree.hID
order by  (firstShowsWatched.eTime ),firstShowsWatched.hID



        """
}