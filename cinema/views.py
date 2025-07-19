from rest_framework import viewsets

from .models import (
    Genre,
    Actor,
    CinemaHall,
    Movie,
    MovieSession
)
from .serializers import (
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    MovieSessionListSerializer,
    MovieSessionDetailSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class CinemaHallViewSet(viewsets.ModelViewSet):
    serializer_class = CinemaHallSerializer
    queryset = CinemaHall.objects.all()


class MovieViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return MovieListSerializer
        return MovieDetailSerializer

    def get_queryset(self):
        return Movie.objects.prefetch_related("actors", "genres")


class MovieSessionViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return MovieSessionListSerializer
        return MovieSessionDetailSerializer

    def get_queryset(self):
        return (
            MovieSession
            .objects
            .select_related("movie", "cinema_hall")
            .prefetch_related("movie__actors", "movie__genres")
        )
