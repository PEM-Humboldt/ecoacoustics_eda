library(tuneR)
library(seewave)
library(ggplot2)

# Get metadata information from a list of files
# Parameters
# ----------
# flist: file list with path to all files to be processed
# path_files = path where audio files are located
# verbose: boolean
# rec_model: either 'SM' (songmeter) or 'AU' (audiomoth)
metadata_audio <- function(flist, path_files='.', verbose=T, rec_model='SM'){
  audio_info = list()
  for(fname in flist){
    
    if(verbose){
      cat(paste(which(fname==flist),'/',length(flist),': ', fname,'\n', sep=''))
    }
      # get info from wave header
    fname_path = paste(path_files, fname, sep='')
    file_header = as.data.frame(readWave(fname_path, header = T))
    audio_info[[fname]] = file_header
    
    # get info from file
    audio_info[[fname]]$fsize = file.info(fname_path)$size
    audio_info[[fname]]$fname_audio = fname
    
    # get info from filename
    if (rec_model=='SM')
      {
      cat('Songmeter recorder \t')
      sm_info = songmeter(gsub('__0__','_0_',fname))
      audio_info[[fname]]$sm_model = sm_info$model
      audio_info[[fname]]$sensor_name = sm_info$prefix
      audio_info[[fname]]$date = format(sm_info$time, format = "%Y-%m-%d %H:%M:%S")
      audio_info[[fname]]$length = round(file_header$samples/file_header$sample.rate,2)
      }
    else if (rec_model=='AU')
      {
      cat('Audiomoth recorder \t')
      aux = strsplit(fname,'/')[[1]]
      fname_audio_wav = aux[[length(aux)]] # name of file with no path to files
      rec_info = strsplit(fname_audio_wav,'_')[[1]]
      audio_info[[fname]]$recorder_model = 'Audiomoth'
      audio_info[[fname]]$sensor_name = rec_info[1]
      audio_info[[fname]]$date = strptime(paste(rec_info[2], substr(rec_info[3],1,6)), format = '%Y%m%d %H%M%S')
      audio_info[[fname]]$time = substr(rec_info[3],1,6)
      audio_info[[fname]]$length = round(file_header$samples/file_header$sample.rate,2)
      }
  }
  
  df = do.call(rbind, audio_info)
  row.names(df) <- NULL
  df = cbind(df['fname_audio'],df[,-which(names(df)=='fname_audio')])
  return(df)
}

# Plot sampling
plot_sampling <- function(xdata, y_axis_factor, color_factor, shape_factor, plot_title){
  xdata$date = as.POSIXct(strptime(xdata$date, format = "%Y-%m-%d %H:%M:%S"))
  base_plot <- ggplot(data = xdata) +
    geom_point(aes(x = date, y=y_axis_factor, color=color_factor, shape=shape_factor), 
               alpha = 0.4,
               size = 3) +
    labs(x = "Date", 
         y = "Recording",
         title = plot_title) +
    theme_minimal()
  
  base_plot
}
