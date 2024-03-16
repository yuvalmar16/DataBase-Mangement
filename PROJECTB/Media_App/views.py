from django.shortcuts import render
from .models import RecordOrders, Programs
from .models import RecordReturns
from .models import ProgramRanks
from .models import Households
from django.db import connection
from datetime import datetime


def dictfetchall(cursor):
    # Returns all rows from a cursor as a dict '''
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):
    return render(request, 'index.html')


# -------------------Query_Results
def Query_Results(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                        select genre, min(title) as title, duration
                        from  max_len_A_programs
                        group by genre, duration
                        order by genre

                         """)
        sql_res = dictfetchall(cursor)

        ########### to fix
        cursor.execute("""
                            select totalRate.title as title,totalRate.rate as AverageRank
                            from totalRate join CosherSum CS on totalRate.title = CS.title where CS.cosher>=3
                            ORDER BY rate desc , title
                                  """, )
        sql_res2 = dictfetchall(cursor)

        cursor.execute("""
                        select  prestigiousShow.title as title
                        from prestigiousShow
                        except
                        (select prestigiousShow.title
                         from prestigiousShow
                                  join ProgramRanks on prestigiousShow.title = ProgramRanks.title and ProgramRanks.rank < 2)
                        order by title
                        """)
        sql_res3 = dictfetchall(cursor)
    return render(request, 'Query_Results.html', {'sql_res': sql_res, 'sql_res2': sql_res2, 'sql_res3': sql_res3})


# ---------------------------------RECORD MANAGMENT

def Records_Management(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                      select top 3 B.hID as NEWhID, count(distinct B.title) as NEWTotalOrders
                      from
                      (select*
                          from RecordOrders union
                      select *from RecordReturns)B
                      group by B.hID
                      order by NEWTotalOrders desc , B.hID
                                  """)
        sql_res5 = dictfetchall(cursor)

        if 'submitOrder' in request.POST and 'submitReturn' not in request.POST:
            ErrorOrder = Records_Management_Order(request)
            # there is an error in order
            if ErrorOrder != [{""}]:
                return render(request, 'Records_Management.html', {'ErrorOrder': ErrorOrder, 'sql_res5': sql_res5})

        if 'submitReturn' in request.POST and 'submitOrder' not in request.POST:
            ErrorReturn = Records_Management_Return(request)
            if ErrorReturn != [{""}]:
                return render(request, 'Records_Management.html', {'ErrorReturn': ErrorReturn, 'sql_res5': sql_res5})

        if 'submitOrder' in request.POST and 'submitReturn' in request.POST:
            ErrorOrder = Records_Management_Order(request)
            ErrorReturn = Records_Management_Return(request)
            if ErrorOrder != [{""}] and ErrorReturn != [{""}]:
                return render(request, 'Records_Management.html', {'ErrorOrder': ErrorOrder,
                                                                   'ErrorReturn': ErrorReturn, 'sql_res5': sql_res5})
        return render(request, 'Records_Management.html', {'sql_res5': sql_res5})


def Records_Management_Order(request):
    with connection.cursor() as cursor:
        hidOrder = None
        titleOrder = None

        if request.method == 'POST' and request.POST["hidOrder"]:
            hidOrder = request.POST["hidOrder"]
        if request.method == 'POST' and request.POST["titleOrder"]:
            titleOrder = request.POST["titleOrder"]

        ErrorOrder = None
        ErrorOrder = checkInputOrder(hidOrder, titleOrder)
        if ErrorOrder != [{""}]:
            return ErrorOrder

        # you can add this Order
        new_Order = RecordOrders(title=Programs(title=titleOrder),
                                 hID=Households(hID=hidOrder))
        new_Order.save()

    return False


def Records_Management_Return(request):
    with connection.cursor() as cursor:
        ErrorReturn = None
        if request.method == 'POST' and request.POST["hidReturn"]:
            hidReturn = request.POST["hidReturn"]
        if request.method == 'POST' and request.POST["titleReturn"]:
            titleReturn = request.POST["titleReturn"]
        ErrorReturn = checkInputReturn(hidReturn, titleReturn)

        if ErrorReturn != [{""}]:
            return ErrorReturn

        deleteFromOrders = RecordOrders(title=Programs(title=titleReturn),
                                        hID=Households(hID=hidReturn))
        deleteFromOrders.delete()

        AddToReturns = RecordReturns(title=Programs(title=titleReturn),
                                     hID=Households(hID=hidReturn))
        AddToReturns.save()
    return False


def checkInputOrder(hidOrder, titleOrder):
    # family check
    with connection.cursor() as cursor1:
        # family doesnt exists
        cursor1.execute("""
                select hid
                    from Households
                where hid=%s
                     """, [hidOrder])
        val1 = dictfetchall(cursor1)
        if val1 == []:
            return "  This Family Doesn't exist"

        # title check
    with connection.cursor() as cursor2:
        # title doesnt exists
        cursor2.execute("""
                   select title
                    from programs
                    where title=%s
                         """, [titleOrder])
        val2 = dictfetchall(cursor2)
        if (val2 == []):
            return "  This title Doesn't exist"

        # already have 3
    with connection.cursor() as cursor3:
        cursor3.execute("""
                                    select hid,titles
                                    from
                                    (select  hid, count(distinct(title)) as titles
                                        from RecordOrders
                                    group by hid)T
                                    where hid=%s and titles<3
                                    """, [hidOrder])
        val3 = dictfetchall(cursor3)
        if (val3 == []):
            return "  This family already have 3 movies"

        # already been ordered by other family
    with connection.cursor() as cursor4:
        cursor4.execute("""
                                    select *
                                    from RecordOrders
                                    where title=%s and hID!=%s
                                        """, [titleOrder, hidOrder])
        val4 = dictfetchall(cursor4)
        if val4 != []:
            return "  another family already booked this movie"

        # the family already ordered this film and have it
    with connection.cursor() as cursor5:
        cursor5.execute("""
                                           select *
                                             from RecordOrders
                                           where title=%s and hID=%s
                                               """, [titleOrder, hidOrder])
        val5 = dictfetchall(cursor5)
        if val5 != []:
            return "  the family already booked this movie"

        # the family booked this film in the past
    with connection.cursor() as cursor6:
        cursor6.execute("""
                                        select  *
                                        from RecordReturns
                                        where title=%s and hID=%s
                                                     """, [titleOrder, hidOrder])
        val5 = dictfetchall(cursor6)
        if val5 != []:
            return "  the family already booked this movie in the past"

        # ordered adults only and have kids
    with connection.cursor() as cursor7:
        cursor7.execute("""
                                            select hid, ChildrenNum
                                            from Households
                                            where ChildrenNum>0 and hid=%s
                                                         """, [hidOrder])
        val6A = dictfetchall(cursor7)
        # they have kids
        if val6A != []:
            with connection.cursor() as cursor8:
                cursor8.execute("""
                                                      select title
                                                       from Programs
                                                       where (genre ='Adults only' or genre ='Reality')
                                                       and title=%s   
                                                       """, [titleOrder])
                val6B = dictfetchall(cursor8)
                # the movie is for adults
                if val6B != []:
                    return "  this movie is for Adults"

    return [{""}]


def checkInputReturn(hidReturn, titleReturn):
    # check if family exists
    with connection.cursor() as cursor1:
        # family doesn't exist
        cursor1.execute("""
                    select hid
                    from Households
                    where hid=%s
                        """, [hidReturn])
        val1 = dictfetchall(cursor1)
        if val1 == []:
            return "  This Family Doesn't exist"

    with connection.cursor() as cursor2:
        # title doesnt exist
        cursor2.execute("""
                 select title
                 from programs
                 where title=%s 
                """, [titleReturn])

        val2 = dictfetchall(cursor2)
        if val2 == []:
            return "  This title doesn't exists"

    with connection.cursor() as cursor3:
        # title exist but the family don't have it
        cursor3.execute("""
                 select *
                 from RecordOrders
                 where (title=%s and hID=%s) 
                """, [titleReturn, hidReturn])

        val3 = dictfetchall(cursor3)
        if val3 == []:
            return "  this title exists but the family doesn't posses it "

    return [{""}]


# rankings-------------------


def Rankings(request):
    with connection.cursor() as cursor:
        hidRank = None
        newRank = None
        titleRank = None
        if request.method == 'POST' and 'submit1' in request.POST:
            if request.method == 'POST' and request.POST["hidRank"]:
                hidRank = request.POST["hidRank"]
            if request.method == 'POST' and request.POST["titleRank"]:
                titleRank = request.POST["titleRank"]
            if request.method == 'POST' and request.POST["Rank"]:
                newRank = request.POST["Rank"]

            AddRank(hidRank, titleRank, newRank)

        cursor.execute("""
                             SELECT  T.genre as genre
                             from
                        (select  count(distinct title) as  titleNum, genre
                            from programs
                        group by genre)T
                             where titleNum>=5
                        order by titleNum desc          
                            """)
        SelectResult = dictfetchall(cursor)

        resultTop5 = None
        Genre = None
        minRank = None
        if request.method == 'POST' and 'submit2' in request.POST:
            if request.method == 'POST' and request.POST["minRank"]:
                minRank = request.POST["minRank"]
            if request.method == 'POST' and request.POST["Genre"]:
                Genre = request.POST["Genre"]
            print(Genre, minRank)
            cursor.execute("""
                                   select Top 5 C.title as title, c.Avgrank as Avgrank
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
                                    
                                    where Countrank>=%s)A
                                     ON A.title=B.title)
                                    C inner join Programs on Programs.title=C.title where genre=%s
                                    order by Avgrank DESC, C.title

                                      """, [minRank, Genre])

            resultTop5 = dictfetchall(cursor)

        return render(request, 'Rankings.html', {'SelectResult': SelectResult, 'resultTop5': resultTop5})


def AddRank(hidRank, titleRank, newRank):
    with connection.cursor() as cursor:
        print(hidRank,titleRank,newRank)
        cursor.execute("""
                select *
                from ProgramRanks
                where  title=%s and hid=%s """,[titleRank,hidRank])
        val = dictfetchall(cursor)
        if val != []:

            cursor.execute(""" update ProgramRanks
                              set rank=%s
                                where title=%s and hid=%s
                               """, [newRank,titleRank, hidRank])

        else:
            AddToRanks = ProgramRanks(title=Programs(title=titleRank), hID=Households(hID=hidRank), rank=newRank)
            AddToRanks.save()
