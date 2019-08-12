library(tidyverse)
library(tidyquant)
library(shiny)

# Data prep
#setwd("C:/Kaggle/googlemerchandise/webkpiapp/")
dtrain <- read.csv("train_new.csv")

dtrain$date <- ymd(dtrain$date)
dtrain$transactionRevenue <- as.numeric(dtrain$transactionRevenue)
dtrain$transactionRevenue[is.na(dtrain$transactionRevenue)] <- 0

dtrain$pageviews[is.na(dtrain$pageviews)] <- 0
dtrain$pageviews <- as.numeric(dtrain$pageviews)
dtrain$bounces[is.na(dtrain$bounces)] <- 0
dtrain$bounces <- as.numeric(dtrain$bounces)
dtrain$newVisits[is.na(dtrain$newVisits)] <- 0
dtrain$newVisits <- as.numeric(dtrain$newVisits)

ui <- fluidPage(
  #inputs - radio, kpi
  h1("Visualizing Web KPIs", align = "center"),
  fluidRow(
    column(width = 6,
           wellPanel(
             tags$p("This app allows us to visualize several Web Marketing KPIs at",tags$strong("Daily"),"and",tags$strong("Monthly"),"level"),
             tags$p("Zoom functionality is available in the Daily Chart on the left. Select an area and zoom in to isolate weekly patterns"),
             tags$p("Choose different KPIs from the drop down on the right"),
             tags$p("Data Used:",tags$strong(tags$i("Kaggle Google Merchandise Data")))
           )
    ),
    column(width = 6, 
           wellPanel(
             selectInput("kpi", 
                         label = h3("Choose the Web KPI"), 
                         choices = list("Mean Transaction Revenue" = "Mean_Transaction_Revenue",
                                        "Session level Conversion Rate" = "Session_Level_Conversion_Rate",
                                        "Bounced Sessions" = "Total_Sessions_Bounced",
                                        "Average Page Views" = "Mean_Page_Views",
                                        "New Visits" = "Total_New_Visits")
             )
           )
    )
  ),
  fluidRow(
    column(style='border-top: groove',
           width=6,
           h4("Daily Patterns", align = "center"),
           plotOutput("dailyplot", 
                      dblclick = "time_series_dblclick",
                      brush = brushOpts(
                        id = "time_series_brush",
                        resetOnNew = TRUE
                      )
           )
    ),
    column(style='border-top: groove;border-left: groove',
           width=6,
           h4("Monthly Patterns", align = "center"),
           plotOutput("monthplot"))
  )
)


server <- function(input, output){
  
  ranges <- reactiveValues(x = NULL, y = NULL)
  
  output$dailyplot = renderPlot({
    dtrain %>%
      group_by(date) %>%
      summarise(convertedSessionCount = sum(transactionRevenue>0), 
                numsessions = n(),
                Mean_Transaction_Revenue = mean(transactionRevenueNew),
                Total_Sessions_Bounced = sum(bounces),
                Mean_Page_Views = mean(pageviews),
                Total_New_Visits = sum(newVisits)
                ) %>%
      mutate(Session_Level_Conversion_Rate = convertedSessionCount/numsessions) %>% 
      ggplot(aes_string("date",input$kpi)) +
      geom_line(col = "blue", size=0.7) +
      coord_x_date(xlim = ranges$x, ylim = ranges$y, expand = FALSE) +
      theme(axis.title.x = element_text(size=20), 
            axis.title.y = element_text(size=20),
            axis.text.x = element_text(size=15, face="bold"), 
            axis.text.y = element_text(size=15, face="bold")) +
      labs(y = input$kpi, x = "Date") #+
      #theme_bw()
  })
  
  observeEvent(input$time_series_dblclick, {
    brush <- input$time_series_brush
    if (!is.null(brush)) {
      ranges$x <- c(brush$xmin, brush$xmax)
      ranges$y <- c(brush$ymin, brush$ymax)
      
    } else {
      ranges$x <- NULL
      ranges$y <- NULL
    }
  })
  
  output$monthplot = renderPlot({
    dtrain %>%
      group_by(month) %>%
      summarise(convertedSessionCount = sum(transactionRevenue>0), 
                numsessions = n(),
                Mean_Transaction_Revenue = mean(transactionRevenueNew),
                Total_Sessions_Bounced = sum(bounces),
                Mean_Page_Views = mean(pageviews),
                Total_New_Visits = sum(newVisits)
      )  %>%
      mutate(Session_Level_Conversion_Rate = convertedSessionCount/numsessions) %>%
      mutate(month = factor(month, month.abb)) %>%
      ggplot(aes_string("month", input$kpi)) +
      geom_col(color = "white", fill="red") +
      theme(legend.position = "none",
            axis.title.x = element_text(size=20),
            axis.title.y = element_text(size=20, vjust=1),
            axis.text.x  = element_text(size=15, face="bold"),
            axis.text.y = element_text(size=15, face="bold")) +
      labs(x = "Month", y = input$kpi)# +
    #  theme_bw()
  })
  
}



shinyApp(ui = ui, server = server)
