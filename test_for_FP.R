library(dplyr)

chess_puzzles <- read.csv("lichess_db_puzzle.csv")

chess_puzzles$RatingDeviation <- NULL
chess_puzzles$GameUrl <- NULL
chess_puzzles$Popularity <- NULL
chess_puzzles$NbPlays <- NULL

filtered_chess_puzzles <- chess_puzzles %>%
  filter(Rating >=1000 & Rating <= 1750)

filtered_chess_puzzles$Themes <- strsplit(filtered_chess_puzzles$Themes, " ")

include_values <- c("middlegame")
exclude_values <- c("mate", "oneMove")

filtered_chess_puzzles <- filtered_chess_puzzles %>%
  rowwise() %>%
  filter(any(Themes %in% include_values)) %>%
  filter(!any(Themes %in% exclude_values)) %>%
  ungroup()

# Checkers for debugging:
#filtered_chess_puzzles$Themes[[1]] # Should return a character list
#any(filtered_chess_puzzles$Themes[[1]] %in% include_values) # Should return true
#class(filtered_chess_puzzles$Themes[[1]]) # Should be character
#str(filtered_chess_puzzles$Themes)
#getwd() # Check that the file is written to this directory

filtered_chess_puzzles$OpeningTags <- NULL
filtered_chess_puzzles$Moves <- NULL
filtered_chess_puzzles$Themes <- NULL
filtered_chess_puzzles$Rating <- NULL

file_path <- "filtered_lichess.csv"
write.csv(filtered_chess_puzzles, file = file_path, row.names = FALSE)

