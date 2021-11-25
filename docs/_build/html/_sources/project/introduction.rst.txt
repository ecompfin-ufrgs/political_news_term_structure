Introduction
============

The problem we will address is whether political events affect the term structure of interest rates in Brazil.
More specifically, we will test the following hypothesis: does the volume of political news in Brazilian
newspapers cause volatility in the risk factor of the term structure of the DI interest rate?

Nowadays the economy and the government are not separate (as in the case of religion and the government).
Governments try to 'steer' the economy with its laws and policies. Financial assets are affected by the state of the
economy, therefore politics arguably has great impact on assets prices. Nevertheless, the impact may differ between
countries with different political structures.

Among financial assets, 'sovereign bonds are the asset most directly associated with government policy.'
:cite:`mcmenamin2016` (p. 3). Thus it can be expected that political events will change the expectations
for government policy and consequently affect bonds' prices. Furthermore, these events may influence
market volatility as an increasing trading volume occurs while investors 'rebalance their portfolios in
light of the news' :cite:`smales2013`.

Various papers have studied the effect of election uncertainty on market uncertainty concludes the former does affect
the latter. :cite:`li2006` and :cite:`goodell2013` find this result studying the effect on U.S. stocks, while
:cite:`smales2015` finds it on Australian stocks. As of government bonds, :cite:`mcmenamin2016`, which analyzes 122
elections over 19 countries, concludes that bonds do (under) react to elections.

As of our research line, which studies the financial market in Brazil, :cite:`marquessantos`
finds stocks do respond to few political events, but the interest rate responds to no event.
:cite:`paulsen2019` finds the exchange coupon also responds to few political news.

This paper contributes to the literature in the following ways. First, we shed light on the interconnections
between politics and financial assets in Brazil, where the structure and power of government differ from the
countries where this relationship has been previously studied. Second, we focus on political events in general,
even the ones that have taken place when the party in power is not changing - unlike previous research on elections.
Third, we analyze the impact of politics in the whole term structure.

Political news will be collected on major Brazilian online newspapers with web scrapping. The scraper is intended
to collect information on all news available on the political section of given newspapers. The information
collected will be the title and date of each news. The DI term structure will be used, and will be collected from
ECONOMATICA via the DI rate and its futures. The sample definition will depend on the availability of data at the online
newpapers.

The risk factor of the term structure will be estimated with a Vasicek model :cite:`vasicek1977`.
Its volatility will be calculated with a GARCH model :cite:`bollerslev1986`. The causality between political
news volume and the volatility of the risk factor of the term structure will be estimated with a Granger model
:cite:`granger1969`.

We expect our results follow the literature, which, in the case of political events such as elections or major events,
indicates politics do influence financial assets. Therefore we expect the existence of causality between political
news volume and the volatility of the risk factor of the term structure of the DI interest rate

In this research we test market efficiency with data which has a daily frequency. It is possible that inefficiencies do
arise but last just some minutes or seconds. Thus one possible future research is to test the same hypothesis we test
in the research but with high frequency data.