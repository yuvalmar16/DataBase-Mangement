from django.shortcuts import render
from .models import Movies
from django.db import connection
from datetime import datetime


def dictfetchall(cursor):
    # Returns all rows from a cursor as a dict '''
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):
    return render(request, 'index.html')


def Query_Results(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                        select FinalTopGrossGenere.genre as genre, 
                        FinalTopGrossGenere.movieTitle as MaxGrossMovie, 
                        FinalTopGrossGenere.gross as MaxGrossMovieGross,
                         isnull((MoviesYear.yearNum),0) as YearCount ,
                        FinalTopLengthGENERE.movieTitle as MaxLengthMovie 
                        from
                        (select Movies.genre,gross, movieTitle
                            from Movies,
                        (select genre, max(gross) as maxGrossmovieGross
                            from Movies
                        group by genre)TopGrossGENERE
                        where TopGrossGENERE.genre=Movies.genre
                        and Movies.gross=TopGrossGENERE.maxGrossmovieGross and Movies.genre is not null) 
                        FinalTopGrossGenere
                            left join
                        (select Movies.genre,min (movieTitle) as movieTitle
                            from Movies,
                        (select genre, max(len(movieTitle)) as maxLengthMovieTitle
                            from Movies
                        group by genre)TopLengthGENERE
                        where TopLengthGENERE.genre=Movies.genre
                        and len(Movies.movieTitle)=maxLengthMovieTitle
                        group by Movies.genre) FinalTopLengthGENERE on 
                        FinalTopLengthGENERE.genre=FinalTopGrossGenere.genre
                        
                        left join
                        (select  genre,count (year) as yearNum
                            from
                        (select Movies.genre, year(Movies.releaseDate) as year, count(movieTitle) as MoviesNum
                            from Movies
                        group by genre, year(Movies.releaseDate)
                        having count(movieTitle)>1) MoviePerYear
                       group by genre)MoviesYear on FinalTopLengthGENERE.genre=MoviesYear.genre                
                         """)
        sql_res = dictfetchall(cursor)

        numberOfMovies=None
        if request.method == 'POST' and request.POST:
            numberOfMovies = request.POST["numberOfMovies"]
        cursor.execute("""
                        SELECT actorsMoviesSum.actor as Actor
                        ,actorsMoviesSum.moviesPlayedBy,
                         ActorsfirstMovieName.FirstMovieName as MovieName
                        FROM
                        (select  AIM.actor,count(distinct (movies.movieTitle)) as moviesPlayedBy
                        from Movies join ActorsInMovies AIM on Movies.movieTitle = AIM.movie
                        group by AIM.actor)actorsMoviesSum
                        
                        left join
                        
                         (select distinct (ActorsFirstMovieDate.actor)as actors, actorsMovies.movieTitle as FirstMovieName
                          from
                        (select AIM2.actor, min(Movies.releaseDate) as FirstDate
                        from Movies join ActorsInMovies AIM2 on Movies.movieTitle = AIM2.movie
                        group by AIM2.actor)ActorsFirstMovieDate
                        
                        left join
                        (select movies.movieTitle ,AIM3.actor, Movies.releaseDate
                        from Movies join ActorsInMovies AIM3 on Movies.movieTitle = AIM3.movie) actorsMovies
                        on ActorsFirstMovieDate.actor=actorsMovies.actor and ActorsFirstMovieDate.FirstDate=actorsMovies.releaseDate)ActorsfirstMovieName
                        on ActorsfirstMovieName.actors=actorsMoviesSum.actor
                        where actorsMoviesSum.moviesPlayedBy > %s
                        order by actorsMoviesSum.moviesPlayedBy desc
                                  """, [numberOfMovies])
        sql_res2 = dictfetchall(cursor)


        cursor.execute("""
                    select top 5 Movies.movieTitle as MovieName
                    , isnull(movieChildActors.ActorsNum,0) as NumberOfChildrenOnlyActors
                    from Movies
                    left join
                    
                    (select movie, count(distinct B.actors) ActorsNum
                    from ActorsInMovies
                    join
                    (select distinct (ActorsInMovies.actor) as actors
                    from ActorsInMovies join Movies M on M.movieTitle = ActorsInMovies.movie
                    where rating='G'
                    group by ActorsInMovies.actor
                    having (count(distinct movieTitle) >=4)
                    
                    except
                    (select distinct (AIM.actor)
                    From movies join ActorsInMovies AIM on Movies.movieTitle = AIM.movie
                    where rating='R')) B
                    on ActorsInMovies.actor=B.actors
                    group by movie)movieChildActors
                    on movieTitle=movieChildActors.movie
                    order by (ActorsNum)desc, movieTitle
                        """)
        sql_res3 = dictfetchall(cursor)
    return render(request, 'Query_Results.html', {'sql_res': sql_res, 'sql_res2': sql_res2,'sql_res3': sql_res3})


def add_movie(request):
    if request.method == 'POST' and request.POST:
        Movie_Title = request.POST["Movie Title"]
        Release_Date = request.POST["Release_Date"]
        Genre = request.POST["Genre"]
        Rating = request.POST["Rating"]
        gross = request.POST["gross"]
        new_content = Movies(Movie_Title=Movie_Title,
                             Release_Date=Release_Date,
                             Genere=Genre,
                             Rating=Rating, gross=gross)
        new_content.save()
    return render(request, 'Add_a_Movie.html')
