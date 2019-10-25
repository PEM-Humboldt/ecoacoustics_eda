# Script adaptaado para hacer el plot de los metadatos guardados en el BSA

rm(list=ls())
library(gdata)
library(ggplot2)
source('audio_metadata_utilities.R')

# plot data
plot_title = 'Monitoreo acústico - Rumiyaco 2019'
fname = '../data_tables/rumiyaco.csv'
fname_png = '../figures/rumiyaco.png'

xdata = read.table(fname, sep=',', header = T)
head(xdata)
names(xdata)

xdata$date_posx = as.POSIXct(strptime(xdata$date, format = "%Y-%m-%d %H:%M:%S"))

## plot
png(fname_png, height = 500, width = 1200, pointsize = 12, res=100)

base_plot <- ggplot(data = xdata) +
  geom_point(aes(x = date_posx, 
                 y = sensor_name, 
                 color=sensor_name), 
             alpha = 1,
             size = 3) +
  labs(x = "Fecha", y = "Grabadora", title = plot_title) +
  theme_minimal()
base_plot

dev.off()


## ------------- combine data from all sites ------- ##
rm(list=ls())
setwd('~/Dropbox/PostDoc/iavh/Putumayo/audio_metadata/data_tables/')
flist = list.files('.', pattern = '.csv')

file_csv = list()
for(fname_csv in flist){
  file_csv[[fname_csv]] = read.table(fname_csv, header = T, sep=',')
  file_csv[[fname_csv]]$cuadrante = substr(fname_csv,1, nchar(fname_csv)-4)
}

df = do.call(rbind, file_csv)
row.names(df) <- NULL

## plot data
library(plyr)

fname_png = 'Putumayo_summary_3.png'
names(df)
df$date_posx = as.POSIXct(strptime(df$date, format = "%Y-%m-%d %H:%M:%S"))

df$Cuadrante = factor(df$cuadrante)
df$Cuadrante = revalue(df$Cuadrante, c('platanillo'='Platanillo', 'rumiyaco'='Rumiyaco', 'venado'='Venado'))

png(fname_png, height = 500, width = 1000, pointsize = 12, res=100)
base_plot <- ggplot(data = df) +
  geom_point(aes(x = date_posx, 
                 y = plot, 
                 color=Cuadrante), 
             alpha = 1,
             size = 3) +
  labs(x = "Fecha", y = "Punto de muestreo") +
  theme_minimal()
base_plot

dev.off()
