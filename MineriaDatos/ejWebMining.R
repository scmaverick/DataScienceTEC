
# carga de paquetes requeridos

 library(tibble)
 library(stringr)
 library(rvest)
 library(FactoMineR)
 library(ggplot2)
 
 # se leen los datos de la página de interés usando read_html
 
  dirPag<-'https://en.wikipedia.org/wiki/List_of_highest-grossing_media_franchises'
  
  pag<- read_html(dirPag,encoding = 'UTF-8')  
  
 # se extraen específicamente las tablas que contenga la página
  
  tablasPag<- html_table(pag,fill=TRUE)
  
  length(tablasPag)
  
  tablasPag
  
 # obtener la tabla de interés, en este caso es la #3
  
   datosFranq<- tablasPag[[3]]
   
   datosFranq
  
  # Elegir las columnas de interés:  Franchise, Year of inception, Total Revenue
  # y Revenue breakdown.  La tabla ya está ordenada por Total Revenue por lo que
  # se descarta la columna Number
   
   datosFranq<-datosFranq[,c(2,3,4,5)]
   colnames(datosFranq)<-c('Franchise','YearOfInception','Revenue','RBreakdown')
  
   head(datosFranq)
  # Limpiar los datos 
  
  
   # se elimina el símbolo $ y el texto est. y billions del campo Revenue
   revenue<- str_remove(datosFranq$Revenue,'est\\.')
   revenue<- str_remove(revenue,'\\s*\\$')
   
   # se elimina palabras como billion, [] y su contenido
   revenue<- str_remove(revenue,'\\s+billion(\\[\\w+\\])*')
   
   # se convierte a numérico la variable
   
   revenue<-round(as.numeric(revenue),digits = 2)
   
   # limpieza del campo revenue breakdown.  Se elimnan $ \n espacios [] y su contenido, las palabras million y billion
   
   breakdown<-str_remove_all(datosFranq$RBreakdown,'\\n')
   
   breakdown<- str_remove_all(breakdown,'\\s*\\$\\d+((\\.|,)\\d+)?\\s*billion(\\[\\w+\\])*')
   breakdown<- str_remove_all(breakdown,'\\s*\\$\\d+((\\.|,)\\d+)?\\s*million(\\[\\w+\\])*')
   
   breakdown<-str_remove_all(breakdown,"[[:punct:]]")
   
   # se convierte a numérico el año
   year<- as.numeric(datosFranq$YearOfInception)
   
   # se conforma el data frame final
   
   datosFinal<- data.frame(datosFranq$Franchise,year,revenue,breakdown)
   colnames(datosFinal)<-c('Franchise','YearInception','Revenue','RevenueSources')
   
   # se eliminan datos faltantes
   
   datosFinal<-na.omit(datosFinal)
   
   # gráfico de barras ordenado descendentemente por Revenue
   
    
   ggplot(head(datosFinal,20),aes(x=reorder(Franchise,Revenue),y=Revenue))+
     geom_bar(stat = 'identity')  + coord_flip()+
     geom_text(mapping=aes(y=Revenue,label=Revenue),vjust = -1.5,color='white') +
     labs(title = 'Top 20 Franchises by revenue',subtitle = 'in $ billions',
          x='Franchise')
     theme(plot.title = element_text(hjust=0.5), plot.subtitle = element_text(hjust = 0.5))+
    theme_minimal()
       
   