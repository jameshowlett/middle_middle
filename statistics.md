# Macroeconomic Statistics


+ Interest Rates Announcement:
	
	Interest rates play the most important role in moving the prices of currencies in the foreign exchange market. As the institutions that set interest rates, central banks are therefore the most influential actors. Interest rates dictate flows of investment. Since currencies are the representations of a country’s economy, differences in interest rates affect the relative worth of currencies in relation to one another. When central banks change interest rates they cause the forex market to experience movement and volatility. In the realm of Forex trading, accurate speculation of central banks’ actions can enhance the trader's chances for a successful trade.

+ Gross Domestic Product (GDP):

	Multiple definitions:
	
	1. The GDP is the broadest measure of a country's economy, and it represents the total market value of all goods and services produced in a country during a given year.
	2. OECD defines GDP as "an aggregate measure of production equal to the sum of the gross values added of all resident, institutional units engaged in production (plus any taxes, and minus any subsidies, on products not included in the value of their outputs).”
	3. Wikipedia defines GDP as "a monetary measure of the value of all final goods and services produced in a period of time (quarterly or yearly)"
	
	There are three ways to calculate this:
	
	1. Production approach:
		1. Estimate the gross value of domestic output out of the many various economic activities (industries);
		2. Determine the intermediate consumption, i.e., the cost of material, supplies and services used to produce final goods or services.
		3. Deduct intermediate consumption from gross value to obtain the gross value added.
		
		```
		gross_value_added = [ ]
		for industry in industries:
			gross_value_added[industry] = gross_value(output, industry) - \
										  value(intermediate_consumption, industry)

		GDP_at_factor_cost = sum(gross_value_added)
		GDP_at_product_price = GDP_at_factor_cost + indirect_taxes - product_subsidies
		```
	2. Income approach:
		
		```
		GDP = COE + GOS + GMI + TPM - SPM
		    = total_factor_income + TPM - SPM
		```
		+ `COE` is _compensation of employees_. It includes wages and salaries, as well as employer contributions to social security and other such programs.
		+ `GOS` is _gross operating surplus_. Often called profits, although only a subset of total costs are subtracted from gross output to calculate GOS.
		+ `GMI` is _gross mixed income_ is the same measure as `GOS`, but for unincorporated businesses. This often includes most small businesses.
		+ `TPM` is _taxes on productions and imports_.
		+ `SPM` is _subsidies on productions and imports_.
	
	3. Expenditure approach:
	
		The third way to estimate GDP is to calculate the sum of the final uses of goods and services (all uses except intermediate consumption) measured in purchasers' prices.

		In economics, most things produced are produced for sale and then sold. Therefore, measuring the total expenditure of money used to buy things is a way of measuring production. This is known as the expenditure method of calculating GDP. Note that if you knit yourself a sweater, it is production but does not get counted as GDP because it is never sold. Sweater-knitting is a small part of the economy, but if one counts some major activities such as child-rearing (generally unpaid) as production, GDP ceases to be an accurate indicator of production. Similarly, if there is a long term shift from non-market provision of services (for example cooking, cleaning, child rearing, do-it yourself repairs) to market provision of services, then this trend toward increased market provision of services may mask a dramatic decrease in actual domestic production, resulting in overly optimistic and inflated reported GDP. This is particularly a problem for economies which have shifted from production economies to service economies.

		```
		GDP = C + I + G + (X − M)
		    = C + I + G + net_exports
		```
		
		+ `C` (consumption) is normally the largest GDP component in the economy, consisting of private (household final consumption expenditure) in the economy. These personal expenditures fall under one of the following categories: durable goods, non-durable goods, and services. Examples include food, rent, jewelry, gasoline, and medical expenses but does not include the purchase of new housing.
		+ `I` (investment) includes, for instance, business investment in equipment, but does not include exchanges of existing assets. Examples include construction of a new mine, purchase of software, or purchase of machinery and equipment for a factory. Spending by households (not government) on new houses is also included in investment. In contrast to its colloquial meaning, "investment" in GDP does not mean purchases of financial products. Buying financial products is classed as 'saving', as opposed to investment. This avoids double-counting: if one buys shares in a company, and the company uses the money received to buy plant, equipment, etc., the amount will be counted toward GDP when the company spends the money on those things; to also count it when one gives it to the company would be to count two times an amount that only corresponds to one group of products. Buying bonds or stocks is a swapping of deeds, a transfer of claims on future production, not directly an expenditure on products.
		+ `G` (government spending) is the sum of government expenditures on final goods and services. It includes salaries of public servants, purchases of weapons for the military and any investment expenditure by a government. It does not include any transfer payments, such as social security or unemployment benefits.
		+ `X` (exports) represents gross exports. GDP captures the amount a country produces, including goods and services produced for other nations' consumption, therefore exports are added.
		+ `M` (imports) represents gross imports. Imports are subtracted since imported goods will be included in the terms G, I, or C, and must be deducted to avoid counting foreign supply as domestic.

as

		- constant prices ???
		- per capita, constant prices ???
		- per hour worked, constant prices ???

+ Labour utilisation (=hours worked per head of population):
	
	For productivity analysis, the underlying concept for labour input is total hours worked by all persons engaged in production. These reflect regular hours worked by full-time and part-time workers, paid and unpaid overtime, hours worked in additional jobs, and time not worked because of public holidays, annual paid leave, strikes and labour disputes and other reasons.

+ Average hours worked per person employed
+ Total hours worked
+ Total capital services:

	For productivity analysis, the preferred measure of capital input is the flow of productive services that can be drawn from the cumulative stock of past investments. These services are estimated by the OECD using the rate of change of the productive capital stock, which takes into account wear and tear, retirements and other sources of reduction in the productive capacity of fixed capital assets. The price of capital services per asset is measured as their rental price. In principle, the latter could be directly observed if markets existed for all capital services. In practice, however, rental prices have to be imputed for most assets, using the implicit rent that capital goods’ owners ‘pay’ to themselves (or the user costs of capital). 

	Estimates of capital services in the OECD Productivity Database can be broken down by eight types of assets: computer hardware, telecommunications equipment, transport equipment, other machinery and equiment and weapons systems, non-residential construction, computer software and databases, research and development and other intellectual property products. To ensure comparability across countries, the OECD capital services measures are based on a common computation method for all countries.

+ Consumer Price Index:

	The Consumer Price Index (CPI) is probably the most crucial indicator of inflation. It represents changes in the level of retail prices for the basic consumer basket. Inflation is tied directly to the purchasing power of a currency within its borders and affects its standing on the international markets. If the economy develops in normal conditions, the increase in CPI can lead to an increase in basic interest rates. This, in turn, leads to an increase in the attractiveness of a currency.

+ Employment Indicators:

	Employment indicators reflect the overall health of an economy or business cycle. In order to understand how an economy is functioning, it is important to know how many jobs are being created or destructed, what percentage of the work force is actively working, and how many new people are claiming unemployment. For inflation measurement, it is also important to monitor the speed at which wages are growing.

+ Retail Sales:

	The retail sales indicator is released on a monthly basis and is important to the foreign exchange trader because it shows the overall strength of consumer spending and the success of retail stores. The report is particularly useful because it is a timely indicator of broad consumer spending patterns that is adjusted for seasonal variables. It can be used to predict the performance of more important lagging indicators, and to assess the immediate direction of an economy.

+ Balance of Payments:
	
	The Balance of Payments represents the ratio between the amount of payments received from abroad and the amount of payments going abroad. In other words, it shows the total foreign trade operations, trade balance, and balance between export and import, transfer payments. If coming payment exceeds payments to other countries and international organizations the balance of payments is positive. The surplus is a favorable factor for growth of the national currency.

+ Government Fiscal and Monetary policy:

	Stabilization of the economy (e.g., full employment, control of inflation, and an equitable balance of payments) is one of the goals that governments attempt to achieve through manipulation of fiscal and monetary policies. Fiscal policy relates to taxes and expenditures, monetary policy to financial markets and the supply of credit, money, and other financial assets.
	
+ Purchasing Power Parities (PPPs):

	PPPs are the rates of currency conversion that equalize the purchasing power of different currencies by eliminating the differences in price levels between countries. In their simplest form, PPPs are simply price relatives that show the ratio of the prices in national currencies of the same good or service in different countries. PPPs are also calculated for product groups and for each of the various levels of aggregation up to and including GDP.
	
	- The calculation is undertaken in three stages. The first stage is at the product level, where price relatives are calculated for individual goods and services. A simple example would be a litre of Coca-Cola. If it costs 2.3 euros in France and 2.00$ in the United States then the PPP for Coca-Cola between France and the USA is 2.3/2.00, or 1.15. This means that for every dollar spent on a litre of Coca-Cola in the USA, 1.15 euros would have to be spent in France to obtain the same quantity and quality - or, in other words, the same volume - of Coca-Cola. The second stage is at the product group level, where the price relatives calculated for the products in the group are averaged to obtain unweighted PPPs for the group. Coca-cola is for example included in the product group “Softdrinks and Concentrates”. And the third stage is at the aggregation levels, where the PPPs for the product groups covered by the aggregation level are weighted and averaged to obtain weighted PPPs for the aggregation level up to GDP (in our example, aggregated levels are Non-alcoholic beverages, Food…). The weights used to aggregate the PPPs in the third stage are the expenditures on the product groups as established in the national accounts. You will find detailed information on the calculation in the “EUROSTAT-OECD Methodological manual on purchasing power parities (PPPs)”, Chapter 12, at www.oecd.org/std/ppp/manual.
	
# Economic Terms (wikipedia)

+ Good:

	In economics, a good is a material that satisfies human wants and provides utility. They can be:
	
	- tangible property -- still called a _good_
	- intangible property -- called a _service_
	
	Commodities may be used as a synonym for economic goods but often refer to marketable raw materials and primary products.
	
	> Anything that might be desired and provides 'utility' is a good...

+ Capital:

	In a fundamental sense, capital consists of any produced thing that can enhance a person's power to perform economically useful work—a stone or an arrow is capital for a caveman who can use it as a hunting instrument, and roads are capital for inhabitants of a city. Capital is an input in the production function. Homes and personal autos are not usually defined as capital but as durable goods because they are not used in a production of saleable goods and services.
	
	-  Capital is distinct from land (or non-renewable resources) in that capital can be increased by human labor. At any given moment in time, _total physical capital_ may be referred to as the __capital stock__ (which is not to be confused with the capital stock of a business entity).
	- __Capital goods__, real capital, or capital assets are already-produced durable goods or any non-financial asset that is used in production of goods or services.
	- __Capital services__ refer to a chain-type index of service flows derived from the stock of physical assets and software. These assets are coordination, equipment, software, structures, land, and inventories. Capital services are estimated as a capital-income weighted average of the growth rates of each asset. Capital services differ from capital stocks because short-lived assets such as equipment and software provide more services per unit of stock than long-lived assets such as land. Unlike capital goods, capital services are owned by the person or group of people providing them.

	> ... any produced thing that can enhance a person's power to perform economically useful work ...
	
+ Primary factors of production (a.k.a. resources, inputs, or producer goods):
	
	These are used in the production process to produce output (typically goods or services to be purchased by consumers), and are accordingly differentiated from _consumer goods_. The three _basic_ resources are:
	
	- Captial goods
	- Land:
	
		In economics, land comprises all naturally occurring resources whose supply is inherently fixed. Examples are any and all particular geographical locations, mineral deposits, forests, fish stocks, atmospheric quality, geostationary orbits, and portions of the electromagnetic spectrum. 
		
		As a tangible asset land is represented in accounting as a fixed asset or a capital asset.
		
	- Labour:
	
		In economics, labour is a measure of the work done by human beings