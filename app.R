                #### MET-k Version 1.8.2 ####
#### MGRS Extraction Toolkit (MET-k) is an RShiny web application
#### with a Python backend, which can extract MGRS coordinates from 
#### .xlsx, .csv, and .txt files, convert the coordinates to Lat/Lon
#### and generate a .kmz file with the extracted information.

# Created by Kevan White (thyripian) - 2022


library(shiny)
library(reticulate)
library(shinyjs)
library(shinyWidgets)

options(shiny.maxRequestSize=38*1024^2)

reticulate::source_python('./core_primary.py')

# Define UI with HTML/CSS formatting.
ui <- fluidPage(

	# import CSS formatting
	tags$head(
		tags$link(rel = 'stylesheet',type='text/css', href = 'MET-k_style.css')
	),
	
	# create page banner
	div(
		id = '#my_banner',
		style = 'height:20px;background-color:[INSERT COLOR OPTION];width:auto;margin:0;position:relative;padding:0px 10px;',
		tags$p('[INSERT BANNER TEXT HERE]')
	),
	
	# name page
	title = 'MET-k: MGRS Extraction Toolkit',
	
	# allow Shiny Javascript functionality
	useShinyjs(),
	
	# display application name and format font
	div(
		id = 'my_title',
		titlePanel(h1('MGRS Extraction Toolkit(MET-k)'))
	),
	
	# sidebar with file upload section
	sidebarLayout(
		sidebarPanel(
			fileInput('upload','Upload a file...',width=300,multiple=TRUE,accept=c('xlsx','csv','txt')),
			
			h4('Coordinate Extraction Progress'),
			progressBar(id='pbar1',value=0,display_pct=T),
			
			selectInput('select','Choose a coordinate display format...',choices=c('MGRS','Lat/Lon')),
			
			downloadButton('download_kmz','Download KMZ'),
			downloadButton('download_csv','Download CSV'),
			
			div(HTML('</br>')),
			div(
				HTML('<center>'),
				id = '#my_contact_button',
				a(
					actionButton(
							inputId = 'support',
							label = 'Contact Us',
							icon = icon('envelope',lib = 'font_awesome')
							),
					href='mailto:[INSERT CONTACT EMAIL HERE]?body=I have a suggestion or have identified an issue with MET-k.
					%0D%0A---------------------------------------------------------------------------------------------
					%0D%0A
					DETAILS:
					%0D%0A
					&subject=MET-k Suggestion or Issue',
				)	
			),
			
			div(
				HTML('<center>'),
				id = 'my_reset_button',
				actionButton(
						inputId = 'page_reset',
						label = 'Reset Page'
				)
			)
		),
		
		# show the extracted coordinates in the table on the main panel
		mainPanel(
			div(
				id = '#my_progress',
				h4('Data Rendering Progress'),
				progressBar(id='pbar2',value=0,display_pct=T),
			),
			div(
				id = '#my_table',
				dataTableOutput('display')
			)
		)
	),
	
	div(
		id = '#my_footer',
		style = 'height:20px;background-color:[INSERT COLOR OPTION];width:auto;margin:0;position:relative;padding:0px 10px;',
		tags$p('[INSERT BANNER TEXT HERE]')
	)
)

# Define server logic to allow file upload, Python package usage, MGRS list visualization, and file download.
server <- function(input, output, session) {
	shinyjs::disable('download_kmz')
	shinyjs::disable('download_csv')
	
	# display pop-up message on page load
	{
		observeEvent(session, {
			showModal(
				modalDialog(
					title = h3('[INSERT MESSAGE TITLE]'),
					size = 'l',
					easyClose = F,
					footer = modalButton('OK'),
					HTML(
						'[INSERT MESSAGE CONTENT]'
					)
				)
			)
		})
	}
	
	observeEvent(input$page_reset, {
		session$reload()
	})
	
	observeEvent(input$support, {
	
	})
	
	observeEvent(input$upload, {
		req(input$upload)
		
		max_i <- 100
		
		# run backend and show progress
		for (i in 1:50) {
			updateProgressBar(session=session,id='pbar1',value=(i))
			Sys.sleep(0.1)
		}
		shinyjs::disable('upload')
		
		upload_names <- eventReactive(input$upload, {
			name_list <- as.list(input$upload$name)
		})
		
		upload_datapath <- eventReactive(input$upload, {
			datapath_list <- as.list(input$upload$datapath)
		})
		
		toolkit <- reactive({TOOLKIT(input_file=upload_datapath(),name=upload_names())})
		
		for (i in 50:80) {
			updateProgressBar(session=session,id='pbar1',value=(i))
			Sys.sleep(0.1)
		}
		
		observeEvent(input$select, {
			for (i in 80:95) {
				updateProgressBar(session=session,id='pbar1',value=(i))
				Sys.sleep(0.1)
			}
			
			showModal(
				modalDialog(
					title=h4('Status'),
					size = 's',
					easyClose = F,
					footer = modalButton('OK'),
					toolkit()$status,
				)
			)
			
			output$display <- renderDataTable({
				req(input$select)
				req(toolkit())
				
				updateProgressBar(session=session,id='pbar1',value=100)
				
				for (i in 1:50) {
					updateProgressBar(session=session,id='pbar2',value=i)
					Sys.sleep(0.1)
				}
				
				if (input$select == 'MGRS') {
					for (i in 50:100) {
						updateProgressBar(session=session,id='pbar2',value=i)
						Sys.sleep(0.1)
					}
					updateProgressBar(session=session=id='pbar1',value=0)
					updateProgressBar(session=session,id='pbar2',value=0)
					
					return(toolkit()$mgrs_df)
				}
				
				else if (input$select == 'Lat/Lon') {
					for (i in 50:100) {
						updateProgressBar(session=session,id='pbar2',value=i)
						Sys.sleep(0.1)
					}
					updateProgressBar(session=session=id='pbar1',value=0)
					updateProgressBar(session=session,id='pbar2',value=0)
					
					return(toolkit()$latlon_disp_df)
				}
			})
		})
		
		shinyjs::enable('download_kmz')
		shinyjs::enable('download_csv')
		
		output$download_kml <- downloadHandler)
			filename <- function() {
				'export.kmz'
			},
			content <- function(file) {
				write(toolkit()$kml(),file)
			},
			contentType = 'application/vnd.google-earth.kmz'
		)
		
		output$download_csv <- downloadHandler(
			filename <- function() {
				'export.csv'
			},
			content <- function(file) {
				write.csv(toolkit()$mgrs_df,file,row.names=FALSE)
			},
			contentType = 'text/csv'
		)
	}
}	

shinyApp(ui = ui, server = server)
