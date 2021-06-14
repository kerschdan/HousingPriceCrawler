# HousingPriceCrawler

Web crawler for finding an undervalued property on behalf of a family member. 

The program queries a real estate listing homepage for all apartments that fulfill certain criterias. From the result page, all URLs of the corresponding apartments are gathered. A request is sent for each URL and the relevant information is extracted from the page. Finally, all data is collected in a dataframe and exported to a .csv file.
