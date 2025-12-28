-- Clean (اختیاری ولی مفید برای تکرار seed)
TRUNCATE TABLE movie_ratings, genres_movie, movies, genres, directors RESTART IDENTITY CASCADE;

-- Directors
INSERT INTO directors (name, birth_year, description) VALUES
('Christopher Nolan', 1970, 'Known for mind-bending narratives.'),
('Quentin Tarantino', 1963, 'Known for stylized violence and dialogue.'),
('Greta Gerwig', 1983, 'Known for character-driven storytelling.');

-- Genres
INSERT INTO genres (name, description) VALUES
('Action', 'Action-packed movies'),
('Drama', 'Dramatic storytelling'),
('Sci-Fi', 'Science fiction movies'),
('Comedy', 'Comedy movies');

-- Movies
INSERT INTO movies (title, director_id, release_year, "cast") VALUES
('Inception', 1, 2010, 'Leonardo DiCaprio, Joseph Gordon-Levitt'),
('Interstellar', 1, 2014, 'Matthew McConaughey, Anne Hathaway'),
('Pulp Fiction', 2, 1994, 'John Travolta, Uma Thurman'),
('Barbie', 3, 2023, 'Margot Robbie, Ryan Gosling');

-- Movie <-> Genre relations
INSERT INTO genres_movie (movie_id, genre_id) VALUES
(1, 1), (1, 3),        -- Inception: Action, Sci-Fi
(2, 3), (2, 2),        -- Interstellar: Sci-Fi, Drama
(3, 1), (3, 2),        -- Pulp Fiction: Action, Drama
(4, 2), (4, 4);        -- Barbie: Drama, Comedy

-- Ratings (score 1..10)
INSERT INTO movie_ratings (movie_id, score) VALUES
(1, 9), (1, 10), (1, 8),
(2, 9), (2, 9),
(3, 10), (3, 9),
(4, 7), (4, 8);
