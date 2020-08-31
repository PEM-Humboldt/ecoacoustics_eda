# Get list of audio files and associated metadata
# Author: Juan Sebastián Ulloa (julloa[at]humboldt.org.co)

# Load functions
source('audio_metadata_utilities.R')
# set variables
path_files = '~/Downloads/tmp/'  # Folder location of acoustic dataset
save_name = '~/Downloads/tmp/test.csv' # Filename of csv that will store the metadata
# ---------------

flist = list.files(path_files, recursive = T, pattern = '.WAV')
df = metadata_audio(flist, path_files, verbose = T, rec_model = 'AU')

## post-process to include factors or sites
# fname_audio
aux = strsplit(df$fname_audio, split = '/')
aux_df = as.data.frame(do.call(rbind, aux))
head(aux_df)
table(aux_df$V1)
df['site'] = aux_df$V1

# Check dataframe manually
head(df)
tail(df)
table(df$sensor_name)  # number of recordings per sensor
table(df$site)  # number of recordings per site

# plot sampling
plot_sampling(df, y_axis_factor = df$site, color_factor = df$site, shape_factor = df$site, plot_title = 'Example')

# save dataframe to csv
write.table(df, save_name, sep=',', col.names = TRUE, row.names = FALSE)

