library(tidyverse)

data <- read.csv("F:/Ohjelmointitiedostot/MoominUniverse/speakers_csv/allcompressed.csv")

datat <- read.csv("F:/Ohjelmointitiedostot/MoominUniverse/Global_speaker_ids/global_speaker_ids_0.9_modifyed.csv")


new_data <- left_join(data, datat, by = join_by(speaker == Speaker_ID))


new_data_inner <- inner_join(data, datat, by = join_by(speaker == Speaker_ID))


threshold <- -2.5   # Adjust this value as needed

# Initialize a new column to indicate if they are speaking to each other
new_data_inner$Speaking_To_Each_Other <- NULL

# Loop through the data to check time differences
for (i in 1:(nrow(new_data_inner) - 1)) {
  time_diff <- new_data_inner$start[i + 1] - new_data_inner$stop[i]
  if (time_diff > threshold) {
    new_data_inner$Speaking_To_Each_Other[i + 1] <- new_data_inner$Global_ID[i]
  }
}

# View the updated data frame
print(data)

new_data_inner$start - new_data_inner$stop

new_data_inner %>% count(Speaking_To_Each_Other, Global_ID)


result_df <- data.frame()

for (i in 1:(nrow(new_data_inner) - 1)) {
  temp_row <- new_data_inner[i, ]
  
  time_diff <- new_data_inner$start[i + 1] - new_data_inner$stop[i]
  
  if (time_diff > threshold) {
    new_data_inner$Speaking_To_Each_Other[i] <- new_data_inner$Global_ID[i+1]
  }
  
  result_df <- rbind(result_df, temp_row)
}

result_df %>% count(Speaking_To_Each_Other, Global_ID)

final_data <- result_df %>% filter(Speaking_To_Each_Other != Global_ID)

write.csv(final_data, "final_data.csv", row.names = F)
